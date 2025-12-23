"""
Data Collection & Preprocessing Module
Handles educational text data preparation and basic EDA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import json
from collections import Counter
import os

class DataPreprocessor:
    def __init__(self, data_path='data/educational_content.csv'):
        """Initialize the data preprocessor"""
        self.data_path = data_path
        self.raw_data = None
        self.cleaned_data = None
        
    def load_data(self):
        """Load the educational content dataset"""
        try:
            self.raw_data = pd.read_csv(self.data_path)
            print(f"✓ Loaded {len(self.raw_data)} records from {self.data_path}")
            return self.raw_data
        except FileNotFoundError:
            print(f"✗ Error: Could not find {self.data_path}")
            return None
    
    def clean_text(self, text):
        """Clean individual text content"""
        if pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        return text.strip()
    
    def preprocess_data(self):
        """Clean and preprocess the dataset"""
        if self.raw_data is None:
            print("✗ No data loaded. Please run load_data() first.")
            return None
        
        # Create a copy for processing
        self.cleaned_data = self.raw_data.copy()
        
        # Remove duplicates
        initial_count = len(self.cleaned_data)
        self.cleaned_data = self.cleaned_data.drop_duplicates()
        duplicates_removed = initial_count - len(self.cleaned_data)
        
        # Clean text content
        self.cleaned_data['text_content_cleaned'] = self.cleaned_data['text_content'].apply(self.clean_text)
        
        # Remove empty content
        self.cleaned_data = self.cleaned_data[self.cleaned_data['text_content_cleaned'] != '']
        
        print(f"✓ Data preprocessing completed:")
        print(f"  - Removed {duplicates_removed} duplicates")
        print(f"  - Final dataset size: {len(self.cleaned_data)} records")
        
        return self.cleaned_data
    
    def perform_eda(self, save_plots=True):
        """Perform Exploratory Data Analysis"""
        if self.cleaned_data is None:
            print("✗ No cleaned data available. Please run preprocess_data() first.")
            return None
        
        # Subject distribution
        subject_counts = self.cleaned_data['subject'].value_counts()
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        
        # Subplot 1: Subject distribution pie chart
        plt.subplot(2, 2, 1)
        colors = plt.cm.Set3(np.linspace(0, 1, len(subject_counts)))
        plt.pie(subject_counts.values, labels=subject_counts.index, autopct='%1.1f%%', 
                colors=colors, startangle=90)
        plt.title('Subject Distribution', fontsize=14, fontweight='bold')
        
        # Subplot 2: Topic count per subject
        plt.subplot(2, 2, 2)
        topic_counts = self.cleaned_data.groupby('subject')['topic'].nunique()
        bars = plt.bar(topic_counts.index, topic_counts.values, color=colors[:len(topic_counts)])
        plt.title('Topics per Subject', fontsize=14, fontweight='bold')
        plt.xlabel('Subject')
        plt.ylabel('Number of Topics')
        plt.xticks(rotation=45)
        
        # Subplot 3: Text length distribution
        plt.subplot(2, 2, 3)
        text_lengths = self.cleaned_data['text_content_cleaned'].str.len()
        plt.hist(text_lengths, bins=15, color='skyblue', alpha=0.7, edgecolor='black')
        plt.title('Text Content Length Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Character Count')
        plt.ylabel('Frequency')
        
        # Subplot 4: Word count distribution
        plt.subplot(2, 2, 4)
        word_counts = self.cleaned_data['text_content_cleaned'].str.split().str.len()
        plt.hist(word_counts, bins=15, color='lightcoral', alpha=0.7, edgecolor='black')
        plt.title('Word Count Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Word Count')
        plt.ylabel('Frequency')
        
        plt.tight_layout()
        
        if save_plots:
            os.makedirs('outputs', exist_ok=True)
            plt.savefig('outputs/data_analysis.png', dpi=300, bbox_inches='tight')
            print("✓ EDA visualization saved to outputs/data_analysis.png")
        
        plt.show()
        
        # Print summary statistics
        print("\n📊 Dataset Summary:")
        print(f"Total records: {len(self.cleaned_data)}")
        print(f"Subjects: {', '.join(subject_counts.index.tolist())}")
        print(f"Average text length: {text_lengths.mean():.1f} characters")
        print(f"Average word count: {word_counts.mean():.1f} words")
        
        return {
            'subject_distribution': subject_counts.to_dict(),
            'topic_counts': topic_counts.to_dict(),
            'avg_text_length': text_lengths.mean(),
            'avg_word_count': word_counts.mean()
        }
    
    def save_user_input(self, subject, study_hours, filename='data/user_inputs.json'):
        """Save user inputs to JSON file"""
        user_data = {
            'subject': subject,
            'study_hours': study_hours,
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        # Load existing data if file exists
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                existing_data = json.load(f)
            if isinstance(existing_data, list):
                existing_data.append(user_data)
            else:
                existing_data = [existing_data, user_data]
        else:
            existing_data = [user_data]
        
        # Save updated data
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        print(f"✓ User input saved to {filename}")
        return user_data
    
    def get_subject_content(self, subject):
        """Get all content for a specific subject"""
        if self.cleaned_data is None:
            return None
        
        subject_data = self.cleaned_data[self.cleaned_data['subject'].str.lower() == subject.lower()]
        return subject_data.to_dict('records')

# Example usage and testing
if __name__ == "__main__":
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    
    # Load and process data
    raw_data = preprocessor.load_data()
    if raw_data is not None:
        cleaned_data = preprocessor.preprocess_data()
        eda_results = preprocessor.perform_eda()
        
        # Save sample user input
        preprocessor.save_user_input("Mathematics", 3)
        
        print("\n✓ Data preprocessing module completed successfully!")