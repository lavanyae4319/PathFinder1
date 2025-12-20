---
title: Ads Deploay1
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.19.2
app_file: app.py
pinned: false
---

# Intelligent Resume Analyzer & Job Matcher

This project is a Resume Analysis and Job Matching system powered by AI (Gemini/OpenAI) and Machine Learning. It has been configured for deployment on **Hugging Face Spaces** using **Gradio**.

## 🚀 Features

- **Resume Parsing**: Extracts details from PDF and DOCX resumes.
- **AI Analysis**: Uses Google Gemini (or others) to provide strengths, weaknesses, and improvement suggestions.
- **Job Matching**: Uses a trained ML model to match the resume against a job database.
- **Interactive UI**: Easy-to-use Gradio interface.

## 📦 Deployment on Hugging Face Spaces

1.  **Create a New Space**:
    - Go to [Hugging Face Spaces](https://huggingface.co/spaces).
    - Click **Create new Space**.
    - Enter a name (e.g., `resume-analyzer`).
    - Select **Gradio** as the SDK.
    - Choose **Public** or **Private**.
    - Click **Create Space**.

2.  **Upload Files**:
    - You can upload files via the Web Interface or using Git.
    - Upload all files from this directory, **ensuring the following are included**:
        - `app.py` (The main Gradio application)
        - `requirements.txt` (Dependencies)
        - `config.py`
        - `job_predictor.py`
        - `simple_resume_parser.py`
        - `gemini_analyzer.py`
        - `models/` folder (Contains `job_matcher_model.pkl`, `tfidf_vectorizer.pkl`, etc.)
        - `dataset/` folder (Contains `cleaned_job_data.csv`)

    *Note: Large files (like models) might need `git lfs`. If uploading via web, wait for them to finish.*

3.  **Set Environment Variables (Secrets)**:
    - Go to the **Settings** tab of your Space.
    - Scroll to **Variables and secrets**.
    - Click **New Secret**.
    - Name: `GEMINI_API_KEY`
    - Value: `your_actual_api_key`
    - (Optional) Add `OPENAI_API_KEY` if using OpenAI.

4.  **Run**:
    - The Space will build and start automatically.
    - Once "Running", you can interact with the app.

## 🛠 Local Installation

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd <repo-name>
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**:
    ```bash
    python app.py
    ```
    Open the URL displayed in the terminal (usually `http://127.0.0.1:7860`).

## 📂 Project Structure

- `app.py`: Main Gradio application.
- `flask_app.py`: Alternative Flask application (backend-centric).
- `job_predictor.py`: ML logic for matching resumes to jobs.
- `simple_resume_parser.py`: Basic rule-based resume parser.
- `gemini_analyzer.py`: Advanced AI-based analyzer.
- `models/`: Contains trained ML models.
- `dataset/`: Contains the job database.

## ⚠️ Troubleshooting

- **Model Not Found**: Ensure the `models/` directory is uploaded and contains `.pkl` and `.npz` files.
- **API Key Error**: Ensure `GEMINI_API_KEY` is set in the Secrets configuration of your Space.
- **Large File Error**: Hugging Face has a file size limit (5MB for direct upload via basic git, larger needs LFS). The `job_matcher.pkl` might be large.
    - If `job_matcher.pkl` > 10MB, ensure you use Git LFS:
      ```bash
      git lfs install
      git lfs track "*.pkl"
      git lfs track "*.npz"
      git add .gitattributes
      ```
