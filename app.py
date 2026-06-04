import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Klasifikasi Ikan vs Kucing", page_icon="🐾")

st.title("🐟 Klasifikasi Gambar: Ikan atau Kucing? 🐈")
st.write("Upload model .h5 kamu dan gambar yang ingin ditebak!")

# --- BAGIAN 1: UPLOAD MODEL ---
st.sidebar.header("Pengaturan Model")
uploaded_model = st.sidebar.file_uploader("1. Upload Model (.h5)", type=["h5"])

# --- BAGIAN 2: UPLOAD GAMBAR ---
uploaded_image = st.file_uploader("2. Upload Gambar (Ikan/Kucing)", type=["jpg", "png", "jpeg"])

# Fungsi untuk memproses gambar agar sesuai dengan input model
def import_and_predict(image_data, model):
    # Sesuaikan ukuran target_size dengan saat kamu melatih model (misal 150x150 atau 224x224)
    size = (150, 150) 
    image = ImageOps.fit(image_data, size, Image.Resampling.LANCZOS)
    image = np.asarray(image)
    
    # Normalisasi (jika saat latihan model kamu membagi 255)
    img_reshape = image.astype('float32') / 255.0
    img_reshape = np.expand_dims(img_reshape, axis=0) # Ubah ke bentuk (1, 150, 150, 3)
    
    prediction = model.predict(img_reshape)
    return prediction

if uploaded_model is not None:
    # Simpan model sementara ke lokal agar bisa dibaca Keras
    with open("temp_model.h5", "wb") as f:
        f.write(uploaded_model.getbuffer())
    
    # Load model
    with st.spinner('Memuat Model...'):
        model = tf.keras.models.load_model("temp_model.h5")
    st.sidebar.success("Model Berhasil Dimuat!")

    if uploaded_image is not None:
        # Tampilkan gambar yang diupload
        image = Image.open(uploaded_image)
        st.image(image, caption='Gambar yang diupload', use_container_width=True)
        
        # Tombol Prediksi
        if st.button("Tentukan Sekarang!", type="primary"):
            with st.spinner('Menganalisis...'):
                prediction = import_and_predict(image, model)
                
                # LOGIKA PENENTUAN KELAS
                # Asumsi: Model kamu menggunakan sigmoid (1 output) 
                # atau softmax (2 output). Ini logika umum:
                if len(prediction[0]) > 1: # Jika output 2 (Softmax)
                    hasil = np.argmax(prediction)
                else: # Jika output 1 (Sigmoid)
                    hasil = 1 if prediction[0][0] > 0.5 else 0
                
                # Mapping Label (Sesuaikan urutan saat kamu training)
                # Contoh: 0 = Ikan, 1 = Kucing
                class_names = ["Ikan", "Kucing"]
                
                st.write("---")
                st.subheader(f"Hasil Prediksi: **{class_names[hasil]}**")
                st.write(f"Tingkat Keyakinan: {np.max(prediction)*100:.2f}%")
else:
    st.info("Silahkan upload file model (.h5) kamu di sidebar sebelah kiri untuk memulai.")

# Footer
st.markdown("---")
st.caption("Pastikan ukuran input model kamu adalah 150x150. Jika berbeda, edit kodingan pada bagian target_size.")
