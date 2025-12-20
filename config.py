"""
Configuration file for Resume Analyzer & Job Match Prediction System
Store your API keys and model settings here
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# AI API Configuration (for Resume Parsing)
# ============================================

# Choose your preferred AI provider: 'openai', 'gemini', or 'anthropic'
AI_PROVIDER = os.getenv('AI_PROVIDER', 'gemini')  # Default to Gemini

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')  # or 'gpt-4'

# Google Gemini Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')

# Anthropic Claude Configuration (optional)
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229')

# ============================================
# Model Configuration (for Job Prediction)
# ============================================

# Path to trained model
MODEL_PATH = 'models/job_matcher_model.pkl'
VECTORIZER_PATH = 'models/tfidf_vectorizer.pkl'
LABEL_ENCODER_PATH = 'models/label_encoder.pkl'

# Model parameters
MAX_FEATURES = 5000
MIN_DF = 2
MAX_DF = 0.8
NGRAM_RANGE = (1, 2)

# ============================================
# Data Paths
# ============================================

CLEANED_DATA_PATH = 'dataset/cleaned_job_data.csv'
RAW_DATA_PATH = 'dataset/naukri_com-job_sample.csv'
RESUME_UPLOAD_FOLDER = 'uploads/resumes'
RESULTS_FOLDER = 'results'

# ============================================
# Application Settings
# ============================================

# Number of top job matches to return
TOP_K_MATCHES = 10

# Similarity threshold (0-1) - Lowered to show more matches
SIMILARITY_THRESHOLD = 0.05

# Resume parsing settings
SUPPORTED_RESUME_FORMATS = ['.pdf', '.docx', '.txt']
MAX_RESUME_SIZE_MB = 5

# ============================================
# System Prompts for AI Resume Parsing
# ============================================

RESUME_PARSING_PROMPT = """
You are an expert resume parser. Analyze the following resume and extract structured information.

Extract the following details in JSON format:
1. Personal Information:
   - Name
   - Email
   - Phone
   - Location
   - LinkedIn (if available)

2. Professional Summary (brief summary of candidate's profile)

3. Skills (as a list):
   - Technical skills
   - Soft skills
   - Tools and technologies

4. Work Experience (as a list of objects):
   - Company name
   - Job title
   - Duration (from - to)
   - Responsibilities (list)

5. Education (as a list of objects):
   - Degree
   - Institution
   - Year of completion
   - Field of study

6. Certifications (if any)

7. Total Years of Experience (calculate from work history)

8. Preferred Job Titles (infer from experience and skills)

9. Preferred Industries (infer from experience)

Resume Text:
{resume_text}

Respond ONLY with valid JSON. Do not include any explanation or markdown formatting.
"""

JOB_MATCHING_PROMPT = """
Based on the candidate's profile and the job descriptions, provide insights on:
1. How well does the candidate match this job?
2. What are the candidate's strengths for this role?
3. What skills might be missing?
4. Suggestions for the candidate

Candidate Profile:
{candidate_profile}

Job Description:
{job_description}

Provide a structured analysis.
"""

# ============================================
# Logging Configuration
# ============================================

LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/resume_analyzer.log'

# Create necessary directories
os.makedirs('models', exist_ok=True)
os.makedirs('uploads/resumes', exist_ok=True)
os.makedirs('results', exist_ok=True)
os.makedirs('logs', exist_ok=True)
