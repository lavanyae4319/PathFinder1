"""
Gemini AI Resume Analyzer - Comprehensive Resume Analysis using Gemini 2.5 Flash
Provides detailed insights, suggestions, and job recommendations
"""

import os
import json
import re
from typing import Dict, Optional
from config import GEMINI_API_KEY, GEMINI_MODEL
from simple_resume_parser import SimpleResumeParser


class GeminiResumeAnalyzer:
    """Comprehensive resume analysis using Gemini AI"""
    
    def __init__(self):
        """Initialize Gemini client"""
        self.simple_parser = SimpleResumeParser()
        self.client = None
        self.model_name = GEMINI_MODEL
        
        try:
            import google.generativeai as genai
            if not GEMINI_API_KEY or 'your-gemini-api-key-here' in GEMINI_API_KEY:
                raise ValueError("Gemini API key not configured")
            genai.configure(api_key=GEMINI_API_KEY)
            self.client = genai.GenerativeModel(self.model_name)
            print(f"✓ Initialized Gemini 2.5 Flash for resume analysis")
        except Exception as e:
            print(f"⚠ Gemini not available: {e}. Using simple parser only.")
            self.client = None
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from resume file"""
        return self.simple_parser.parse_resume(file_path).get('raw_text', '')
    
    def analyze_resume_comprehensive(self, file_path: str) -> Dict:
        """
        Comprehensive resume analysis using Gemini AI
        
        Returns:
            Dictionary with detailed analysis including:
            - Parsed resume data
            - Strengths and weaknesses
            - Improvement suggestions
            - Job recommendations
            - Skills gap analysis
            - Career path suggestions
            - ATS optimization tips
        """
        # Extract text from resume
        resume_text = self.extract_text_from_file(file_path)
        
        if not resume_text or len(resume_text) < 50:
            raise ValueError("Resume text is too short or could not be extracted")
        
        # If Gemini is not available, return basic analysis
        if not self.client:
            return self._fallback_analysis(file_path, reason="client_unavailable")
        
        # Comprehensive analysis prompt
        resume_text_limited = resume_text[:15000]  # Limit to avoid token limits
        analysis_prompt = f"""You are an expert career counselor and resume analyst. Analyze the following resume comprehensively and provide detailed insights.

RESUME TEXT:
{resume_text_limited}

Please provide a comprehensive analysis in JSON format with the following structure:

{{
    "parsed_data": {{
        "personal_info": {{
            "name": "extracted name",
            "email": "extracted email",
            "phone": "extracted phone",
            "location": "extracted location",
            "linkedin": "extracted LinkedIn if available"
        }},
        "professional_summary": "extracted or generated summary",
        "skills": ["list of all skills found"],
        "work_experience": [
            {{
                "company": "company name",
                "title": "job title",
                "duration": "time period",
                "responsibilities": ["list of responsibilities"],
                "achievements": ["key achievements"]
            }}
        ],
        "education": [
            {{
                "degree": "degree name",
                "institution": "institution name",
                "year": "graduation year",
                "field": "field of study"
            }}
        ],
        "certifications": ["list of certifications"],
        "total_experience_years": number,
        "preferred_job_titles": ["inferred job titles"],
        "preferred_industries": ["inferred industries"]
    }},
    "analysis": {{
        "overall_score": number between 0-100,
        "strengths": [
            "strength 1 with explanation",
            "strength 2 with explanation",
            "at least 5-7 strengths"
        ],
        "weaknesses": [
            "weakness 1 with explanation",
            "weakness 2 with explanation",
            "at least 3-5 weaknesses"
        ],
        "suggestions": [
            "specific improvement suggestion 1",
            "specific improvement suggestion 2",
            "at least 8-10 actionable suggestions"
        ],
        "job_recommendations": [
            {{
                "job_title": "recommended job title",
                "match_reason": "why this job fits",
                "required_skills": ["skills needed"],
                "salary_range": "estimated range if possible",
                "growth_potential": "career growth potential"
            }}
        ],
        "skills_gap_analysis": [
            {{
                "missing_skill": "skill name",
                "importance": "high/medium/low",
                "how_to_acquire": "suggestion to learn it",
                "relevance": "why it's important"
            }}
        ],
        "career_path_suggestions": [
            {{
                "path": "career path name",
                "description": "description of the path",
                "next_steps": ["step 1", "step 2"],
                "timeline": "estimated timeline"
            }}
        ],
        "ats_optimization": [
            "ATS tip 1",
            "ATS tip 2",
            "at least 5-7 ATS optimization tips"
        ],
        "keywords_to_add": ["keyword 1", "keyword 2", "relevant keywords"],
        "summary_paragraph": "2-3 paragraph comprehensive summary of the resume analysis"
    }}
}}

IMPORTANT:
- Be specific and actionable in all suggestions
- Provide realistic job recommendations based on experience and skills
- Focus on practical improvements
- Return ONLY valid JSON, no markdown formatting
- Ensure all arrays have meaningful content
"""
        
        # Try multiple Gemini models to avoid quota issues
        try:
            import google.generativeai as genai
            candidate_models = [
                self.model_name,
                'gemini-2.0-flash-lite',
                'gemini-1.5-flash-8b',
                'gemini-1.5-flash'
            ]
            last_error = None
            for model in candidate_models:
                try:
                    model_client = genai.GenerativeModel(model)
                    response = model_client.generate_content(analysis_prompt)
                    result_text = response.text
                    json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                    if json_match:
                        result_json = json.loads(json_match.group())
                    else:
                        result_json = json.loads(result_text)
                    # Attach meta
                    result_json['meta'] = {
                        'provider': 'gemini',
                        'model': model
                    }
                    return result_json
                except Exception as e:
                    last_error = e
                    continue
            # If all Gemini attempts failed, fallback
            return self._fallback_analysis(file_path, reason=str(last_error))
        except Exception as e:
            # Unexpected error path
            return self._fallback_analysis(file_path, reason=str(e))

    def _fallback_analysis(self, file_path: str, reason: str):
        """Generate improved local analysis when Gemini is unavailable."""
        parsed_data = self.simple_parser.parse_resume(file_path)
        # Normalize parsed_data to expected schema
        # Flatten common fields for convenience
        personal = parsed_data.get('Personal Information', {})
        flattened = {
            'name': personal.get('Name', 'N/A'),
            'email': personal.get('Email', 'N/A'),
            'phone': personal.get('Phone', 'N/A'),
            'location': personal.get('Location', 'N/A'),
            'professional_summary': parsed_data.get('Professional Summary', ''),
            'skills': parsed_data.get('Skills', []),
            'education': parsed_data.get('Education', []),
            'work_experience': parsed_data.get('Work Experience', []),
            'total_experience_years': parsed_data.get('Total Years of Experience', 0),
            'raw_text': parsed_data.get('raw_text', '')
        }

        skills = flattened.get('skills', [])
        experience = flattened.get('total_experience_years', 0)
        suggestions = [
            'Highlight key accomplishments with metrics',
            'Emphasize leadership and collaboration',
            'Include relevant certifications',
            'Customize summary to target roles'
        ]
        analysis = {
            'overall_score': min(60 + (len(skills) * 3) + (experience * 2), 80),
            'strengths': ['Clear contact information'] if flattened.get('email') and flattened.get('phone') else [],
            'weaknesses': ['Add measurable achievements' if not flattened.get('professional_summary') else ''],
            'suggestions': suggestions,
            'job_recommendations': [],
            'skills_gap_analysis': [
                {
                    'missing_skill': 'Cloud (AWS/Azure/GCP)',
                    'importance': 'High',
                    'relevance': 'Common requirement across modern roles',
                    'how_to_acquire': 'Take online coursework and build small projects'
                }
            ],
            'career_path_suggestions': [],
            'ats_optimization': [
                'Use standard headings and fonts',
                'Include role-specific keywords',
                'Avoid tables/graphics',
                'Export to PDF after finalizing'
            ],
            'keywords_to_add': ['Project Management', 'Leadership', 'Problem Solving'],
            'summary_paragraph': f'Local analysis was used (Gemini unavailable: {reason}). Your resume shows {experience} years experience and {len(skills)} skills.'
        }
        return {
            'parsed_data': {
                'personal_info': {
                    'name': flattened['name'],
                    'email': flattened['email'],
                    'phone': flattened['phone'],
                    'location': flattened['location']
                },
                'professional_summary': flattened['professional_summary'],
                'skills': skills,
                'education': flattened['education'],
                'work_experience': flattened['work_experience'],
                'total_experience_years': experience
            },
            'analysis': analysis,
            'meta': {
                'provider': 'fallback_simple',
                'reason': reason
            }
        }

