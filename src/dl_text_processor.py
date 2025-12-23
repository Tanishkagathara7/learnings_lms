"""
Deep Learning Module - Text Summarization & Feedback Generation
Implements neural networks using Keras for text processing tasks
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, LSTM, Embedding, Input, GlobalMaxPooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import pickle
import os
import random
import re

class TextProcessor:
    def __init__(self, max_vocab_size=5000, max_sequence_length=100):
        """Initialize the text processing system"""
        self.max_vocab_size = max_vocab_size
        self.max_sequence_length = max_sequence_length
        self.tokenizer = None
        self.summarization_model = None
        self.feedback_model = None
        self.glove_embeddings = None
        
    def create_sample_data(self):
        """Create sample data for training text summarization"""
        # Sample educational texts with their summaries
        training_data = [
            {
                'text': "Algebra is a branch of mathematics dealing with symbols and the rules for manipulating those symbols. In elementary algebra, those symbols represent quantities without fixed values, known as variables. Linear equations form the foundation of algebraic thinking, where we solve for unknown variables using mathematical operations. The distributive property allows us to expand expressions like a(b + c) = ab + ac. Solving equations involves isolating the variable on one side of the equation.",
                'summary': "Algebra uses symbols as variables in mathematical equations and operations."
            },
            {
                'text': "Classical mechanics is a physical theory describing the motion of macroscopic objects, from projectiles to parts of machinery, and astronomical objects. It provides extremely accurate results when studying large objects that are not extremely massive and speeds not approaching the speed of light. Newton's laws of motion form the foundation of classical mechanics, describing the relationship between forces and motion.",
                'summary': "Classical mechanics describes motion of large objects using Newton's laws."
            },
            {
                'text': "Cell biology is a branch of biology studying the structure and function of the cell, the basic unit of life. Cells consist of cytoplasm enclosed within a membrane, which contains many biomolecules such as proteins and nucleic acids. The nucleus controls cell activities and contains genetic material. Mitochondria produce energy for cellular processes through cellular respiration.",
                'summary': "Cell biology studies cells, the basic units of life with specialized structures."
            },
            {
                'text': "Computer programming is the process of creating a set of instructions that tell a computer how to perform a task. Programming can be done using a variety of computer programming languages, such as Python, Java, C++, and many others. Each language has its own syntax and rules. Programs are written in source code, which is then compiled or interpreted to create executable instructions.",
                'summary': "Programming creates computer instructions using various programming languages."
            },
            {
                'text': "Organic chemistry is a subdiscipline of chemistry that studies the structure, properties, composition, reactions, and preparation of carbon-based compounds. These compounds may contain any number of other elements, including hydrogen, nitrogen, oxygen, and halogens. Carbon atoms can form four bonds, allowing for complex molecular structures. Functional groups determine the chemical properties of organic molecules.",
                'summary': "Organic chemistry studies carbon-based compounds and their properties."
            },
            {
                'text': "Statistics is the discipline that concerns the collection, organization, analysis, interpretation, and presentation of data. Descriptive statistics summarize data from a sample using indexes such as the mean or standard deviation. Inferential statistics draw conclusions from data that are subject to random variation. Probability theory provides the mathematical foundation for statistical inference.",
                'summary': "Statistics involves collecting, analyzing, and interpreting data using mathematical methods."
            }
        ]
        
        return training_data
    
    def prepare_tokenizer(self, texts):
        """Prepare and fit tokenizer on text data"""
        self.tokenizer = Tokenizer(num_words=self.max_vocab_size, oov_token="<OOV>")
        self.tokenizer.fit_on_texts(texts)
        
        print(f"✓ Tokenizer prepared with vocabulary size: {len(self.tokenizer.word_index)}")
        return self.tokenizer
    
    def create_simple_embeddings(self, embedding_dim=50):
        """Create simple embeddings matrix (simulating GloVe-style embeddings)"""
        vocab_size = min(self.max_vocab_size, len(self.tokenizer.word_index) + 1)
        
        # Create random embeddings (in practice, you'd load pre-trained GloVe)
        embeddings_matrix = np.random.normal(0, 0.1, (vocab_size, embedding_dim))
        
        # Set padding token to zeros
        embeddings_matrix[0] = np.zeros(embedding_dim)
        
        self.glove_embeddings = embeddings_matrix
        print(f"✓ Created embeddings matrix: {embeddings_matrix.shape}")
        return embeddings_matrix
    
    def build_summarization_model(self, embedding_dim=50):
        """Build a simple neural network for text summarization"""
        vocab_size = min(self.max_vocab_size, len(self.tokenizer.word_index) + 1)
        
        # Create embeddings if not exists
        if self.glove_embeddings is None:
            self.create_simple_embeddings(embedding_dim)
        
        # Build model architecture
        model = Sequential([
            Embedding(vocab_size, embedding_dim, 
                     weights=[self.glove_embeddings],
                     input_length=self.max_sequence_length,
                     trainable=False),
            GlobalMaxPooling1D(),
            Dense(128, activation='relu'),
            Dense(64, activation='relu'),
            Dense(vocab_size, activation='softmax')  # Predict next word
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.summarization_model = model
        print("✓ Summarization model built successfully")
        return model
    
    def train_summarization_model(self):
        """Train the text summarization model"""
        print("🔄 Training text summarization model...")
        
        # Get training data
        training_data = self.create_sample_data()
        
        # Prepare texts
        all_texts = [item['text'] for item in training_data]
        all_summaries = [item['summary'] for item in training_data]
        
        # Prepare tokenizer
        self.prepare_tokenizer(all_texts + all_summaries)
        
        # Convert texts to sequences
        text_sequences = self.tokenizer.texts_to_sequences(all_texts)
        summary_sequences = self.tokenizer.texts_to_sequences(all_summaries)
        
        # Pad sequences
        X = pad_sequences(text_sequences, maxlen=self.max_sequence_length, padding='post')
        
        # For simplicity, we'll predict the first word of the summary
        y = np.array([seq[0] if len(seq) > 0 else 0 for seq in summary_sequences])
        
        # Build model
        self.build_summarization_model()
        
        # Train model (with limited epochs for demo)
        history = self.summarization_model.fit(
            X, y,
            epochs=10,
            batch_size=2,
            validation_split=0.2,
            verbose=1
        )
        
        print("✓ Text summarization model trained")
        return history
    
    def summarize_text(self, text, max_summary_length=50):
        """Generate a summary for input text"""
        if self.summarization_model is None or self.tokenizer is None:
            return "Model not trained. Please train the model first."
        
        # Simple extractive summarization approach
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= 2:
            return text[:max_summary_length] + "..."
        
        # Score sentences based on word frequency
        words = text.lower().split()
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        sentence_scores = {}
        for sentence in sentences:
            sentence_words = sentence.lower().split()
            score = sum(word_freq.get(word, 0) for word in sentence_words)
            sentence_scores[sentence] = score / len(sentence_words) if sentence_words else 0
        
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Create summary
        summary_sentences = [sent[0] for sent in top_sentences[:2]]
        summary = '. '.join(summary_sentences)
        
        # Truncate if too long
        if len(summary) > max_summary_length:
            summary = summary[:max_summary_length] + "..."
        
        return summary
    
    def generate_motivational_feedback(self, subject, performance_score=None):
        """Generate motivational feedback messages"""
        feedback_templates = {
            'Mathematics': [
                "Great work on Mathematics! Keep practicing those problem-solving skills.",
                "Mathematics is all about practice. You're building strong analytical thinking!",
                "Excellent progress in Math! Each problem you solve makes you stronger.",
                "Keep up the mathematical thinking! You're developing logical reasoning skills."
            ],
            'Physics': [
                "Physics concepts are clicking! Keep exploring the laws of nature.",
                "Great job understanding Physics! The universe's secrets are unfolding.",
                "Excellent work in Physics! You're thinking like a scientist.",
                "Keep questioning and experimenting! Physics rewards curiosity."
            ],
            'Chemistry': [
                "Chemistry progress is fantastic! You're mastering molecular interactions.",
                "Great work with Chemistry! Understanding reactions takes practice.",
                "Excellent chemical thinking! Keep exploring molecular structures.",
                "Chemistry success! You're building strong laboratory skills."
            ],
            'Biology': [
                "Biology understanding is growing! Life sciences are fascinating.",
                "Great progress in Biology! You're connecting with living systems.",
                "Excellent work exploring life! Biology rewards careful observation.",
                "Keep studying living systems! Your biological knowledge is expanding."
            ],
            'Computer Science': [
                "Coding skills are improving! Keep building those algorithms.",
                "Great programming progress! Logic and creativity are combining well.",
                "Excellent computational thinking! You're solving problems systematically.",
                "Keep coding! Each program you write strengthens your skills."
            ]
        }
        
        # Select appropriate feedback
        if subject in feedback_templates:
            feedback_options = feedback_templates[subject]
        else:
            feedback_options = [
                "Great work on your studies! Keep up the excellent effort.",
                "Learning progress is fantastic! Stay curious and keep exploring.",
                "Excellent academic work! Your dedication is paying off."
            ]
        
        # Add performance-based feedback
        if performance_score is not None:
            if performance_score >= 0.8:
                performance_feedback = "Outstanding performance! You're mastering this subject."
            elif performance_score >= 0.6:
                performance_feedback = "Good progress! Keep building on this foundation."
            else:
                performance_feedback = "Keep practicing! Every step forward counts."
            
            base_feedback = random.choice(feedback_options)
            return f"{base_feedback} {performance_feedback}"
        
        return random.choice(feedback_options)
    
    def save_models(self):
        """Save trained models and tokenizer"""
        os.makedirs('models', exist_ok=True)
        
        if self.summarization_model:
            self.summarization_model.save('models/summarization_model.h5')
        
        if self.tokenizer:
            with open('models/tokenizer.pkl', 'wb') as f:
                pickle.dump(self.tokenizer, f)
        
        if self.glove_embeddings is not None:
            np.save('models/embeddings.npy', self.glove_embeddings)
        
        print("✓ Deep learning models saved")
    
    def load_models(self):
        """Load trained models and tokenizer"""
        try:
            if os.path.exists('models/summarization_model.h5'):
                self.summarization_model = keras.models.load_model('models/summarization_model.h5')
            
            if os.path.exists('models/tokenizer.pkl'):
                with open('models/tokenizer.pkl', 'rb') as f:
                    self.tokenizer = pickle.load(f)
            
            if os.path.exists('models/embeddings.npy'):
                self.glove_embeddings = np.load('models/embeddings.npy')
            
            print("✓ Deep learning models loaded")
            return True
        except Exception as e:
            print(f"⚠ Error loading models: {e}")
            return False

# Example usage and testing
if __name__ == "__main__":
    # Initialize text processor
    processor = TextProcessor()
    
    # Train summarization model
    history = processor.train_summarization_model()
    
    # Test summarization
    sample_text = """
    Calculus is the mathematical study of continuous change. It has two major branches: 
    differential calculus concerning instantaneous rates of change and slopes of curves, 
    and integral calculus concerning accumulation of quantities and areas under curves. 
    The fundamental theorem of calculus connects these two branches and shows that 
    differentiation and integration are inverse operations.
    """
    
    summary = processor.summarize_text(sample_text)
    print(f"\n📝 Original text length: {len(sample_text)} characters")
    print(f"📝 Summary: {summary}")
    print(f"📝 Summary length: {len(summary)} characters")
    
    # Test feedback generation
    feedback = processor.generate_motivational_feedback("Mathematics", 0.85)
    print(f"\n💬 Motivational feedback: {feedback}")
    
    # Save models
    processor.save_models()
    
    print("\n✓ Deep Learning text processing module completed!")