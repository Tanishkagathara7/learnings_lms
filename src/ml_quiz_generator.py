"""
Machine Learning Module - Quiz Generation System
Implements Logistic Regression for difficulty classification and K-Means for resource clustering
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
import pickle
import json
import random
import os

class QuizGenerator:
    def __init__(self):
        """Initialize the quiz generation system"""
        self.difficulty_model = None
        self.clustering_model = None
        self.vectorizer = None
        self.tfidf_vectorizer = None
        self.quiz_data = self._create_quiz_database()
        
    def _create_quiz_database(self):
        """Create a comprehensive quiz database with questions and answers"""
        quiz_db = {
            'Mathematics': {
                'Algebra': [
                    {
                        'question': 'What is the solution to the equation 2x + 5 = 13?',
                        'options': ['x = 4', 'x = 6', 'x = 8', 'x = 9'],
                        'correct': 0,
                        'difficulty': 'easy'
                    },
                    {
                        'question': 'Which property allows us to write a(b + c) = ab + ac?',
                        'options': ['Commutative', 'Associative', 'Distributive', 'Identity'],
                        'correct': 2,
                        'difficulty': 'medium'
                    },
                    {
                        'question': 'What is the slope of the line passing through points (2, 3) and (4, 7)?',
                        'options': ['1', '2', '3', '4'],
                        'correct': 1,
                        'difficulty': 'medium'
                    }
                ],
                'Calculus': [
                    {
                        'question': 'What is the derivative of x²?',
                        'options': ['x', '2x', 'x²', '2x²'],
                        'correct': 1,
                        'difficulty': 'easy'
                    },
                    {
                        'question': 'What does the fundamental theorem of calculus connect?',
                        'options': ['Addition and subtraction', 'Multiplication and division', 
                                  'Differentiation and integration', 'Algebra and geometry'],
                        'correct': 2,
                        'difficulty': 'medium'
                    }
                ],
                'Statistics': [
                    {
                        'question': 'What measure of central tendency is most affected by outliers?',
                        'options': ['Mean', 'Median', 'Mode', 'Range'],
                        'correct': 0,
                        'difficulty': 'easy'
                    },
                    {
                        'question': 'In a normal distribution, what percentage of data falls within one standard deviation?',
                        'options': ['68%', '95%', '99.7%', '50%'],
                        'correct': 0,
                        'difficulty': 'medium'
                    }
                ]
            },
            'Physics': {
                'Mechanics': [
                    {
                        'question': 'What is Newton\'s first law of motion also known as?',
                        'options': ['Law of acceleration', 'Law of inertia', 'Law of action-reaction', 'Law of gravity'],
                        'correct': 1,
                        'difficulty': 'easy'
                    },
                    {
                        'question': 'If a ball is thrown horizontally, what is its initial vertical velocity?',
                        'options': ['Maximum', 'Minimum', 'Zero', 'Cannot be determined'],
                        'correct': 2,
                        'difficulty': 'medium'
                    }
                ],
                'Thermodynamics': [
                    {
                        'question': 'What does the first law of thermodynamics state?',
                        'options': ['Energy increases with temperature', 'Energy cannot be created or destroyed',
                                  'Heat flows from cold to hot', 'Entropy always decreases'],
                        'correct': 1,
                        'difficulty': 'easy'
                    }
                ],
                'Electromagnetism': [
                    {
                        'question': 'What type of charge do electrons carry?',
                        'options': ['Positive', 'Negative', 'Neutral', 'Variable'],
                        'correct': 1,
                        'difficulty': 'easy'
                    }
                ]
            },
            'Chemistry': {
                'Organic Chemistry': [
                    {
                        'question': 'What element is the basis of organic chemistry?',
                        'options': ['Hydrogen', 'Oxygen', 'Carbon', 'Nitrogen'],
                        'correct': 2,
                        'difficulty': 'easy'
                    },
                    {
                        'question': 'What type of bond is most common in organic compounds?',
                        'options': ['Ionic', 'Covalent', 'Metallic', 'Hydrogen'],
                        'correct': 1,
                        'difficulty': 'medium'
                    }
                ],
                'Inorganic Chemistry': [
                    {
                        'question': 'Which type of compound typically has high melting points?',
                        'options': ['Organic', 'Ionic', 'Covalent', 'Molecular'],
                        'correct': 1,
                        'difficulty': 'easy'
                    }
                ]
            },
            'Biology': {
                'Cell Biology': [
                    {
                        'question': 'What is the basic unit of life?',
                        'options': ['Atom', 'Molecule', 'Cell', 'Tissue'],
                        'correct': 2,
                        'difficulty': 'easy'
                    },
                    {
                        'question': 'What organelle is known as the powerhouse of the cell?',
                        'options': ['Nucleus', 'Mitochondria', 'Ribosome', 'Golgi apparatus'],
                        'correct': 1,
                        'difficulty': 'easy'
                    }
                ],
                'Genetics': [
                    {
                        'question': 'What does DNA stand for?',
                        'options': ['Deoxyribonucleic acid', 'Dinitrogen acid', 'Dynamic nucleic acid', 'Double nucleic acid'],
                        'correct': 0,
                        'difficulty': 'easy'
                    }
                ]
            },
            'Computer Science': {
                'Algorithms': [
                    {
                        'question': 'What is the time complexity of binary search?',
                        'options': ['O(n)', 'O(log n)', 'O(n²)', 'O(1)'],
                        'correct': 1,
                        'difficulty': 'medium'
                    },
                    {
                        'question': 'Which sorting algorithm has the best average-case time complexity?',
                        'options': ['Bubble sort', 'Selection sort', 'Merge sort', 'Insertion sort'],
                        'correct': 2,
                        'difficulty': 'medium'
                    }
                ],
                'Data Structures': [
                    {
                        'question': 'Which data structure follows LIFO principle?',
                        'options': ['Queue', 'Stack', 'Array', 'Linked List'],
                        'correct': 1,
                        'difficulty': 'easy'
                    }
                ]
            }
        }
        return quiz_db
    
    def prepare_training_data(self):
        """Prepare training data for difficulty classification"""
        questions = []
        difficulties = []
        
        for subject in self.quiz_data:
            for topic in self.quiz_data[subject]:
                for quiz_item in self.quiz_data[subject][topic]:
                    questions.append(quiz_item['question'])
                    difficulties.append(quiz_item['difficulty'])
        
        return questions, difficulties
    
    def train_difficulty_classifier(self):
        """Train logistic regression model for difficulty classification"""
        print("🔄 Training difficulty classification model...")
        
        questions, difficulties = self.prepare_training_data()
        
        # Convert text to features using Bag of Words
        self.vectorizer = CountVectorizer(max_features=1000, stop_words='english')
        X = self.vectorizer.fit_transform(questions)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, difficulties, test_size=0.2, random_state=42, stratify=difficulties
        )
        
        # Train logistic regression
        self.difficulty_model = LogisticRegression(random_state=42)
        self.difficulty_model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.difficulty_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"✓ Difficulty Classification Results:")
        print(f"  - Accuracy: {accuracy:.3f}")
        print(f"  - F1-Score: {f1:.3f}")
        print(f"  - Training samples: {X_train.shape[0]}")
        print(f"  - Test samples: {X_test.shape[0]}")
        
        return {
            'accuracy': accuracy,
            'f1_score': f1,
            'classification_report': classification_report(y_test, y_pred)
        }
    
    def train_topic_clustering(self, educational_data):
        """Train K-Means clustering for resource suggestions"""
        print("🔄 Training topic clustering model...")
        
        if educational_data is None or len(educational_data) == 0:
            print("✗ No educational data provided for clustering")
            return None
        
        # Prepare text data for clustering
        texts = [item['text_content_cleaned'] for item in educational_data]
        
        # Use TF-IDF for clustering
        self.tfidf_vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        X_tfidf = self.tfidf_vectorizer.fit_transform(texts)
        
        # Apply K-Means clustering
        n_clusters = min(5, len(texts))  # Ensure we don't have more clusters than samples
        self.clustering_model = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = self.clustering_model.fit_predict(X_tfidf)
        
        # Create cluster information
        cluster_info = {}
        for i, (text, label, item) in enumerate(zip(texts, cluster_labels, educational_data)):
            if label not in cluster_info:
                cluster_info[label] = {
                    'topics': [],
                    'subjects': set(),
                    'sample_text': text[:100] + "..."
                }
            cluster_info[label]['topics'].append(item['topic'])
            cluster_info[label]['subjects'].add(item['subject'])
        
        # Convert sets to lists for JSON serialization
        for cluster in cluster_info:
            cluster_info[cluster]['subjects'] = list(cluster_info[cluster]['subjects'])
        
        print(f"✓ Topic Clustering Results:")
        print(f"  - Number of clusters: {n_clusters}")
        print(f"  - Documents clustered: {len(texts)}")
        
        return cluster_info
    
    def generate_quiz(self, subject, num_questions=5):
        """Generate a quiz for a specific subject"""
        if subject not in self.quiz_data:
            return None
        
        # Collect all questions for the subject
        all_questions = []
        for topic in self.quiz_data[subject]:
            all_questions.extend(self.quiz_data[subject][topic])
        
        # Randomly select questions
        selected_questions = random.sample(
            all_questions, 
            min(num_questions, len(all_questions))
        )
        
        # Predict difficulty if model is trained
        if self.difficulty_model and self.vectorizer:
            for question in selected_questions:
                question_vector = self.vectorizer.transform([question['question']])
                predicted_difficulty = self.difficulty_model.predict(question_vector)[0]
                question['predicted_difficulty'] = predicted_difficulty
        
        quiz_result = {
            'subject': subject,
            'total_questions': len(selected_questions),
            'questions': selected_questions
        }
        
        return quiz_result
    
    def get_resource_suggestions(self, cluster_info):
        """Generate learning resource suggestions based on clusters"""
        resource_suggestions = {}
        
        # Predefined resource templates
        resource_templates = {
            'Mathematics': [
                "Khan Academy - Interactive math exercises",
                "MIT OpenCourseWare - Advanced mathematics",
                "Wolfram Alpha - Mathematical computation engine"
            ],
            'Physics': [
                "PhET Interactive Simulations - Physics concepts",
                "MIT Physics courses - Comprehensive lectures",
                "Feynman Lectures - Classic physics explanations"
            ],
            'Chemistry': [
                "ChemCollective - Virtual chemistry labs",
                "Coursera Chemistry courses - University level",
                "Royal Society of Chemistry - Educational resources"
            ],
            'Biology': [
                "Biology Online - Comprehensive biology dictionary",
                "NCBI Education - Molecular biology resources",
                "Crash Course Biology - Video explanations"
            ],
            'Computer Science': [
                "LeetCode - Programming practice problems",
                "GeeksforGeeks - Algorithm explanations",
                "Coursera CS courses - University partnerships"
            ]
        }
        
        for cluster_id, cluster_data in cluster_info.items():
            subjects = cluster_data['subjects']
            suggestions = []
            
            for subject in subjects:
                if subject in resource_templates:
                    suggestions.extend(random.sample(
                        resource_templates[subject], 
                        min(2, len(resource_templates[subject]))
                    ))
            
            resource_suggestions[f"Cluster_{cluster_id}"] = {
                'topics': cluster_data['topics'][:3],  # Show top 3 topics
                'subjects': subjects,
                'resources': suggestions[:3]  # Limit to 3 resources
            }
        
        return resource_suggestions
    
    def save_models(self):
        """Save trained models to disk"""
        os.makedirs('models', exist_ok=True)
        
        if self.difficulty_model:
            with open('models/difficulty_classifier.pkl', 'wb') as f:
                pickle.dump(self.difficulty_model, f)
            with open('models/count_vectorizer.pkl', 'wb') as f:
                pickle.dump(self.vectorizer, f)
        
        if self.clustering_model:
            with open('models/clustering_model.pkl', 'wb') as f:
                pickle.dump(self.clustering_model, f)
            with open('models/tfidf_vectorizer.pkl', 'wb') as f:
                pickle.dump(self.tfidf_vectorizer, f)
        
        print("✓ Models saved to models/ directory")
    
    def load_models(self):
        """Load trained models from disk"""
        try:
            with open('models/difficulty_classifier.pkl', 'rb') as f:
                self.difficulty_model = pickle.load(f)
            with open('models/count_vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
            with open('models/clustering_model.pkl', 'rb') as f:
                self.clustering_model = pickle.load(f)
            with open('models/tfidf_vectorizer.pkl', 'rb') as f:
                self.tfidf_vectorizer = pickle.load(f)
            print("✓ Models loaded successfully")
            return True
        except FileNotFoundError:
            print("⚠ Model files not found. Please train models first.")
            return False

# Example usage and testing
if __name__ == "__main__":
    # Initialize quiz generator
    quiz_gen = QuizGenerator()
    
    # Train difficulty classifier
    metrics = quiz_gen.train_difficulty_classifier()
    
    # Generate sample quiz
    math_quiz = quiz_gen.generate_quiz("Mathematics", 3)
    if math_quiz:
        print(f"\n📝 Sample Quiz for {math_quiz['subject']}:")
        for i, q in enumerate(math_quiz['questions'], 1):
            print(f"{i}. {q['question']}")
            for j, option in enumerate(q['options']):
                print(f"   {chr(65+j)}. {option}")
            print(f"   Correct: {chr(65+q['correct'])}")
            if 'predicted_difficulty' in q:
                print(f"   Predicted Difficulty: {q['predicted_difficulty']}")
            print()
    
    # Save models
    quiz_gen.save_models()
    
    print("✓ Machine Learning quiz generation module completed!")