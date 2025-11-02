import streamlit as st
import ollama
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Ollama Chat Interface",
    layout="centered"
)

# Inisialisasi session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function cek koneksi model Ollama
def check_ollama_connection():
    """
    Fungsi untuk mengecek koneksi model Ollama

    Returns:
        boolena: Status koneksi ke Ollama
    """
    try:
        ollama.list()
        return True, "Ollama service running"
    except Exception as e:
        return False, f"Ollama service error: {str(e)}"


# Function untuk mendapatkan response dari model
def get_ollama_response(prompt):
    """
    Fungsi ini digunakan untuk mengirim prompt dan mendapatkan response dari model

    Args:
        prompt (str): Prompt dari user

    Returns:
        str: Response dari model
    """
    
    model="gemma3:1b"
    try:
        # Options dari model Ollama
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        return response['message']['content'], None
    except Exception as e:
        return None, f"Error: {str(e)}"


# Header aplikasi
st.title("Ollama Chat Interface")
st.markdown("### (Menggunakan Model Gemma3:1b)")

# Tampilkan history chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message["timestamp"])

# Input chat dari user
if prompt := st.chat_input("Ketik pertanyaan Anda di sini..."):
    # Tambahkan pesan user ke history
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Tampilkan pesan user
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)
    
    # Dapatkan dan tampilkan response dari model
    with st.chat_message("assistant"):
        with st.spinner("Mohon menunggu, Ollama sedang berpikir..."):
            response, error = get_ollama_response(
                prompt,
            )
            
            if error:
                st.error(error)
                if "model" in error.lower():
                    st.info("Jalankan model Ollama: `ollama pull gemma3:1b`")
            else:
                st.markdown(response)
                response_timestamp = datetime.now().strftime("%H:%M:%S")
                st.caption(response_timestamp)
                
                # Tambahkan response model ke history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": response_timestamp
                })

# Sidebar
with st.sidebar:
    # Mengecek status koneksi ollama
    st.markdown("### Status Ollama:")
    is_conn, msg = check_ollama_connection()
    if is_conn:
        st.success("Connected")
    else:
        st.error(f"{msg}")
        st.info("""
        **Troubleshooting:**
        1. Pastikan Ollama sudah terinstall
        2. Cek dengan command: `ollama list`
        4. Jalankan kembali aplikasi
        """)
        st.stop()
    
    st.markdown("---")
    
    # Button untuk clear chat history
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    