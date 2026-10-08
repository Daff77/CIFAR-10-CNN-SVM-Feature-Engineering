"""
Modul dasar generator laporan akademik Word (.docx)
Mengikuti standar format akademik Universitas Islam Negeri Sunan Ampel Surabaya.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# Palet warna akademik UIN Sunan Ampel (Emerald Dark Green & Slate Neutral)
COLOR_PRIMARY_HEX = "2E5339"      # Hijau Resmi UIN
COLOR_SECONDARY_HEX = "1C3D29"    # Hijau Gelap
COLOR_BG_ALT_HEX = "F4F7F5"       # Latar baris selang-seling lembut
COLOR_BORDER_HEX = "C5D0C8"       # Garis pembatas tabel halus
COLOR_CALLOUT_HEX = "EBF2EC"      # Kotak informasi penting

def set_cell_background(cell, hex_color):
    """Mengatur warna latar belakang sel tabel."""
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    """Mengatur padding internal sel tabel."""
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    cell._tc.get_or_add_tcPr().append(tcMar)

def set_table_borders(table, color=COLOR_BORDER_HEX, sz="4", val="single"):
    """Mengatur garis batas tabel agar rapi dan profesional."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def set_full_grid_borders(table, color="444444", sz="4", val="single"):
    """Mengatur garis batas penuh (grid lengkap) pada semua sisi dan kolom tabel."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def create_base_document():
    """Membuat dokumen Word dasar dengan ukuran kertas A4, margin standar, dan footer nomor halaman."""
    doc = docx.Document()
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)   # A4 Width
        section.page_height = Inches(11.69) # A4 Height
        
        # Tambahkan nomor halaman di footer
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ft = p_ft.add_run("Halaman ")
        r_ft.font.name = "Times New Roman"
        r_ft.font.size = Pt(9.5)
        r_ft.font.color.rgb = RGBColor(100, 100, 100)
        fld = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
        p_ft._p.append(fld)
    
    # Atur style Normal
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(11.5)
    font.color.rgb = RGBColor(30, 30, 30)
    
    return doc

def add_cover(doc, pertemuan_title, subjudul, notebook_name):
    """Menyusun halaman sampul (cover) sesuai standar akademik UIN Sunan Ampel."""
    # Judul Header
    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(4)
    run1 = p1.add_run(f"LAPORAN PERTEMUAN\n{pertemuan_title.upper()}")
    run1.bold = True
    run1.font.name = "Times New Roman"
    run1.font.size = Pt(14)
    run1.font.color.rgb = RGBColor(46, 83, 57)
    
    # Subjudul / Modul
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(4)
    p2.paragraph_format.space_after = Pt(14)
    run2 = p2.add_run(f"{subjudul}\n({notebook_name})")
    run2.font.name = "Times New Roman"
    run2.font.size = Pt(12)
    run2.bold = True
    
    # Mata Kuliah & Dosen Pengampu
    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_before = Pt(8)
    p3.paragraph_format.space_after = Pt(22)
    run3 = p3.add_run("Mata Kuliah: Big Data Analytic\nDosen Pengampu: Bayu Adi Nugroho, Ph.D")
    run3.font.name = "Times New Roman"
    run3.font.size = Pt(12)
    
    # Logo UIN Sunan Ampel
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(10)
    p_logo.paragraph_format.space_after = Pt(26)
    if os.path.exists("uin_logo.png"):
        p_logo.add_run().add_picture("uin_logo.png", width=Inches(2.2))
    
    # Identitas Mahasiswa
    p4 = doc.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p4.paragraph_format.space_before = Pt(14)
    p4.paragraph_format.space_after = Pt(4)
    run4 = p4.add_run("Disusun Oleh:")
    run4.font.name = "Times New Roman"
    run4.font.size = Pt(12)
    run4.bold = True
    
    p5 = doc.add_paragraph()
    p5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p5.paragraph_format.space_before = Pt(0)
    p5.paragraph_format.space_after = Pt(30)
    run5 = p5.add_run("Daffa Danendra Fairuzza – 09020624026")
    run5.font.name = "Times New Roman"
    run5.font.size = Pt(12)
    run5.bold = True
    
    # Institusi
    p6 = doc.add_paragraph()
    p6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p6.paragraph_format.space_before = Pt(18)
    p6.paragraph_format.space_after = Pt(0)
    run6 = p6.add_run(
        "PROGRAM STUDI SISTEM INFORMASI\n"
        "FAKULTAS SAINS DAN TEKNOLOGI\n"
        "UNIVERSITAS ISLAM NEGERI SUNAN AMPEL SURABAYA\n"
        "2026"
    )
    run6.font.name = "Times New Roman"
    run6.font.size = Pt(12)
    run6.bold = True
    
    doc.add_page_break()

def add_h1(doc, title):
    """Menambahkan Heading 1 dengan warna hijau UIN dan format bold."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(title)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.bold = True
    run.font.color.rgb = RGBColor(46, 83, 57)
    return p

def add_h2(doc, title):
    """Menambahkan Heading 2."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(title)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.bold = True
    run.font.color.rgb = RGBColor(30, 30, 30)
    return p

def add_h3(doc, title):
    """Menambahkan Heading 3."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(title)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.bold = True
    run.font.color.rgb = RGBColor(50, 50, 50)
    return p

def add_p(doc, text, bold_prefix="", italic=False):
    """Menambahkan paragraf dengan alignment justified dan line spacing 1.15."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(11.5)
        r_b.bold = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    r.italic = italic
    return p

def add_callout(doc, text, title="CATATAN PENTING"):
    """Menambahkan kotak callout informasi penting dengan border samping hijau."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.27)
    cell = table.cell(0, 0)
    set_cell_background(cell, COLOR_CALLOUT_HEX)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{COLOR_PRIMARY_HEX}"/>'
        f'<w:top w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    r_t = p.add_run(f"💡 {title}: ")
    r_t.bold = True
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(10.5)
    r_t.font.color.rgb = RGBColor(46, 83, 57)
    
    r_c = p.add_run(text)
    r_c.font.name = "Times New Roman"
    r_c.font.size = Pt(10.5)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def add_bullet(doc, text, bold_prefix=""):
    """Menambahkan poin daftar (bullet item)."""
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(11.5)
        r_b.bold = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    return p

def add_environment_table(doc, sumber_kode, dataset_desc, artefak_desc, is_test=False):
    """
    Menyusun Tabel Identitas Lingkungan Komputasi persis seperti pada referensi dan tangkapan layar pengguna:
    Item | Keterangan
    - Sumber Kode
    - Environment: Jupyter Notebook (lokal), kernel Python (CNNgpu), TensorFlow 2.10.1, GPU terdeteksi (GPU available: True)
    - CPU: Intel Core i7-13620H
    - GPU: Hybrid Graphics: NVIDIA GeForce RTX 2050 4GB (Discrete GPU) + Intel UHD Graphics (Integrated GPU)
    - RAM: 16 GB
    - Framework: TensorFlow / Keras, scikit-learn (GridSearchCV, SVC, Pipeline), h5py, Matplotlib
    - Dataset: [Spesifik dataset]
    - Reproducibility: RANDOM_STATE = 23092026
    - Artefak Output / Model yang Diuji: [Spesifik artefak]
    """
    table = doc.add_table(rows=10, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Border grid hitam penuh persis seperti pada contoh tabel Word pengguna
    set_full_grid_borders(table, color="000000", sz="4")
    
    col_widths = [Inches(1.8), Inches(4.47)]
    
    # Header Row: Bold, teks hitam, latar putih bersih
    headers = ["Item", "Keterangan"]
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "FFFFFF")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=130, right=130)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)
            r.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
            
    artefak_label = "Model yang Diuji" if is_test else "Artefak Output"
    
    rows_data = [
        ["Sumber Kode", sumber_kode],
        ["Environment", "Jupyter Notebook (lokal), kernel Python (CNNgpu), TensorFlow 2.10.1, GPU terdeteksi (GPU available: True)"],
        ["CPU", "Intel Core i7-13620H"],
        ["GPU", "Hybrid Graphics: NVIDIA GeForce RTX 2050 4GB (Discrete GPU) + Intel UHD Graphics (Integrated GPU)"],
        ["RAM", "16 GB"],
        ["Framework", "TensorFlow / Keras, scikit-learn (GridSearchCV, SVC, Pipeline), h5py, Matplotlib"],
        ["Dataset", dataset_desc],
        ["Reproducibility", "RANDOM_STATE = 23092026"],
        [artefak_label, artefak_desc]
    ]
    
    for r_idx, (item, ket) in enumerate(rows_data):
        row_cells = table.rows[r_idx + 1].cells
        row_cells[0].text = item
        row_cells[1].text = ket
        
        for c_idx in range(2):
            set_cell_background(row_cells[c_idx], "FFFFFF")
            set_cell_margins(row_cells[c_idx], top=85, bottom=85, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(10)
                r.bold = False
                r.font.color.rgb = RGBColor(0, 0, 0)
                    
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width
            
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)
    return table


def add_table_data(doc, headers, rows_data, col_widths=None):
    """Menyusun tabel data berformat rapi dengan header hijau UIN."""
    table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_full_grid_borders(table, color="555555", sz="4")
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = str(h)
        set_cell_background(hdr_cells[i], COLOR_PRIMARY_HEX)
        set_cell_margins(hdr_cells[i], top=110, bottom=110, left=130, right=130)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    # Data Rows
    for r_idx, row in enumerate(rows_data):
        row_cells = table.rows[r_idx + 1].cells
        bg_col = COLOR_BG_ALT_HEX if (r_idx % 2 == 1) else "FFFFFF"
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_col)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            if c_idx == 0 and len(headers) > 2 and len(str(val)) < 15:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif any(k in headers[c_idx].lower() for k in ['loss', 'accuracy', 'akurasi', 'precision', 'recall', 'f1', 'support', 'epoch', 'dimensi', 'shape', 'parameter', 'score', 'nilai']):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(9.5)
                
    if col_widths and len(col_widths) == len(headers):
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width
                
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)
    return table

def add_figure(doc, img_path, caption_text, width=Inches(5.6)):
    """Menyisipkan gambar dan caption resmi dengan format Gambar X. [Deskripsi]."""
    if not os.path.exists(img_path):
        print(f"[PERINGATAN GAGAL GAMBAR] File gambar TIDAK DITEMUKAN: {img_path}")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(3)
    p_img.paragraph_format.keep_with_next = True
    p_img.add_run().add_picture(img_path, width=width)
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(10)
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(9.5)
    r_cap.italic = True
    r_cap.font.color.rgb = RGBColor(60, 60, 60)
