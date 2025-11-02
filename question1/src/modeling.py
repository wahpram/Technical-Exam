
"""
Modul untuk training dan evaluasi model
"""

import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt

import config


def prepare_data(data_file):
    """
    Load dan split data untuk training

    Args:
        data_file (str): Path ke data modeling
        
    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    
    # Read data
    df = pd.read_csv(data_file)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        df['question'],
        df['label'],
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE,
        stratify=df['label']
    )
    
    print(f"Training data: {len(X_train)}")
    print(f"Test data: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test


def vectorize_text(X_train, X_test):
    """
    TF-IDF Vectorization
    
    Args:
        X_train: Train text data
        X_test: Test text data
    
    Returns:
        tuple: vectorizer, X_train_tfidf, X_test_tfidf
    """
    vectorizer = TfidfVectorizer(
        max_features=config.TFIDF_MAX_FEATURES,
        ngram_range=config.TFIDF_NGRAM_RANGE
    )
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"TF-IDF features shape: {X_train_tfidf.shape}")
    
    return vectorizer, X_train_tfidf, X_test_tfidf


def train_svm_model(X_train_tfidf, y_train):
    """
    Melatih mode SVM dengan balanced class weight
    
    Args:
        X_train_tfidf: Vectorized training data
        y_train: Training labels
    
    Returns:
        model: Trained SVM model
    """
    # Menghitung sample weights
    sample_weights = compute_sample_weight(class_weight='balanced', y=y_train)
    
    # Train model SVM
    svm_model = SVC(
        kernel=config.SVM_KERNEL,
        class_weight=config.SVM_CLASS_WEIGHT,
        random_state=config.RANDOM_STATE
    )
    
    print("Training SVM model...")
    svm_model.fit(X_train_tfidf, y_train, sample_weight=sample_weights)
    print("Training completed!")
    
    return svm_model


def evaluate_model(model, X_test_tfidf, y_test):
    """
    Evaluasi performa model
    
    Args:
        model: Trained model
        X_test_tfidf: Vectorized test data
        y_test: Test labels
    
    Returns:
        dict: Evaluation metrics
    """
    # Predict
    y_pred = model.predict(X_test_tfidf)
    
    # Evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"\n{'='*50}")
    print("MODEL EVALUATION RESULTS")
    print(f"{'='*50}")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"\n{classification_report(y_test, y_pred)}")
    
    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }
    
    return y_pred, metrics


def plot_confusion_matrix(y_test, y_pred, label_encoder):
    """
    Plot confusion matrix
    
    Args:
        y_test: True labels
        y_pred: Predicted labels
        label_encoder: LabelEncoder object
    """
    labels = sorted(list(set(y_test) | set(y_pred)))
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=label_encoder.classes_
    )
    disp.plot(cmap='Blues')
    plt.title('Confusion Matrix - SVM Model')
    plt.tight_layout()
    plt.savefig(os.path.join(config.RESULTS_DIR, 'confusion_matrix.png'))
    print("\nConfusion matrix saved as 'confusion_matrix.png'")


def save_models(model, vectorizer, label_encoder):
    """
    Save trained model, vectorizer, dan label encoder
    
    Args:
        model: Trained SVM model
        vectorizer: TF-IDF vectorizer
        label_encoder: Label encoder
    """
    joblib.dump(model, config.SVM_MODEL_FILE)
    joblib.dump(vectorizer, config.VECTORIZER_FILE)
    joblib.dump(label_encoder, config.LABEL_ENCODER_FILE)
    
    print(f"\nModels saved:")
    print(f"- SVM model: {config.SVM_MODEL_FILE}")
    print(f"- Vectorizer: {config.VECTORIZER_FILE}")
    print(f"- Label encoder: {config.LABEL_ENCODER_FILE}")


def train_pipeline(data_file):
    """
    Training pipeline
    
    Args:
        data_file (str): Path ke cleaned data file
    
    Returns:
        tuple: model, vectorizer, label_encoder, metrics
    """
    print("Starting training pipeline...\n")
    
    # 1. Prepare data
    X_train, X_test, y_train, y_test = prepare_data(data_file)
    
    # 2. Label encoding
    df = pd.read_csv(data_file)
    le = LabelEncoder()
    le.fit(df['label'])
    
    # 3. Vectorize text
    vectorizer, X_train_tfidf, X_test_tfidf = vectorize_text(X_train, X_test)
    
    # 4. Train model
    model = train_svm_model(X_train_tfidf, y_train)
    
    # 5. Evaluasi model
    y_pred, metrics = evaluate_model(model, X_test_tfidf, y_test)
    
    # 6. Plot confusion matrix
    plot_confusion_matrix(y_test, y_pred, le)
    
    # 7. Save model
    save_models(model, vectorizer, le)
    
    return model, vectorizer, le, metrics


if __name__ == "__main__":
    # Test training
    train_pipeline(config.PROCESSED_DATA)

    