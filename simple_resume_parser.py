"""
Simple Resume Parser - No AI Dependencies
Extracts text from resume files and structures basic information
"""
import re
import PyPDF2
from docx import Document

class SimpleResumeParser:
    """Parse resumes without AI - using text extraction only"""
    
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    
    def parse_resume(self, file_path):
        """Extract text and basic information from resume"""
        # Extract text based on file type
        if file_path.lower().endswith('.pdf'):
            text = self._extract_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            text = self._extract_from_docx(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        
        # Extract basic information
        parsed_data = {
            'Personal Information': {
                'Name': self._extract_name(text),
                'Email': self._extract_email(text),
                'Phone': self._extract_phone(text),
                'Location': 'N/A'
            },
            'Professional Summary': self._extract_summary(text),
            'Skills': self._extract_skills(text),
            'Education': self._extract_education(text),
            'Work Experience': [],
            'Total Years of Experience': self._estimate_experience(text),
            'raw_text': text
        }
        
        return parsed_data
    
    def _extract_from_pdf(self, file_path):
        """Extract text from PDF"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text
    
    def _extract_from_docx(self, file_path):
        """Extract text from DOCX"""
        text = ""
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX: {e}")
        return text
    
    def _extract_email(self, text):
        """Extract email address"""
        match = re.search(self.email_pattern, text)
        return match.group(0) if match else 'N/A'
    
    def _extract_phone(self, text):
        """Extract phone number"""
        match = re.search(self.phone_pattern, text)
        return match.group(0) if match else 'N/A'
    
    def _extract_name(self, text):
        """Extract name (first few words)"""
        lines = text.strip().split('\n')
        for line in lines[:5]:
            line = line.strip()
            if line and len(line.split()) <= 4 and len(line) > 3:
                return line
        return 'N/A'
    
    def _extract_summary(self, text):
        """Extract professional summary"""
        # Look for summary section
        summary_keywords = ['summary', 'profile', 'objective', 'about']
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in summary_keywords):
                # Get next few lines
                summary_lines = []
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip():
                        summary_lines.append(lines[j].strip())
                if summary_lines:
                    return ' '.join(summary_lines)
        
        # If no summary section, return first paragraph
        paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 50]
        return paragraphs[0] if paragraphs else text[:200]
    
    def _extract_skills(self, text):
        """Extract skills"""
        # Common technical skills
        common_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
            'sql', 'mongodb', 'aws', 'azure', 'docker', 'kubernetes', 'git',
            'machine learning', 'data science', 'ai', 'deep learning', 'tensorflow',
            'pytorch', 'flask', 'django', 'spring', 'html', 'css', 'typescript',
            'c++', 'c#', '.net', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return found_skills if found_skills else ['General Skills']
    
    def _extract_education(self, text):
        """Extract education"""
        degrees = ['bachelor', 'master', 'phd', 'mba', 'degree', 'diploma', 'b.tech', 'm.tech', 'bsc', 'msc']
        text_lower = text.lower()
        
        education = []
        for degree in degrees:
            if degree in text_lower:
                education.append(f"{degree.upper()} Degree")
        
        return education if education else ['Education details in resume']
    
    def _estimate_experience(self, text):
        """Estimate years of experience"""
        # Look for patterns like "5 years", "3+ years", etc.
        experience_pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
        matches = re.findall(experience_pattern, text.lower())
        
        if matches:
            years = max([int(m) for m in matches])
            return years
        
        # Count occurrence of year ranges (2018-2020, etc.)
        year_ranges = re.findall(r'(20\d{2})\s*[-–]\s*(20\d{2}|present|current)', text.lower())
        if year_ranges:
            total_years = 0
            for start, end in year_ranges:
                end_year = 2025 if end in ['present', 'current'] else int(end)
                total_years += end_year - int(start)
            return total_years
        
        return 0
