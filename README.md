# classifier_bot
# 🤖 Smart Issue Classifier Bot

## 🚀 Project Overview

This project solves the following problem statement:

> **"A customer types in his / her issue on mail or WhatsApp. Develop an agent that can read the message, classify the issue, and raise the service request to the relevant group."**

### ✅ What It Does

- Accepts **image of a message/invoice** via frontend
- Extracts text using **OCR (Tesseract)**
- Classifies the issue into categories (e.g., Technical, Billing, General)
- Assigns it to the **correct support team**
- Logs the request in a simple **CSV (Excel-like)** format

---

## 🧰 Tech Stack

### Frontend
- React.js
- Tailwind CSS
- Axios
- Framer Motion / Lottie
- Vite (build tool)
- Netlify / Vercel (deployment)

### Backend
- Flask (Python)
- Pytesseract (OCR)
- Scikit-learn (text classification)
- Pandas (data handling)
- joblib (ML model persistence)
- CSV (simple database)

---

## 🛠 Setup Instructions

### 🔧 Backend Setup

1. Install Tesseract OCR:
   - Windows: [Download](https://github.com/UB-Mannheim/tesseract/wiki)
   - macOS: `brew install tesseract`
   - Linux: `sudo apt install tesseract-ocr`

2. Clone the repository:
   ```bash
   git clone https://github.com/your-username/issue-classifier-bot.git
   cd backend
