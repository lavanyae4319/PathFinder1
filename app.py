import gradio as gr
import os
import pandas as pd
from job_predictor import JobPredictor
from simple_resume_parser import SimpleResumeParser
from gemini_analyzer import GeminiResumeAnalyzer
from config import RESUME_UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(RESUME_UPLOAD_FOLDER, exist_ok=True)

# Initialize components
print("Initializing components...")
job_predictor = JobPredictor()
simple_parser = SimpleResumeParser()
gemini_analyzer = GeminiResumeAnalyzer()

def analyze_and_match(resume_file, top_k=5):
    if resume_file is None:
        return "Please upload a resume.", pd.DataFrame()

    try:
        file_path = resume_file.name
        
        # 1. Parse Resume
        # Try Gemini first if available
        parsed_data = None
        analysis_text = ""
        
        if gemini_analyzer.client:
            print("Using Gemini for analysis...")
            try:
                gemini_result = gemini_analyzer.analyze_resume_comprehensive(file_path)
                parsed_data = gemini_result.get('parsed_data', {})
                analysis = gemini_result.get('analysis', {})
                
                # Format analysis for display
                analysis_text += f"## Analysis Score: {analysis.get('overall_score', 'N/A')}\n\n"
                
                analysis_text += "### Strengths\n"
                for s in analysis.get('strengths', []):
                    analysis_text += f"- {s}\n"
                
                analysis_text += "\n### Suggestions for Improvement\n"
                for s in analysis.get('suggestions', []):
                    analysis_text += f"- {s}\n"
                    
            except Exception as e:
                print(f"Gemini analysis failed: {e}")
                analysis_text += f"**Note:** AI Analysis failed ({str(e)}). Using basic parsing.\n\n"
        
        # Fallback to simple parser if needed
        if not parsed_data:
            print("Using simple parser...")
            parsed_data = simple_parser.parse_resume(file_path)
            analysis_text += "### Resume Summary\n"
            analysis_text += f"**Name:** {parsed_data.get('Personal Information', {}).get('Name', 'N/A')}\n"
            analysis_text += f"**Email:** {parsed_data.get('Personal Information', {}).get('Email', 'N/A')}\n"
            analysis_text += f"**Experience:** {parsed_data.get('Total Years of Experience', 0)} years\n"
            
            skills = parsed_data.get('Skills', [])
            if skills:
                analysis_text += f"**Skills:** {', '.join(skills[:10])}...\n"

        # 2. Get Job Recommendations
        print("Getting job recommendations...")
        # Prepare data for JobPredictor (it handles different formats relatively well, but let's be safe)
        # The JobPredictor expects a dictionary that structure-wise matches what SimpleResumeParser output OR what Gemini outputs.
        # Let's check JobPredictor.create_resume_text to be sure.
        
        # It looks for 'Professional Summary', 'Skills', 'Work Experience', 'Education', 'Preferred Job Titles'
        # Gemini output structure (from gemini_analyzer.py):
        # parsed_data = { 'personal_info': ..., 'professional_summary': ..., 'skills': [], ... }
        
        # Simple parser output structure:
        # parsed_data = { 'Personal Information': ..., 'Professional Summary': ..., 'Skills': [], ... }
        
        # We need to map Gemini structure to what JobPredictor expects if it differs too much.
        # JobPredictor.create_resume_text uses keys: 'Professional Summary', 'Skills', 'Work Experience', 'Education', 'Preferred Job Titles'
        
        input_data = parsed_data
        if 'professional_summary' in parsed_data: # Gemini style
            input_data = {
                'Professional Summary': parsed_data.get('professional_summary', ''),
                'Skills': parsed_data.get('skills', []),
                'Work Experience': parsed_data.get('work_experience', []),
                'Education': parsed_data.get('education', []),
                'Total Years of Experience': parsed_data.get('total_experience_years', 0),
                'Preferred Job Titles': parsed_data.get('preferred_job_titles', [])
            }

        recommendations = job_predictor.get_job_recommendations(input_data, top_k=int(top_k))
        
        # 3. Format Results
        candidate_summary = recommendations.get('candidate_summary', {})
        analysis_text += "\n## Job Match Prediction\n"
        analysis_text += f"**Predicted Category:** {candidate_summary.get('predicted_category', 'Unknown')}\n"
        analysis_text += f"**Confidence:** {candidate_summary.get('category_confidence', 0):.2%}\n"
        
        matches = recommendations.get('matching_jobs', [])
        
        # Convert to DataFrame for display
        jobs_df = pd.DataFrame(matches)
        if not jobs_df.empty:
            # Select relevant columns
            cols_to_show = ['jobtitle', 'company', 'primary_location', 'match_percentage', 'similarity_score']
            # Renaissance columns if necessary
            display_df = jobs_df[cols_to_show].copy()
            display_df.columns = ['Job Title', 'Company', 'Location', 'Match %', 'Score']
        else:
            display_df = pd.DataFrame(columns=['Job Title', 'Company', 'Location', 'Match %', 'Score'])
            
        return analysis_text, display_df

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}", pd.DataFrame()

# Create Gradio Interface
with gr.Blocks(title="Resume Analyzer & Job Matcher") as demo:
    gr.Markdown("# 🚀 AI Resume Analyzer & Job Matcher")
    gr.Markdown("Upload your resume (PDF, DOCX) to get AI-powered analysis and job recommendations.")
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="Upload Resume", file_types=[".pdf", ".docx", ".txt"])
            top_k_slider = gr.Slider(minimum=1, maximum=20, value=5, step=1, label="Number of Job Matches")
            analyze_btn = gr.Button("Analyze & Match", variant="primary")
        
        with gr.Column(scale=2):
            output_markdown = gr.Markdown(label="Analysis Results")
            output_table = gr.Dataframe(label="Recommended Jobs")
            
    analyze_btn.click(
        fn=analyze_and_match,
        inputs=[file_input, top_k_slider],
        outputs=[output_markdown, output_table]
    )

if __name__ == "__main__":
    demo.launch(share=True)
