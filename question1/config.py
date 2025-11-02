"""
Configuration File Customer Message Classification
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data/clean')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

RAW_DATA = os.path.join(DATA_DIR, 'question_list_labeled.csv')
PROCESSED_DATA = os.path.join(DATA_DIR, 'question_list_modeling.csv')

SVM_MODEL_FILE = os.path.join(MODELS_DIR, 'svm_model.pkl')
VECTORIZER_FILE = os.path.join(MODELS_DIR, 'tfidf_vectorizer.pkl')
LABEL_ENCODER_FILE = os.path.join(MODELS_DIR, 'label_encoder.pkl')

TEST_SIZE = 0.2
RANDOM_STATE = 42
TFIDF_MAX_FEATURES = 5000
TFIDF_NGRAM_RANGE = (1, 2)

SVM_KERNEL = 'linear'
SVM_CLASS_WEIGHT = 'balanced'

CATEGORIES = ['Information', 'Problem', 'Request']

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)