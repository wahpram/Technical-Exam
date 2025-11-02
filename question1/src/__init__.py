
"""
Package Klasifikasi Pesa Customer

Module untuk klasifikasi pesan customer Biznet ke dalam kategori:
- Information: Pertanyaan tentang informasi/layanan
- Problem: Keluhan/masalah teknis
- Request: Permintaan layanan

Author: Wahyu Adwitya
Version: 1.0.0
"""

from .preprocessing import (
    preprocess_text,
    clean_data,
    remove_noise,
    remove_punctuation,
    remove_stopwords,
    stem_text
)

from .modeling import (
    prepare_data,
    vectorize_text,
    train_svm_model,
    evaluate_model,
    train_pipeline,
    save_models
)

from .prediction import (
    MessageClassifier,
    predict_category,
    predict_batch
)

__version__ = "1.0.0"
__author__ = "Your Name"

__all__ = [
    # Preprocessing
    'preprocess_text',
    'clean_data',
    'remove_noise',
    'remove_punctuation',
    'remove_stopwords',
    'stem_text',
    
    # Modeling
    'prepare_data',
    'vectorize_text',
    'train_svm_model',
    'evaluate_model',
    'train_pipeline',
    'save_models',
    
    # Prediction
    'MessageClassifier',
    'predict_category',
    'predict_batch'
]