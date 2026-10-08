"""
Script audit dan pemeriksaan statis kualitas 8 file laporan Word (.docx).
"""

import os
import docx

REPORTS = [
    "1_RGB_train.docx",
    "2_RGB_test.docx",
    "3_GrayAvg_train.docx",
    "4_GrayAvg_test.docx",
    "5_GrayNTSC_train.docx",
    "6_GrayNTSC_test.docx",
    "7_Fusion_train.docx",
    "8_Fusion_test.docx"
]

def audit():
    print("================================================================================")
    print("                     AUDIT STATIS 8 LAPORAN WORD CIFAR-10                       ")
    print("================================================================================")
    
    all_passed = True
    summary_results = []
    
    for r_name in REPORTS:
        paths_to_check = [os.path.join("Laporan_CIFAR10", r_name), r_name]
        for p in paths_to_check:
            if not os.path.exists(p):
                print(f"[GAGAL] File tidak ditemukan: {p}")
                all_passed = False
                continue
                
        doc = docx.Document(os.path.join("Laporan_CIFAR10", r_name))
        
        # Check text content
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        for tbl in doc.tables:
            for row in tbl.rows:
                for cell in row.cells:
                    full_text.append(cell.text)
        all_text = " ".join(full_text)
        
        # Check placeholders
        has_placeholder = False
        for bad_word in ["[ISI DI SINI]", "TODO", "[TODO]", "[PLACEHOLDER]", "TBD", "[TBD]"]:
            if bad_word in all_text:
                print(f"[GAGAL] Terdeteksi placeholder '{bad_word}' di {r_name}")
                has_placeholder = True
                all_passed = False
                
        # Check student identity
        has_student = ("Daffa Danendra Fairuzza" in all_text) and ("09020624026" in all_text)
        if not has_student:
            print(f"[GAGAL] Identitas mahasiswa tidak ditemukan di {r_name}")
            all_passed = False
            
        # Check lecturer
        has_lecturer = ("Bayu Adi Nugroho, Ph.D" in all_text)
        if not has_lecturer:
            print(f"[GAGAL] Nama dosen tidak ditemukan di {r_name}")
            all_passed = False
            
        # Check UIN logo / images
        num_imgs = len(doc.inline_shapes)
        num_tables = len(doc.tables)
        num_paras = len(doc.paragraphs)
        file_size = os.path.getsize(os.path.join("Laporan_CIFAR10", r_name))
        
        # Check captions
        captions = [p.text for p in doc.paragraphs if p.text.startswith("Gambar ")]
        for cap in captions:
            if not any(cap.startswith(f"Gambar {i}.") for i in range(1, 10)):
                print(f"[PERINGATAN] Format caption tidak sesuai: {cap}")
                
        # Check headings
        headings = [p.text for p in doc.paragraphs if p.text.strip() and p.text[0].isdigit() and "." in p.text[:3]]
        
        summary_results.append({
            "name": r_name,
            "paragraphs": num_paras,
            "tables": num_tables,
            "images": num_imgs,
            "captions": len(captions),
            "headings": len(headings),
            "size_kb": file_size // 1024,
            "has_student": has_student,
            "has_lecturer": has_lecturer,
            "clean_text": not has_placeholder
        })
        
    print("\nRingkasan Metrik Tiap Laporan:")
    print(f"{'Nama File':<22} | {'Paragraf':<8} | {'Tabel':<6} | {'Gambar':<6} | {'Heading':<8} | {'Ukuran (KB)':<11} | {'Status'}")
    print("-" * 80)
    for s in summary_results:
        status_str = "LULUS AUDIT" if (s['has_student'] and s['has_lecturer'] and s['clean_text']) else "GAGAL"
        print(f"{s['name']:<22} | {s['paragraphs']:<8} | {s['tables']:<6} | {s['images']:<6} | {s['headings']:<8} | {s['size_kb']:<11} | {status_str}")
        
    print("\nStatus Akhir Audit:", "SEMUA 8 DOKUMEN LULUS PEMERIKSAAN STATIS 100%" if all_passed else "ADA KESALAHAN")

if __name__ == "__main__":
    audit()
