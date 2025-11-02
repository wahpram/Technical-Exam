# Question 2

OLLAMA CHAT INTERFACE - AI MODEL INTEGRATION

Repository sturcture:
-----------------------------
* app.py — aplikasi chat interface Streamlit
* requirements.txt — daftar dependencies Python
* README.txt — dokumentasi project (file ini)

Quickstart
----------

1. Siapkan Environment
   * Python 3.8+ rekomendasi
   * Install Ollama dari https://ollama.com
   * Install dependency:
```
pip install -r requirements.txt
```

2. Download Model
   * Pull model Gemma3:1b:
```
ollama pull gemma3:1b
```

   * Verifikasi model tersedia:
```
ollama list
```

3. Jalankan Aplikasi
   * Start aplikasi:
```
streamlit run app.py
```

   * Akses di browser: http://localhost:8501

Penggunaan:

* Chat Interface:
  - Ketik prompt di input box
  - Tekan Enter untuk mengirim
  - AI akan merespons dalam beberapa detik

* Clear History:
  - Klik tombol "Clear Chat History" di sidebar untuk menghapus history chat

* Status Monitoring:
  - Cek status koneksi Ollama di sidebar
  - Status "Connected" menunjukkan Ollama siap digunakan


Fungsi Utama

* `check_ollama_connection()` — app.py
  Mengecek koneksi ke Ollama service dan mengembalikan status koneksi

* `get_ollama_response(prompt)` — app.py
  Mengirim prompt ke model Gemma3:1b dan menerima respons dari AI

* Streamlit session_state — menyimpan history percakapan selama session aktif

Flow Aplikasi

1. Aplikasi mengecek koneksi ke Ollama service
2. User memasukkan prompt melalui chat input
3. Query dikirim ke Ollama API dengan model gemma3:1b
4. Model memproses dan generate respons
5. Respons ditampilkan di chat interface dengan timestamp
6. History chat disimpan di session state
7. User dapat melanjutkan percakapan atau clear history

Tips

* Pastikan status Ollama "Connected" sebelum memulai chat
* Clear history secara berkala jika percakapan sudah sangat panjang
* Test dengan berbagai jenis pertanyaan untuk evaluasi model
* Periksa console/terminal untuk log error jika ada masalah

Referensi Cepat File/Symbol

* app.py — aplikasi utama
* requirements.txt
  - ollama==0.3.3
  - streamlit==1.39.0
  - requests==2.32.3
* `check_ollama_connection()` — app.py
* `get_ollama_response(prompt)` — app.py
* Streamlit session_state — penyimpanan history chat

========================================