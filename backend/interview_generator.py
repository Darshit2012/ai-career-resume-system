"""
Interview Preparation Module
Generates interview questions based on resume and job role.
"""

import streamlit as st
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional


class InterviewQuestion(BaseModel):
    """Single interview question."""
    question: str = Field(description="The interview question")
    category: str = Field(description="Category: technical, behavioral, role-specific")
    why_asked: str = Field(description="Why this question is relevant")
    tip: Optional[str] = Field(description="Tip for answering this question")


class InterviewSet(BaseModel):
    """Complete set of interview questions."""
    role: str = Field(description="Job role")
    company_context: Optional[str] = Field(description="Company context if available")
    technical_questions: List[InterviewQuestion] = Field(description="Technical questions")
    behavioral_questions: List[InterviewQuestion] = Field(description="Behavioral questions")
    role_specific_questions: List[InterviewQuestion] = Field(description="Role-specific questions")
    preparation_tips: List[str] = Field(description="General preparation tips")


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


@st.cache_data(show_spinner="🎤 Generating interview questions...")
def generate_interview_questions(
    resume_dict: dict,
    job_description: str,
    job_title: Optional[str] = None,
    company_name: Optional[str] = None
) -> InterviewSet:
    """
    Generate interview questions based on resume and job description.
    
    Args:
        resume_dict: Parsed resume data
        job_description: Job description text
        job_title: Optional job title
        company_name: Optional company name
    
    Returns:
        InterviewSet with questions across categories
    """
    try:
        # Format resume for context
        resume_text = format_resume_for_interview(resume_dict)
        
        job_context = f"Job Title: {job_title}\nCompany: {company_name}\n" if job_title else ""
        
        prompt = f"""You are an expert interviewer. Generate a comprehensive set of interview questions for a candidate with this background applying for this role.

CANDIDATE RESUME:
{resume_text}

JOB POSTING:
{job_context}{job_description}

Generate 3 questions in each category:
1. Technical Questions: Based on skills and technical requirements
2. Behavioral Questions: Standard STAR format questions (situation, task, action, result)
3. Role-Specific Questions: Specific to this job role and company

For each question, provide:
- The question
- Why it's being asked
- A tip for answering well

Also provide 3-4 general preparation tips for this interview."""

        # Enforce clean JSON output to avoid markdown wrappers
        prompt += "\n\nReturn only valid JSON with keys: role (string), company_context (string|null), technical_questions (list of {question, category, why_asked, tip}), behavioral_questions (same shape), role_specific_questions (same shape), preparation_tips (list of strings). No extra text or markdown."

        model = get_gemini_model()
        response = model.generate_content(prompt)

        interview_set = InterviewSet.model_validate_json(response.text)
        
        # Update role if provided
        if job_title:
            interview_set.role = job_title
        if company_name:
            interview_set.company_context = f"Interviewing at {company_name}"
        
        return interview_set
        
    except Exception as e:
        st.error(f"Error generating interview questions: {str(e)}")
        return None


def format_resume_for_interview(resume_dict: dict) -> str:
    """Format resume for interview question generation."""
    text_parts = []
    
    if resume_dict.get('name'):
        text_parts.append(f"Candidate: {resume_dict['name']}")
    
    if resume_dict.get('summary'):
        text_parts.append(f"\nProfessional Summary:\n{resume_dict['summary']}")
    
    if resume_dict.get('experience'):
        text_parts.append("\nWork Experience:")
        for i, exp in enumerate(resume_dict['experience'], 1):
            if isinstance(exp, dict):
                text_parts.append(
                    f"{i}. {exp.get('title', 'Unknown')} at {exp.get('company', 'Unknown')} "
                    f"({exp.get('duration', 'Unknown')})"
                )
                if exp.get('description'):
                    text_parts.append(f"   {exp['description']}")
    
    if resume_dict.get('skills'):
        text_parts.append("\nKey Skills:")
        skills = resume_dict['skills']
        skill_list = []
        if isinstance(skills, list):
            if skills and isinstance(skills[0], dict):
                skill_list = [skill.get('name', str(skill)) for skill in skills]
            else:
                skill_list = [str(skill) for skill in skills]
        text_parts.append(", ".join(skill_list[:15]))
    
    if resume_dict.get('education'):
        text_parts.append("\nEducation:")
        for edu in resume_dict['education']:
            if isinstance(edu, dict):
                text_parts.append(
                    f"- {edu.get('degree', 'Unknown')} from "
                    f"{edu.get('institution', 'Unknown')} "
                    f"({edu.get('graduation_year', 'Unknown')})"
                )
    
    if resume_dict.get('certifications'):
        text_parts.append("\nCertifications:")
        for cert in resume_dict['certifications']:
            text_parts.append(f"- {cert}")
    
    if resume_dict.get('projects'):
        text_parts.append("\nProjects:")
        for project in resume_dict['projects'][:3]:
            text_parts.append(f"- {project}")
    
    return "\n".join(text_parts)


# Common behavioral interview questions
COMMON_BEHAVIORAL_QUESTIONS = [
    {
        "question": "Tell me about a time when you had to solve a difficult problem. How did you approach it?",
        "category": "behavioral",
        "why_asked": "Assesses problem-solving methodology and thinking process",
        "tip": "Use STAR method: Situation, Task, Action, Result. Be specific with metrics if possible."
    },
    {
        "question": "Describe a situation where you had to work with a difficult team member.",
        "category": "behavioral",
        "why_asked": "Evaluates interpersonal skills and conflict resolution",
        "tip": "Focus on understanding their perspective and the positive resolution."
    },
    {
        "question": "Tell me about a project where you exceeded expectations.",
        "category": "behavioral",
        "why_asked": "Identifies high performers and those with drive",
        "tip": "Highlight your contribution, the challenge, and quantifiable results."
    },
    {
        "question": "Give an example of when you had to learn something new quickly.",
        "category": "behavioral",
        "why_asked": "Tests adaptability and learning ability",
        "tip": "Show your learning strategy and how you applied the new skill."
    },
    {
        "question": "Tell me about a time you failed. What did you learn?",
        "category": "behavioral",
        "why_asked": "Assesses resilience and learning from mistakes",
        "tip": "Be honest about failure but focus on lessons learned and growth."
    }
]

# Common technical interview questions by domain
TECHNICAL_QUESTIONS_BY_DOMAIN = {
    'backend': [
        {
            "question": "Explain the difference between SQL and NoSQL databases. When would you use each?",
            "category": "technical",
            "why_asked": "Tests database knowledge and understanding of trade-offs",
            "tip": "Discuss scalability, data structure, and use case suitability."
        },
        {
            "question": "How would you design a scalable API for millions of requests?",
            "category": "technical",
            "why_asked": "Evaluates systems design and scalability thinking",
            "tip": "Consider caching, load balancing, database optimization."
        },
        {
            "question": "What is the difference between REST and GraphQL?",
            "category": "technical",
            "why_asked": "Tests understanding of API architectures",
            "tip": "Compare flexibility, over-fetching, under-fetching, performance."
        }
    ],
    'frontend': [
        {
            "question": "How do you optimize frontend performance?",
            "category": "technical",
            "why_asked": "Evaluates understanding of web performance",
            "tip": "Discuss caching, lazy loading, minification, CDN, bundle size."
        },
        {
            "question": "Explain the virtual DOM and why React uses it.",
            "category": "technical",
            "why_asked": "Tests framework-specific knowledge",
            "tip": "Discuss diffing algorithm and performance benefits."
        }
    ],
    'data-science': [
        {
            "question": "How do you handle missing data in a dataset?",
            "category": "technical",
            "why_asked": "Tests data preprocessing knowledge",
            "tip": "Discuss imputation, deletion, and the impact on model."
        },
        {
            "question": "Explain overfitting and how to prevent it.",
            "category": "technical",
            "why_asked": "Tests ML fundamentals",
            "tip": "Discuss cross-validation, regularization, ensemble methods."
        }
    ]
}


def get_behavioral_questions() -> List[dict]:
    """Get common behavioral interview questions."""
    return COMMON_BEHAVIORAL_QUESTIONS


def get_technical_questions(domain: str = 'general') -> List[dict]:
    """Get technical questions for a specific domain."""
    return TECHNICAL_QUESTIONS_BY_DOMAIN.get(domain, [])


def generate_simple_questions(
    skills: List[str],
    job_title: str
) -> InterviewSet:
    """
    Generate interview questions using templates (for fallback/testing).
    
    Args:
        skills: List of candidate skills
        job_title: Job title
    
    Returns:
        InterviewSet with template-based questions
    """
    # Identify domain
    domain = identify_domain(job_title)
    
    technical_qs = get_technical_questions(domain)
    behavioral_qs = get_behavioral_questions()
    
    # Role-specific questions based on title
    role_specific_qs = generate_role_specific_questions(job_title, skills)
    
    return InterviewSet(
        role=job_title,
        company_context=None,
        technical_questions=[InterviewQuestion(**q) for q in technical_qs[:3]],
        behavioral_questions=[InterviewQuestion(**q) for q in behavioral_qs[:3]],
        role_specific_questions=role_specific_qs,
        preparation_tips=get_preparation_tips(job_title)
    )


def identify_domain(job_title: str) -> str:
    """Identify job domain from title."""
    job_title_lower = job_title.lower()
    
    if any(word in job_title_lower for word in ['backend', 'server', 'api']):
        return 'backend'
    elif any(word in job_title_lower for word in ['frontend', 'ui', 'ux', 'react', 'vue']):
        return 'frontend'
    elif any(word in job_title_lower for word in ['data', 'ml', 'ai', 'science']):
        return 'data-science'
    
    return 'general'


def generate_role_specific_questions(job_title: str, skills: List[str]) -> List[InterviewQuestion]:
    """Generate questions specific to the role."""
    questions = []
    
    job_title_lower = job_title.lower()
    
    if 'senior' in job_title_lower:
        questions.append(InterviewQuestion(
            question="How do you approach mentoring junior developers?",
            category="role-specific",
            why_asked="Tests leadership and mentoring capability",
            tip="Share examples of how you've helped others grow."
        ))
    
    if 'lead' in job_title_lower or 'architect' in job_title_lower:
        questions.append(InterviewQuestion(
            question="Tell me about a major technical decision you made and how you communicated it to stakeholders.",
            category="role-specific",
            why_asked="Evaluates technical leadership and communication",
            tip="Show how you balanced technical and business considerations."
        ))
    
    if 'manager' in job_title_lower:
        questions.append(InterviewQuestion(
            question="How do you handle performance issues with team members?",
            category="role-specific",
            why_asked="Tests people management skills",
            tip="Discuss constructive feedback and development."
        ))
    
    # Default role-specific question
    if not questions:
        questions.append(InterviewQuestion(
            question=f"What excites you about the {job_title} position?",
            category="role-specific",
            why_asked="Gauges genuine interest in the role",
            tip="Be specific about skills you want to develop and impact you want to make."
        ))
    
    return questions


def get_preparation_tips(job_title: str) -> List[str]:
    """Get preparation tips specific to the job."""
    tips = [
        "✅ Research the company: mission, values, recent news",
        "✅ Review the job description thoroughly and note key requirements",
        "✅ Prepare STAR format examples for behavioral questions",
        "✅ Practice talking about your projects and quantify results",
        "✅ Prepare thoughtful questions to ask the interviewer"
    ]
    
    job_title_lower = job_title.lower()
    
    if any(word in job_title_lower for word in ['technical', 'developer', 'engineer', 'backend', 'frontend']):
        tips.append("✅ Be ready for technical problem-solving during the interview")
        tips.append("✅ Explain your thought process clearly, not just the solution")
    
    if any(word in job_title_lower for word in ['data', 'ml', 'ai', 'science']):
        tips.append("✅ Prepare to discuss a recent ML project in detail")
        tips.append("✅ Be ready to discuss trade-offs in model selection")
    
    if any(word in job_title_lower for word in ['manager', 'lead', 'senior']):
        tips.append("✅ Prepare examples of team leadership and conflict resolution")
        tips.append("✅ Discuss how you foster team growth and development")
    
    return tips
