# 🚀 QUICK START GUIDE - Flask Web Application

## ⚡ 3-Step Launch

### Step 1: Install Dependencies (One-time)
```bash
pip install Flask reportlab
```

### Step 2: Start the Server
```bash
python app.py
```
**OR** just double-click `start_webapp.bat`

### Step 3: Open Browser
Navigate to: **http://localhost:5000**

---

## 🎯 Features Overview

### 1. 📊 Resume Analysis (`/analyze`)
- Upload resume (PDF/DOCX/TXT)
- AI-powered parsing
- Get top job matches
- View match scores & insights

### 2. ✨ Resume Generator (`/generator`)
- Fill in your information
- Add work experience & education
- Generate professional PDF/DOCX
- ATS-friendly templates

### 3. ℹ️ About Page (`/about`)
- Technology stack info
- Platform statistics
- Contact information

---

## 📋 Prerequisites Checklist

Before running the web app:

✅ **Python packages installed**
```bash
pip install -r requirements.txt
```

✅ **ML models trained**
- Run `data_cleaning.ipynb`
- Run `model_training.ipynb`

✅ **API key configured** (in `.env` file)
```env
OPENAI_API_KEY=your_key_here
# OR
GOOGLE_API_KEY=your_key_here
```

---

## 🎨 UI Highlights

- **Modern Dark Theme** - Professional & eye-friendly
- **Fully Responsive** - Works on all devices
- **Drag & Drop Upload** - Easy file handling
- **Real-time Progress** - Visual feedback
- **Smooth Animations** - Engaging UX
- **Interactive Charts** - Data visualization

---

## 🛠️ Troubleshooting

### Port Already in Use?
Change port in `app.py` (last line):
```python
app.run(debug=True, host='0.0.0.0', port=8000)
```

### Models Not Found?
1. Run `data_cleaning.ipynb`
2. Run `model_training.ipynb`
3. Restart Flask app

### API Error?
Check `.env` file has correct API key

---

## 📁 Project Structure
```
Data_Science_project/
├── app.py                 ← Flask application
├── templates/             ← HTML pages
│   ├── index.html        ← Homepage
│   ├── analyze.html      ← Analysis page
│   └── generator.html    ← Generator page
├── static/
│   ├── css/style.css     ← Styling
│   └── js/               ← Interactive features
├── uploads/              ← Uploaded resumes
├── results/              ← Analysis results
└── models/               ← Trained ML models
```

---

## 🔗 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analyze` | POST | Analyze resume |
| `/api/generate-resume` | POST | Generate resume |
| `/api/system-status` | GET | Check system status |

---

## 📖 Documentation

- **Full README:** `README.md`
- **Setup Guide:** `SETUP_GUIDE.md`
- **Web App Guide:** `WEB_APP_GUIDE.md` ← Detailed web app docs

---

## 🎉 You're Ready!

Run `python app.py` and visit **http://localhost:5000**

Enjoy your AI-Powered Resume Analyzer! 🚀

---

**Need Help?** Check `WEB_APP_GUIDE.md` for detailed documentation.
