# QUESTION 1

Klasifikasi Pesan Customer Biznet:

- `Information` — pertanyaan/info layanan  
- `Problem` — keluhan/masalah teknis  
- `Request` — permintaan layanan

Repository structure:

- [main.py](main.py) — CLI untuk preprocess, train, predict, batch, evaluate  
- [config.py](config.py) — konfigurasi (path & hyperparameter), contoh: [`config.RAW_DATA`](config.py), [`config.PROCESSED_DATA`](config.py), [`config.CATEGORIES`](config.py)  
- data/
  - [data/raw](data/raw) — dataset raw (e.g. `question_list.csv`, `question_list_labeled.csv`)  
  - [data/clean](data/clean) — dataset hasil preprocessing (e.g. `question_list_modeling.csv`)  
- src/ — modul inti
  - [`src.preprocessing.preprocess_text`](src/preprocessing.py) — pipeline pembersihan teks  
  - [`src.modeling.prepare_data`](src/modeling.py), [`src.modeling.train_pipeline`](src/modeling.py) — split, vektorisasi, training dan evaluasi  
  - [`src.prediction.MessageClassifier`](src/prediction.py), [`src.prediction.predict_category`](src/prediction.py) — inference single & batch  
- notebooks/ — notebook eksplorasi & modeling  
- models/ — model, tokenizer, dan encoder (.pkl)  
- results/ — output evaluasi  
- [requirements.txt](requirements.txt)

Quickstart

1. Siapkan environment
   - Python 3.11 rekomendasi
   - Install dependency:
     ```
     pip install -r [requirements.txt](http://_vscodecontentref_/0)
     ```

2. Preprocessing
   - Jalankan pipeline preprocessing via CLI:
     ```
     python [main.py](http://_vscodecontentref_/1) --mode preprocess
     ```
   - Fungsi utama: [`src.preprocessing.preprocess_text`](src/preprocessing.py)  
   - Input/Output default diatur di [config.py](config.py)

3. Training
   - Jalankan training pipeline:
     ```
     python [main.py](http://_vscodecontentref_/2) --mode train
     ```
   - Fungsi utama: [`src.modeling.prepare_data`](src/modeling.py), [`src.modeling.train_pipeline`](src/modeling.py)  
   - Model tersimpan di `models/` sesuai `[config.SVM_MODEL_FILE](config.py)`, vektorizer di `[config.VECTORIZER_FILE](config.py)`

4. Predict / Inference
   - Single prediction:
     ```
     python [main.py](http://_vscodecontentref_/3) --mode predict --text "Internet saya down, tolong bantu cek"
     ```
   - Batch prediction:
     ```
     python [main.py](http://_vscodecontentref_/4) --mode batch --file input.txt
     ```
   - API kelas: [`src.prediction.MessageClassifier`](src/prediction.py), fungsi util: [`src.prediction.predict_category`](src/prediction.py)

5. Evaluasi
   - Jalankan:
     ```
     python [main.py](http://_vscodecontentref_/5) --mode evaluate
     ```
   - Evaluasi menggunakan split & metrik di [`src.modeling.evaluate_model`](src/modeling.py)

Data notes
- Dataset:
  - [data/clean/question_list_labeled.csv](data/raw/question_list_labeled.csv)
  - [data/clean/question_list_modeling.csv](data/clean/question_list_modeling.csv)
- Notebooks untuk eksplorasi & preprocessing:
  - [notebooks/01_data_exploration_and_preprocessing.ipynb](notebooks/01_data_exploration_and_preprocessing.ipynb)  
  - [notebooks/02_modeling.ipynb](notebooks/02_modeling.ipynb)

Tips
- Periksa dan ubah pengaturan di [config.py](config.py) saat butuh mengubah path / hyperparameter.  
- Untuk debugging preprocessing, jalankan dan cek fungsi di [src/preprocessing.py](src/preprocessing.py).  
- Simpan model baru ke folder [models/](models) agar kode inference dapat memuat model yang benar.

Referensi cepat file/symbol:
- [main.py](main.py)  
- [config.py](config.py)  
- [`src.preprocessing.preprocess_text`](src/preprocessing.py) — [src/preprocessing.py](src/preprocessing.py)  
- [`src.modeling.prepare_data`](src/modeling.py), [`src.modeling.train_pipeline`](src/modeling.py) — [src/modeling.py](src/modeling.py)  
- [`src.prediction.MessageClassifier`](src/prediction.py), [`src.prediction.predict_category`](src/prediction.py) — [src/prediction.py](src/prediction.py)  
- [requirements.txt](requirements.txt)
