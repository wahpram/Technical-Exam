"""
Module untuk preprocessing data
"""

import pandas as pd
import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Initialisasi Sastrawi
factory_sw = StopWordRemoverFactory()
stopword_remover = factory_sw.create_stop_word_remover()

factory_stem = StemmerFactory()
stemmer = factory_stem.create_stemmer()


def remove_noise(text):
    """Menghapuse URL, emails, mentions, hashtag"""
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    return text


def remove_punctuation(text):
    """Menghapus Punctuation/Tanda Baca"""
    text = text.translate(str.maketrans('','', string.punctuation))
    return text


def remove_stopwords(text):
    """"Menghapus Stopwords Indonesia"""
    text = stopword_remover.remove(text)
    return text


def stem_text(text):
    """Stemming dengan Sastrawi"""
    stemmed = stemmer.stem(text)
    return stemmed


def preprocess_text(text):
    """
    Preprocessing pipeline:
    1. Lowercase/Casefolding
    2. Menghapus noise
    3. Menghapus punctuation
    4. Menghapus stopwords
    5. Stemming
    """
    
    # Lowercase/Casefolding
    text = str(text).lower()
    
    # Menghapus Noise
    text = remove_noise(text)
    
    # Menghapus Punctuation
    text = remove_punctuation(text)
    
    # Menghapus Stopwords
    text = remove_stopwords(text)
    
    # Stemming
    text = stem_text(text) 
    
    return text


def clean_data(input_file, output_file):
    """
    Membersihkan dataset dan save ke file csv

    Args:
        input_file (str): Path ke data raw
        output_file (str): Path untuk save clean data

    Returns:
        pd.Dataframe: Cleaned dataframe
    """
    
    # Read dataset
    df = pd.read_csv(input_file)
    
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns='Unnamed: 0')
    
    print(f"Original data shape: {df.shape}")
    
    # Cek missing values
    print(f"\nMissing values:\n{df.isnull().sum()}")
    
    # Menghapus data duplikat
    duplicates = df.duplicated().sum()
    print(f"\nDuplicate data: {duplicates}")
    df = df.drop_duplicates()
    print(f"Data shape after removing duplicates: {df.shape}")
    
    # Cek distribusi data
    print(f"\nLabel distribution:\n{df['label'].value_counts()}")
    
    # Preprocess data questions
    print("\nPreprocessing text...")
    df['question'] = df['question'].apply(preprocess_text)
    
    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"\nCleaned data saved to: {output_file}")
    
    return df


if __name__ == "__main__":
    # Test data preprocessing
    test_text = "Internet mati, bisakah ada teknisi membantu?"
    print(f"Original: {test_text}")
    print(f"Preprocessed: {preprocess_text(test_text)}")