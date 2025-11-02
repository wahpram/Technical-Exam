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
    try:
        ollama.list()
        return True, "Ollama service running"
    except Exception as e:
        return False, f"Ollama service error: {str(e)}"


# Function untuk mendapatkan response dari model
def get_ollama_response(prompt, model="gemma3:1b", temperature=0.7, max_tokens=500):
    try:
        # Options dari model Ollama
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": temperature,
                "num_predict": max_tokens,
            }
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
    # Ambil settings dari sidebar
    temperature = st.session_state.get('temperature', 0.7)
    max_tokens = st.session_state.get('max_tokens', 500)
    selected_model = st.session_state.get('selected_model', 'gemma3:1b')
    
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
                model=selected_model,
                temperature=temperature,
                max_tokens=max_tokens
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

# Sidebar dan konfigurasi model
with st.sidebar:
    # Model Settings
    st.header("Model Settings")
    
    # Temperature slider
    st.session_state.temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Controls randomness. Lower = more focused, Higher = more creative"
    )
    
    # Max tokens
    st.session_state.max_tokens = st.number_input(
        "Max Tokens",
        min_value=100,
        max_value=2000,
        value=500,
        step=100,
        help="Maximum length of response"
    )
    
    
    st.markdown("---")
    
    # Button untuk clear chat history
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    
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