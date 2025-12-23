"""
Resume Parser Module
Extracts and structures information from resume documents.
"""

import streamlit as st
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional
import re
import json


class Education(BaseModel):
    """Education entry in resume."""
    degree: Optional[str] = Field(description="e.g., B.Tech in Computer Science")
    institution: Optional[str] = Field(description="e.g., Indian Institute of Technology")
    graduation_year: Optional[str] = Field(description="e.g., 2024")
    gpa: Optional[str] = Field(description="e.g., 3.8/4.0")


class Experience(BaseModel):
    """Work experience entry in resume."""
    title: Optional[str] = Field(description="Job title")
    company: Optional[str] = Field(description="Company name")
    duration: Optional[str] = Field(description="Employment duration")
    description: Optional[str] = Field(description="Responsibilities and achievements")


class Skill(BaseModel):
    """Skill with category."""
    name: str
    category: str  # 'technical', 'tool', 'soft_skill'


class ParsedResume(BaseModel):
    """Structured resume data."""
    name: Optional[str] = Field(description="Full name")
    email: Optional[str] = Field(description="Email address")
    phone: Optional[str] = Field(description="Phone number")
    summary: Optional[str] = Field(description="Professional summary or objective")
    skills: List[Skill] = Field(description="List of skills with categories")
    education: List[Education] = Field(description="Education history")
    experience: List[Experience] = Field(description="Work experience")
    certifications: List[str] = Field(description="Certifications and courses")
    projects: List[str] = Field(description="Notable projects")


def get_gemini_model(model_name="models/gemini-2.5-flash"):
    """Configure Gemini model to return JSON output."""
    generation_config = genai.GenerationConfig(
        response_mime_type="application/json"
    )
    return genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config
    )


@st.cache_data(show_spinner="📄 Parsing resume...")
def parse_resume_from_file(uploaded_file):
    """
    Parse resume from uploaded file using Gemini API.
    
    Args:
        uploaded_file: Streamlit uploaded file (PDF, DOCX, TXT)
    
    Returns:
        ParsedResume object or None if parsing fails
    """
    if not uploaded_file:
        return None
    
    try:
        bytes_data = uploaded_file.getvalue()
        resume_file_part = {
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }
        
        prompt = [
            """You are an expert resume parser. Analyze the provided resume document and extract:
1. Name, email, phone
2. Professional summary
3. Skills (categorize as: technical, tool, or soft_skill)
4. Education (degree, institution, graduation year, GPA if available)
5. Work experience (title, company, duration, description)
6. Certifications and courses
7. Notable projects

Return ONLY valid JSON matching this schema (no markdown, no explanations):
{
    "name": string|null,
    "email": string|null,
    "phone": string|null,
    "summary": string|null,
    "skills": [{"name": string, "category": "technical"|"tool"|"soft_skill"}],
    "education": [{"degree": string|null, "institution": string|null, "graduation_year": string|null, "gpa": string|null}],
    "experience": [{"title": string|null, "company": string|null, "duration": string|null, "description": string|null}],
    "certifications": [string],
    "projects": [string]
}
If any field is not present, use null.
For skills, ensure each skill has a category.
Do not include triple backticks or any extra text.""",
            resume_file_part
        ]
        
        model = get_gemini_model()
        response = model.generate_content(prompt)
        
        parsed = ParsedResume.model_validate_json(response.text)
        return parsed
        
    except Exception as e:
        st.error(f"Error parsing resume: {str(e)}")
        return None


def extract_keywords_from_resume(resume: ParsedResume) -> set:
    """Extract all relevant keywords from parsed resume."""
    keywords = set()
    
    if resume.summary:
        keywords.update(extract_keywords_from_text(resume.summary))
    
    for skill in resume.skills:
        keywords.add(skill.name.lower())
    
    for exp in resume.experience:
        if exp.description:
            keywords.update(extract_keywords_from_text(exp.description))
    
    return keywords


def extract_keywords_from_text(text: str) -> set:
    """Extract keywords from text using simple NLP."""
    if not text:
        return set()
    
    # Convert to lowercase and split
    words = text.lower().split()
    
    # Filter out common stopwords and short words
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'up', 'is', 'are', 'was', 'were', 'be',
        'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
    }
    
    keywords = {
        word.strip('.,;:!?\"\'') 
        for word in words 
        if len(word.strip('.,;:!?\"\'')) > 2 and word.lower() not in stopwords
    }
    
    return keywords


def detect_missing_sections(resume: ParsedResume) -> dict:
    """Detect missing resume sections."""
    missing = {
        'summary': not resume.summary or len(resume.summary) < 20,
        'experience': len(resume.experience) == 0,
        'education': len(resume.education) == 0,
        'skills': len(resume.skills) == 0,
        'certifications': len(resume.certifications) == 0,
        'projects': len(resume.projects) == 0
    }
    return missing


def categorize_skills(skills: List[Skill]) -> dict:
    """Categorize skills by type."""
    categorized = {
        'technical': [],
        'tools': [],
        'soft_skills': []
    }
    
    for skill in skills:
        category = skill.category.lower()
        if category == 'technical':
            categorized['technical'].append(skill.name)
        elif category == 'tool':
            categorized['tools'].append(skill.name)
        elif category == 'soft_skill':
            categorized['soft_skills'].append(skill.name)
    
    return categorized
