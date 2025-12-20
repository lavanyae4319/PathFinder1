# Flask Web Application - Setup & Usage Guide

## 🚀 Quick Start

### 1. Install Additional Dependencies

```bash
pip install Flask reportlab
```

Or reinstall all requirements:
```bash
pip install -r requirements.txt
```

### 2. Run the Web Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

### 3. Access the Application

Open your browser and navigate to:
- **Home:** http://localhost:5000
- **Analyze Resume:** http://localhost:5000/analyze
- **Generate Resume:** http://localhost:5000/generator
- **About:** http://localhost:5000/about

## 📱 Features

### 1. **Resume Analysis**
- Upload resume (PDF, DOCX, TXT)
- AI-powered parsing using OpenAI/Gemini/Claude
- Get top job matches with similarity scores
- View detailed candidate profile and skills
- Download results as JSON/Excel

### 2. **Job Prediction**
- ML-based job category prediction
- Cosine similarity matching
- Confidence scores for predictions
- Top companies and locations insights

### 3. **Resume Generator**
- Create professional resumes
- Modern, ATS-friendly templates
- Export as PDF or DOCX
- Multiple sections: Experience, Education, Skills, Certifications

## 🎨 UI Features

- **Modern Dark Theme** - Eye-friendly dark mode design
- **Responsive Layout** - Works on desktop, tablet, and mobile
- **Smooth Animations** - Engaging user experience
- **Interactive Elements** - Drag & drop file upload
- **Real-time Validation** - Instant feedback on forms
- **Progress Indicators** - Visual progress tracking

## 🔧 Configuration

### API Keys
Make sure you have configured your AI API key in `.env`:

```env
# Choose one provider
OPENAI_API_KEY=your_openai_key_here
# OR
GOOGLE_API_KEY=your_gemini_key_here
# OR
ANTHROPIC_API_KEY=your_claude_key_here

# Set active provider in config.py
AI_PROVIDER=openai  # or gemini or anthropic
```

### File Upload Settings
Edit in `config.py`:
- `MAX_RESUME_SIZE_MB` - Maximum file size (default: 10MB)
- `SUPPORTED_RESUME_FORMATS` - Allowed file types

## 📂 Project Structure

```
Data_Science_project/
├── app.py                      # Flask application
├── resume_parser.py            # AI resume parser
├── job_predictor.py           # ML job predictor
├── config.py                  # Configuration
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── index.html            # Home page
│   ├── analyze.html          # Analysis page
│   ├── generator.html        # Generator page
│   ├── about.html            # About page
│   ├── 404.html              # 404 error
│   └── 500.html              # 500 error
├── static/                    # Static files
│   ├── css/
│   │   └── style.css         # Main stylesheet
│   └── js/
│       ├── main.js           # Common JS
│       ├── analyze.js        # Analysis page JS
│       └── generator.js      # Generator page JS
├── uploads/                   # Uploaded resumes
├── results/                   # Analysis results
└── models/                    # Trained ML models
```

## 🔌 API Endpoints

### POST `/api/analyze`
Analyze a resume and get job matches

**Request:**
- Form data with `resume` file
- Optional: `top_k` (number of matches)

**Response:**
```json
{
  "success": true,
  "parsed_data": {...},
  "predictions": {...},
  "matching_jobs": [...]
}
```

### POST `/api/generate-resume`
Generate a professional resume

**Request:**
```json
{
  "personal_info": {...},
  "summary": "...",
  "skills": [...],
  "experience": [...],
  "education": [...],
  "format": "docx" or "pdf"
}
```

**Response:**
- File download (PDF or DOCX)

### GET `/api/system-status`
Check system status

**Response:**
```json
{
  "parser_ready": true,
  "predictor_ready": true,
  "ai_provider": "openai",
  "total_jobs": 22001
}
```

## 🎯 Usage Examples

### Analyze a Resume
1. Navigate to "Analyze Resume" page
2. Drag & drop your resume or click to browse
3. Select number of job matches (5-20)
4. Click "Analyze Resume"
5. View results with match scores, skills, and insights

### Generate a Resume
1. Navigate to "Generate Resume" page
2. Fill in personal information
3. Add professional summary
4. Add skills (click + to add each skill)
5. Add work experience and education
6. Select format (PDF or DOCX)
7. Click "Generate Resume" to download

## 🛠️ Troubleshooting

### Models Not Found
If you get "Models not found" error:
1. Run `data_cleaning.ipynb` notebook
2. Run `model_training.ipynb` notebook
3. Restart the Flask application

### API Key Error
If you get API authentication error:
1. Check `.env` file exists
2. Verify API key is correct
3. Ensure `AI_PROVIDER` matches your key

### Port Already in Use
If port 5000 is busy:
```bash
# Change port in app.py (last line)
app.run(debug=True, host='0.0.0.0', port=8000)
```

## 🎨 Customization

### Change Theme Colors
Edit `static/css/style.css` root variables:
```css
:root {
    --primary-color: #4F46E5;
    --secondary-color: #06B6D4;
    /* ... more colors */
}
```

### Modify Templates
Edit HTML files in `templates/` folder to customize layout and content.

### Add New Features
1. Add route in `app.py`
2. Create template in `templates/`
3. Add styles in `static/css/`
4. Add JS logic in `static/js/`

## 📊 Performance

- Average analysis time: < 30 seconds
- Supports concurrent requests
- File upload limit: 10MB
- Recommended: Use production WSGI server for deployment

## 🚀 Production Deployment

For production use, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or use waitress (Windows-friendly):
```bash
pip install waitress
waitress-serve --port=5000 app:app
```

## 📝 Notes

- First analysis may take longer (model loading)
- Large resumes (>10MB) will be rejected
- AI parsing quality depends on resume format
- Best results with well-structured resumes

## 🆘 Support

For issues or questions:
- Check the main README.md
- Review SETUP_GUIDE.md
- Run `python test_system.py` to verify setup

## 🔐 Security

- API keys stored in `.env` (not committed to git)
- File uploads validated for type and size
- User data not stored permanently
- HTTPS recommended for production

---

**Enjoy your AI-Powered Resume Analyzer! 🎉**
