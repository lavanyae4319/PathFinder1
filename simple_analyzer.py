"""
Simple Resume Analyzer - Provides basic resume analysis without AI
"""

def analyze_resume_simple(parsed_data):
    """
    Analyze resume and provide feedback without using AI
    Returns analysis dict with scores, strengths, weaknesses, and suggestions
    """
    analysis = {
        'overall_score': 0,
        'strengths': [],
        'weaknesses': [],
        'suggestions': [],
        'job_recommendations': [],
        'skills_gap_analysis': [],
        'career_path_suggestions': [],
        'ats_optimization': [],
        'keywords_to_add': [],
        'summary_paragraph': ''
    }
    
    # Extract data
    skills = parsed_data.get('Skills', parsed_data.get('skills', []))
    experience = parsed_data.get('Work Experience', parsed_data.get('work_experience', parsed_data.get('experience', [])))
    education = parsed_data.get('Education', parsed_data.get('education', []))
    summary = parsed_data.get('Professional Summary', parsed_data.get('professional_summary', parsed_data.get('summary', '')))
    experience_years = parsed_data.get('Total Years of Experience', parsed_data.get('total_experience_years', parsed_data.get('experience_years', 0)))
    
    # Convert experience_years to float
    if isinstance(experience_years, str):
        import re
        numbers = re.findall(r'\d+\.?\d*', str(experience_years))
        experience_years = float(numbers[0]) if numbers else 0
    else:
        experience_years = float(experience_years) if experience_years else 0
    
    score = 0
    max_score = 100
    
    # 1. Skills Analysis (30 points)
    if isinstance(skills, list):
        num_skills = len(skills)
    else:
        num_skills = len(str(skills).split(',')) if skills else 0
    
    if num_skills >= 10:
        score += 30
        analysis['strengths'].append(f"Strong skill set with {num_skills} skills listed")
    elif num_skills >= 5:
        score += 20
        analysis['strengths'].append(f"Good skill diversity with {num_skills} skills")
        analysis['suggestions'].append("Consider adding more technical skills to strengthen your profile")
    else:
        score += 10
        analysis['weaknesses'].append(f"Limited skills listed ({num_skills} skills)")
        analysis['suggestions'].append("Add more relevant technical and soft skills to your resume")
        analysis['keywords_to_add'].extend(['Communication', 'Problem Solving', 'Teamwork', 'Leadership'])
    
    # 2. Experience Analysis (25 points)
    if isinstance(experience, list):
        num_experiences = len(experience)
    else:
        num_experiences = 1 if experience else 0
    
    if experience_years >= 5:
        score += 25
        analysis['strengths'].append(f"Extensive professional experience ({experience_years} years)")
    elif experience_years >= 2:
        score += 20
        analysis['strengths'].append(f"Solid work experience ({experience_years} years)")
    elif experience_years >= 1:
        score += 15
        analysis['suggestions'].append("Build more professional experience to strengthen your profile")
    else:
        score += 5
        analysis['weaknesses'].append("Limited professional experience")
        analysis['suggestions'].append("Consider internships or entry-level positions to gain experience")
    
    if num_experiences >= 3:
        score += 5
        analysis['strengths'].append(f"Diverse work history with {num_experiences} positions")
    elif num_experiences == 0:
        analysis['weaknesses'].append("No work experience listed")
    
    # 3. Education Analysis (20 points)
    if isinstance(education, list):
        num_education = len(education)
    else:
        num_education = 1 if education else 0
    
    if num_education >= 1:
        score += 20
        analysis['strengths'].append("Educational background documented")
    else:
        score += 5
        analysis['weaknesses'].append("No education information provided")
        analysis['suggestions'].append("Add your educational qualifications")
    
    # 4. Professional Summary (15 points)
    if summary and len(str(summary)) > 50:
        score += 15
        analysis['strengths'].append("Well-written professional summary")
    elif summary and len(str(summary)) > 20:
        score += 10
        analysis['suggestions'].append("Expand your professional summary to highlight key achievements")
    else:
        score += 0
        analysis['weaknesses'].append("Missing or weak professional summary")
        analysis['suggestions'].append("Add a compelling professional summary (3-5 sentences) highlighting your key strengths")
    
    # 5. ATS Optimization (10 points)
    ats_score = 0
    if skills and len(skills) > 0:
        ats_score += 5
        analysis['ats_optimization'].append("✓ Skills section present - helps with keyword matching")
    else:
        analysis['ats_optimization'].append("✗ Add a dedicated skills section with relevant keywords")
    
    if summary:
        ats_score += 5
        analysis['ats_optimization'].append("✓ Professional summary included")
    else:
        analysis['ats_optimization'].append("✗ Add a professional summary at the top of your resume")
    
    score += ats_score
    
    # Additional ATS tips
    analysis['ats_optimization'].extend([
        "Use standard section headings (Experience, Education, Skills)",
        "Include relevant keywords from job descriptions",
        "Avoid images, tables, and complex formatting",
        "Use a simple, clean font (Arial, Calibri, Times New Roman)",
        "Save as PDF or DOCX format"
    ])
    
    # Calculate final score
    analysis['overall_score'] = min(score, max_score)
    
    # Generate summary paragraph
    if analysis['overall_score'] >= 80:
        rating = "excellent"
        action = "Your resume is well-structured and comprehensive."
    elif analysis['overall_score'] >= 60:
        rating = "good"
        action = "Your resume has a solid foundation but could benefit from some improvements."
    elif analysis['overall_score'] >= 40:
        rating = "fair"
        action = "Your resume needs significant improvements to stand out."
    else:
        rating = "needs improvement"
        action = "Consider restructuring your resume with more details."
    
    analysis['summary_paragraph'] = f"Your resume scores {analysis['overall_score']}/100, which is {rating}. {action}"
    
    # Skills gap analysis based on experience level
    if experience_years < 2:
        analysis['skills_gap_analysis'] = [
            {
                'missing_skill': 'Industry-specific tools',
                'importance': 'High',
                'relevance': 'Essential for entry-level positions in your field',
                'how_to_acquire': 'Take online courses on platforms like Coursera, Udemy, or LinkedIn Learning'
            },
            {
                'missing_skill': 'Soft skills (Communication, Teamwork)',
                'importance': 'High',
                'relevance': 'Critical for workplace success and collaboration',
                'how_to_acquire': 'Participate in group projects, volunteer work, or join professional organizations'
            }
        ]
    else:
        analysis['skills_gap_analysis'] = [
            {
                'missing_skill': 'Leadership and Management',
                'importance': 'Medium',
                'relevance': 'Important for career advancement',
                'how_to_acquire': 'Take leadership courses or seek mentorship opportunities'
            },
            {
                'missing_skill': 'Advanced technical certifications',
                'importance': 'Medium',
                'relevance': 'Demonstrates expertise and commitment to professional development',
                'how_to_acquire': 'Pursue industry-recognized certifications relevant to your field'
            }
        ]
    
    # Career path suggestions
    if experience_years < 2:
        analysis['career_path_suggestions'] = [
            {
                'path': 'Junior to Mid-Level Professional',
                'description': 'Focus on building foundational skills and gaining diverse experience',
                'timeline': '2-3 years',
                'next_steps': [
                    'Seek mentorship from senior professionals',
                    'Take on challenging projects to build your portfolio',
                    'Develop both technical and soft skills',
                    'Network within your industry'
                ]
            }
        ]
    elif experience_years < 5:
        analysis['career_path_suggestions'] = [
            {
                'path': 'Mid-Level to Senior Professional',
                'description': 'Transition into leadership roles and specialized expertise',
                'timeline': '3-5 years',
                'next_steps': [
                    'Lead projects or small teams',
                    'Develop expertise in a specific domain',
                    'Pursue advanced certifications',
                    'Build your professional network and personal brand'
                ]
            }
        ]
    else:
        analysis['career_path_suggestions'] = [
            {
                'path': 'Senior Professional to Leadership',
                'description': 'Move into management, consulting, or executive roles',
                'timeline': '3-7 years',
                'next_steps': [
                    'Develop strategic thinking and business acumen',
                    'Mentor junior team members',
                    'Build cross-functional expertise',
                    'Consider MBA or executive education programs'
                ]
            }
        ]
    
    # Add general improvement suggestions
    if not analysis['suggestions']:
        analysis['suggestions'].append("Your resume is well-structured. Keep it updated with new skills and achievements.")
    
    # Add keywords to improve ATS matching
    if len(analysis['keywords_to_add']) < 5:
        common_keywords = [
            'Project Management', 'Data Analysis', 'Problem Solving',
            'Team Collaboration', 'Strategic Planning', 'Process Improvement',
            'Client Relations', 'Technical Documentation'
        ]
        analysis['keywords_to_add'].extend(common_keywords[:5 - len(analysis['keywords_to_add'])])
    
    return analysis
