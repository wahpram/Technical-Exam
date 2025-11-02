"""
Modul untuk prediksi menggunakan trained model
"""

import joblib
from .preprocessing import preprocess_text
import config


class MessageClassifier:
    """Class untuk klasifikasi pesan cutomer"""
    
    def __init__(self):
        """Inisialisasi dengan trained models"""
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self.load_models()
        
    
    def load_models(self):
        """Load trained model, vectorizer, dan label encoder"""
        try:
            self.model = joblib.load(config.SVM_MODEL_FILE)
            self.vectorizer = joblib.load(config.VECTORIZER_FILE)
            self.label_encoder = joblib.load(config.LABEL_ENCODER_FILE)
            print("Model load success")
        except FileNotFoundError as e:
            print(f"Error loading model: {e}")
            print("Train model dengan: python main.py --mode train")
    
    
    def predict(self, text):
        """
        Predict kategori untuk teks input

        Args:
            text (str): Input teks untuk diprediksi
        
        Returns:
            str: Predicted category
        """
        if not all([self.model, self.vectorizer, self.label_encoder]):
            raise ValueError("Model not loaded. Train or load model first")
        
        # Preprocess
        preprocessed_text = preprocess_text(text)
        
        # Vectorize
        text_vectorized = self.vectorizer.transform([preprocessed_text])
        
        # Predict
        prediction = self.model.predict(text_vectorized)[0]
        
        return prediction

    
    def predict_proba(self, text):
        """
        Predict probabilitas untuk setiap kategori
        
        Args:
            text (str): Input text
        
        Returns:
            dict: Dictionary dengan kategori dan probabilitasnya
        """
        if not hasattr(self.model, 'decision_function'):
            return None
        
        # Preprocess
        processed_text = preprocess_text(text)
        
        # Vectorize
        text_vectorized = self.vectorizer.transform([processed_text])
        
        # Get decision scores
        scores = self.model.decision_function(text_vectorized)[0]
        
        # Create result dictionary
        result = {}
        for i, label in enumerate(self.label_encoder.classes_):
            result[label] = scores[i] if len(scores) > 1 else scores
        
        return result
    
    
def predict_category(text):
    """
    Function untuk prediksi single input

    Args:
        text (str): Input text
    
    Returns:
        str: Predicted category
    """
    classifier = MessageClassifier()
    return classifier.predict(text)


def predict_batch(texts):
    """
    Function untuk prediksi batch input

    Args:
        texts (str): Input text
    
    Returns:
        list: List of prediction
    """
    classifier = MessageClassifier()
    predictions = []
    
    for text in texts:
        pred = classifier.predict(text)
        predictions.append({
            'text': text,
            'prediction': pred
        })
    
    return predictions


if __name__ == "__main__":
    # Test prediction
    test_texts = [
        "Wifi saya bermasalah, bisa kirimkan teknisi?",
        "Saya mau tau paket di Biznet",
        "Ping saya tinggi"
    ]
    
    print("Testing predictions:\n")
    classifier = MessageClassifier()
    
    for text in test_texts:
        pred = classifier.predict(text)
        print(f"Text: {text}")
        print(f"Prediction: {pred}\n")