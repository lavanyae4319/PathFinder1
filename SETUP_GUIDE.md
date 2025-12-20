# Quick Setup Guide - Resume Analyzer System

## Step-by-Step Instructions

### ✅ Step 1: Install Dependencies

```powershell
# Navigate to project directory
cd "c:\mca code\Data_Science_project"

# Install all required packages
pip install -r requirements.txt
```

### ✅ Step 2: Configure AI API Key

1. Get your API key:
   - **OpenAI**: https://platform.openai.com/api-keys
   - **Gemini**: https://makersuite.google.com/app/apikey
   - **Claude**: https://console.anthropic.com/

2. Create `.env` file (copy from .env.example):
```powershell
copy .env.example .env
```

3. Edit `.env` and add your API key:
```
AI_PROVIDER=openai
OPENAI_API_KEY=sk-YOUR-ACTUAL-API-KEY-HERE
```

### ✅ Step 3: Clean the Data

Run the data cleaning notebook to prepare your dataset:

```powershell
jupyter notebook data_cleaning.ipynb
```

**What it does:**
- Loads raw job data
- Removes duplicates and handles missing values
- Cleans text fields
- Creates new features
- Saves cleaned data to `dataset/cleaned_job_data.csv`

**Run all cells in the notebook!**

### ✅ Step 4: Train the ML Model

Run the model training notebook:

```powershell
jupyter notebook model_training.ipynb
```

**What it does:**
- Creates TF-IDF features from job descriptions
- Trains multiple ML models (Random Forest, Gradient Boosting, Logistic Regression)
- Selects the best model
- Saves trained models to `models/` folder

**Run all cells in the notebook!**

Expected outputs:
- `models/job_matcher_model.pkl`
- `models/tfidf_vectorizer.pkl`
- `models/label_encoder.pkl`
- `models/model_metadata.json`

### ✅ Step 5: Test the System

Create a sample resume or use an existing one:

**Option A: Create a sample resume**
Create file `uploads/resumes/sample_resume.txt` with content:
```
John Doe
Email: john.doe@email.com
Phone: +91-9876543210

PROFESSIONAL SUMMARY
Experienced Software Engineer with 5 years in Python, JavaScript, and web development.
Strong background in Django, Flask, React, and cloud technologies like AWS.

SKILLS
- Programming: Python, JavaScript, Java, SQL
- Frameworks: Django, Flask, React, Node.js
- Cloud: AWS, Azure, Docker
- Database: PostgreSQL, MySQL, MongoDB

WORK EXPERIENCE
Senior Software Engineer at Tech Corp (2020 - Present)
- Developed web applications using Django and React
- Led team of 5 developers
- Implemented CI/CD pipelines

Software Engineer at StartupXYZ (2019 - 2020)
- Built REST APIs using Flask
- Worked with PostgreSQL databases

EDUCATION
B.Tech in Computer Science
XYZ University, 2019
```

**Option B: Use your own resume (PDF/DOCX/TXT)**
Place it in `uploads/resumes/` folder

### ✅ Step 6: Run the Analyzer

```powershell
# Analyze a specific resume
python main.py "uploads/resumes/sample_resume.txt"

# Or just run with default
python main.py
```

**What happens:**
1. 🤖 AI parses your resume (extracts skills, experience, education)
2. 🎯 ML model finds matching jobs
3. 📊 Generates match scores for each job
4. 💾 Saves results to `results/` folder (JSON + Excel)

### ✅ Expected Output

```
======================================================================
INTELLIGENT RESUME ANALYZER & JOB MATCH PREDICTION SYSTEM
======================================================================

Initializing components...

1️⃣ Initializing AI Resume Parser...
✓ Initialized OpenAI client with model: gpt-3.5-turbo

2️⃣ Initializing ML Job Predictor...
✓ Loaded vectorizer from models/tfidf_vectorizer.pkl
✓ Loaded model from models/job_matcher_model.pkl
✓ Loaded label encoder from models/label_encoder.pkl
✓ Loaded 15000 job records from dataset/cleaned_job_data.csv

======================================================================
STARTING RESUME ANALYSIS
======================================================================

🤖 STEP 1: Parsing resume using OPENAI AI
📄 Extracting text from resume: sample_resume.txt
✓ Extracted 850 characters
🤖 Parsing resume using OPENAI AI...
✓ Resume parsed successfully!

📄 Extracted Information:
   Name: John Doe
   Email: john.doe@email.com
   Total Experience: 5 years
   Skills Count: 15
   Top Skills: Python, JavaScript, Java, SQL, Django

🎯 STEP 2: Finding matching jobs using ML model

📊 Analysis Results:
   Predicted Job Category: IT & Software
   Category Confidence: 87.50%
   Total Matching Jobs: 10
   Average Match Score: 75.23%

======================================================================
TOP 5 JOB MATCHES
======================================================================

1. Senior Python Developer
   ──────────────────────────────────────────────────────────────────
   🏢 Company: Tech Solutions Ltd
   📍 Location: Bengaluru
   💼 Experience: 4-7 years
   🎯 Match Score: 89.5%
   📂 Category: IT & Software
   🔧 Skills: Python, Django, Flask, AWS, PostgreSQL...

2. Full Stack Developer - Python/React
   ──────────────────────────────────────────────────────────────────
   🏢 Company: Innovative Systems
   📍 Location: Mumbai
   💼 Experience: 5-8 years
   🎯 Match Score: 85.2%
   ...
```

## 🎉 You're Done!

Your system is now ready to:
- Parse resumes using AI
- Match candidates with jobs using ML
- Generate comprehensive reports

## 📊 Check Your Results

Results are saved in `results/` folder:
- `resume_analysis_YYYYMMDD_HHMMSS.json` - Full JSON report
- `resume_analysis_YYYYMMDD_HHMMSS.xlsx` - Excel report

## 🔧 Troubleshooting

### Issue: "Model not found"
**Solution:** Run `model_training.ipynb` first

### Issue: "API key invalid"
**Solution:** Check your `.env` file, ensure API key is correct

### Issue: "Cleaned data not found"
**Solution:** Run `data_cleaning.ipynb` first

### Issue: "Module not found"
**Solution:** Run `pip install -r requirements.txt`

## 💡 Tips

1. **Better results:** Use GPT-4 instead of GPT-3.5 (costs more but more accurate)
   ```
   OPENAI_MODEL=gpt-4
   ```

2. **Save API costs:** Use Gemini (free tier available)
   ```
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your-key
   ```

3. **Batch processing:** Modify `main.py` to loop through multiple resumes

4. **Custom filtering:** Edit `job_predictor.py` to add more filters

## 📞 Need Help?

Check the full documentation in `README.md`

Happy analyzing! 🚀
