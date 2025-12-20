"""
Job Predictor - Uses trained ML model to match resumes with jobs
"""

import os
import pickle
import pandas as pd
import numpy as np
from typing import Dict, List
from sklearn.metrics.pairwise import cosine_similarity
from config import (
    MODEL_PATH, VECTORIZER_PATH, LABEL_ENCODER_PATH,
    CLEANED_DATA_PATH, TOP_K_MATCHES, SIMILARITY_THRESHOLD
)


class JobPredictor:
    """Predict job matches using trained ML model"""
    
    def __init__(self):
        """Initialize the job predictor by loading trained models"""
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self.job_data = None
        self.job_vectors = None
        
        self._load_models()
        # Load job data lazily when needed
        self._job_data_loaded = False
    
    def _load_models(self):
        """Load trained models from disk"""
        try:
            # Load TF-IDF vectorizer
            if os.path.exists(VECTORIZER_PATH):
                with open(VECTORIZER_PATH, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                print(f"[OK] Loaded vectorizer from {VECTORIZER_PATH}")
            else:
                raise FileNotFoundError(f"Vectorizer not found at {VECTORIZER_PATH}")
            
            # Load classifier model
            if os.path.exists(MODEL_PATH):
                with open(MODEL_PATH, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"[OK] Loaded model from {MODEL_PATH}")
            else:
                print(f"[WARN] Model not found at {MODEL_PATH}. Classification will be unavailable.")
            
            # Load label encoder
            if os.path.exists(LABEL_ENCODER_PATH):
                with open(LABEL_ENCODER_PATH, 'rb') as f:
                    self.label_encoder = pickle.load(f)
                print(f"[OK] Loaded label encoder from {LABEL_ENCODER_PATH}")
            else:
                print(f"[WARN] Label encoder not found. Category prediction will be unavailable.")
        
        except Exception as e:
            raise Exception(f"Error loading models: {str(e)}")
    
    def _load_job_data(self):
        """Load job dataset - use CSV for faster, reliable loading"""
        try:
            if os.path.exists(CLEANED_DATA_PATH):
                self.job_data = pd.read_csv(CLEANED_DATA_PATH)
                print(f"[OK] Loaded {len(self.job_data)} job records from {CLEANED_DATA_PATH}")
                
                # Create combined text if not exists
                if 'combined_text' not in self.job_data.columns:
                    print("Creating combined text features...")
                    self.job_data['combined_text'] = self.job_data.apply(
                        self._create_job_text, axis=1
                    )
                
                # Load pre-computed job vectors if available
                job_vectors_path = 'models/job_vectors.npz'
                if os.path.exists(job_vectors_path):
                    import scipy.sparse
                    self.job_vectors = scipy.sparse.load_npz(job_vectors_path)
                    print(f"[OK] Loaded pre-computed job vectors with shape {self.job_vectors.shape}")
                else:
                    # Create job vectors for similarity matching
                    print("Creating job vectors (this will take ~10 seconds)...")
                    self.job_vectors = self.vectorizer.transform(self.job_data['combined_text'])
                    # Save for next time
                    import scipy.sparse
                    scipy.sparse.save_npz(job_vectors_path, self.job_vectors)
                    print(f"[OK] Created and saved job vectors with shape {self.job_vectors.shape}")
            else:
                raise FileNotFoundError(f"Job data not found at {CLEANED_DATA_PATH}")
        
        except Exception as e:
            raise Exception(f"Error loading job data: {str(e)}")
    
    def _create_job_text(self, row):
        """Combine job fields into single text"""
        parts = []
        
        if pd.notna(row.get('jobtitle')):
            parts.append(str(row['jobtitle']))
        
        if pd.notna(row.get('jobdescription')):
            parts.append(str(row['jobdescription']))
        
        if pd.notna(row.get('skills')):
            parts.append(str(row['skills']))
        
        return ' '.join(parts).lower()
    
    def create_resume_text(self, parsed_resume: Dict) -> str:
        """
        Create combined text from parsed resume for matching
        
        Args:
            parsed_resume: Dictionary containing parsed resume data
            
        Returns:
            Combined text string
        """
        # Ensure job data is loaded
        if not self._job_data_loaded:
            self._load_job_data()
        
        parts = []
        
        # Add professional summary
        if 'Professional Summary' in parsed_resume:
            parts.append(str(parsed_resume['Professional Summary']))
        
        # Add skills
        if 'Skills' in parsed_resume:
            skills = parsed_resume['Skills']
            if isinstance(skills, list):
                parts.extend(skills)
            elif isinstance(skills, dict):
                for skill_list in skills.values():
                    if isinstance(skill_list, list):
                        parts.extend(skill_list)
        
        # Add work experience
        if 'Work Experience' in parsed_resume:
            for exp in parsed_resume['Work Experience']:
                if isinstance(exp, dict):
                    if 'Job title' in exp:
                        parts.append(exp['Job title'])
                    if 'Responsibilities' in exp:
                        if isinstance(exp['Responsibilities'], list):
                            parts.extend(exp['Responsibilities'])
        
        # Add education
        if 'Education' in parsed_resume:
            for edu in parsed_resume['Education']:
                if isinstance(edu, dict):
                    if 'Degree' in edu:
                        parts.append(edu['Degree'])
                    if 'Field of study' in edu:
                        parts.append(edu['Field of study'])
        
        # Add preferred job titles
        if 'Preferred Job Titles' in parsed_resume:
            if isinstance(parsed_resume['Preferred Job Titles'], list):
                parts.extend(parsed_resume['Preferred Job Titles'])
        
        return ' '.join(str(p) for p in parts).lower()
    
    def predict_job_category(self, resume_text: str) -> Dict:
        """
        Predict job category for a resume
        
        Args:
            resume_text: Combined resume text
            
        Returns:
            Dictionary with predicted category and probabilities
        """
        # Ensure job data is loaded
        if not self._job_data_loaded:
            self._load_job_data()
        
        if self.model is None or self.label_encoder is None:
            return {'error': 'Model or label encoder not available'}
        
        try:
            # Vectorize resume text
            resume_vector = self.vectorizer.transform([resume_text])
            
            # Predict category
            predicted_class = self.model.predict(resume_vector)[0]
            predicted_category = self.label_encoder.inverse_transform([predicted_class])[0]
            
            # Get prediction probabilities if available
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(resume_vector)[0]
                top_3_indices = probabilities.argsort()[-3:][::-1]
                
                top_categories = [
                    {
                        'category': self.label_encoder.inverse_transform([idx])[0],
                        'probability': float(probabilities[idx])
                    }
                    for idx in top_3_indices
                ]
            else:
                top_categories = [{'category': predicted_category, 'probability': 1.0}]
            
            return {
                'predicted_category': predicted_category,
                'confidence': float(max(probabilities)) if 'probabilities' in locals() else 1.0,
                'top_categories': top_categories
            }
        
        except Exception as e:
            return {'error': f'Prediction error: {str(e)}'}
    
    def find_matching_jobs(self, resume_text: str, top_k: int = TOP_K_MATCHES,
                          min_similarity: float = SIMILARITY_THRESHOLD,
                          filters: Dict = None) -> pd.DataFrame:
        """
        Find matching jobs for a resume using cosine similarity
        
        Args:
            resume_text: Combined resume text
            top_k: Number of top matches to return
            min_similarity: Minimum similarity threshold
            filters: Optional filters (e.g., location, experience, category)
            
        Returns:
            DataFrame with matching jobs
        """
        try:
            # Vectorize resume text
            resume_vector = self.vectorizer.transform([resume_text])
            
            # Calculate cosine similarity with all jobs
            similarities = cosine_similarity(resume_vector, self.job_vectors)[0]
            
            # Filter by minimum similarity
            valid_indices = similarities >= min_similarity
            
            if not valid_indices.any():
                print(f"[WARN] No jobs found with similarity >= {min_similarity}, lowering threshold...")
                # Progressively lower the threshold to ensure we always get some results
                for threshold in [0.05, 0.03, 0.01, 0.0]:
                    valid_indices = similarities >= threshold
                    if valid_indices.any():
                        print(f"[OK] Found jobs with similarity >= {threshold}")
                        break
            
            # If still no jobs found, get top_k by similarity
            if not valid_indices.any():
                print(f"[WARN] No jobs found even with zero threshold, selecting top {top_k} by similarity")
                valid_indices = np.ones(len(similarities), dtype=bool)
            
            # Apply additional filters if provided
            if filters:
                filter_mask = pd.Series([True] * len(self.job_data))
                
                if 'location' in filters and filters['location']:
                    filter_mask &= self.job_data['primary_location'].str.contains(
                        filters['location'], case=False, na=False
                    )
                
                if 'category' in filters and filters['category']:
                    filter_mask &= self.job_data['job_category'] == filters['category']
                
                if 'min_experience' in filters:
                    filter_mask &= self.job_data['min_experience'] >= filters['min_experience']
                
                if 'max_experience' in filters:
                    filter_mask &= self.job_data['max_experience'] <= filters['max_experience']
                
                valid_indices &= filter_mask.values
            
            # Get valid job indices
            valid_job_indices = np.where(valid_indices)[0]
            valid_similarities = similarities[valid_indices]
            
            # Sort by similarity and get top k
            sorted_indices = valid_similarities.argsort()[-top_k:][::-1]
            top_indices = valid_job_indices[sorted_indices]
            
            # Create results dataframe
            results = self.job_data.iloc[top_indices].copy()
            results['similarity_score'] = similarities[top_indices]
            results['match_percentage'] = (similarities[top_indices] * 100).round(2)
            
            # Select relevant columns
            output_columns = [
                'jobid', 'jobtitle', 'company', 'job_category', 'primary_location',
                'experience', 'min_experience', 'max_experience', 'skills',
                'education', 'payrate', 'jobdescription', 'match_percentage', 'similarity_score'
            ]
            
            # Keep only existing columns
            output_columns = [col for col in output_columns if col in results.columns]
            
            return results[output_columns].reset_index(drop=True)
        
        except Exception as e:
            raise Exception(f"Error finding matching jobs: {str(e)}")
    
    def get_job_recommendations(self, parsed_resume: Dict, top_k: int = 10) -> Dict:
        """
        Get comprehensive job recommendations for a parsed resume
        
        Args:
            parsed_resume: Dictionary containing parsed resume data
            top_k: Number of recommendations to return
            
        Returns:
            Dictionary with recommendations and insights
        """
        try:
            # Create resume text
            resume_text = self.create_resume_text(parsed_resume)
            
            # Predict job category
            category_prediction = self.predict_job_category(resume_text)
            
            # Find matching jobs
            matching_jobs = self.find_matching_jobs(resume_text, top_k=top_k)
            
            # Extract candidate info
            experience_years = parsed_resume.get('Total Years of Experience', 0)
            if isinstance(experience_years, str):
                import re
                numbers = re.findall(r'\d+', experience_years)
                experience_years = int(numbers[0]) if numbers else 0
            
            # Create recommendations summary
            recommendations = {
                'candidate_summary': {
                    'experience_years': experience_years,
                    'top_skills': parsed_resume.get('Skills', [])[:10],
                    'education': parsed_resume.get('Education', []),
                    'predicted_category': category_prediction.get('predicted_category', 'Unknown'),
                    'category_confidence': category_prediction.get('confidence', 0)
                },
                'matching_jobs': matching_jobs.to_dict('records'),
                'total_matches': len(matching_jobs),
                'avg_match_score': float(matching_jobs['match_percentage'].mean()) if len(matching_jobs) > 0 else 0,
                'top_companies': matching_jobs['company'].value_counts().head(5).to_dict() if len(matching_jobs) > 0 else {},
                'top_locations': matching_jobs['primary_location'].value_counts().head(5).to_dict() if len(matching_jobs) > 0 else {}
            }
            
            return recommendations
        
        except Exception as e:
            raise Exception(f"Error generating recommendations: {str(e)}")


def main():
    """Example usage"""
    # Initialize predictor
    print("Initializing Job Predictor...")
    predictor = JobPredictor()
    
    # Example parsed resume
    sample_parsed_resume = {
        'Professional Summary': 'Experienced software engineer with expertise in Python and web development',
        'Skills': ['Python', 'Django', 'Flask', 'JavaScript', 'React', 'SQL', 'AWS'],
        'Work Experience': [
            {
                'Company name': 'Tech Corp',
                'Job title': 'Senior Software Engineer',
                'Duration (from - to)': '2020 - Present',
                'Responsibilities': ['Develop web applications', 'Lead team of 5 developers']
            }
        ],
        'Education': [
            {
                'Degree': 'B.Tech',
                'Institution': 'XYZ University',
                'Year of completion': '2019',
                'Field of study': 'Computer Science'
            }
        ],
        'Total Years of Experience': 5,
        'Preferred Job Titles': ['Software Engineer', 'Backend Developer', 'Full Stack Developer']
    }
    
    print("\n" + "="*70)
    print("GETTING JOB RECOMMENDATIONS")
    print("="*70)
    
    # Get recommendations
    recommendations = predictor.get_job_recommendations(sample_parsed_resume, top_k=5)
    
    # Display results
    print(f"\n📊 Candidate Summary:")
    print(f"   Experience: {recommendations['candidate_summary']['experience_years']} years")
    print(f"   Predicted Category: {recommendations['candidate_summary']['predicted_category']}")
    print(f"   Confidence: {recommendations['candidate_summary']['category_confidence']:.2%}")
    
    print(f"\n[INFO] Job Matches Found: {recommendations['total_matches']}")
    print(f"   Average Match Score: {recommendations['avg_match_score']:.2f}%")
    
    print(f"\n[TOP 5] Matching Jobs:")
    print("="*70)
    for i, job in enumerate(recommendations['matching_jobs'][:5], 1):
        print(f"\n{i}. {job['jobtitle']} ({job['match_percentage']}% match)")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['primary_location']}")
        print(f"   Experience: {job['experience']}")


if __name__ == "__main__":
    main()
