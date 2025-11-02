
"""
Main script untuk Klasifikasi Pesan Customer

Usage:
    # Data preprocessing
    python main.py --mode preprocess
    
    # Model training
    python main.py --mode train
    
    # Single prediction
    python main.py --mode predict --text "Contoh text"
    
    # Batch prediction
    python main.py --mode batch --file input.txt
    
    # Model evaluation
    python main.py --mode evaluate
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src import (
    clean_data,
    train_pipeline,
    MessageClassifier,
    predict_category
)
import config


def run_preprocessing():
    """Jalankan data preprocessing pipeline"""
    print("Data Preprocessing...")
    print("-"*40 + "\n")
    
    try:
        clean_data(config.RAW_DATA, config.PROCESSED_DATA)
        print("\nPreprocess completed")
    except Exception as e:
        print(f"\nError preprocessing: {e}")
        sys.exit(1)


def run_training():
    """Jalankan model training pipeline"""
    print("Model Training...")
    print("-"*40 + "\n")
    
    try:
        model, vectorizer, le, metrics = train_pipeline(config.PROCESSED_DATA)
        
        print("\n" + "-"*40)
        print("Hasil Train Model")
        print("-"*40)
        print(f"Model: SVM (Support Vector Machine)")
        print(f"Kernel: {config.SVM_KERNEL}")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"F1 Score: {metrics['f1_score']:.4f}")
        print("\nTraining completed")
        
    except Exception as e:
        print(f"\nError training: {e}")
        sys.exit(1)


def run_prediction(text):
    """Jalankan single text prediction"""
    print("Predict text...")
    print("-"*40 + "\n")
    
    try:
        classifier = MessageClassifier()
        prediction = classifier.predict(text)
        
        print(f"Input Text: {text}")
        print(f"Predicted Category: {prediction}")
        
        # Dapatkan probability score
        scores = classifier.predict_proba(text)
        if scores:
            print("\nDecision Scores:")
            for category, score in scores.items():
                print(f"  {category}: {score:.4f}")
        
        print("\nPrediction completed!")
        
    except Exception as e:
        print(f"\nError during prediction: {e}")
        sys.exit(1)


def run_batch_prediction(input_file):
    """Jalankan batch prediction from file"""
    print("Batch Prediction...")
    print("-"*40 + "\n")
    
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f if line.strip()]
        
        print(f"Processing {len(texts)} messages...\n")
        
        classifier = MessageClassifier()
        
        # Predict
        results = []
        for i, text in enumerate(texts, 1):
            pred = classifier.predict(text)
            results.append({
                'no': i,
                'text': text,
                'prediction': pred
            })
            print(f"{i}. [{pred}] {text}")
        
        # Save results
        output_file = input_file.replace('.txt', '_results.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            for r in results:
                f.write(f"{r['no']}. [{r['prediction']}] {r['text']}\n")
        
        print(f"\nHasil disimpan: {output_file}")
        
    except Exception as e:
        print(f"\nError during batch prediction: {e}")
        sys.exit(1)


def run_evaluation():
    """Jalankan model evaluation"""
    print("-"*40 + "\n")
    print("Model Evaluation...")
    print("-"*40 + "\n")
    
    try:
        from src.modeling import prepare_data, evaluate_model
        import joblib
        
        # Load model
        model = joblib.load(config.SVM_MODEL_FILE)
        vectorizer = joblib.load(config.VECTORIZER_FILE)
        
        # Prepare test data
        _, X_test, _, y_test = prepare_data(config.PROCESSED_DATA)
        X_test_tfidf = vectorizer.transform(X_test)
        
        # Evaluate
        y_pred, metrics = evaluate_model(model, X_test_tfidf, y_test)
        
        print("\nEvaluation completed")
        
    except Exception as e:
        print(f"\n✗ Error during evaluation: {e}")
        sys.exit(1)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Klasifikasi Teks Customer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            python main.py --mode preprocess
            python main.py --mode train
            python main.py --mode predict --text "Internet mati nih"
            python main.py --mode batch --file messages.txt
            python main.py --mode evaluate
        """
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        required=True,
        choices=['preprocess', 'train', 'predict', 'batch', 'evaluate'],
        help='Operation mode'
    )
    
    parser.add_argument(
        '--text',
        type=str,
        help='Text untuk single prediction'
    )
    
    parser.add_argument(
        '--file',
        type=str,
        help='Input file untuk batch prediction'
    )
    
    args = parser.parse_args()
    
    # Route ke masing-masing fungsi
    if args.mode == 'preprocess':
        run_preprocessing()
        
    elif args.mode == 'train':
        run_training()
        
    elif args.mode == 'predict':
        if not args.text:
            print("Error: --text argument required for predict mode")
            sys.exit(1)
        run_prediction(args.text)
        
    elif args.mode == 'batch':
        if not args.file:
            print("Error: --file argument required for batch mode")
            sys.exit(1)
        run_batch_prediction(args.file)
        
    elif args.mode == 'evaluate':
        run_evaluation()


if __name__ == "__main__":
    main()