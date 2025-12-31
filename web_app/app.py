"""
Flask Web Application for AI Study Pal
Integrates all AI components into a user-friendly web interface
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import sys
import os
import json
from datetime import datetime
import traceback

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import our AI modules
from data_preprocessing import DataPreprocessor
from ml_quiz_generator import QuizGenerator
from dl_text_processor import TextProcessor
from nlp_study_tips import StudyTipsGenerator
from study_planner import StudyPlanner

app = Flask(__name__)
app.secret_key = 'ai_study_pal_secret_key_2024'

# Initialize AI components with correct paths
data_processor = DataPreprocessor(data_path='../data/educational_content.csv')
quiz_generator = QuizGenerator()
text_processor = TextProcessor()
tips_generator = StudyTipsGenerator()
study_planner = StudyPlanner()

# Global variables to store results
app_results = {
    'last_subject': None,
    'last_hours': None,
    'study_plan': None,
    'quiz': None,
    'summary': None,
    'tips': None,
    'feedback': None
}

@app.route('/')
def home():
    """Home page with input form"""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_study_request():
    """Process the study request and generate all AI outputs"""
    try:
        # Get form data
        subject = request.form.get('subject', '').strip()
        study_hours = float(request.form.get('study_hours', 2))
        scenario = request.form.get('scenario', 'general_study')
        selected_topics = request.form.getlist('topics')  # Get selected topics
        
        if not subject:
            return jsonify({'error': 'Please enter a subject'}), 400
        
        if study_hours <= 0 or study_hours > 12:
            return jsonify({'error': 'Study hours must be between 0.5 and 12'}), 400
        
        # Store inputs
        app_results['last_subject'] = subject
        app_results['last_hours'] = study_hours
        app_results['selected_topics'] = selected_topics
        
        # Save user input with topics
        data_processor.save_user_input(subject, study_hours, selected_topics)
        
        # Load and process educational data
        data_processor.load_data()
        cleaned_data = data_processor.preprocess_data()
        subject_content = data_processor.get_subject_content(subject)
        
        # 1. Generate Study Plan with topics
        study_plan = study_planner.create_comprehensive_plan(
            subject=subject,
            daily_hours=study_hours,
            scenario=scenario,
            selected_topics=selected_topics
        )
        app_results['study_plan'] = study_plan
        
        # 2. Generate Quiz
        # Train ML models if not already trained
        try:
            quiz_generator.load_models()
            print("✓ Models loaded successfully")
        except:
            print("⚠️ Models not found, training new models...")
            # Train difficulty classifier
            difficulty_metrics = quiz_generator.train_difficulty_classifier()
            print(f"✓ Difficulty classifier trained with accuracy: {difficulty_metrics['accuracy']:.3f}")
            
            # Train topic clustering if we have content
            if subject_content:
                cluster_info = quiz_generator.train_topic_clustering(subject_content)
                print(f"✓ Topic clustering completed")
            
            # Save the trained models
            quiz_generator.save_models()
            print("✓ Models saved successfully")
        
        quiz = quiz_generator.generate_quiz(subject, num_questions=5)
        app_results['quiz'] = quiz
        
        if quiz:
            print(f"✓ Generated quiz with {len(quiz['questions'])} questions")
            for i, q in enumerate(quiz['questions']):
                difficulty = q.get('predicted_difficulty', 'unknown')
                print(f"  Question {i+1}: {difficulty} difficulty")
        else:
            print("⚠️ Failed to generate quiz")
        
        # 3. Generate Text Summary
        if subject_content and len(subject_content) > 0:
            # Combine text content for summarization
            combined_text = ' '.join([item['text_content'] for item in subject_content[:3]])
            
            # Train text processor if needed
            try:
                text_processor.load_models()
            except:
                text_processor.train_summarization_model()
                text_processor.save_models()
            
            summary = text_processor.summarize_text(combined_text, max_summary_length=100)
        else:
            summary = f"Study {subject} systematically by focusing on core concepts and regular practice."
        
        app_results['summary'] = summary
        
        # 4. Generate Study Tips
        sample_text = f"Studying {subject} requires understanding fundamental concepts and regular practice."
        if subject_content:
            sample_text = subject_content[0]['text_content']
        
        tips_result = tips_generator.generate_contextual_tips(sample_text, subject, num_tips=5)
        app_results['tips'] = tips_result
        
        # 5. Generate Motivational Feedback
        feedback = text_processor.generate_motivational_feedback(subject, performance_score=0.8)
        app_results['feedback'] = feedback
        
        return redirect(url_for('results'))
        
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        print(f"Error: {error_msg}")
        print(traceback.format_exc())
        return jsonify({'error': error_msg}), 500

@app.route('/results')
def results():
    """Display results page with all AI outputs"""
    if not app_results['study_plan']:
        return redirect(url_for('home'))
    
    return render_template('results.html', results=app_results)

@app.route('/download_plan')
def download_plan():
    """Download study plan as CSV"""
    try:
        if not app_results['study_plan']:
            return jsonify({'error': 'No study plan available'}), 400
        
        # Generate CSV file
        filename = study_planner.save_study_plan_csv(app_results['study_plan'])
        
        return send_file(
            filename,  # filename is now absolute path
            as_attachment=True,
            download_name=f"study_plan_{app_results['last_subject']}.csv"
        )
    except Exception as e:
        return jsonify({'error': f'Error generating download: {str(e)}'}), 500

@app.route('/api/quiz_check', methods=['POST'])
def check_quiz_answers():
    """API endpoint to check quiz answers"""
    try:
        answers = request.json.get('answers', {})
        quiz = app_results.get('quiz')
        
        if not quiz:
            return jsonify({'error': 'No quiz available'}), 400
        
        results = []
        correct_count = 0
        
        for i, question in enumerate(quiz['questions']):
            user_answer = int(answers.get(str(i), -1))
            correct_answer = question['correct']
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct_count += 1
            
            results.append({
                'question_index': i,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'correct_option': question['options'][correct_answer]
            })
        
        score = correct_count / len(quiz['questions']) if quiz['questions'] else 0
        
        return jsonify({
            'results': results,
            'score': score,
            'correct_count': correct_count,
            'total_questions': len(quiz['questions'])
        })
        
    except Exception as e:
        return jsonify({'error': f'Error checking answers: {str(e)}'}), 500

@app.route('/data_analytics')
def data_analytics():
    """Data analytics dashboard showing EDA visualizations"""
    try:
        # Set matplotlib to use non-interactive backend for web apps
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        
        # Generate fresh analytics
        data_processor.load_data(include_wikipedia=False)  # Skip Wikipedia for faster loading
        cleaned_data = data_processor.preprocess_data()
        
        # Perform EDA and generate visualizations
        eda_results = data_processor.perform_eda(save_plots=True)
        
        # Analyze user behavior if data exists
        behavior_insights = data_processor.analyze_user_behavior()
        
        # Generate comprehensive report
        report = data_processor.generate_data_report()
        
        # Add timestamp for cache busting
        import time
        timestamp = int(time.time())
        
        return render_template('analytics.html', 
                             eda_results=eda_results,
                             behavior_insights=behavior_insights,
                             report=report,
                             timestamp=timestamp)
    except Exception as e:
        print(f"Error in data analytics: {e}")
        import traceback
        traceback.print_exc()
        return render_template('analytics.html', 
                             error=f"Error generating analytics: {str(e)}")

@app.route('/analytics_image/<image_name>')
def serve_analytics_image(image_name):
    """Serve analytics images from outputs directory"""
    try:
        # Get the absolute path to the outputs directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(base_dir, 'outputs', image_name)
        
        print(f"🔍 Looking for image at: {image_path}")
        print(f"🔍 Image exists: {os.path.exists(image_path)}")
        
        if os.path.exists(image_path):
            # Add cache-busting headers
            from flask import make_response
            response = make_response(send_file(image_path, mimetype='image/png'))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            print(f"✓ Serving image: {image_name}")
            return response
        else:
            print(f"✗ Image not found: {image_path}")
            return "Image not found", 404
    except Exception as e:
        print(f"✗ Error serving image: {str(e)}")
        return f"Error serving image: {str(e)}", 500

@app.route('/debug_quiz/<subject>')
def debug_quiz(subject):
    """Debug route to test quiz generation"""
    try:
        # Force retrain the model
        quiz_generator.train_difficulty_classifier()
        
        # Generate quiz
        quiz = quiz_generator.generate_quiz(subject, num_questions=3)
        
        return jsonify({
            'success': True,
            'quiz': quiz,
            'debug_info': {
                'model_trained': quiz_generator.difficulty_model is not None,
                'vectorizer_ready': quiz_generator.vectorizer is not None,
                'questions_with_difficulty': [
                    {
                        'question': q['question'][:50] + '...',
                        'predicted_difficulty': q.get('predicted_difficulty', 'missing'),
                        'original_difficulty': q.get('difficulty', 'missing')
                    } for q in quiz['questions']
                ] if quiz else []
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'debug_info': {
                'model_trained': quiz_generator.difficulty_model is not None,
                'vectorizer_ready': quiz_generator.vectorizer is not None
            }
        })

@app.route('/about')
def about():
    """About page with project information"""
    return render_template('about.html')
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Ensure output directories exist
    os.makedirs('../outputs', exist_ok=True)
    os.makedirs('../models', exist_ok=True)
    
    # Initialize data on startup
    try:
        print("🚀 Initializing AI Study Pal...")
        
        # Load educational data
        data_processor.load_data()
        data_processor.preprocess_data()
        
        print("✓ AI Study Pal initialized successfully!")
        print("🌐 Starting web server...")
        
    except Exception as e:
        print(f"⚠ Warning during initialization: {e}")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)