# 🧾 Receipt OCR API – FastAPI + MongoDB

This project is part of the **Automate Accounts Developer Hiring Assessment**.

It provides REST APIs to:
- Upload scanned receipt PDFs
- Validate them
- Extract key data using OCR (Tesseract)
- Store structured info in MongoDB
- Retrieve receipt records via APIs

---

## 📦 Tech Stack

- **FastAPI** – Web framework
- **MongoDB + MongoEngine** – NoSQL database
- **pdf2image** – Convert PDF pages to images
- **Tesseract OCR** – Extract text from images

---

## 🚀 Setup Instructions

### 🧱 Prerequisites
- Python 3.8+
- MongoDB running locally on default port (`27017`)
- Poppler (for `pdf2image`)
- Tesseract OCR

### 🔧 Install System Dependencies

#### macOS
```bash
brew install poppler tesseract
