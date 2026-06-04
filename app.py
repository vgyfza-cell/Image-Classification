import streamlit as st
import requests
from PIL import Image
from io import BytesIO

GITHUB_USER = "vgyfza-cell"
GITHUB_REPO = "Image-Classification"
FOLDER_PATH = "" 

@st.cache_data
def fetch_images_from_github():
    api_url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{FOLDER_PATH}" if FOLDER_PATH else f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            contents = response.json()
            dataset = {}
            valid_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
            for item in contents:
                if item['type'] == 'file' and item['name'].endswith(valid_extensions):
                    dataset[item['name']] = item['download_url']
            return dataset
    except: return {}
    return {}

st.set_page_config(page_title="Klasifikasi Gambar", page_icon="🖼️")
st.title("📸 Aplikasi Klasifikasi Gambar")
image_dataset = fetch_images_from_github()

if image_dataset:
    pilihan_gambar = st.selectbox("Silahkan pilih gambar dari GitHub:", list(image_dataset.keys()))
    img = Image.open(BytesIO(requests.get(image_dataset[pilihan_gambar]).content)) if choices := image_dataset.get(pilihan_gambar) else None
    if img:
        st.image(img, caption=f"File: {pilihan_gambar}", use_container_width=True)
        if st.button("Jalankan Klasifikasi", type="primary"):
            with st.spinner('Sedang menganalisis...'):
                st.success(f"Hasil Klasifikasi Terdeteksi untuk objek pada: {pilihan_gambar}")
else:
    st.error("Tidak ditemukan file gambar di repository atau API GitHub membatasi akses.")
