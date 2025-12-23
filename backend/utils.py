"""
Utility Functions
Common utilities for the resume analysis system.
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime


def load_skill_database() -> Dict[str, List[str]]:
    """Load skill categories database."""
    return {
        'programming_languages': [
            'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Go', 'Rust',
            'TypeScript', 'PHP', 'Ruby', 'Swift', 'Kotlin', 'R', 'SQL'
        ],
        'web_frameworks': [
            'React', 'Vue', 'Angular', 'Django', 'Flask', 'FastAPI',
            'Express', 'Spring', 'ASP.NET', 'Rails', 'Next.js', 'Nuxt'
        ],
        'databases': [
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch',
            'DynamoDB', 'Cassandra', 'Firebase', 'Oracle', 'SQL Server'
        ],
        'cloud_platforms': [
            'AWS', 'Azure', 'Google Cloud', 'Heroku', 'Vercel',
            'DigitalOcean', 'Linode', 'AWS Lambda', 'CloudRun'
        ],
        'devops_tools': [
            'Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'GitHub Actions',
            'Terraform', 'Ansible', 'CloudFormation', 'Prometheus', 'Grafana'
        ],
        'data_science': [
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy',
            'Matplotlib', 'Seaborn', 'XGBoost', 'Keras', 'NLTK'
        ],
        'soft_skills': [
            'Communication', 'Leadership', 'Problem-solving', 'Teamwork',
            'Time management', 'Attention to detail', 'Adaptability',
            'Critical thinking', 'Creativity', 'Project management'
        ]
    }


def categorize_skill(skill_name: str) -> str:
    """
    Categorize a skill into a category.
    
    Returns:
        One of: 'programming_languages', 'web_frameworks', 'databases',
                'cloud_platforms', 'devops_tools', 'data_science', 'soft_skills', 'other'
    """
    skill_lower = skill_name.lower()
    skills_db = load_skill_database()
    
    for category, skills_list in skills_db.items():
        if any(skill.lower() == skill_lower for skill in skills_list):
            return category
    
    return 'other'


def calculate_experience_years(duration: str) -> Optional[int]:
    """
    Estimate years of experience from duration string.
    
    Args:
        duration: String like "2022-Present", "Jan 2020 - Dec 2023", etc.
    
    Returns:
        Approximate years or None
    """
    try:
        current_year = datetime.now().year
        
        # Extract years from string
        import re
        years = re.findall(r'\b(19|20)\d{2}\b', duration)
        
        if len(years) >= 1:
            start_year = int(years[0])
            if 'present' in duration.lower():
                end_year = current_year
            elif len(years) >= 2:
                end_year = int(years[1])
            else:
                end_year = current_year
            
            return max(0, end_year - start_year)
    except:
        pass
    
    return None


def estimate_seniority_level(experience_years: Optional[int], job_title: str) -> str:
    """
    Estimate seniority level based on experience and title.
    
    Returns:
        One of: 'entry-level', 'mid-level', 'senior', 'lead'
    """
    if experience_years is None:
        experience_years = 0
    
    job_title_lower = job_title.lower()
    
    # Check title indicators
    if any(word in job_title_lower for word in ['lead', 'principal', 'architect', 'director', 'vp']):
        return 'lead'
    elif any(word in job_title_lower for word in ['senior', 'sr', 'staff']):
        return 'senior'
    elif any(word in job_title_lower for word in ['junior', 'jr', 'associate', 'intern']):
        return 'entry-level'
    
    # Check experience years
    if experience_years >= 5:
        return 'senior'
    elif experience_years >= 2:
        return 'mid-level'
    else:
        return 'entry-level'


def format_ats_score_display(score: int) -> tuple:
    """
    Format ATS score for display with emoji and color-coding.
    
    Returns:
        (emoji, color, assessment)
    """
    if score >= 80:
        return '🟢', 'green', 'Excellent'
    elif score >= 60:
        return '🟡', 'orange', 'Good'
    elif score >= 40:
        return '🟠', 'orange', 'Fair'
    else:
        return '🔴', 'red', 'Needs Improvement'


def format_match_percentage(percentage: int) -> tuple:
    """Format match percentage with emoji and assessment."""
    if percentage >= 80:
        return '🟢', 'Perfect Match'
    elif percentage >= 60:
        return '🟡', 'Good Match'
    elif percentage >= 40:
        return '🟠', 'Partial Match'
    else:
        return '🔴', 'Poor Match'


def resume_dict_to_text(resume_dict: Dict[str, Any]) -> str:
    """Convert resume dictionary to readable text format."""
    lines = []
    
    # Header
    if resume_dict.get('name'):
        lines.append(f"\n{'=' * 60}")
        lines.append(f"{resume_dict['name'].upper()}")
        lines.append(f"{'=' * 60}\n")
    
    # Contact
    contact = []
    if resume_dict.get('email'):
        contact.append(f"📧 {resume_dict['email']}")
    if resume_dict.get('phone'):
        contact.append(f"📱 {resume_dict['phone']}")
    if contact:
        lines.append(" | ".join(contact) + "\n")
    
    # Summary
    if resume_dict.get('summary'):
        lines.append("PROFESSIONAL SUMMARY")
        lines.append("-" * 40)
        lines.append(f"{resume_dict['summary']}\n")
    
    # Experience
    if resume_dict.get('experience'):
        lines.append("PROFESSIONAL EXPERIENCE")
        lines.append("-" * 40)
        for exp in resume_dict['experience']:
            if isinstance(exp, dict):
                title = exp.get('title', 'Unknown')
                company = exp.get('company', 'Unknown')
                duration = exp.get('duration', '')
                desc = exp.get('description', '')
                
                lines.append(f"{title} | {company}")
                if duration:
                    lines.append(f"{duration}")
                if desc:
                    lines.append(f"{desc}")
                lines.append("")
    
    # Education
    if resume_dict.get('education'):
        lines.append("\nEDUCATION")
        lines.append("-" * 40)
        for edu in resume_dict['education']:
            if isinstance(edu, dict):
                degree = edu.get('degree', '')
                institution = edu.get('institution', '')
                year = edu.get('graduation_year', '')
                gpa = edu.get('gpa', '')
                
                edu_line = f"{degree} | {institution}"
                if year:
                    edu_line += f" ({year})"
                if gpa:
                    edu_line += f" - GPA: {gpa}"
                lines.append(edu_line)
        lines.append("")
    
    # Skills
    if resume_dict.get('skills'):
        lines.append("\nSKILLS")
        lines.append("-" * 40)
        skills = resume_dict['skills']
        if isinstance(skills, list) and skills:
            if isinstance(skills[0], dict):
                for skill in skills:
                    category = skill.get('category', 'General')
                    name = skill.get('name', skill)
                    lines.append(f"• {name} ({category})")
            else:
                lines.append(", ".join(str(s) for s in skills))
        lines.append("")
    
    # Certifications
    if resume_dict.get('certifications'):
        lines.append("\nCERTIFICATIONS")
        lines.append("-" * 40)
        for cert in resume_dict['certifications']:
            lines.append(f"✓ {cert}")
        lines.append("")
    
    # Projects
    if resume_dict.get('projects'):
        lines.append("\nPROJECTS")
        lines.append("-" * 40)
        for project in resume_dict['projects']:
            lines.append(f"• {project}")
        lines.append("")
    
    return "\n".join(lines)


def create_comparison_table(results: List[Dict[str, Any]]) -> str:
    """Create a formatted comparison table of multiple resumes."""
    if not results:
        return "No results to compare"
    
    # Simple text-based table
    lines = []
    lines.append("\n" + "=" * 100)
    lines.append(f"{'Name':<25} {'Score':<10} {'Skills Match':<15} {'Fit':<20}")
    lines.append("=" * 100)
    
    for result in results:
        name = result.get('name', 'Unknown')[:25]
        score = str(result.get('match_score', 0))
        skills = str(result.get('skill_match', 0)) + "%"
        fit = result.get('summary', 'N/A')[:20]
        
        lines.append(f"{name:<25} {score:<10} {skills:<15} {fit:<20}")
    
    lines.append("=" * 100)
    
    return "\n".join(lines)


def validate_resume_data(resume_dict: Dict[str, Any]) -> tuple:
    """
    Validate resume data completeness.
    
    Returns:
        (is_valid, missing_fields, score)
    """
    required_fields = {
        'name': False,
        'email': False,
        'phone': False,
        'experience': False,
        'education': False,
        'skills': False
    }
    
    completeness_score = 0
    
    for field in required_fields:
        if resume_dict.get(field):
            data = resume_dict[field]
            if isinstance(data, (list, str)):
                if data:
                    required_fields[field] = True
                    completeness_score += 15
    
    missing = [field for field, present in required_fields.items() if not present]
    is_valid = len(missing) <= 2  # Allow up to 2 missing fields
    
    return is_valid, missing, completeness_score


def get_improvement_priority(
    ats_score: int,
    section_completeness: int,
    keyword_match: int
) -> List[str]:
    """Get prioritized list of improvements."""
    priorities = []
    
    if ats_score < 50:
        priorities.append("1️⃣ Critical: Improve overall ATS compatibility")
    
    if section_completeness < 60:
        priorities.append("2️⃣ High: Complete missing resume sections")
    
    if keyword_match < 50:
        priorities.append("3️⃣ High: Add missing job-relevant keywords")
    
    if ats_score >= 70:
        priorities.append("4️⃣ Medium: Quantify achievements with metrics")
        priorities.append("5️⃣ Medium: Use stronger action verbs")
    
    if not priorities:
        priorities.append("✅ Your resume is in good shape! Minor refinements can help.")
    
    return priorities


def estimate_application_success(ats_score: int, match_percentage: int) -> str:
    """Estimate likelihood of success."""
    combined_score = (ats_score * 0.6) + (match_percentage * 0.4)
    
    if combined_score >= 80:
        return "🎯 Very High - Your profile is a great match for this role!"
    elif combined_score >= 60:
        return "👍 Moderate - You have most of the required skills. Worth applying!"
    elif combined_score >= 40:
        return "⚠️ Low - Consider developing some key skills before applying."
    else:
        return "❌ Very Low - This role may require different expertise. Consider alternatives."
