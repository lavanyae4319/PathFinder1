"""
Resume Parser using AI API (OpenAI/Gemini/Claude)
Extracts structured information from resume text
"""

import os
import json
import re
from typing import Dict, List, Optional

import PyPDF2
import docx

from config import (
    AI_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL,
    RESUME_PARSING_PROMPT,
)
from simple_resume_parser import SimpleResumeParser


class ResumeParser:
    """Parse resumes using AI APIs"""
    
    def __init__(self, provider: str = None):
        """
        Initialize the resume parser.

        If the configured AI provider/API key is not available or invalid,
        this class will automatically fall back to using SimpleResumeParser
        so that the system can still work purely with the locally trained
        ML model and without any external API keys.
        """
        self.provider = provider or AI_PROVIDER
        self.simple_parser = SimpleResumeParser()
        self.ai_enabled = False

        # Try to initialize the AI client, but don't fail the whole system
        # if API keys are missing or invalid – we'll just use SimpleResumeParser.
        try:
            self._initialize_client()
            self.ai_enabled = True
        except Exception as e:
            print(
                f"⚠ AI resume parsing is disabled ({e}). "
                f"Falling back to SimpleResumeParser (no API key required)."
            )
            self.ai_enabled = False
    
    def _initialize_client(self):
        """Initialize the AI client based on provider"""
        if self.provider == 'openai':
            # If the API key is still the placeholder, don't even try to use OpenAI
            if not OPENAI_API_KEY or 'your-openai-api-key-here' in OPENAI_API_KEY:
                raise RuntimeError(
                    "OpenAI API key is not configured. "
                    "Set OPENAI_API_KEY in .env to enable AI parsing."
                )
            try:
                import openai
                self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
                self.model = OPENAI_MODEL
                print(f"✓ Initialized OpenAI client with model: {self.model}")
            except ImportError:
                raise ImportError("Please install openai: pip install openai")
        
        elif self.provider == 'gemini':
            try:
                import google.generativeai as genai
                genai.configure(api_key=GEMINI_API_KEY)
                self.client = genai.GenerativeModel(GEMINI_MODEL)
                self.model = GEMINI_MODEL
                print(f"✓ Initialized Gemini client with model: {self.model}")
            except ImportError:
                raise ImportError("Please install google-generativeai: pip install google-generativeai")
        
        elif self.provider == 'anthropic':
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                self.model = ANTHROPIC_MODEL
                print(f"✓ Initialized Anthropic client with model: {self.model}")
            except ImportError:
                raise ImportError("Please install anthropic: pip install anthropic")
        
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(docx_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from resume file (PDF, DOCX, or TXT)"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return self.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def parse_with_openai(self, resume_text: str) -> Dict:
        """Parse resume using OpenAI API"""
        try:
            prompt = RESUME_PARSING_PROMPT.format(resume_text=resume_text)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert resume parser. Extract information in valid JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
        
        except Exception as e:
            raise Exception(f"OpenAI parsing error: {str(e)}")
    
    def parse_with_gemini(self, resume_text: str) -> Dict:
        """Parse resume using Google Gemini API"""
        try:
            prompt = RESUME_PARSING_PROMPT.format(resume_text=resume_text)
            
            response = self.client.generate_content(prompt)
            result_text = response.text
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return json.loads(result_text)
        
        except Exception as e:
            raise Exception(f"Gemini parsing error: {str(e)}")
    
    def parse_with_anthropic(self, resume_text: str) -> Dict:
        """Parse resume using Anthropic Claude API"""
        try:
            prompt = RESUME_PARSING_PROMPT.format(resume_text=resume_text)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result_text = response.content[0].text
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return json.loads(result_text)
        
        except Exception as e:
            raise Exception(f"Anthropic parsing error: {str(e)}")
    
    def parse_resume(self, file_path: str) -> Dict:
        """
        Main method to parse resume.

        Preference order:
        1. Use the configured AI provider if available.
        2. If AI is not available or fails (e.g. invalid API key),
           fall back to SimpleResumeParser (no external API calls).
        
        Args:
            file_path: Path to resume file (PDF, DOCX, or TXT)
            
        Returns:
            Dictionary containing parsed resume information
        """
        print(f"📄 Extracting text from resume: {os.path.basename(file_path)}")
        resume_text = self.extract_text_from_file(file_path)
        
        if len(resume_text) < 100:
            raise ValueError("Resume text is too short. Please provide a valid resume.")
        
        print(f"✓ Extracted {len(resume_text)} characters")

        # Try AI parsing first (if enabled); otherwise immediately fall back
        if self.ai_enabled:
            print(f"🤖 Parsing resume using {self.provider.upper()} AI...")
            try:
                if self.provider == 'openai':
                    parsed_data = self.parse_with_openai(resume_text)
                elif self.provider == 'gemini':
                    parsed_data = self.parse_with_gemini(resume_text)
                elif self.provider == 'anthropic':
                    parsed_data = self.parse_with_anthropic(resume_text)
                else:
                    raise ValueError(f"Unsupported provider: {self.provider}")

                # Add raw text for reference
                parsed_data['raw_text'] = resume_text[:500]  # First 500 chars
                parsed_data['parsing_provider'] = self.provider

                print("✓ Resume parsed successfully with AI!")
                return parsed_data

            except Exception as e:
                # If anything goes wrong with AI (e.g. 401 invalid API key),
                # log it and transparently fall back to SimpleResumeParser.
                print(
                    f"⚠ AI parsing failed ({e}). "
                    f"Falling back to SimpleResumeParser (no API key)."
                )

        # Fallback path: simple, local parsing only (no external APIs)
        print("🔍 Using SimpleResumeParser for local resume parsing...")
        parsed_data = self.simple_parser.parse_resume(file_path)
        parsed_data['parsing_provider'] = 'simple'
        return parsed_data
    
    def extract_key_info_for_matching(self, parsed_resume: Dict) -> Dict:
        """
        Extract key information needed for job matching
        
        Args:
            parsed_resume: Parsed resume dictionary
            
        Returns:
            Dictionary with key matching information
        """
        matching_info = {
            'skills': [],
            'experience_years': 0,
            'education_level': '',
            'job_titles': [],
            'industries': [],
            'summary': ''
        }
        
        # Extract skills
        if 'Skills' in parsed_resume:
            if isinstance(parsed_resume['Skills'], list):
                matching_info['skills'] = parsed_resume['Skills']
            elif isinstance(parsed_resume['Skills'], dict):
                # Flatten skills if nested
                for skill_category in parsed_resume['Skills'].values():
                    if isinstance(skill_category, list):
                        matching_info['skills'].extend(skill_category)
        
        # Extract experience years
        if 'Total Years of Experience' in parsed_resume:
            try:
                exp = parsed_resume['Total Years of Experience']
                if isinstance(exp, (int, float)):
                    matching_info['experience_years'] = float(exp)
                elif isinstance(exp, str):
                    # Extract number from string
                    numbers = re.findall(r'\d+\.?\d*', exp)
                    if numbers:
                        matching_info['experience_years'] = float(numbers[0])
            except:
                matching_info['experience_years'] = 0
        
        # Extract education
        if 'Education' in parsed_resume and parsed_resume['Education']:
            if isinstance(parsed_resume['Education'], list) and len(parsed_resume['Education']) > 0:
                # Get highest education
                matching_info['education_level'] = parsed_resume['Education'][0].get('Degree', '')
        
        # Extract preferred job titles
        if 'Preferred Job Titles' in parsed_resume:
            matching_info['job_titles'] = parsed_resume['Preferred Job Titles']
        
        # Extract industries
        if 'Preferred Industries' in parsed_resume:
            matching_info['industries'] = parsed_resume['Preferred Industries']
        
        # Extract summary
        if 'Professional Summary' in parsed_resume:
            matching_info['summary'] = parsed_resume['Professional Summary']
        
        return matching_info


def main():
    """Example usage"""
    # Initialize parser
    parser = ResumeParser(provider='openai')  # or 'gemini' or 'anthropic'
    
    # Example resume file path
    resume_path = "uploads/resumes/sample_resume.pdf"
    
    if os.path.exists(resume_path):
        try:
            # Parse resume
            parsed_data = parser.parse_resume(resume_path)
            
            # Display results
            print("\n" + "="*70)
            print("PARSED RESUME DATA")
            print("="*70)
            print(json.dumps(parsed_data, indent=2))
            
            # Extract matching info
            matching_info = parser.extract_key_info_for_matching(parsed_data)
            print("\n" + "="*70)
            print("KEY MATCHING INFORMATION")
            print("="*70)
            print(json.dumps(matching_info, indent=2))
            
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print(f"Resume file not found: {resume_path}")
        print("Please place a resume file in the uploads/resumes/ folder")


if __name__ == "__main__":
    main()
