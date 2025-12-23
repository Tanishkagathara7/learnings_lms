"""
NLP Module - Study Tips Generator
Implements NLP fundamentals using NLTK for keyword extraction and tip generation
"""

import nltk
import pandas as pd
import numpy as np
from collections import Counter
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import os

class StudyTipsGenerator:
    def __init__(self):
        """Initialize the study tips generator"""
        self.download_nltk_data()
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.study_tips_database = self._create_tips_database()
        
    def download_nltk_data(self):
        """Download required NLTK data"""
        nltk_downloads = [
            'punkt', 'stopwords', 'averaged_perceptron_tagger',
            'wordnet', 'maxent_ne_chunker', 'words'
        ]
        
        for item in nltk_downloads:
            try:
                nltk.data.find(f'tokenizers/{item}')
            except LookupError:
                try:
                    nltk.download(item, quiet=True)
                except:
                    pass  # Continue if download fails
        
        print("✓ NLTK data initialized")
    
    def _create_tips_database(self):
        """Create a comprehensive database of study tips"""
        tips_db = {
            'general': [
                "Create a dedicated study schedule and stick to it consistently",
                "Take regular breaks using the Pomodoro Technique (25 min study, 5 min break)",
                "Find a quiet, well-lit study environment free from distractions",
                "Use active recall by testing yourself without looking at notes",
                "Teach concepts to others to reinforce your understanding",
                "Review material regularly using spaced repetition",
                "Get adequate sleep to consolidate memory and improve focus"
            ],
            'mathematics': [
                "Practice solving problems daily to build mathematical intuition",
                "Work through examples step-by-step before attempting new problems",
                "Create formula sheets and review them regularly",
                "Use visual aids like graphs and diagrams to understand concepts",
                "Join study groups to discuss problem-solving strategies",
                "Review basic arithmetic and algebra skills regularly",
                "Apply mathematical concepts to real-world scenarios"
            ],
            'physics': [
                "Understand the physical meaning behind mathematical equations",
                "Draw diagrams and free-body diagrams for every problem",
                "Practice dimensional analysis to check your answers",
                "Connect theoretical concepts with experimental observations",
                "Use simulation software to visualize physical phenomena",
                "Memorize key formulas and understand when to apply them",
                "Work on conceptual understanding before mathematical manipulation"
            ],
            'chemistry': [
                "Memorize the periodic table and understand periodic trends",
                "Practice balancing chemical equations regularly",
                "Understand molecular geometry and its effects on properties",
                "Connect macroscopic observations with molecular-level explanations",
                "Use molecular models to visualize three-dimensional structures",
                "Practice stoichiometry calculations with various problem types",
                "Review laboratory safety procedures and techniques"
            ],
            'biology': [
                "Create concept maps to connect biological processes",
                "Use mnemonics to remember complex biological terms",
                "Study biological processes at different organizational levels",
                "Connect structure and function relationships in living systems",
                "Use diagrams and flowcharts to understand biological pathways",
                "Practice identifying biological specimens and structures",
                "Stay updated with current biological research and discoveries"
            ],
            'computer_science': [
                "Practice coding problems daily to improve programming skills",
                "Understand algorithms and data structures thoroughly",
                "Debug code systematically using proper debugging techniques",
                "Read and analyze other people's code to learn different approaches",
                "Work on personal projects to apply theoretical knowledge",
                "Participate in coding competitions and challenges",
                "Stay updated with new programming languages and technologies"
            ],
            'reading': [
                "Preview the material before detailed reading",
                "Take notes while reading to maintain active engagement",
                "Summarize each section in your own words",
                "Ask questions about the material as you read",
                "Look up unfamiliar terms and concepts immediately"
            ],
            'practice': [
                "Start with easier problems and gradually increase difficulty",
                "Time yourself to improve speed and efficiency",
                "Review mistakes carefully to understand error patterns",
                "Seek help when stuck on challenging problems",
                "Practice under exam-like conditions regularly"
            ],
            'revision': [
                "Create comprehensive review schedules before exams",
                "Use multiple review methods: reading, writing, and verbal",
                "Focus extra time on your weakest topics",
                "Form study groups for collaborative review sessions",
                "Use past exams and practice tests for review"
            ]
        }
        return tips_db
    
    def preprocess_text(self, text):
        """Preprocess text for NLP analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords
        tokens = [token for token in tokens if token not in self.stop_words]
        
        # Remove short words
        tokens = [token for token in tokens if len(token) > 2]
        
        return tokens
    
    def extract_keywords(self, text, top_k=10):
        """Extract top keywords from text using frequency analysis"""
        # Preprocess text
        tokens = self.preprocess_text(text)
        
        # Count word frequencies
        word_freq = Counter(tokens)
        
        # Get top keywords
        top_keywords = word_freq.most_common(top_k)
        
        # Also perform POS tagging to identify important nouns and verbs
        pos_tokens = pos_tag(word_tokenize(text))
        important_pos = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        
        pos_keywords = []
        for word, pos in pos_tokens:
            if pos in important_pos and word.lower() not in self.stop_words and len(word) > 2:
                pos_keywords.append(word.lower())
        
        pos_freq = Counter(pos_keywords)
        top_pos_keywords = pos_freq.most_common(top_k)
        
        # Combine and deduplicate
        all_keywords = list(set([word for word, freq in top_keywords] + 
                               [word for word, freq in top_pos_keywords]))
        
        return {
            'frequency_keywords': [word for word, freq in top_keywords],
            'pos_keywords': [word for word, freq in top_pos_keywords],
            'combined_keywords': all_keywords[:top_k]
        }
    
    def identify_subject_domain(self, keywords):
        """Identify the subject domain based on keywords"""
        domain_keywords = {
            'mathematics': ['equation', 'algebra', 'calculus', 'geometry', 'statistics', 
                          'function', 'derivative', 'integral', 'matrix', 'probability'],
            'physics': ['force', 'energy', 'motion', 'wave', 'particle', 'field', 
                       'momentum', 'acceleration', 'velocity', 'thermodynamics'],
            'chemistry': ['molecule', 'atom', 'reaction', 'bond', 'element', 'compound', 
                         'solution', 'acid', 'base', 'organic'],
            'biology': ['cell', 'organism', 'gene', 'protein', 'evolution', 'species', 
                       'tissue', 'organ', 'dna', 'ecosystem'],
            'computer_science': ['algorithm', 'data', 'structure', 'programming', 'code', 
                               'software', 'computer', 'system', 'network', 'database']
        }
        
        domain_scores = {}
        for domain, domain_words in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in domain_words)
            domain_scores[domain] = score
        
        # Return the domain with highest score
        if domain_scores:
            best_domain = max(domain_scores, key=domain_scores.get)
            if domain_scores[best_domain] > 0:
                return best_domain
        
        return 'general'
    
    def generate_contextual_tips(self, text, subject=None, num_tips=5):
        """Generate contextual study tips based on text content"""
        # Extract keywords
        keyword_analysis = self.extract_keywords(text)
        keywords = keyword_analysis['combined_keywords']
        
        # Identify subject domain if not provided
        if subject is None:
            subject = self.identify_subject_domain(keywords)
        else:
            subject = subject.lower().replace(' ', '_')
        
        # Get base tips for the subject
        base_tips = self.study_tips_database.get(subject, self.study_tips_database['general'])
        
        # Generate contextual tips
        contextual_tips = []
        
        # Add subject-specific tips
        contextual_tips.extend(np.random.choice(base_tips, 
                                              min(3, len(base_tips)), 
                                              replace=False))
        
        # Add keyword-specific tips
        keyword_tips = []
        for keyword in keywords[:3]:  # Use top 3 keywords
            if 'problem' in keyword or 'equation' in keyword:
                keyword_tips.append(f"Practice {keyword}-related exercises daily")
            elif 'theory' in keyword or 'concept' in keyword:
                keyword_tips.append(f"Create concept maps for {keyword} understanding")
            elif 'experiment' in keyword or 'lab' in keyword:
                keyword_tips.append(f"Review {keyword} procedures and safety protocols")
            else:
                keyword_tips.append(f"Focus on understanding {keyword} fundamentals")
        
        contextual_tips.extend(keyword_tips)
        
        # Add general study strategy tips
        general_strategies = [
            "Use active recall techniques to test your knowledge",
            "Create summary notes for quick review sessions",
            "Form study groups to discuss challenging concepts",
            "Use spaced repetition for long-term retention",
            "Apply the Feynman Technique: explain concepts simply"
        ]
        
        contextual_tips.extend(np.random.choice(general_strategies, 2, replace=False))
        
        # Remove duplicates and limit to requested number
        unique_tips = list(dict.fromkeys(contextual_tips))  # Preserve order while removing duplicates
        
        return {
            'subject_identified': subject,
            'keywords_extracted': keywords,
            'study_tips': unique_tips[:num_tips],
            'total_tips_generated': len(unique_tips)
        }
    
    def analyze_study_content(self, text):
        """Perform comprehensive NLP analysis of study content"""
        # Basic text statistics
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        
        # Preprocessing
        clean_tokens = self.preprocess_text(text)
        
        # Keyword extraction
        keywords = self.extract_keywords(text)
        
        # POS tagging analysis
        pos_tags = pos_tag(words)
        pos_distribution = Counter([pos for word, pos in pos_tags])
        
        # Named entity recognition
        try:
            entities = ne_chunk(pos_tags)
            named_entities = []
            for chunk in entities:
                if hasattr(chunk, 'label'):
                    entity_name = ' '.join([token for token, pos in chunk.leaves()])
                    named_entities.append((entity_name, chunk.label()))
        except:
            named_entities = []
        
        # Readability metrics (simplified)
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        avg_word_length = np.mean([len(word) for word in clean_tokens]) if clean_tokens else 0
        
        analysis_result = {
            'text_statistics': {
                'total_sentences': len(sentences),
                'total_words': len(words),
                'unique_words': len(set(clean_tokens)),
                'avg_sentence_length': round(avg_sentence_length, 2),
                'avg_word_length': round(avg_word_length, 2)
            },
            'keywords': keywords,
            'pos_distribution': dict(pos_distribution.most_common(10)),
            'named_entities': named_entities[:5],  # Top 5 entities
            'readability': {
                'complexity_score': min(10, avg_sentence_length / 10 + avg_word_length / 5),
                'difficulty_level': 'Easy' if avg_sentence_length < 15 else 'Medium' if avg_sentence_length < 25 else 'Hard'
            }
        }
        
        return analysis_result
    
    def save_analysis_results(self, analysis_results, filename='outputs/nlp_analysis.json'):
        """Save NLP analysis results to file"""
        import json
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Convert numpy types to native Python types for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        # Clean the results for JSON serialization
        clean_results = {}
        for key, value in analysis_results.items():
            if isinstance(value, dict):
                clean_results[key] = {k: convert_numpy(v) for k, v in value.items()}
            else:
                clean_results[key] = convert_numpy(value)
        
        with open(filename, 'w') as f:
            json.dump(clean_results, f, indent=2)
        
        print(f"✓ NLP analysis results saved to {filename}")

# Example usage and testing
if __name__ == "__main__":
    # Initialize study tips generator
    tips_generator = StudyTipsGenerator()
    
    # Sample educational text
    sample_text = """
    Calculus is the mathematical study of continuous change. It has two major branches: 
    differential calculus and integral calculus. Differential calculus concerns 
    instantaneous rates of change and slopes of curves. Integral calculus concerns 
    accumulation of quantities and areas under curves. Students should practice 
    derivative calculations and integration techniques regularly. Understanding 
    the fundamental theorem of calculus is essential for connecting these concepts.
    """
    
    # Generate study tips
    tips_result = tips_generator.generate_contextual_tips(sample_text, num_tips=5)
    
    print("🎯 Study Tips Generation Results:")
    print(f"Subject identified: {tips_result['subject_identified']}")
    print(f"Keywords extracted: {', '.join(tips_result['keywords_extracted'][:5])}")
    print("\n📚 Generated Study Tips:")
    for i, tip in enumerate(tips_result['study_tips'], 1):
        print(f"{i}. {tip}")
    
    # Perform comprehensive NLP analysis
    analysis = tips_generator.analyze_study_content(sample_text)
    
    print(f"\n📊 NLP Analysis Results:")
    print(f"Total words: {analysis['text_statistics']['total_words']}")
    print(f"Unique words: {analysis['text_statistics']['unique_words']}")
    print(f"Difficulty level: {analysis['readability']['difficulty_level']}")
    print(f"Top keywords: {', '.join(analysis['keywords']['frequency_keywords'][:5])}")
    
    # Save results
    tips_generator.save_analysis_results(analysis)
    
    print("\n✓ NLP Study Tips Generator module completed!")