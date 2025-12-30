#!/usr/bin/env python3
"""
Test the enhanced data preprocessing module
"""

import sys
import os

# Add src directory to path
sys.path.append('src')

def test_enhanced_preprocessing():
    """Test the enhanced data preprocessing functionality"""
    print("🔄 Testing Enhanced Data Preprocessing Module...")
    
    try:
        from data_preprocessing import DataPreprocessor
        
        # Initialize preprocessor
        preprocessor = DataPreprocessor()
        print("✓ DataPreprocessor initialized successfully")
        
        # Test data loading
        raw_data = preprocessor.load_data(include_wikipedia=False)  # Skip Wikipedia for now
        if raw_data is None:
            print("✗ Failed to load data")
            return False
        print(f"✓ Loaded {len(raw_data)} records")
        
        # Test data preprocessing
        cleaned_data = preprocessor.preprocess_data()
        if cleaned_data is None:
            print("✗ Failed to preprocess data")
            return False
        print(f"✓ Preprocessed data: {len(cleaned_data)} records")
        
        # Test EDA (without showing plots)
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        
        eda_results = preprocessor.perform_eda(save_plots=True)
        if eda_results is None:
            print("✗ Failed to perform EDA")
            return False
        print("✓ EDA completed successfully")
        
        # Test user input saving
        user_data = preprocessor.save_user_input("Mathematics", 3, selected_topics=["Algebra", "Calculus"])
        if not user_data:
            print("✗ Failed to save user input")
            return False
        print("✓ User input saved successfully")
        
        # Test user behavior analysis
        behavior_insights = preprocessor.analyze_user_behavior()
        if behavior_insights:
            print("✓ User behavior analysis completed")
        else:
            print("ℹ️  No user behavior data to analyze (expected for first run)")
        
        # Test data report generation
        report = preprocessor.generate_data_report()
        if not report:
            print("✗ Failed to generate data report")
            return False
        print("✓ Data report generated successfully")
        
        # Test subject content retrieval
        content = preprocessor.get_subject_content("Mathematics")
        if not content:
            print("✗ Failed to retrieve subject content")
            return False
        print(f"✓ Retrieved {len(content)} Mathematics records")
        
        print("\n✅ Enhanced Data Preprocessing Module: ALL TESTS PASSED")
        print("📊 Features tested:")
        print("  • Data loading and preprocessing")
        print("  • Comprehensive EDA with visualizations")
        print("  • User input tracking")
        print("  • User behavior analysis")
        print("  • Data quality reporting")
        print("  • Subject content retrieval")
        
        return True
        
    except Exception as e:
        print(f"✗ Enhanced Data Preprocessing Module: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Ensure output directories exist
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    success = test_enhanced_preprocessing()
    if success:
        print("\n🎉 Enhanced data preprocessing is working correctly!")
    else:
        print("\n⚠️  Some issues found. Please check the errors above.")
    
    sys.exit(0 if success else 1)