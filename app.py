import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Konfigurasi repositori GitHub kamu
GITHUB_USER = "vgyfza-cell"
GITHUB_REPO = "Image-Classification"
FOLDER_PATH = "" 

@st.cache_data
def fetch_images_from_github():
    # Menentukan URL API GitHub berdasarkan folder
    if FOLDER_PATH:
        api_url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{FOLDER_PATH}"
    else:
        api_url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents"
        
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            contents = response.json()
            dataset = {}
            # Format gambar yang diizinkan
            valid_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
            for item in contents:
                if item['type'] == 'file' and item['name'].endswith(valid_extensions):
                    dataset[item['name']] = item['download_url']
            return dataset
    except:
        return {}
    return {}

def load_image_from_url(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return Image.open(BytesIO(res.content))
    except:
        return None
    return None

# --- Tampilan Aplikasi Streamlit ---
st.set_page_config(page_title="Klasifikasi Gambar", page_icon="🖼️")
st.title("📸 Aplikasi Klasifikasi Gambar")
st.write("Memuat data gambar langsung dari repositori GitHub...")

# Ambil list dataset gambar dari GitHub
image_dataset = fetch_images_from_github()

if image_dataset:
    # Dropdown pilihan file gambar
    pilihan_gambar = st.selectbox("Silahkan pilih gambar dari GitHub:", list(image_dataset.keys()))
    
    # Ambil URL mentah gambar yang dipilih
    url_gambar = image_dataset.get(pilihan_gambar)
    
    if url_gambar:
        # Load gambar menggunakan fungsi yang aman
        img = load_image_from_url(url_gambar)
        
        if img is not None:
            # Tampilkan gambar di web Streamlit
            st.image(img, caption=f"File: {pilihan_gambar}", use_container_width=True)
            
            # Tombol untuk melakukan klasifikasi
            if st.button("Jalankan Klasifikasi", type="primary"):
                with st.spinner('Sedang menganalisis gambar...'):
                    # Output sementara sebelum kamu memasukkan model AI aslimu
                    st.success(f"Hasil Klasifikasi Terdeteksi untuk objek pada file: {pilihan_gambar}")
        else:
            st.error("Gagal mengubah data biner menjadi gambar PIL.")
    else:
        st.error("URL gambar tidak ditemukan.")
else:
    st.error("Tidak ditemukan file gambar (.jpg/.png) di repository atau akses API GitHub dibatasi.")
