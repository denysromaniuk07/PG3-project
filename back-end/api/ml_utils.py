import re
import PyPDF2
from docx import Document

# Common technical skills database
SKILLS_DATABASE = {
    # Programming Languages
    'python': 'Backend',
    'javascript': 'Frontend/Backend',
    'typescript': 'Frontend/Backend',
    'java': 'Backend',
    'csharp': 'Backend',
    'cpp': 'Backend',
    'go': 'Backend',
    'rust': 'Backend',
    'ruby': 'Backend',
    'php': 'Backend',
    
    # Frontend
    'react': 'Frontend',
    'vue': 'Frontend',
    'angular': 'Frontend',
    'html': 'Frontend',
    'css': 'Frontend',
    'tailwind': 'Frontend',
    'bootstrap': 'Frontend',
    'webpack': 'Frontend',
    
    # Backend Frameworks
    'django': 'Backend',
    'flask': 'Backend',
    'fastapi': 'Backend',
    'express': 'Backend',
    'spring': 'Backend',
    'rails': 'Backend',
    'laravel': 'Backend',
    'nest': 'Backend',
    
    # Databases
    'sql': 'Backend',
    'postgresql': 'Backend',
    'mysql': 'Backend',
    'mongodb': 'Backend',
    'redis': 'Backend',
    'firebase': 'Backend',
    'elasticsearch': 'Backend',
    
    # DevOps
    'docker': 'DevOps',
    'kubernetes': 'DevOps',
    'aws': 'DevOps',
    'gcp': 'DevOps',
    'azure': 'DevOps',
    'terraform': 'DevOps',
    'jenkins': 'DevOps',
    'git': 'DevOps',
    'linux': 'DevOps',
    
    # Data Science
    'machine learning': 'Data Science',
    'tensorflow': 'Data Science',
    'pytorch': 'Data Science',
    'pandas': 'Data Science',
    'numpy': 'Data Science',
    'sklearn': 'Data Science',
    'scikit-learn': 'Data Science',
    'keras': 'Data Science',
    
    # Mobile
    'react native': 'Mobile',
    'flutter': 'Mobile',
    'swift': 'Mobile',
    'kotlin': 'Mobile',
    'ios': 'Mobile',
    'android': 'Mobile',
    
    # Soft Skills
    'communication': 'Soft Skills',
    'teamwork': 'Soft Skills',
    'leadership': 'Soft Skills',
    'project management': 'Soft Skills',
    'problem solving': 'Soft Skills',
}

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        file.seek(0)
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract PDF: {str(e)}")

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        file.seek(0)
        doc = Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract DOCX: {str(e)}")

def extract_text_from_file(file):
    """Extract text from various file types"""
    filename = file.name.lower()
    
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif filename.endswith('.docx'):
        return extract_text_from_docx(file)
    elif filename.endswith('.doc'):
        return extract_text_from_docx(file)
    elif filename.endswith('.txt'):
        file.seek(0)
        return file.read().decode('utf-8')
    else:
        raise ValueError("Unsupported file type")

def extract_skills(text):
    """Extract skills from resume text using pattern matching"""
    text_lower = text.lower()
    found_skills = {}
    
    for skill, category in SKILLS_DATABASE.items():
        if skill in text_lower:
            if skill not in found_skills:
                found_skills[skill] = {
                    'name': skill.title(),
                    'category': category,
                    'confidence': 85
                }
    
    return found_skills

def identify_skill_gaps(found_skills):
    """Identify skill gaps based on found skills"""
    gaps = []
    
    # Define recommended skills by category
    recommendations = {
        'Frontend': ['TypeScript', 'React', 'Vue.js', 'Tailwind CSS'],
        'Backend': ['Node.js', 'PostgreSQL', 'Redis', 'API Design'],
        'DevOps': ['Docker', 'Kubernetes', 'AWS', 'CI/CD'],
        'Data Science': ['Machine Learning', 'TensorFlow', 'Data Visualization'],
        'Mobile': ['React Native', 'Flutter', 'Mobile Performance'],
    }
    
    found_skill_names = [s['name'].lower() for s in found_skills.values()]
    
    for category, skills in recommendations.items():
        for skill in skills:
            if skill.lower() not in found_skill_names:
                gaps.append({
                    'name': skill,
                    'demand': 'High',
                    'priority': 'Critical' if category in ['Backend', 'DevOps'] else 'Important'
                })
    
    return gaps[:5]

def extract_experience_level(text):
    """Estimate experience level from resume"""
    text_lower = text.lower()
    
    years_match = re.findall(r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)', text_lower)
    if years_match:
        years = int(years_match[0])
        if years >= 10:
            return 'Senior'
        elif years >= 5:
            return 'Mid-level'
        else:
            return 'Junior'
    
    return 'Entry-level'

def analyze_resume(file):
    """Complete resume analysis"""
    try:
        text = extract_text_from_file(file)
        skills = extract_skills(text)
        gaps = identify_skill_gaps(skills)
        experience_level = extract_experience_level(text)
        skill_score = min(100, len(skills) * 10)
        
        return {
            'extracted_text': text[:1000],
            'skills': list(skills.values()),
            'skill_gaps': gaps,
            'experience_level': experience_level,
            'skill_score': skill_score,
            'total_score': (skill_score * 0.6) + (len(gaps) * 5),
        }
    except Exception as e:
        raise ValueError(f"Resume analysis failed: {str(e)}")
