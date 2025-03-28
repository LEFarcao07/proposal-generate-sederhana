📌**Note:** The better result is achieved by opening it with Microsoft Word.
# Table of Contents
1. [Document Structure (for .docx)](#document-structure-for-docx)
   - [Page 1: Cover Page](#page-1-cover-page)
   - [Page 2: Daftar Isi (Table of Contents)](#page-2-daftar-isi-table-of-contents)
   - [Page 3: Kata Pengantar (Preface)](#page-3-kata-pengantar-preface)
   - [Page 4: Latar Belakang (Background)](#page-4-latar-belakang-background)
   - [Page 5: Visi, Misi, Tujuan (Vision, Mission, and Goals)](#page-5-visi-misi-tujuan-vision-mission-and-goals)
2. [Installation Guide](#installation-guide)
3. [API Keys](#api-keys)
   - [Tiny API Key](#tiny-api-key)
   - [OpenAI API Key](#openai-api-key)
4. [Running the Application](#running-the-application)

---

# Document Structure (for .docx)

This is the recommended structure for your document:

## Page 1: Cover Page
- **Title**: Main Title of Your Document
- **Subtitle**: Subtitle or Additional Info
- **Image**: Insert an image (e.g., logo or relevant picture)
- **Your Name**: [Your Name]
- **Other Information**: Any additional details (e.g., organization, date, etc.)

## Page 2: Daftar Isi (Table of Contents)
- List all sections and sub-sections of your document with page numbers.

## Page 3: Kata Pengantar (Preface)
- A short introduction to the document and its purpose.

## Page 4: Latar Belakang (Background)
- Discuss the background or context of the document's subject.

## Page 5: Visi, Misi, Tujuan (Vision, Mission, and Goals)
- **Vision**: Your vision statement.
- **Mission**: Your mission statement.
- **Goals**: A list of goals or objectives for the project or document.

---

# Installation Guide

To install the required libraries, run the following commands:

```markdown
pip install mammoth
pip install flask
pip install python-docx
pip install beautifulsoup4
```

---

## API Keys

### Tiny API Key

1. Get your API key here: [Tiny Cloud](https://www.tiny.cloud/)
2. Open `index.html` and locate the TinyMCE script tag:
   ```html
   <script src="https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js"></script>
   ```
3. Replace `no-api-key` with your actual API key.

### OpenAI API Key

1. Get your API key here: [OpenAI API](https://platform.openai.com/docs/api-reference)
2. Open `chat.html` and update the `Authorization` header as follows:
   ```javascript
   'Authorization': 'Bearer YOUR_OPENAI_API_KEY'
   ```
3. Replace `YOUR_OPENAI_API_KEY` with your actual API key.

---

## Running the Application

1. Run the application with the following command:

   ```bash
   python app.py
   ```

2. Open your browser and access the app at: [http://localhost:5000](http://localhost:5000).

---
