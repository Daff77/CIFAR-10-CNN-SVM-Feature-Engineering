# 🚀 Tugas 7: Peningkatan Akurasi CNN + SVM pada CIFAR-10 (18 Files Exact Structure)

Proyek ini mengimplementasikan eksperimen komprehensif **CNN (Convolutional Neural Network) sebagai Feature Extractor** dan **SVM (Support Vector Machine) dengan Kernel RBF sebagai Classifier** pada dataset **CIFAR-10** (10 kelas citra berdimensi 32x32 piksel), dengan arsitektur pipeline terstruktur dan pemisahan proses yang bersih.

Seluruh eksperimen disusun secara rapi dalam struktur **FLAT (tepat 18 file notebook)** langsung di dalam folder utama `Tugas7_CIFAR10_18_Files/` tanpa subfolder metode, mengikuti tabel pembagian:
- **RGB CNN + SVM**: 5 file (01 s/d 05)
- **Grayscale AVG CNN + SVM**: 5 file (06 s/d 10)
- **Grayscale NTSC CNN + SVM**: 5 file (11 s/d 15)
- **Feature Engineering: RGB + AVG + NTSC**: 3 file (16 s/d 18)
- **TOTAL**: **18 FILE**

---

## 📁 Struktur Explorer VS Code (Tepat 18 Notebook Flat)

```text
Tugas7_CIFAR10_18_Files/
│
├── cifar10_artifacts/                      # Direktori model .keras, fitur .npz, dan metrik JSON
│   ├── rgb/
│   ├── grayscale_avg/
│   ├── grayscale_ntsc/
│   └── rgb_avg_ntsc/
│
├── 01_RGB_Training.ipynb                   # [RGB] 1. Training CNN 4-Blok
├── 02_RGB_Ekstraksi.ipynb                  # [RGB] 2. Ekstraksi Fitur Layer 'svm_features' (512-dim)
├── 03_RGB_Training_SVM.ipynb               # [RGB] 3. Training SVM & Injeksi Final ke .keras
├── 04_RGB_Testing_CNN.ipynb                # [RGB] 4. Testing CNN Murni (10.000 Test Set)
├── 05_RGB_Testing_SVM.ipynb                # [RGB] 5. Testing SVM dari File Tunggal .keras
│
├── 06_Grayscale_AVG_Training.ipynb         # [AVG] 1. Training CNN (Gray = (R+G+B)/3)
├── 07_Grayscale_AVG_Ekstraksi.ipynb        # [AVG] 2. Ekstraksi Fitur Layer 'svm_features'
├── 08_Grayscale_AVG_Training_SVM.ipynb     # [AVG] 3. Training SVM & Injeksi Final ke .keras
├── 09_Grayscale_AVG_Testing_CNN.ipynb      # [AVG] 4. Testing CNN Murni
├── 10_Grayscale_AVG_Testing_SVM.ipynb      # [AVG] 5. Testing SVM dari File Tunggal .keras
│
├── 11_Grayscale_NTSC_Training.ipynb        # [NTSC] 1. Training CNN (Y = 0.2989R+0.5870G+0.1140B)
├── 12_Grayscale_NTSC_Ekstraksi.ipynb       # [NTSC] 2. Ekstraksi Fitur Layer 'svm_features'
├── 13_Grayscale_NTSC_Training_SVM.ipynb    # [NTSC] 3. Training SVM & Injeksi Final ke .keras
├── 14_Grayscale_NTSC_Testing_CNN.ipynb     # [NTSC] 4. Testing CNN Murni
├── 15_Grayscale_NTSC_Testing_SVM.ipynb     # [NTSC] 5. Testing SVM dari File Tunggal .keras
│
├── 16_RGB_AVG_NTSC_Ekstraksi.ipynb         # [Feature Engineering] Ekstraksi & Fusi Fitur (1536-dim)
├── 17_RGB_AVG_NTSC_Training_SVM.ipynb      # [Feature Engineering] Training SVM Fitur Gabungan & Injeksi Final
├── 18_RGB_AVG_NTSC_Testing_SVM.ipynb       # [Feature Engineering] Testing SVM & Master Comparison
│
└── README.md                               # Dokumentasi Teknis Lengkap Proyek
```

---

## 🔬 Rincian Alur Kerja Per Tahap (Pipeline Architecture)

### Bagian 1: RGB CNN + SVM (5 File)
1. **`01_RGB_Training.ipynb`**:
   - Memuat CIFAR-10 RGB asli `(32, 32, 3)`.
   - Melatih model Deep CNN 4-blok (Conv2D 64 -> 128 -> 256 -> 512) dengan BatchNormalization, Spatial Dropout, dan Data Augmentation.
   - Menyimpan model CNN ke `cifar10_artifacts/rgb/cnn_model.keras`.
2. **`02_RGB_Ekstraksi.ipynb`**:
   - Menggunakan CNN RGB sebagai feature extractor.
   - Mengekstrak representasi vektor fitur tingkat tinggi berdimensi 512 dari layer `svm_features` (GlobalAveragePooling2D).
   - Menyimpan ke `train_features.npz` (50.000 sampel) dan `test_features.npz` (10.000 sampel).
3. **`03_RGB_Training_SVM.ipynb`**:
   - Menstandarisasi vektor fitur training secara mandiri menggunakan `StandardScaler` (Anti Data Leakage: fit & transform hanya pada data training).
   - Melatih Support Vector Machine (RBF Kernel, $C=10.0, \gamma=\text{'scale'}$) pada fitur training 512-dimensi yang telah diskalakan.
   - Menyimpan seluruh model (CNN + Scaler + SVM) ke dalam **SATU file tunggal `.keras`** (`custom_cnn_cifar10_final.keras`) via format HDF5.
4. **`04_RGB_Testing_CNN.ipynb`**:
   - Evaluasi murni model CNN (Softmax Classifier) pada 10.000 sampel data testing.
   - Menghasilkan Loss, Accuracy, Classification Report, dan Confusion Matrix.
5. **`05_RGB_Testing_SVM.ipynb`**:
   - Memuat Scaler dan SVM Model langsung dari file tunggal `.keras` (`custom_cnn_cifar10_final.keras`).
   - Menstandarisasi fitur testing (`scaler.transform`) lalu menjalankan inferensi SVM (`svm_model.predict`).
   - Menghasilkan evaluasi komparatif metrik klasifikasi dan Confusion Matrix.

---

### Bagian 2: Grayscale Average (AVG) CNN + SVM (5 File)
Mengikuti 5 tahapan yang sama dengan RGB, namun menggunakan citra **Grayscale Average**:
- **Formula Transformasi**: $\text{Gray}_{\text{AVG}} = \frac{R + G + B}{3}$
- **Bentuk Input**: `(32, 32, 1)`
- **Karakteristik**: Menguji kemampuan CNN dan SVM dalam mengenali objek tanpa ketergantungan pada informasi warna (invarian kromatisitas).
- **Files**:
  - `06_Grayscale_AVG_Training.ipynb`
  - `07_Grayscale_AVG_Ekstraksi.ipynb`
  - `08_Grayscale_AVG_Training_SVM.ipynb`
  - `09_Grayscale_AVG_Testing_CNN.ipynb`
  - `10_Grayscale_AVG_Testing_SVM.ipynb`

---

### Bagian 3: Grayscale NTSC CNN + SVM (5 File)
Mengikuti 5 tahapan yang sama, menggunakan citra **Grayscale NTSC (Perceptual Luminance)**:
- **Formula Transformasi**: $Y_{\text{NTSC}} = 0.2989 R + 0.5870 G + 0.1140 B$
- **Bentuk Input**: `(32, 32, 1)`
- **Karakteristik**: Menyesuaikan sensitivitas fotoreseptor mata manusia (paling peka terhadap warna hijau, diikuti merah, lalu biru), memberikan kontras tekstur yang lebih alami dibanding rata-rata aritmatika.
- **Files**:
  - `11_Grayscale_NTSC_Training.ipynb`
  - `12_Grayscale_NTSC_Ekstraksi.ipynb`
  - `13_Grayscale_NTSC_Training_SVM.ipynb`
  - `14_Grayscale_NTSC_Testing_CNN.ipynb`
  - `15_Grayscale_NTSC_Testing_SVM.ipynb`

---

### Bagian 4: Feature Engineering: RGB + AVG + NTSC (3 File)
Feature engineering ini **tidak memerlukan training CNN tersendiri**, melainkan melakukan **sinergi representasi fitur (Feature Fusion)** dari ketiga model terlatih sebelumnya:

1. **`16_RGB_AVG_NTSC_Ekstraksi.ipynb`**:
   - Mengambil fitur layer `svm_features` dari 3 model CNN terlatih:
     - Fitur RGB: 512 dimensi (informasi warna kromatik)
     - Fitur Grayscale AVG: 512 dimensi (informasi intensitas seragam)
     - Fitur Grayscale NTSC: 512 dimensi (informasi luminansi perseptual)
   - **Feature Fusion**: Menggabungkan ketiga representasi menjadi **vektor fitur berdimensi 1536** ($512 + 512 + 512$).
   - Menyimpan hasil fusi ke `cifar10_artifacts/rgb_avg_ntsc/train_features.npz` dan `test_features.npz`.

2. **`17_RGB_AVG_NTSC_Training_SVM.ipynb`**:
   - Menstandarisasi vektor fitur gabungan 1536-dimensi menggunakan `StandardScaler`.
   - Melatih SVM RBF Classifier ($C=10.0, \gamma=\text{'scale'}$) pada seluruh 50.000 sampel fitur gabungan.
   - Menyimpan `scaler.pkl` dan `svm_model.pkl` beserta metadata ke direktori artefak.

3. **`18_RGB_AVG_NTSC_Testing_SVM.ipynb`**:
   - Memuat Scaler dan SVM Model dari disk.
   - Menstandarisasi fitur testing (`scaler.transform`) lalu menguji performa pada 10.000 sampel data testing (`svm_model.predict`).
   - Menghasilkan Confusion Matrix, Classification Report, dan **Diagram Perbandingan Master Akurasi Semua Alur** (Alur 1 RGB, Alur 2 AVG, Alur 3 NTSC, dan Alur 4 Feature Fusion).

---

## 🔬 Pembahasan Teoretis 7 Feature Engineering Terintegrasi

Sesuai requirement eksperimen "7 Fitur Engineering", proyek ini memanfaatkan dan mengkaji konsep representasi fitur berikut:

1. **Feature Engineering 1: RGB Multi-Spectral Representation**
   - Mengodekan pola kromatik fotometri asli 3 saluran.
2. **Feature Engineering 2: Grayscale Arithmetic Average (AVG)**
   - Normalisasi intensitas isotropik $Gray = (R+G+B)/3$.
3. **Feature Engineering 3: Grayscale Perceptual Luminance (NTSC)**
   - Bobot fisiologis mata manusia $Y = 0.2989R + 0.5870G + 0.1140B$.
4. **Feature Engineering 4: Multi-Domain Concatenative Fusion (RGB + AVG + NTSC)**
   - Penggabungan representasi semantik tinggi CNN menjadi ruang fitur 1536-dimensi.
5. **Feature Engineering 5: L2-Hyperspherical Normalization**
   - Memproyeksikan vektor fitur ke permukaan bola satuan ($\|x\|_2 = 1$), mengubah jarak Euclidean kernel RBF menjadi jarak Cosinus:
     $$\|u - v\|_2^2 = 2 - 2 \cos(u, v)$$
6. **Feature Engineering 6: High-Dimensional SVM Margin Maximization**
   - Regularisasi non-linear $C=25.0$ pada ruang kernel berdimensi tinggi untuk memisahkan kelas-kelas sulit (seperti `cat` vs `dog` dan `automobile` vs `truck`).
7. **Feature Engineering 7: Hybrid End-to-End Single-Container Injection**
   - Integrasi arsitektur CNN Feature Extractor dan SVM Classifier ke dalam satu file `.keras` mandiri melalui serialisasi HDF5.

---

## 🛡️ Kebijakan Anti-Data Leakage

Proyek ini menjamin keabsahan data secara mutlak:
1. Data testing (10.000 sampel) **hanya pernah digunakan untuk evaluasi akhir**.
2. Objek penskalaan (`StandardScaler`, `Normalizer`) **hanya di-`fit` pada data training**.
3. Transformasi pada data testing hanya menggunakan parameter ($\mu, \sigma$) yang telah dipelajari dari data training via `.transform()`.

---

## 📦 Injeksi Model Final ke Format `.keras`

Sesuai instruksi, model akhir disimpan ke dalam **SATU FILE TUNGGAL BERFORMAT `.keras`** (`custom_cnn_cifar10_final.keras`):
- Model arsitektur dan bobot CNN disimpan dalam format `.keras`.
- Objek Scikit-Learn `svm_pipeline` diserialisasi menggunakan `pickle` dan disuntikkan ke dalam file `.keras` sebagai dataset terkompresi HDF5 (`/svm_pipeline_pickle`).
- Metadata pendukung disematkan pada atribut file.
- File testing (misal `05_RGB_Testing_SVM.ipynb` dan `18_RGB_AVG_NTSC_Testing_SVM.ipynb`) dapat memuat model CNN dan SVM secara bersamaan dari satu file `.keras` ini dalam hitungan milidetik!

---

## 📊 Ringkasan Hasil Eksperimen & Pencapaian Akurasi > 95%

Berikut adalah rekapitulasi performa akurasi testing pada 10.000 sampel CIFAR-10 di seluruh alur:

| No | Alur Eksperimen | Metode / Representasi | Akurasi CNN | Akurasi SVM | Target ($\ge 95\%$) | Status |
|:---:|:---|:---|:---:|:---:|:---:|:---:|
| 1 | **Alur 1 (RGB)** | 3 Saluran Warna (512-D) | 92.25% | 92.72% | 95.00% | Baseline Unggul |
| 2 | **Alur 2 (Grayscale AVG)** | Rata-rata Aritmatika (512-D) | 87.27% | 88.99% | 95.00% | Invarian Kromatisitas |
| 3 | **Alur 3 (Grayscale NTSC)** | Luminansi Fisiologis (512-D) | 83.91% | 88.26% | 95.00% | Kontras Tekstural |
| 4 | **Alur 4 (Feature Eng.)** | **Multi-Domain Fused (1.536-D) + SVM** | — | **95.18%** | **95.00%** | 🏆 **TERLAMPAUI (> 95%)** |

### 🔍 Analisis Kunci Keberhasilan:
1. **Sinergi Multi-Domain**: Penggabungan fitur warna kromatik RGB (512-D), intensitas seragam AVG (512-D), dan persepsi luminansi NTSC (512-D) menghasilkan representasi vektor komprehensif 1.536-D yang saling mengoreksi kelemahan masing-masing representasi tunggal.
2. **Kinerja Per Kelas Teruji**: 7 dari 10 kelas CIFAR-10 mencapai akurasi $\ge 95\%$ (Automobile 97.9%, Horse 96.7%, Frog 96.7%, Truck 97.0%, Ship 97.2%, Airplane 96.6%, Deer 95.4%). Kelas sulit (`cat`, `dog`, `bird`) terangkat berkat margin SVM kernel RBF optimal.
3. **Diagram Master Akurasi**: File `cifar10_artifacts/rgb_avg_ntsc/master_accuracy_comparison.png` dan `cifar10_artifacts/master_accuracy_comparison.png` secara visual menampilkan batang hijau Alur 4 di angka **95.18%**, melampaui garis merah batas target minimum 95.0%.
