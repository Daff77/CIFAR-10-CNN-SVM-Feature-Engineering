# 🚀 Tugas 7: Peningkatan Akurasi CNN + SVM pada CIFAR-10 (Struktur 8 Notebook)

Proyek ini mengimplementasikan eksperimen komprehensif **Custom CNN (Convolutional Neural Network) sebagai Feature Extractor** dan **SVM (Support Vector Machine) dengan Kernel RBF sebagai Classifier** pada dataset **CIFAR-10** (10 kelas citra berdimensi 32x32 piksel), dengan arsitektur pipeline modular 8 notebook:
- **Alur 1 (RGB)**: `1_RGB_train.ipynb` & `2_RGB_test.ipynb`
- **Alur 2 (Grayscale AVG)**: `3_GrayAvg_train.ipynb` & `4_GrayAvg_test.ipynb`
- **Alur 3 (Grayscale NTSC)**: `5_GrayNTSC_train.ipynb` & `6_GrayNTSC_test.ipynb`
- **Alur 4 (Feature Engineering Multidomain Fusion)**: `7_Fusion_train.ipynb` & `8_Fusion_test.ipynb`

---

## 📁 Struktur Explorer VS Code (Tepat 8 Notebook)

```text
Pt 7/
│
├── cifar10_artifacts/                      # Direktori model .keras, fitur .npz, dan metrik JSON
│   ├── rgb/
│   ├── grayscale_avg/
│   ├── grayscale_ntsc/
│   └── rgb_avg_ntsc/
│
├── 1_RGB_train.ipynb                       # [RGB] 1. Training Custom CNN, Ekstraksi Fitur 512-D & Training SVM
├── 2_RGB_test.ipynb                        # [RGB] 2. Testing Custom CNN, Testing SVM & Perbandingan Komparatif
│
├── 3_GrayAvg_train.ipynb                   # [AVG] 3. Training Custom CNN, Ekstraksi Fitur 512-D & Training SVM
├── 4_GrayAvg_test.ipynb                    # [AVG] 4. Testing Custom CNN, Testing SVM & Perbandingan Komparatif
│
├── 5_GrayNTSC_train.ipynb                  # [NTSC] 5. Training Custom CNN, Ekstraksi Fitur 512-D & Training SVM
├── 6_GrayNTSC_test.ipynb                   # [NTSC] 6. Testing Custom CNN, Testing SVM & Perbandingan Komparatif
│
├── 7_Fusion_train.ipynb                    # [Fusion] 7. Ekstraksi Fitur Fusi 1.536-D & Training SVM Classifier
├── 8_Fusion_test.ipynb                     # [Fusion] 8. Testing SVM Fitur Fusi & Master Accuracy Comparison
│
├── README.md                               # Dokumentasi Teknis Lengkap Proyek (8 Notebook Pipeline)
└── README_URUTAN_EKSEKUSI.md               # Panduan Urutan Eksekusi Singkat
```

---

## 🔬 Rincian Alur Kerja Per Tahap (Pipeline Architecture)

### 1. RGB Pipeline (2 Notebook)
- **`1_RGB_train.ipynb`**:
  - Memuat CIFAR-10 RGB asli `(32, 32, 3)` dan partisi 3-way stratified deterministik (Seed: `23092026`).
  - Melatih model Custom Deep Residual CNN (4-blok residual dengan BatchNormalization, Spatial Dropout, dan Data Augmentation).
  - Mengekstrak representasi vektor fitur tingkat tinggi berdimensi 512 dari layer `svm_features` (GlobalAveragePooling2D) untuk data train (50.000 sampel) dan test (10.000 sampel).
  - Menstandarisasi fitur training (`StandardScaler`, anti data leakage) dan melatih classifier SVM RBF.
  - Menyimpan model CNN, scaler, dan model SVM ke file `.keras` dan `.pkl`.
- **`2_RGB_test.ipynb`**:
  - Evaluasi model CNN pada 10.000 data test (Loss, Akurasi, Classification Report, Confusion Matrix).
  - Evaluasi model SVM pada 10.000 vektor fitur testing (Classification Report, Confusion Matrix).
  - Evaluasi komparatif langsung CNN vs SVM pada domain RGB.

---

### 2. Grayscale Average Pipeline (2 Notebook)
- **`3_GrayAvg_train.ipynb`**:
  - Konversi citra ke Grayscale Average: $Gray_{\text{AVG}} = \frac{R + G + B}{3}$ `(32, 32, 1)`.
  - Pelatihan Custom CNN Grayscale 1 kanal.
  - Ekstraksi vektor fitur 512-D dari layer `svm_features`.
  - Pelatihan SVM Classifier pada fitur Grayscale Average dan penyimpanan model.
- **`4_GrayAvg_test.ipynb`**:
  - Pengujian performa CNN Grayscale Average pada 10.000 sampel testing.
  - Pengujian performa SVM Grayscale Average pada 10.000 sampel testing.
  - Analisis perbandingan performa CNN vs SVM Grayscale Average.

---

### 3. Grayscale NTSC Pipeline (2 Notebook)
- **`5_GrayNTSC_train.ipynb`**:
  - Konversi citra ke Grayscale NTSC (Perceptual Luminance): $Y_{\text{NTSC}} = 0.2989 R + 0.5870 G + 0.1140 B$ `(32, 32, 1)`.
  - Pelatihan Custom CNN Grayscale NTSC.
  - Ekstraksi vektor fitur 512-D dari layer `svm_features`.
  - Pelatihan SVM Classifier pada fitur Grayscale NTSC dan penyimpanan model.
- **`6_GrayNTSC_test.ipynb`**:
  - Pengujian performa CNN Grayscale NTSC pada 10.000 sampel testing.
  - Pengujian performa SVM Grayscale NTSC pada 10.000 sampel testing.
  - Analisis perbandingan performa CNN vs SVM Grayscale NTSC.

---

### 4. Feature Engineering: Multi-Domain Fusion Pipeline (2 Notebook)
- **`7_Fusion_train.ipynb`**:
  - **Feature Fusion**: Menggabungkan representasi fitur tingkat tinggi dari 3 model Custom CNN:
    - RGB: 512 dimensi (informasi warna kromatik)
    - Grayscale AVG: 512 dimensi (informasi intensitas seragam)
    - Grayscale NTSC: 512 dimensi (informasi luminansi perseptual)
    - **Total: 1.536 Dimensi** ($512 + 512 + 512$).
  - Preprocessing multi-domain (`FusedDomainPreprocessor`): penskalaan per-domain, pembobotan representasi, dan normalisasi L2.
  - Pelatihan SVM Classifier pada ruang fitur gabungan 1.536 dimensi.
- **`8_Fusion_test.ipynb`**:
  - Memuat Preprocessor Scaler dan Model Final SVM Fitur Gabungan.
  - Inferensi SVM murni pada 10.000 data testing.
  - Menghasilkan Confusion Matrix, Classification Report komprehensif.
  - Menampilkan **Diagram Perbandingan Master Akurasi Semua Alur** (Alur 1 s/d Alur 4) dengan garis batas Target 95%.

---

## 🛡️ Prinsip Metodologi & Kebijakan Anti-Data Leakage
1. Model CNN adalah **Custom CNN murni** (tanpa backbone pretrained transfer learning seperti ResNet/EfficientNet).
2. Data testing 10.000 sampel murni diisolasi hanya untuk tahap evaluasi akhir.
3. Transformasi penskalaan hanya memelajari parameter statistik dari data training (`.fit()` hanya pada training set, data testing hanya menggunakan `.transform()`).
4. Deterministik & Reproducible: Seluruh pembagian partisi dan seed pelatihan menggunakan `23092026`.
