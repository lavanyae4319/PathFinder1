"""
Main Application - Intelligent Resume Analyzer & Job Match Prediction System
Combines AI-powered resume parsing with ML-based job matching
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Optional

import pandas as pd

from simple_resume_parser import SimpleResumeParser
from job_predictor import JobPredictor
from config import (
    RESUME_UPLOAD_FOLDER,
    RESULTS_FOLDER,
    SUPPORTED_RESUME_FORMATS,
    MAX_RESUME_SIZE_MB,
)


class ResumeAnalyzer:
    """Main application class combining resume parsing and job prediction"""
    
    def __init__(self):
        """
        Initialize the Resume Analyzer
        """
        print("="*70)
        print("INTELLIGENT RESUME ANALYZER & JOB MATCH PREDICTION SYSTEM")
        print("="*70)
        print("\nInitializing components...")
        
        # Initialize resume parser (local, no external AI)
        print("\n1️⃣ Initializing Local Resume Parser (no API key required)...")
        self.parser = SimpleResumeParser()
        
        # Initialize job predictor (ML-based)
        print("\n2️⃣ Initializing ML Job Predictor...")
        self.predictor = JobPredictor()
        
        print("\n✅ All components initialized successfully!")
    
    def validate_resume_file(self, file_path: str) -> bool:
        """Validate resume file format and size"""
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Resume file not found: {file_path}")
        
        # Check file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in SUPPORTED_RESUME_FORMATS:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: {SUPPORTED_RESUME_FORMATS}")
        
        # Check file size
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > MAX_RESUME_SIZE_MB:
            raise ValueError(f"File size ({file_size_mb:.2f} MB) exceeds maximum allowed size ({MAX_RESUME_SIZE_MB} MB)")
        
        return True
    
    def analyze_resume(self, resume_path: str, top_k_jobs: int = 10,
                      save_results: bool = True) -> Dict:
        """
        Complete resume analysis pipeline
        
        Args:
            resume_path: Path to resume file
            top_k_jobs: Number of top job matches to return
            save_results: Whether to save results to file
            
        Returns:
            Dictionary containing analysis results
        """
        print("\n" + "="*70)
        print("STARTING RESUME ANALYSIS")
        print("="*70)
        
        # Validate resume file
        print(f"\n📋 Validating resume file: {os.path.basename(resume_path)}")
        self.validate_resume_file(resume_path)
        print("✓ Validation passed")
        
        # Step 1: Parse resume using AI
        print(f"\n🤖 STEP 1: Parsing resume using local text parser")
        print("-"*70)
        parsed_resume = self.parser.parse_resume(resume_path)
        
        # Display parsed information
        print("\n📄 Extracted Information:")
        if 'Personal Information' in parsed_resume:
            print(f"   Name: {parsed_resume['Personal Information'].get('Name', 'N/A')}")
            print(f"   Email: {parsed_resume['Personal Information'].get('Email', 'N/A')}")
        
        print(f"   Total Experience: {parsed_resume.get('Total Years of Experience', 'N/A')} years")
        
        if 'Skills' in parsed_resume:
            skills = parsed_resume['Skills']
            if isinstance(skills, list):
                print(f"   Skills Count: {len(skills)}")
                print(f"   Top Skills: {', '.join(skills[:5])}")
        
        # Step 2: Get job recommendations using ML model
        print(f"\n🎯 STEP 2: Finding matching jobs using ML model")
        print("-"*70)
        recommendations = self.predictor.get_job_recommendations(parsed_resume, top_k=top_k_jobs)
        
        # Display recommendations summary
        print("\n📊 Analysis Results:")
        print(f"   Predicted Job Category: {recommendations['candidate_summary']['predicted_category']}")
        print(f"   Category Confidence: {recommendations['candidate_summary']['category_confidence']:.2%}")
        print(f"   Total Matching Jobs: {recommendations['total_matches']}")
        print(f"   Average Match Score: {recommendations['avg_match_score']:.2f}%")
        
        # Combine results
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'resume_file': os.path.basename(resume_path),
            'parsing_provider': 'simple',
            'parsed_resume': parsed_resume,
            'job_recommendations': recommendations,
        }
        
        # Save results if requested
        if save_results:
            self._save_results(analysis_results, resume_path)
        
        return analysis_results
    
    def _save_results(self, results: Dict, resume_path: str):
        """Save analysis results to file"""
        try:
            # Create results filename
            resume_name = os.path.splitext(os.path.basename(resume_path))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_filename = f"{resume_name}_analysis_{timestamp}.json"
            results_path = os.path.join(RESULTS_FOLDER, results_filename)
            
            # Save as JSON
            with open(results_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Results saved to: {results_path}")
            
            # Also save as Excel for easy viewing
            excel_path = results_path.replace('.json', '.xlsx')
            self._save_excel_report(results, excel_path)
            print(f"💾 Excel report saved to: {excel_path}")
        
        except Exception as e:
            print(f"⚠ Warning: Could not save results: {str(e)}")
    
    def _save_excel_report(self, results: Dict, excel_path: str):
        """Save analysis results as Excel report"""
        try:
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                # Sheet 1: Candidate Summary
                candidate_summary = results['job_recommendations']['candidate_summary']
                summary_df = pd.DataFrame([{
                    'Experience (Years)': candidate_summary.get('experience_years', 'N/A'),
                    'Predicted Category': candidate_summary.get('predicted_category', 'N/A'),
                    'Category Confidence': f"{candidate_summary.get('category_confidence', 0):.2%}",
                    'Total Matches': results['job_recommendations']['total_matches'],
                    'Avg Match Score': f"{results['job_recommendations']['avg_match_score']:.2f}%"
                }])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Sheet 2: Matching Jobs
                if results['job_recommendations']['matching_jobs']:
                    jobs_df = pd.DataFrame(results['job_recommendations']['matching_jobs'])
                    # Select key columns
                    display_cols = ['jobtitle', 'company', 'primary_location', 'experience', 
                                   'match_percentage', 'job_category']
                    display_cols = [col for col in display_cols if col in jobs_df.columns]
                    jobs_df[display_cols].to_excel(writer, sheet_name='Matching Jobs', index=False)
                
                # Sheet 3: Skills
                if 'Skills' in results['parsed_resume']:
                    skills = results['parsed_resume']['Skills']
                    if isinstance(skills, list):
                        skills_df = pd.DataFrame({'Skills': skills})
                        skills_df.to_excel(writer, sheet_name='Skills', index=False)
        
        except Exception as e:
            print(f"⚠ Could not create Excel report: {str(e)}")
    
    def display_top_matches(self, results: Dict, top_n: int = 5):
        """Display top job matches in a formatted way"""
        print("\n" + "="*70)
        print(f"TOP {top_n} JOB MATCHES")
        print("="*70)
        
        jobs = results['job_recommendations']['matching_jobs'][:top_n]
        
        for i, job in enumerate(jobs, 1):
            print(f"\n{i}. {job['jobtitle']}")
            print(f"   {'─'*66}")
            print(f"   🏢 Company: {job['company']}")
            print(f"   📍 Location: {job['primary_location']}")
            print(f"   💼 Experience: {job['experience']}")
            print(f"   🎯 Match Score: {job['match_percentage']}%")
            print(f"   📂 Category: {job.get('job_category', 'N/A')}")
            
            # Display top skills if available
            if 'skills' in job and job['skills'] and job['skills'] != 'Not Specified':
                skills_preview = str(job['skills'])[:100]
                print(f"   🔧 Skills: {skills_preview}...")


def main():
    """Main application entry point"""
    print("\n" + "="*70)
    print("INTELLIGENT RESUME ANALYZER - DEMO")
    print("="*70)
    
    # Check if resume file is provided as command line argument
    if len(sys.argv) > 1:
        resume_path = sys.argv[1]
    else:
        # Use default test resume
        resume_path = os.path.join(RESUME_UPLOAD_FOLDER, "sample_resume.pdf")
        
        if not os.path.exists(resume_path):
            print(f"\n❌ No resume file found at: {resume_path}")
            print(f"\nUsage: python main.py <path_to_resume>")
            print(f"\nSupported formats: {', '.join(SUPPORTED_RESUME_FORMATS)}")
            print(f"\nPlease place a resume file in: {RESUME_UPLOAD_FOLDER}/")
            return
    
    try:
        # Initialize analyzer
        analyzer = ResumeAnalyzer()
        
        # Analyze resume
        results = analyzer.analyze_resume(
            resume_path=resume_path,
            top_k_jobs=10,
            save_results=True
        )
        
        # Display top matches
        analyzer.display_top_matches(results, top_n=5)
        
        print("\n" + "="*70)
        print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print(f"\n📁 Results saved in: {RESULTS_FOLDER}/")
        print("\nThank you for using Resume Analyzer! 🎉")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {str(e)}")
        print(f"\nPlease ensure the resume file exists at the specified path.")
    
    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
