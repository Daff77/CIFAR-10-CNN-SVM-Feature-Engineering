# Tugas 7 - CIFAR-10: CNN + SVM (Struktur 8 Notebook)

Seed: `23092026` | Dataset: CIFAR-10 (10 kelas, 32x32 piksel).
Arsitektur: Custom Deep Residual CNN (4-Blok dengan Global Average Pooling) + SVM RBF Classifier.
Seluruh model dan artefak tersimpan di dalam folder `cifar10_artifacts/`.

---

## 📋 Urutan Eksekusi Notebook (1 s/d 8)

| No | File Notebook | Representasi / Alur | Deskripsi Tahapan |
|:--:|:---|:---|:---|
| **1** | `1_RGB_train.ipynb` | RGB Pipeline | Training Custom CNN, Ekstraksi Fitur 512-D (`svm_features`), dan Training SVM |
| **2** | `2_RGB_test.ipynb` | RGB Pipeline | Testing CNN (10k test set), Testing SVM, dan Evaluasi Komparatif CNN vs SVM |
| **3** | `3_GrayAvg_train.ipynb` | Grayscale AVG Pipeline | Konversi $Gray = (R+G+B)/3$, Training CNN, Ekstraksi Fitur, dan Training SVM |
| **4** | `4_GrayAvg_test.ipynb` | Grayscale AVG Pipeline | Testing CNN Grayscale AVG, Testing SVM, dan Evaluasi Komparatif |
| **5** | `5_GrayNTSC_train.ipynb` | Grayscale NTSC Pipeline | Konversi $Y = 0.2989R+0.5870G+0.1140B$, Training CNN, Ekstraksi Fitur, dan Training SVM |
| **6** | `6_GrayNTSC_test.ipynb` | Grayscale NTSC Pipeline | Testing CNN Grayscale NTSC, Testing SVM, dan Evaluasi Komparatif |
| **7** | `7_Fusion_train.ipynb` | Feature Engineering | Ekstraksi & Fusi Fitur Multidomain 1.536-D ($512\times 3$) dan Training SVM Final |
| **8** | `8_Fusion_test.ipynb` | Feature Engineering | Testing SVM Fitur Gabungan & Visualisasi Diagram Master Akurasi Semua Alur |

---

## ⚙️ Petunjuk Eksekusi
1. Jalankan semua notebook secara berurutan dari `1` sampai `8`.
2. Notebook `7_Fusion_train.ipynb` membutuhkan fitur dari notebook `1`, `3`, dan `5`.
3. Notebook `8_Fusion_test.ipynb` membutuhkan fitur testing dari notebook `2`, `4`, `6`, serta model dari notebook `7`.
4. Jika ingin melakukan pengujian langsung tanpa re-training, notebook testing (`2`, `4`, `6`, `8`) dapat langsung dijalankan karena artefak model dan fitur telah tersedia di `cifar10_artifacts/`.
