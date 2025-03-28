import os
from flask import Flask, request, send_file, render_template, after_this_request, send_from_directory, jsonify
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from bs4 import BeautifulSoup

# Inisialisasi Flask
app = Flask(__name__, template_folder=os.getcwd())

# Path untuk folder assets dan temp
ASSETS_DIR = os.path.join(os.getcwd(), 'assets')
TEMP_DIR = os.path.join(ASSETS_DIR, 'temp')

# Pastikan folder assets dan temp ada
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Format file yang diizinkan
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Fungsi untuk memeriksa ekstensi file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route untuk melayani file statis (CSS, JS, dll.)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.getcwd(), filename)

# Route untuk halaman chat
@app.route('/chat')
def chat():
    return render_template('chat.html')

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk menghasilkan dokumen
@app.route('/generate', methods=['POST'])
def generate_docx():
    try:
        # Ambil file logo
        logo = request.files['logo']
        if not logo or not allowed_file(logo.filename):
            return jsonify({"error": "Format file tidak didukung. Harap unggah file dengan format: PNG, JPG, atau JPEG."}), 400

        # Simpan file logo
        logo_path = os.path.join(ASSETS_DIR, 'logo.' + logo.filename.rsplit('.', 1)[1].lower())
        logo.save(logo_path)

        # Ambil data dari form
        judul = request.form['judul']
        subjudul = request.form['subjudul']
        nama_kelompok = request.form['nama_kelompok']
        informasi_lain = request.form['informasi_lain']
        kata_pengantar = request.form['kata_pengantar']
        latar_belakang = request.form['latar_belakang']
        visi = request.form['visi']
        misi = request.form['misi']
        tujuan = request.form['tujuan']

        # Buat dokumen baru
        doc = Document()

        # Atur margin halaman
        sections = doc.sections
        for section in sections:
            section.top_margin = Cm(2)
            section.bottom_margin = Cm(2)
            section.left_margin = Cm(2)
            section.right_margin = Cm(2)

        # Fungsi untuk menambahkan teks dengan format HTML
        def add_html_paragraph(doc, html, alignment=WD_ALIGN_PARAGRAPH.LEFT, font_size=Pt(12), prefix=None, line_spacing=1.0, paragraph_spacing=Pt(12)):
            soup = BeautifulSoup(html, 'html.parser')
            
            if prefix:
                prefix_paragraph = doc.add_paragraph(prefix)
                prefix_paragraph.alignment = alignment
                prefix_paragraph.paragraph_format.space_after = paragraph_spacing
                for run in prefix_paragraph.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = font_size

            for element in soup.find_all(['p', 'ul']):
                if element.name == 'ul':
                    for li in element.find_all('li'):
                        paragraph = doc.add_paragraph(style='List Bullet')
                        paragraph.alignment = alignment
                        paragraph.paragraph_format.line_spacing = line_spacing
                        paragraph.paragraph_format.space_after = paragraph_spacing

                        for content in li.contents:
                            if content.name is None:
                                run = paragraph.add_run(str(content))
                                run.font.name = 'Times New Roman'
                                run.font.size = font_size
                            else:
                                run = paragraph.add_run()
                                for child in content.contents:
                                    if child.name is None:
                                        run.add_text(str(child))
                                    else:
                                        if child.name == 'strong' or (child.name == 'span' and 'font-weight: bold' in child.get('style', '')):
                                            run.add_text(str(child)).bold = True
                                        if child.name == 'em' or (child.name == 'span' and 'font-style: italic' in child.get('style', '')):
                                            run.add_text(str(child)).italic = True
                                        if child.name == 'u' or (child.name == 'span' and 'text-decoration: underline' in child.get('style', '')):
                                            run.add_text(str(child)).underline = True
                else:
                    paragraph = doc.add_paragraph()
                    paragraph.alignment = alignment
                    paragraph.paragraph_format.line_spacing = line_spacing
                    paragraph.paragraph_format.space_after = paragraph_spacing

                    def process_content(content):
                        if content.name is None:
                            run = paragraph.add_run(str(content))
                            run.font.name = 'Times New Roman'
                            run.font.size = font_size
                        else:
                            for child in content.contents:
                                process_content(child)
                            
                            run = paragraph.runs[-1]
                            if content.name == 'strong' or (content.name == 'span' and 'font-weight: bold' in content.get('style', '')):
                                run.bold = True
                            if content.name == 'em' or (content.name == 'span' and 'font-style: italic' in content.get('style', '')):
                                run.italic = True
                            if content.name == 'u' or (content.name == 'span' and 'text-decoration: underline' in content.get('style', '')):
                                run.underline = True

                    for content in element.contents:
                        process_content(content)

        # Judul Proposal
        add_html_paragraph(doc, judul, alignment=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(28))

        # Subjudul Proposal
        add_html_paragraph(doc, subjudul, alignment=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(17))

        # Tambahkan jarak vertikal
        doc.add_paragraph().paragraph_format.space_after = Pt(34)

        # Logo Perusahaan
        logo_width = Inches(2.5)
        doc.add_picture(logo_path, width=logo_width)
        last_paragraph = doc.paragraphs[-1]
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Tambahkan jarak vertikal
        doc.add_paragraph().paragraph_format.space_after = Pt(16)

        # Nama/Kelompok
        add_html_paragraph(doc, nama_kelompok, alignment=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(14), line_spacing=1.0, paragraph_spacing=Pt(12), prefix="Oleh :")

        # Tambahkan jarak vertikal
        doc.add_paragraph().paragraph_format.space_after = Pt(108)

        # Informasi Lain
        add_html_paragraph(doc, informasi_lain, alignment=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(12), line_spacing=1.0, paragraph_spacing=Pt(12))

        # Halaman Baru (Daftar Isi)
        doc.add_page_break()

        # Daftar Isi (Title)
        daftar_isi_title = doc.add_paragraph('DAFTAR ISI')
        daftar_isi_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in daftar_isi_title.runs:
            run.bold = True
            run.font.size = Pt(16)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Fungsi untuk menambahkan baris daftar isi
        def add_daftar_isi_line(doc, text):
            paragraph = doc.add_paragraph()
            paragraph.paragraph_format.tab_stops.add_tab_stop(Inches(6), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
            paragraph.add_run(text).bold = False
            paragraph.add_run("\t")
            run = paragraph.add_run()
            fldChar = OxmlElement('w:fldChar')
            fldChar.set(qn('w:fldCharType'), 'begin')
            run._r.append(fldChar)
            instrText = OxmlElement('w:instrText')
            instrText.set(qn('xml:space'), 'preserve')
            instrText.text = 'PAGE'
            run._r.append(instrText)
            fldChar = OxmlElement('w:fldChar')
            fldChar.set(qn('w:fldCharType'), 'end')
            run._r.append(fldChar)
            for run in paragraph.runs:
                run.font.size = Pt(12)
                run.font.name = 'Times New Roman'
                run.font.color.rgb = RGBColor(0, 0, 0)

        # Isi Daftar Isi
        add_daftar_isi_line(doc, 'SAMPUL')
        add_daftar_isi_line(doc, 'DAFTAR ISI')
        add_daftar_isi_line(doc, 'KATA PENGANTAR')
        add_daftar_isi_line(doc, 'BAB I')
        add_daftar_isi_line(doc, '   LATAR BELAKANG')
        add_daftar_isi_line(doc, '   1.1 LATAR BELAKANG')
        add_daftar_isi_line(doc, 'BAB II')
        add_daftar_isi_line(doc, '   VISI, MISI, DAN TUJUAN')
        add_daftar_isi_line(doc, '   2.1 VISI')
        add_daftar_isi_line(doc, '   2.2 MISI')
        add_daftar_isi_line(doc, '   2.3 TUJUAN')

        # Halaman Baru (Kata Pengantar)
        doc.add_page_break()

        # Kata Pengantar (Title)
        kata_pengantar_title = doc.add_paragraph('KATA PENGANTAR')
        kata_pengantar_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in kata_pengantar_title.runs:
            run.bold = True
            run.font.size = Pt(16)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Isi Kata Pengantar
        add_html_paragraph(doc, kata_pengantar, font_size=Pt(12))

        # Halaman Baru (BAB I)
        doc.add_page_break()

        # BAB I: Latar Belakang Perusahaan (Title)
        bab1_title = doc.add_paragraph('BAB I: LATAR BELAKANG')
        bab1_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in bab1_title.runs:
            run.bold = True
            run.font.size = Pt(16)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Latar (Subtitle)
        latar_belakang_title = doc.add_paragraph('1.1 Latar Belakang')
        latar_belakang_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in latar_belakang_title.runs:
            run.bold = True
            run.font.size = Pt(14)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Isi Latar
        add_html_paragraph(doc, latar_belakang, font_size=Pt(12))

        # Halaman Baru (BAB II)
        doc.add_page_break()

        # BAB II: Visi, Misi, dan Tujuan Perusahaan (Title)
        bab2_title = doc.add_paragraph('BAB II: VISI, MISI, DAN TUJUAN')
        bab2_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in bab2_title.runs:
            run.bold = True
            run.font.size = Pt(16)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Visi (Subtitle)
        visi_title = doc.add_paragraph('2.1 Visi')
        visi_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in visi_title.runs:
            run.bold = True
            run.font.size = Pt(14)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Isi Visi
        add_html_paragraph(doc, visi, font_size=Pt(12))

        # Tambahkan jarak vertikal
        doc.add_paragraph().paragraph_format.space_after = Pt(24)

        # Misi (Subtitle)
        misi_title = doc.add_paragraph('2.2 Misi')
        misi_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in misi_title.runs:
            run.bold = True
            run.font.size = Pt(14)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Isi Misi
        add_html_paragraph(doc, misi, font_size=Pt(12))

        # Tambahkan jarak vertikal
        doc.add_paragraph().paragraph_format.space_after = Pt(24)

        # Tujuan (Subtitle)
        tujuan_title = doc.add_paragraph('2.3 Tujuan')
        tujuan_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in tujuan_title.runs:
            run.bold = True
            run.font.size = Pt(14)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Isi Tujuan
        add_html_paragraph(doc, tujuan, font_size=Pt(12))

        # Tambahkan nomor halaman di pojok kanan bawah
        def add_page_number(doc):
            section = doc.sections[0]
            footer = section.footer
            paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            run = paragraph.add_run()
            fldChar = OxmlElement('w:fldChar')
            fldChar.set(qn('w:fldCharType'), 'begin')
            run._r.append(fldChar)
            instrText = OxmlElement('w:instrText')
            instrText.set(qn('xml:space'), 'preserve')
            instrText.text = 'PAGE'
            run._r.append(instrText)
            fldChar = OxmlElement('w:fldChar')
            fldChar.set(qn('w:fldCharType'), 'end')
            run._r.append(fldChar)

        add_page_number(doc)

        # Simpan dokumen sementara di folder temp
        doc_path = os.path.join(TEMP_DIR, 'proposal.docx')
        doc.save(doc_path)

        # Fungsi untuk menghapus file sementara setelah dikirim
        @after_this_request
        def remove_file(response):
            try:
                if os.path.exists(doc_path):
                    os.remove(doc_path)
                    print(f"File {doc_path} berhasil dihapus.")
                
                if os.path.exists(logo_path):
                    os.remove(logo_path)
                    print(f"File {logo_path} berhasil dihapus.")
            except Exception as e:
                print(f"Gagal menghapus file sementara: {e}")
            return response

        # Kirim file sebagai respons
        return send_file(doc_path, as_attachment=True, download_name='proposal.docx')
    except Exception as e:
        return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)