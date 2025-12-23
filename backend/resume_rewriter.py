"""
Resume Rewriter Module
Generates AI-powered suggestions to improve resume content.
"""

import streamlit as st
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional


class ResumeSuggestion(BaseModel):
    """Single resume improvement suggestion."""
    original_text: str = Field(description="Original resume text")
    suggested_text: str = Field(description="Improved version")
    reason: str = Field(description="Why this improvement helps")
    focus_area: str = Field(description="Area: clarity, ats, professional, quantification")


class ResumeFeedback(BaseModel):
    """Overall resume feedback."""
    overall_assessment: str = Field(description="General feedback on the resume")
    suggestions: List[ResumeSuggestion] = Field(description="Specific improvement suggestions")
    top_actions: List[str] = Field(description="Top 3 actions to take")


class ActionVerbSuggestion(BaseModel):
    """Action verb suggestion for bullet points."""
    original_phrase: str
    action_verbs: List[str] = Field(description="Better action verbs")
    revised_bullet: str


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


@st.cache_data(show_spinner="💡 Generating improvement suggestions...")
def generate_resume_suggestions(
    parsed_resume_dict: dict,
    job_description: str
) -> ResumeFeedback:
    """
    Generate AI-powered resume improvement suggestions.
    
    Args:
        parsed_resume_dict: Dictionary of parsed resume data
        job_description: Target job description
    
    Returns:
        ResumeFeedback object with suggestions
    """
    try:
        # Prepare resume text
        resume_text = format_resume_for_analysis(parsed_resume_dict)
        
        prompt = f"""You are an expert career coach and resume specialist. Analyze this resume against the job description and provide specific, actionable improvement suggestions.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide 3-5 specific suggestions to improve the resume for this job role. Focus on:
1. Using stronger action verbs
2. Adding quantifiable metrics and results
3. Incorporating relevant keywords from the job description
4. Improving clarity and professional language
5. ATS-friendly formatting

For each suggestion, provide the original text, improved version, and reason."""

        # Enforce clean JSON output to avoid markdown fences
        prompt += "\n\nReturn only valid JSON with keys: overall_assessment (string), suggestions (list of {original_text, suggested_text, reason, focus_area}), top_actions (list of strings). No extra text or markdown."

        model = get_gemini_model()
        response = model.generate_content(prompt)

        feedback = ResumeFeedback.model_validate_json(response.text)
        return feedback
        
    except Exception as e:
        st.error(f"Error generating suggestions: {str(e)}")
        return None


def format_resume_for_analysis(resume_dict: dict) -> str:
    """Format parsed resume dictionary into readable text."""
    text_parts = []
    
    if resume_dict.get('name'):
        text_parts.append(f"Name: {resume_dict['name']}")
    
    if resume_dict.get('email'):
        text_parts.append(f"Email: {resume_dict['email']}")
    
    if resume_dict.get('phone'):
        text_parts.append(f"Phone: {resume_dict['phone']}")
    
    if resume_dict.get('summary'):
        text_parts.append(f"\nProfessional Summary:\n{resume_dict['summary']}")
    
    if resume_dict.get('experience'):
        text_parts.append("\nExperience:")
        for exp in resume_dict['experience']:
            if isinstance(exp, dict):
                text_parts.append(
                    f"- {exp.get('title', 'Unknown')} at {exp.get('company', 'Unknown')} "
                    f"({exp.get('duration', 'Unknown')})\n"
                    f"  {exp.get('description', '')}"
                )
    
    if resume_dict.get('skills'):
        text_parts.append("\nSkills:")
        skills = resume_dict['skills']
        if isinstance(skills, list):
            if skills and isinstance(skills[0], dict):
                for skill in skills:
                    text_parts.append(f"- {skill.get('name', skill)}")
            else:
                for skill in skills:
                    text_parts.append(f"- {skill}")
    
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
        for project in resume_dict['projects']:
            text_parts.append(f"- {project}")
    
    return "\n".join(text_parts)


# Action verbs for different industries
ACTION_VERBS = {
    'general': [
        'Developed', 'Implemented', 'Created', 'Designed', 'Built',
        'Achieved', 'Improved', 'Enhanced', 'Optimized', 'Streamlined'
    ],
    'technical': [
        'Architected', 'Engineered', 'Deployed', 'Configured', 'Debugged',
        'Integrated', 'Optimized', 'Scaled', 'Automated', 'Refactored'
    ],
    'leadership': [
        'Led', 'Directed', 'Managed', 'Supervised', 'Coordinated',
        'Delegated', 'Mentored', 'Guided', 'Orchestrated', 'Championed'
    ],
    'analytics': [
        'Analyzed', 'Measured', 'Evaluated', 'Tracked', 'Quantified',
        'Assessed', 'Calculated', 'Determined', 'Identified', 'Concluded'
    ]
}


def suggest_action_verbs(bullet_point: str) -> List[str]:
    """Suggest stronger action verbs for a bullet point."""
    weak_verbs = ['was', 'did', 'made', 'helped', 'worked', 'handled', 'dealt']
    
    suggested = ACTION_VERBS['general'].copy()
    
    # Add context-specific verbs
    if any(word in bullet_point.lower() for word in ['code', 'software', 'data', 'algorithm']):
        suggested.extend(ACTION_VERBS['technical'])
    
    if any(word in bullet_point.lower() for word in ['team', 'people', 'staff', 'group']):
        suggested.extend(ACTION_VERBS['leadership'])
    
    if any(word in bullet_point.lower() for word in ['metric', 'percent', 'number', 'report']):
        suggested.extend(ACTION_VERBS['analytics'])
    
    return list(set(suggested))[:5]  # Return top 5 unique suggestions


def identify_quantification_opportunities(bullet_point: str) -> bool:
    """Check if a bullet point lacks quantifiable metrics."""
    metrics_indicators = ['%', 'million', 'thousand', 'increased', 'decreased', 'reduced']
    has_metrics = any(indicator in bullet_point.lower() for indicator in metrics_indicators)
    return not has_metrics


def improve_clarity(text: str) -> str:
    """Basic text clarity improvements."""
    # Remove passive voice indicators
    improvements = text
    
    # Replace wordy phrases with concise ones
    replacements = {
        'was able to': 'successfully',
        'in order to': 'to',
        'at the end of the day': 'ultimately',
        'it is important to note that': '',
        'the fact that': ''
    }
    
    for wordy, concise in replacements.items():
        improvements = improvements.replace(wordy, concise)
    
    return improvements.strip()


@st.cache_data(show_spinner="✍️ Analyzing bullet points...")
def generate_bullet_improvements(experience_descriptions: List[str]) -> List[ResumeSuggestion]:
    """Generate improvements for experience bullet points."""
    suggestions = []
    
    for bullet in experience_descriptions:
        if len(bullet) > 10:
            # Check for quantification opportunities
            needs_metrics = identify_quantification_opportunities(bullet)
            
            # Suggest action verbs
            action_verbs = suggest_action_verbs(bullet)
            
            # Improve clarity
            improved = improve_clarity(bullet)
            
            reason_parts = []
            if needs_metrics:
                reason_parts.append("Add quantifiable metrics")
            if action_verbs:
                reason_parts.append(f"Use stronger verb: {action_verbs[0]}")
            
            if reason_parts:
                suggestions.append(ResumeSuggestion(
                    original_text=bullet,
                    suggested_text=improved,
                    reason=" and ".join(reason_parts),
                    focus_area="clarity" if len(improved) > len(bullet) else "professional"
                ))
    
    return suggestions
