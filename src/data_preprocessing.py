"""
Data Collection & Preprocessing Module
Handles educational text data preparation and basic EDA
Features: Wikipedia data collection, comprehensive EDA, user behavior analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import json
import requests
import time
from collections import Counter
from datetime import datetime
import os

class DataPreprocessor:
    def __init__(self, data_path='data/educational_content.csv'):
        """Initialize the data preprocessor"""
        self.data_path = data_path
        self.raw_data = None
        self.cleaned_data = None
        self.wikipedia_data = None
        
    def collect_wikipedia_data(self, topics_per_subject=3, max_chars=500):
        """
        Collect educational content from Wikipedia
        
        Args:
            topics_per_subject (int): Number of topics to collect per subject
            max_chars (int): Maximum characters per snippet
        """
        print("🔄 Collecting educational content from Wikipedia...")
        
        # Define subjects and their related topics
        subject_topics = {
            'Mathematics': ['Linear algebra', 'Differential calculus', 'Probability theory', 
                          'Number theory', 'Geometry', 'Trigonometry'],
            'Physics': ['Quantum mechanics', 'Relativity theory', 'Optics', 
                       'Atomic physics', 'Fluid dynamics', 'Waves'],
            'Chemistry': ['Biochemistry', 'Analytical chemistry', 'Polymer chemistry',
                         'Electrochemistry', 'Crystallography', 'Spectroscopy'],
            'Biology': ['Molecular biology', 'Ecology', 'Microbiology',
                       'Neuroscience', 'Immunology', 'Botany'],
            'Computer Science': ['Machine learning', 'Database systems', 'Computer networks',
                               'Software engineering', 'Artificial intelligence', 'Cybersecurity']
        }
        
        collected_data = []
        
        for subject, topics in subject_topics.items():
            print(f"  📚 Collecting {subject} content...")
            
            # Limit topics per subject
            selected_topics = topics[:topics_per_subject]
            
            for topic in selected_topics:
                try:
                    # Wikipedia API call
                    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(' ', '_')
                    response = requests.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Extract and clean content
                        content = data.get('extract', '')
                        if content:
                            # Limit content length
                            if len(content) > max_chars:
                                content = content[:max_chars] + "..."
                            
                            collected_data.append({
                                'subject': subject,
                                'topic': topic,
                                'text_content': content,
                                'source': 'Wikipedia',
                                'collected_date': datetime.now().isoformat()
                            })
                            
                            print(f"    ✓ {topic}")
                        else:
                            print(f"    ✗ {topic} (no content)")
                    else:
                        print(f"    ✗ {topic} (API error: {response.status_code})")
                        
                except Exception as e:
                    print(f"    ✗ {topic} (error: {str(e)[:50]}...)")
                
                # Rate limiting
                time.sleep(0.5)
        
        # Convert to DataFrame
        self.wikipedia_data = pd.DataFrame(collected_data)
        
        if not self.wikipedia_data.empty:
            # Save collected data
            wiki_path = 'data/wikipedia_content.csv'
            os.makedirs('data', exist_ok=True)
            self.wikipedia_data.to_csv(wiki_path, index=False)
            print(f"✓ Collected {len(self.wikipedia_data)} Wikipedia articles")
            print(f"✓ Saved to {wiki_path}")
        else:
            print("✗ No Wikipedia data collected")
            
        return self.wikipedia_data
        
    def load_data(self, include_wikipedia=True):
        """Load the educational content dataset"""
        try:
            # Load main dataset
            self.raw_data = pd.read_csv(self.data_path)
            print(f"✓ Loaded {len(self.raw_data)} records from {self.data_path}")
            
            # Load Wikipedia data if available and requested
            if include_wikipedia:
                wiki_path = 'data/wikipedia_content.csv'
                if os.path.exists(wiki_path):
                    wiki_data = pd.read_csv(wiki_path)
                    # Combine datasets
                    self.raw_data = pd.concat([self.raw_data, wiki_data], ignore_index=True)
                    print(f"✓ Combined with {len(wiki_data)} Wikipedia records")
                    print(f"✓ Total dataset size: {len(self.raw_data)} records")
                else:
                    print("ℹ️  No Wikipedia data found. Use collect_wikipedia_data() to gather more content.")
            
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
        """Perform Exploratory Data Analysis with comprehensive visualizations"""
        if self.cleaned_data is None:
            print("✗ No cleaned data available. Please run preprocess_data() first.")
            return None
        
        print("📊 Performing comprehensive EDA...")
        
        # Set matplotlib backend for web compatibility
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        import matplotlib.pyplot as plt
        
        # Calculate statistics
        subject_counts = self.cleaned_data['subject'].value_counts()
        topic_counts = self.cleaned_data.groupby('subject')['topic'].nunique()
        text_lengths = self.cleaned_data['text_content_cleaned'].str.len()
        word_counts = self.cleaned_data['text_content_cleaned'].str.split().str.len()
        
        # Create comprehensive visualization
        plt.style.use('default')
        fig = plt.figure(figsize=(15, 10))
        
        # Subplot 1: Subject distribution pie chart
        plt.subplot(2, 4, 1)
        colors = plt.cm.Set3(np.linspace(0, 1, len(subject_counts)))
        wedges, texts, autotexts = plt.pie(subject_counts.values, labels=subject_counts.index, 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Subject Distribution', fontsize=14, fontweight='bold')
        
        # Subplot 2: Topic count per subject
        plt.subplot(2, 4, 2)
        bars = plt.bar(topic_counts.index, topic_counts.values, color=colors[:len(topic_counts)])
        plt.title('Topics per Subject', fontsize=14, fontweight='bold')
        plt.xlabel('Subject')
        plt.ylabel('Number of Topics')
        plt.xticks(rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom')
        
        # Subplot 3: Text length distribution
        plt.subplot(2, 4, 3)
        plt.hist(text_lengths, bins=20, color='skyblue', alpha=0.7, edgecolor='black')
        plt.axvline(text_lengths.mean(), color='red', linestyle='--', 
                   label=f'Mean: {text_lengths.mean():.0f}')
        plt.title('Text Content Length Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Character Count')
        plt.ylabel('Frequency')
        plt.legend()
        
        # Subplot 4: Word count distribution
        plt.subplot(2, 4, 4)
        plt.hist(word_counts, bins=20, color='lightcoral', alpha=0.7, edgecolor='black')
        plt.axvline(word_counts.mean(), color='red', linestyle='--',
                   label=f'Mean: {word_counts.mean():.1f}')
        plt.title('Word Count Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Word Count')
        plt.ylabel('Frequency')
        plt.legend()
        
        # Subplot 5: Subject vs Average Text Length
        plt.subplot(2, 4, 5)
        avg_lengths = self.cleaned_data.groupby('subject')['text_content_cleaned'].apply(lambda x: x.str.len().mean())
        bars = plt.bar(avg_lengths.index, avg_lengths.values, color='lightgreen', alpha=0.7)
        plt.title('Average Text Length by Subject', fontsize=14, fontweight='bold')
        plt.xlabel('Subject')
        plt.ylabel('Average Character Count')
        plt.xticks(rotation=45)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{int(height)}', ha='center', va='bottom')
        
        # Subplot 6: Text complexity analysis (sentence count)
        plt.subplot(2, 4, 6)
        sentence_counts = self.cleaned_data['text_content_cleaned'].str.count(r'[.!?]+')
        plt.hist(sentence_counts, bins=15, color='gold', alpha=0.7, edgecolor='black')
        plt.title('Sentence Count Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Sentences')
        plt.ylabel('Frequency')
        
        # Subplot 7: Most common words analysis
        plt.subplot(2, 4, 7)
        all_text = ' '.join(self.cleaned_data['text_content_cleaned'])
        words = re.findall(r'\b\w+\b', all_text.lower())
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                     'should', 'may', 'might', 'must', 'can', 'that', 'this', 'these', 'those'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        word_freq = Counter(filtered_words).most_common(10)
        
        if word_freq:
            words_list, counts_list = zip(*word_freq)
            plt.barh(range(len(words_list)), counts_list, color='mediumpurple', alpha=0.7)
            plt.yticks(range(len(words_list)), words_list)
            plt.title('Top 10 Most Common Words', fontsize=14, fontweight='bold')
            plt.xlabel('Frequency')
            plt.gca().invert_yaxis()
        
        # Subplot 8: Subject-wise word count comparison
        plt.subplot(2, 4, 8)
        avg_word_counts = self.cleaned_data.groupby('subject')['text_content_cleaned'].apply(lambda x: x.str.split().str.len().mean())
        bars = plt.bar(avg_word_counts.index, avg_word_counts.values, color='lightsteelblue', alpha=0.7)
        plt.title('Average Word Count by Subject', fontsize=14, fontweight='bold')
        plt.xlabel('Subject')
        plt.ylabel('Average Word Count')
        plt.xticks(rotation=45)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_plots:
            os.makedirs('outputs', exist_ok=True)
            
            # Remove old image file to force regeneration
            old_image_path = 'outputs/comprehensive_data_analysis.png'
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
                print("✓ Removed old analytics image")
            
            plt.savefig('outputs/comprehensive_data_analysis.png', dpi=300, bbox_inches='tight')
            print("✓ Comprehensive EDA visualization saved to outputs/comprehensive_data_analysis.png")
        
        # Close the figure to free memory
        plt.close(fig)
        
        # Print detailed summary statistics
        print("\n📊 Comprehensive Dataset Summary:")
        print("=" * 50)
        print(f"📚 Total records: {len(self.cleaned_data)}")
        print(f"📖 Subjects: {len(subject_counts)} ({', '.join(subject_counts.index.tolist())})")
        print(f"📝 Total topics: {self.cleaned_data['topic'].nunique()}")
        print(f"📊 Average text length: {text_lengths.mean():.1f} characters")
        print(f"📊 Average word count: {word_counts.mean():.1f} words")
        print(f"📊 Average sentences: {sentence_counts.mean():.1f} per text")
        
        # Subject-wise breakdown
        print(f"\n📋 Subject-wise Breakdown:")
        for subject in subject_counts.index:
            count = subject_counts[subject]
            topics = topic_counts[subject]
            avg_len = self.cleaned_data[self.cleaned_data['subject'] == subject]['text_content_cleaned'].str.len().mean()
            print(f"  • {subject}: {count} records, {topics} topics, avg {avg_len:.0f} chars")
        
        return {
            'total_records': len(self.cleaned_data),
            'subject_distribution': subject_counts.to_dict(),
            'topic_counts': topic_counts.to_dict(),
            'avg_text_length': text_lengths.mean(),
            'avg_word_count': word_counts.mean(),
            'avg_sentence_count': sentence_counts.mean(),
            'most_common_words': word_freq[:10] if word_freq else [],
            'subjects': subject_counts.index.tolist()
        }
    
    def save_user_input(self, subject, study_hours, selected_topics=None, filename=None):
        """Save user inputs to JSON file"""
        if filename is None:
            # Use absolute path to ensure it works from any directory
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filename = os.path.join(base_dir, 'data', 'user_inputs.json')
            
        user_data = {
            'subject': subject,
            'study_hours': study_hours,
            'selected_topics': selected_topics or [],
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
    
    def analyze_user_behavior(self, user_inputs_path=None):
        """
        Analyze user behavior patterns from saved user inputs
        
        Args:
            user_inputs_path (str): Path to user inputs JSON file
        """
        if user_inputs_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            user_inputs_path = os.path.join(base_dir, 'data', 'user_inputs.json')
        
        if not os.path.exists(user_inputs_path):
            print(f"ℹ️  No user behavior data found at {user_inputs_path}")
            return None
        
        try:
            with open(user_inputs_path, 'r') as f:
                user_data = json.load(f)
            
            if not isinstance(user_data, list):
                user_data = [user_data]
            
            df = pd.DataFrame(user_data)
            
            if df.empty:
                print("ℹ️  No user behavior data to analyze")
                return None
            
            print("📈 Analyzing user behavior patterns...")
            
            # Set matplotlib backend for web compatibility
            import matplotlib
            matplotlib.use('Agg')  # Use non-interactive backend
            import matplotlib.pyplot as plt
            
            # Create behavior analysis visualization
            plt.figure(figsize=(15, 10))
            
            # Subject preferences
            plt.subplot(2, 3, 1)
            if 'subject' in df.columns:
                subject_prefs = df['subject'].value_counts()
                colors = plt.cm.Pastel1(np.linspace(0, 1, len(subject_prefs)))
                plt.pie(subject_prefs.values, labels=subject_prefs.index, autopct='%1.1f%%',
                       colors=colors, startangle=90)
                plt.title('Subject Preferences', fontsize=14, fontweight='bold')
            
            # Study hours distribution
            plt.subplot(2, 3, 2)
            if 'study_hours' in df.columns:
                plt.hist(df['study_hours'], bins=10, color='lightblue', alpha=0.7, edgecolor='black')
                plt.axvline(df['study_hours'].mean(), color='red', linestyle='--',
                           label=f'Mean: {df["study_hours"].mean():.1f}h')
                plt.title('Study Hours Distribution', fontsize=14, fontweight='bold')
                plt.xlabel('Hours per Day')
                plt.ylabel('Frequency')
                plt.legend()
            
            # Usage timeline
            plt.subplot(2, 3, 3)
            if 'timestamp' in df.columns:
                try:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df['date'] = df['timestamp'].dt.date
                    daily_usage = df.groupby('date').size()
                    daily_usage.plot(kind='line', marker='o', color='green', alpha=0.7)
                    plt.title('Daily Usage Pattern', fontsize=14, fontweight='bold')
                    plt.xlabel('Date')
                    plt.ylabel('Number of Sessions')
                    plt.xticks(rotation=45)
                except:
                    plt.text(0.5, 0.5, 'Timeline data\nnot available', 
                            ha='center', va='center', transform=plt.gca().transAxes,
                            fontsize=12)
                    plt.axis('off')
            
            # Topic selection patterns
            plt.subplot(2, 3, 4)
            if 'selected_topics' in df.columns:
                all_topics = []
                for topics in df['selected_topics']:
                    if isinstance(topics, list):
                        all_topics.extend(topics)
                
                if all_topics:
                    topic_counts = Counter(all_topics).most_common(10)
                    if topic_counts:
                        topics, counts = zip(*topic_counts)
                        plt.barh(range(len(topics)), counts, color='coral', alpha=0.7)
                        plt.yticks(range(len(topics)), topics)
                        plt.title('Most Selected Topics', fontsize=14, fontweight='bold')
                        plt.xlabel('Selection Count')
                        plt.gca().invert_yaxis()
                    else:
                        plt.text(0.5, 0.5, 'No topic\nselections', 
                                ha='center', va='center', transform=plt.gca().transAxes)
                        plt.axis('off')
                else:
                    plt.text(0.5, 0.5, 'No topic\nselections', 
                            ha='center', va='center', transform=plt.gca().transAxes)
                    plt.axis('off')
            
            # Study hours vs Subject correlation
            plt.subplot(2, 3, 5)
            if 'subject' in df.columns and 'study_hours' in df.columns:
                subject_hours = df.groupby('subject')['study_hours'].mean()
                bars = plt.bar(subject_hours.index, subject_hours.values, 
                              color='lightgreen', alpha=0.7)
                plt.title('Avg Study Hours by Subject', fontsize=14, fontweight='bold')
                plt.xlabel('Subject')
                plt.ylabel('Average Hours')
                plt.xticks(rotation=45)
                
                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                            f'{height:.1f}', ha='center', va='bottom')
            
            # User engagement metrics
            plt.subplot(2, 3, 6)
            metrics_text = f"""
User Engagement Metrics:

📊 Total Sessions: {len(df)}
📚 Unique Subjects: {df['subject'].nunique() if 'subject' in df.columns else 'N/A'}
⏰ Avg Study Hours: {df['study_hours'].mean():.1f}h
📈 Most Popular Subject: {df['subject'].mode().iloc[0] if 'subject' in df.columns and not df['subject'].empty else 'N/A'}
🎯 Total Topics Selected: {sum(len(topics) if isinstance(topics, list) else 0 for topics in df.get('selected_topics', []))}
            """
            plt.text(0.1, 0.9, metrics_text, transform=plt.gca().transAxes, 
                    fontsize=11, verticalalignment='top',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.7))
            plt.axis('off')
            plt.title('Engagement Summary', fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            
            # Save plot
            os.makedirs('outputs', exist_ok=True)
            plt.savefig('outputs/user_behavior_analysis.png', dpi=300, bbox_inches='tight')
            print("✓ User behavior analysis saved to outputs/user_behavior_analysis.png")
            
            # Close the figure to free memory
            plt.close()
            
            # Generate insights
            insights = {
                'total_sessions': len(df),
                'unique_subjects': df['subject'].nunique() if 'subject' in df.columns else 0,
                'avg_study_hours': df['study_hours'].mean() if 'study_hours' in df.columns else 0,
                'most_popular_subject': df['subject'].mode().iloc[0] if 'subject' in df.columns and not df['subject'].empty else None,
                'subject_preferences': df['subject'].value_counts().to_dict() if 'subject' in df.columns else {},
                'study_hours_distribution': df['study_hours'].describe().to_dict() if 'study_hours' in df.columns else {}
            }
            
            print("\n📈 User Behavior Insights:")
            print("=" * 40)
            print(f"📊 Total study sessions: {insights['total_sessions']}")
            print(f"📚 Subjects explored: {insights['unique_subjects']}")
            print(f"⏰ Average study time: {insights['avg_study_hours']:.1f} hours/day")
            if insights['most_popular_subject']:
                print(f"🎯 Most popular subject: {insights['most_popular_subject']}")
            
            return insights
            
        except Exception as e:
            print(f"✗ Error analyzing user behavior: {e}")
            return None
    
    def get_subject_content(self, subject):
        """Get all content for a specific subject"""
        if self.cleaned_data is None:
            return None
        
        subject_data = self.cleaned_data[self.cleaned_data['subject'].str.lower() == subject.lower()]
        return subject_data.to_dict('records')
    
    def generate_data_report(self, output_path='outputs/data_report.json'):
        """Generate comprehensive data report"""
        if self.cleaned_data is None:
            print("✗ No cleaned data available for report generation")
            return None
        
        print("📋 Generating comprehensive data report...")
        
        # Collect all statistics
        report = {
            'generation_timestamp': datetime.now().isoformat(),
            'dataset_overview': {
                'total_records': len(self.cleaned_data),
                'total_subjects': self.cleaned_data['subject'].nunique(),
                'total_topics': self.cleaned_data['topic'].nunique(),
                'data_sources': self.cleaned_data['source'].value_counts().to_dict() if 'source' in self.cleaned_data.columns else {'original': len(self.cleaned_data)}
            },
            'subject_analysis': {
                'distribution': self.cleaned_data['subject'].value_counts().to_dict(),
                'topics_per_subject': self.cleaned_data.groupby('subject')['topic'].nunique().to_dict(),
                'avg_text_length_per_subject': self.cleaned_data.groupby('subject')['text_content_cleaned'].apply(lambda x: x.str.len().mean()).to_dict()
            },
            'content_statistics': {
                'avg_text_length': self.cleaned_data['text_content_cleaned'].str.len().mean(),
                'avg_word_count': self.cleaned_data['text_content_cleaned'].str.split().str.len().mean(),
                'text_length_distribution': {
                    'min': self.cleaned_data['text_content_cleaned'].str.len().min(),
                    'max': self.cleaned_data['text_content_cleaned'].str.len().max(),
                    'median': self.cleaned_data['text_content_cleaned'].str.len().median(),
                    'std': self.cleaned_data['text_content_cleaned'].str.len().std()
                }
            }
        }
        
        # Save report
        os.makedirs('outputs', exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"✓ Data report saved to {output_path}")
        return report

# Example usage and testing
if __name__ == "__main__":
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    
    # Collect Wikipedia data (optional - comment out if you want to skip)
    print("🌐 Collecting Wikipedia data...")
    wikipedia_data = preprocessor.collect_wikipedia_data(topics_per_subject=2)
    
    # Load and process data
    raw_data = preprocessor.load_data(include_wikipedia=True)
    if raw_data is not None:
        cleaned_data = preprocessor.preprocess_data()
        
        # Perform comprehensive EDA
        eda_results = preprocessor.perform_eda()
        
        # Save sample user input
        preprocessor.save_user_input("Mathematics", 3, selected_topics=["Algebra", "Calculus"])
        preprocessor.save_user_input("Physics", 2, selected_topics=["Mechanics"])
        
        # Analyze user behavior
        behavior_insights = preprocessor.analyze_user_behavior()
        
        # Generate comprehensive report
        report = preprocessor.generate_data_report()
        
        print("\n✅ Enhanced data preprocessing module completed successfully!")
        print("📊 Features demonstrated:")
        print("  • Wikipedia data collection")
        print("  • Comprehensive EDA with 9 visualizations")
        print("  • User behavior analysis")
        print("  • Data quality reporting")
        print("  • Enhanced data cleaning and preprocessing")
    else:
        print("✗ Failed to load data. Please check data files.")