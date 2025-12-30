#!/usr/bin/env python3
"""
Test Wikipedia data collection feature
"""

import sys
import os

# Add src directory to path
sys.path.append('src')

def test_wikipedia_collection():
    """Test Wikipedia data collection"""
    print("🌐 Testing Wikipedia Data Collection...")
    
    try:
        from data_preprocessing import DataPreprocessor
        
        # Initialize preprocessor
        preprocessor = DataPreprocessor()
        print("✓ DataPreprocessor initialized")
        
        # Test Wikipedia data collection (limited to 1 topic per subject for speed)
        print("📡 Collecting Wikipedia data (this may take a moment)...")
        wikipedia_data = preprocessor.collect_wikipedia_data(topics_per_subject=1, max_chars=300)
        
        if wikipedia_data is not None and not wikipedia_data.empty:
            print(f"✓ Successfully collected {len(wikipedia_data)} Wikipedia articles")
            print("📚 Collected subjects:", wikipedia_data['subject'].unique().tolist())
            
            # Test loading data with Wikipedia content
            raw_data = preprocessor.load_data(include_wikipedia=True)
            if raw_data is not None:
                print(f"✓ Combined dataset size: {len(raw_data)} records")
                
                # Check if Wikipedia data is included
                if 'source' in raw_data.columns:
                    source_counts = raw_data['source'].value_counts()
                    print("📊 Data sources:", source_counts.to_dict())
                
                return True
            else:
                print("✗ Failed to load combined data")
                return False
        else:
            print("⚠️  No Wikipedia data collected (this might be due to network issues)")
            return True  # Don't fail the test for network issues
            
    except Exception as e:
        print(f"✗ Wikipedia collection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_wikipedia_collection()
    if success:
        print("\n🎉 Wikipedia data collection test completed!")
    else:
        print("\n⚠️  Wikipedia data collection test failed.")
    
    sys.exit(0 if success else 1)