"""
Job Matcher Module
Matches resume against job descriptions and identifies alignment.
"""

import streamlit as st
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional
from difflib import SequenceMatcher


class JobMatchResult(BaseModel):
    """Job matching result."""
    match_percentage: int = Field(description="Overall match percentage (0-100)")
    job_title_match: str = Field(description="Assessment of job title fit")
    matching_skills: List[str] = Field(description="Skills that match the job")
    missing_skills: List[str] = Field(description="Skills required but missing")
    matching_experience: List[str] = Field(description="Relevant experience areas")
    growth_areas: List[str] = Field(description="Areas to develop for this role")
    suitability_assessment: str = Field(description="Overall fit assessment")
    career_alignment: str = Field(description="How this role aligns with career path")


class SampleJob(BaseModel):
    """Sample job description template."""
    title: str
    company: str
    description: str
    required_skills: List[str]


def get_gemini_model():
    """Configure Gemini model to return JSON output."""
    generation_config = genai.GenerationConfig(
        response_mime_type="application/json",
        temperature=0.7
    )
    return genai.GenerativeModel(
        model_name="models/gemini-2.5-flash",
        generation_config=generation_config
    )


# Sample job descriptions for demonstration
SAMPLE_JOBS = [
    SampleJob(
        title="Software Engineer",
        company="Tech Startup",
        description="""
        We are looking for a Software Engineer to develop scalable web applications.
        - Design and implement backend services using Python/Node.js
        - Build RESTful APIs and microservices
        - Work with databases (SQL/NoSQL)
        - Collaborate with frontend team
        - Optimize application performance
        - Write unit and integration tests
        - Participate in code reviews
        Requirements:
        - 2+ years of software development experience
        - Strong programming skills in Python, Java, or JavaScript
        - Understanding of databases and SQL
        - Experience with Git and CI/CD pipelines
        - Good problem-solving skills
        """,
        required_skills=['Python', 'JavaScript', 'REST API', 'Database', 'Git', 'CI/CD']
    ),
    SampleJob(
        title="Data Scientist",
        company="Analytics Firm",
        description="""
        We need a Data Scientist to build predictive models and extract insights from data.
        - Develop machine learning models
        - Perform data analysis and statistical testing
        - Create data visualizations
        - Deploy models to production
        - Collaborate with stakeholders
        Requirements:
        - 2+ years in data science or analytics
        - Proficiency in Python/R
        - Experience with pandas, scikit-learn, TensorFlow
        - SQL and database knowledge
        - Strong statistics and math background
        - Data visualization skills
        """,
        required_skills=['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Visualization', 'TensorFlow']
    ),
    SampleJob(
        title="Frontend Developer",
        company="Web Agency",
        description="""
        Join us as a Frontend Developer to build beautiful and responsive web interfaces.
        - Develop responsive web applications
        - Work with React/Vue/Angular
        - Implement modern UI/UX designs
        - Optimize frontend performance
        - Test code across browsers
        - Collaborate with designers and backend teams
        Requirements:
        - 2+ years of frontend development experience
        - Strong HTML, CSS, JavaScript knowledge
        - Experience with modern frameworks (React/Vue/Angular)
        - Understanding of responsive design
        - Git and version control
        - Problem-solving skills
        """,
        required_skills=['React', 'JavaScript', 'HTML/CSS', 'Responsive Design', 'Git', 'Web Performance']
    )
]


@st.cache_data(show_spinner="🎯 Analyzing job match...")
def match_resume_with_job(
    resume_dict: dict,
    job_description: str
) -> JobMatchResult:
    """
    Match resume with job description using AI analysis.
    
    Args:
        resume_dict: Parsed resume dictionary
        job_description: Job description text
    
    Returns:
        JobMatchResult object
    """
    try:
        # Format resume for analysis
        resume_text = format_resume_for_job_match(resume_dict)
        
        prompt = f"""You are a career advisor and job matching expert. Analyze how well this resume matches the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide:
1. Overall match percentage (0-100)
2. Assessment of job title fit
3. Skills that match the job
4. Missing required skills
5. Relevant experience areas
6. Growth areas to develop
7. Overall suitability assessment
8. Career alignment assessment

Be realistic and constructive in your analysis."""

        # Enforce clean JSON output to avoid markdown wrappers
        prompt += "\n\nReturn only valid JSON with keys: match_percentage (0-100 int), job_title_match (string), matching_skills (list of strings), missing_skills (list of strings), matching_experience (list of strings), growth_areas (list of strings), suitability_assessment (string), career_alignment (string). No extra commentary or markdown."

        model = get_gemini_model()
        response = model.generate_content(prompt)

        result = JobMatchResult.model_validate_json(response.text)
        return result
        
    except Exception as e:
        st.error(f"Error analyzing job match: {str(e)}")
        return None


def format_resume_for_job_match(resume_dict: dict) -> str:
    """Format resume for job matching analysis."""
    text_parts = []
    
    if resume_dict.get('name'):
        text_parts.append(f"Name: {resume_dict['name']}")
    
    if resume_dict.get('summary'):
        text_parts.append(f"\nProfessional Summary:\n{resume_dict['summary']}")
    
    if resume_dict.get('experience'):
        text_parts.append("\nProfessional Experience:")
        for exp in resume_dict['experience']:
            if isinstance(exp, dict):
                text_parts.append(
                    f"- {exp.get('title', 'Unknown')} at {exp.get('company', 'Unknown')} "
                    f"({exp.get('duration', 'Unknown')})"
                )
                if exp.get('description'):
                    text_parts.append(f"  {exp['description']}")
    
    if resume_dict.get('skills'):
        text_parts.append("\nTechnical Skills:")
        skills = resume_dict['skills']
        if isinstance(skills, list):
            if skills and isinstance(skills[0], dict):
                skill_names = [skill.get('name', str(skill)) for skill in skills]
            else:
                skill_names = [str(skill) for skill in skills]
            text_parts.append(", ".join(skill_names[:20]))
    
    if resume_dict.get('education'):
        text_parts.append("\nEducation:")
        for edu in resume_dict['education']:
            if isinstance(edu, dict):
                text_parts.append(
                    f"- {edu.get('degree', 'Unknown')} in "
                    f"{edu.get('institution', 'Unknown')}"
                )
    
    if resume_dict.get('certifications'):
        text_parts.append("\nCertifications:")
        for cert in resume_dict['certifications']:
            text_parts.append(f"- {cert}")
    
    return "\n".join(text_parts)


def calculate_simple_skill_match(
    resume_skills: List[str],
    job_required_skills: List[str]
) -> tuple:
    """
    Calculate simple skill match without LLM.
    
    Returns:
        (matching_skills, missing_skills, match_percentage)
    """
    resume_skills_lower = {skill.lower() for skill in resume_skills}
    job_skills_lower = {skill.lower() for skill in job_required_skills}
    
    matching = resume_skills_lower.intersection(job_skills_lower)
    missing = job_skills_lower - resume_skills_lower
    
    if len(job_skills_lower) == 0:
        match_pct = 0
    else:
        match_pct = int((len(matching) / len(job_skills_lower)) * 100)
    
    return list(matching), list(missing), match_pct


def calculate_experience_match(
    resume_experience: List[dict],
    job_description: str
) -> float:
    """
    Estimate experience relevance based on keywords.
    Returns match percentage (0-100).
    """
    job_keywords = {
        'develop', 'design', 'implement', 'build', 'create',
        'manage', 'lead', 'coordinate', 'analyze', 'optimize',
        'test', 'deploy', 'architect', 'scale', 'improve'
    }
    
    total_score = 0
    count = 0
    
    for exp in resume_experience:
        if isinstance(exp, dict) and exp.get('description'):
            description = exp['description'].lower()
            found_keywords = sum(1 for kw in job_keywords if kw in description)
            score = min(int((found_keywords / len(job_keywords)) * 100), 100)
            total_score += score
            count += 1
    
    if count == 0:
        return 0
    
    return int(total_score / count)


def estimate_match_score(
    skill_match_pct: int,
    experience_match_pct: int,
    section_completeness: int
) -> int:
    """Estimate overall match score based on components."""
    # Weighted average
    score = int(
        (skill_match_pct * 0.4) +
        (experience_match_pct * 0.35) +
        (section_completeness * 0.25)
    )
    return min(max(score, 0), 100)


def get_sample_jobs() -> List[SampleJob]:
    """Get list of sample job descriptions."""
    return SAMPLE_JOBS


def get_sample_job_by_index(index: int) -> Optional[SampleJob]:
    """Get a specific sample job by index."""
    if 0 <= index < len(SAMPLE_JOBS):
        return SAMPLE_JOBS[index]
    return None
