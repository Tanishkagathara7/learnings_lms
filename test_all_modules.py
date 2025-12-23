#!/usr/bin/env python3
"""
AI Study Pal - Comprehensive Module Testing Script
Tests all AI components to ensure they work correctly before deployment
"""

import sys
import os
import traceback
from datetime import datetime

# Add src directory to path
sys.path.append('src')

def test_data_preprocessing():
    """Test the data preprocessing module"""
    print("🔄 Testing Data Preprocessing Module...")
    try:
        from data_preprocessing import DataPreprocessor
        
        # Initialize and test
        preprocessor = DataPreprocessor()
        raw_data = preprocessor.load_data()
        
        if raw_data is None:
            print("✗ Failed to load data")
            return False
        
        cleaned_data = preprocessor.preprocess_data()
        if cleaned_data is None:
            print("✗ Failed to preprocess data")
            return False
        
        # Test EDA
        eda_results = preprocessor.perform_eda(save_plots=True)
        if eda_results is None:
            print("✗ Failed to perform EDA")
            return False
        
        # Test user input saving
        preprocessor.save_user_input("Mathematics", 3)
        
        # Test subject content retrieval
        content = preprocessor.get_subject_content("Mathematics")
        if not content:
            print("✗ Failed to retrieve subject content")
            return False
        
        print("✓ Data Preprocessing Module: PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Data Preprocessing Module: FAILED - {e}")
        traceback.print_exc()
        return False

def test_ml_quiz_generator():
    """Test the machine learning quiz generator module"""
    print("🔄 Testing ML Quiz Generator Module...")
    try:
        from ml_quiz_generator import QuizGenerator
        from data_preprocessing import DataPreprocessor
        
        # Initialize components
        quiz_gen = QuizGenerator()
        preprocessor = DataPreprocessor()
        
        # Load data for clustering
        preprocessor.load_data()
        cleaned_data = preprocessor.preprocess_data()
        subject_content = preprocessor.get_subject_content("Mathematics")
        
        # Test difficulty classifier training
        metrics = quiz_gen.train_difficulty_classifier()
        if not metrics or metrics['accuracy'] < 0.1:
            print("✗ Failed to train difficulty classifier")
            return False
        
        # Test clustering
        if subject_content:
            cluster_info = quiz_gen.train_topic_clustering(subject_content)
            if not cluster_info:
                print("✗ Failed to train clustering model")
                return False
        
        # Test quiz generation
        quiz = quiz_gen.generate_quiz("Mathematics", 3)
        if not quiz or not quiz['questions']:
            print("✗ Failed to generate quiz")
            return False
        
        # Test model saving
        quiz_gen.save_models()
        
        print("✓ ML Quiz Generator Module: PASSED")
        return True
        
    except Exception as e:
        print(f"✗ ML Quiz Generator Module: FAILED - {e}")
        traceback.print_exc()
        return False

def test_dl_text_processor():
    """Test the deep learning text processor module"""
    print("🔄 Testing DL Text Processor Module...")
    try:
        from dl_text_processor import TextProcessor
        
        # Initialize processor
        processor = TextProcessor()
        
        # Test model training
        history = processor.train_summarization_model()
        if not history:
            print("✗ Failed to train summarization model")
            return False
        
        # Test text summarization
        sample_text = """
        Machine learning is a subset of artificial intelligence that focuses on algorithms 
        that can learn from and make predictions on data. It involves training models on 
        datasets to recognize patterns and make decisions with minimal human intervention.
        """
        
        summary = processor.summarize_text(sample_text)
        if not summary or len(summary) < 10:
            print("✗ Failed to generate text summary")
            return False
        
        # Test feedback generation
        feedback = processor.generate_motivational_feedback("Mathematics", 0.8)
        if not feedback:
            print("✗ Failed to generate motivational feedback")
            return False
        
        # Test model saving
        processor.save_models()
        
        print("✓ DL Text Processor Module: PASSED")
        return True
        
    except Exception as e:
        print(f"✗ DL Text Processor Module: FAILED - {e}")
        traceback.print_exc()
        return False

def test_nlp_study_tips():
    """Test the NLP study tips generator module"""
    print("🔄 Testing NLP Study Tips Module...")
    try:
        from nlp_study_tips import StudyTipsGenerator
        
        # Initialize generator
        tips_gen = StudyTipsGenerator()
        
        # Test keyword extraction
        sample_text = """
        Calculus is the mathematical study of continuous change. It has two major branches: 
        differential calculus and integral calculus. Students should practice derivative 
        calculations and integration techniques regularly.
        """
        
        keywords = tips_gen.extract_keywords(sample_text)
        if not keywords or not keywords['combined_keywords']:
            print("✗ Failed to extract keywords")
            return False
        
        # Test study tips generation
        tips_result = tips_gen.generate_contextual_tips(sample_text, "Mathematics", 5)
        if not tips_result or not tips_result['study_tips']:
            print("✗ Failed to generate study tips")
            return False
        
        # Test NLP analysis
        analysis = tips_gen.analyze_study_content(sample_text)
        if not analysis or not analysis['text_statistics']:
            print("✗ Failed to perform NLP analysis")
            return False
        
        # Test saving results
        tips_gen.save_analysis_results(analysis)
        
        print("✓ NLP Study Tips Module: PASSED")
        return True
        
    except Exception as e:
        print(f"✗ NLP Study Tips Module: FAILED - {e}")
        traceback.print_exc()
        return False

def test_study_planner():
    """Test the study planner module"""
    print("🔄 Testing Study Planner Module...")
    try:
        from study_planner import StudyPlanner
        
        # Initialize planner
        planner = StudyPlanner()
        
        # Test time distribution calculation
        time_dist = planner.calculate_time_distribution("Mathematics", 3, "exam_prep")
        if not time_dist or time_dist['total'] <= 0:
            print("✗ Failed to calculate time distribution")
            return False
        
        # Test daily schedule generation
        daily_schedule = planner.generate_daily_schedule("Mathematics", 3, "exam_prep")
        if not daily_schedule:
            print("✗ Failed to generate daily schedule")
            return False
        
        # Test weekly plan creation
        weekly_plan = planner.create_comprehensive_plan("Mathematics", 3, "exam_prep")
        if not weekly_plan or not weekly_plan['daily_schedules']:
            print("✗ Failed to create weekly plan")
            return False
        
        # Test CSV export
        csv_file = planner.save_study_plan_csv(weekly_plan)
        if not os.path.exists(csv_file):
            print("✗ Failed to save CSV file")
            return False
        
        print("✓ Study Planner Module: PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Study Planner Module: FAILED - {e}")
        traceback.print_exc()
        return False

def test_web_app_imports():
    """Test that the web app can import all modules correctly"""
    print("🔄 Testing Web App Imports...")
    try:
        # Test Flask app imports
        sys.path.append('web_app')
        
        # Import all modules that the web app uses
        from data_preprocessing import DataPreprocessor
        from ml_quiz_generator import QuizGenerator
        from dl_text_processor import TextProcessor
        from nlp_study_tips import StudyTipsGenerator
        from study_planner import StudyPlanner
        
        # Test basic initialization
        data_processor = DataPreprocessor()
        quiz_generator = QuizGenerator()
        text_processor = TextProcessor()
        tips_generator = StudyTipsGenerator()
        study_planner = StudyPlanner()
        
        print("✓ Web App Imports: PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Web App Imports: FAILED - {e}")
        traceback.print_exc()
        return False

def run_comprehensive_test():
    """Run all module tests"""
    print("🚀 Starting AI Study Pal Comprehensive Testing")
    print("=" * 60)
    
    start_time = datetime.now()
    
    # Ensure output directories exist
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Run all tests
    tests = [
        ("Data Preprocessing", test_data_preprocessing),
        ("ML Quiz Generator", test_ml_quiz_generator),
        ("DL Text Processor", test_dl_text_processor),
        ("NLP Study Tips", test_nlp_study_tips),
        ("Study Planner", test_study_planner),
        ("Web App Imports", test_web_app_imports)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} Test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name}: CRITICAL FAILURE - {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    print(f"⏱️  Duration: {duration:.2f} seconds")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! AI Study Pal is ready for deployment.")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)