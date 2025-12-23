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
        
        if not subject:
            return jsonify({'error': 'Please enter a subject'}), 400
        
        if study_hours <= 0 or study_hours > 12:
            return jsonify({'error': 'Study hours must be between 0.5 and 12'}), 400
        
        # Store inputs
        app_results['last_subject'] = subject
        app_results['last_hours'] = study_hours
        
        # Save user input
        data_processor.save_user_input(subject, study_hours)
        
        # Load and process educational data
        data_processor.load_data()
        cleaned_data = data_processor.preprocess_data()
        subject_content = data_processor.get_subject_content(subject)
        
        # 1. Generate Study Plan
        study_plan = study_planner.create_comprehensive_plan(
            subject=subject,
            daily_hours=study_hours,
            scenario=scenario
        )
        app_results['study_plan'] = study_plan
        
        # 2. Generate Quiz
        # Train ML models if not already trained
        try:
            quiz_generator.load_models()
        except:
            quiz_generator.train_difficulty_classifier()
            if subject_content:
                quiz_generator.train_topic_clustering(subject_content)
            quiz_generator.save_models()
        
        quiz = quiz_generator.generate_quiz(subject, num_questions=5)
        app_results['quiz'] = quiz
        
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

@app.route('/about')
def about():
    """About page with project information"""
    return render_template('about.html')

@app.errorhandler(404)
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