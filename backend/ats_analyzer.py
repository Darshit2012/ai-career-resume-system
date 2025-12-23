"""
ATS (Applicant Tracking System) Analyzer Module
Scores resumes against job descriptions using keyword matching and similarity analysis.
"""

import streamlit as st
from pydantic import BaseModel, Field
from typing import List, Optional
import re
from difflib import SequenceMatcher


class ATSScoreResult(BaseModel):
    """ATS scoring result for the resume itself (no job description required)."""
    ats_score: int = Field(description="Overall score out of 100")
    structure_score: int = Field(description="Section completeness / structure score")
    contact_score: int = Field(description="Contact info availability score")
    action_verb_score: int = Field(description="Use of strong action verbs")
    metrics_score: int = Field(description="Use of quantified results")
    strengths: List[str] = Field(description="Strong resume signals")
    improvement_tips: List[str] = Field(description="Actionable improvement suggestions")


def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text


ACTION_VERBS = {
    'developed', 'implemented', 'created', 'designed', 'built', 'achieved', 'improved', 'optimized',
    'led', 'managed', 'spearheaded', 'directed', 'launched', 'automated', 'increased', 'reduced',
    'analyzed', 'delivered', 'deployed', 'configured', 'debugged', 'architected', 'scaled'
}


def count_action_verbs(resume_text: str) -> int:
    """Count occurrences of strong action verbs."""
    words = normalize_text(resume_text).split()
    return sum(1 for w in words if w in ACTION_VERBS)


def count_metric_statements(resume_text: str) -> int:
    """Count occurrences of numbers/percentages indicating quantified impact."""
    numbers = re.findall(r"\b\d+\b|%", resume_text)
    return len(numbers)


def has_contact_info(resume_data: dict) -> int:
    """Return a contact score based on presence of email/phone."""
    email = resume_data.get('email')
    phone = resume_data.get('phone')
    if email and phone:
        return 100
    if email or phone:
        return 70
    return 30


def assess_section_completeness(resume_data: dict) -> int:
    """
    Assess completeness of resume sections.
    Expected sections: summary, experience, education, skills, projects, certifications
    """
    required_sections = ['summary', 'experience', 'education', 'skills']
    optional_sections = ['projects', 'certifications']
    
    completed_required = 0
    completed_optional = 0
    
    for section in required_sections:
        if section in resume_data and resume_data[section]:
            if isinstance(resume_data[section], (list, str)):
                if resume_data[section]:
                    completed_required += 1
    
    for section in optional_sections:
        if section in resume_data and resume_data[section]:
            if isinstance(resume_data[section], (list, str)):
                if resume_data[section]:
                    completed_optional += 1
    
    # Calculate score: 70% for required sections, 30% for optional
    required_score = int((completed_required / len(required_sections)) * 70)
    optional_score = int((completed_optional / len(optional_sections)) * 30)
    
    return min(required_score + optional_score, 100)


def generate_improvement_tips(
    structure_score: int,
    contact_score: int,
    action_verb_score: int,
    metrics_score: int
) -> List[str]:
    """Generate actionable improvement tips based on resume-only signals."""
    tips = []

    if structure_score < 80:
        tips.append("📋 Add or expand key sections (summary, experience, education, skills)")
        tips.append("📋 Use clear headings and consistent formatting")

    if contact_score < 100:
        tips.append("☎️ Include both a professional email and phone number in the header")

    if action_verb_score < 70:
        tips.append("⚡ Start bullet points with strong action verbs (e.g., Led, Built, Optimized)")

    if metrics_score < 70:
        tips.append("📈 Quantify impact with numbers or percentages where possible")

    if not tips:
        tips.append("✅ Solid foundation. Fine-tune by tailoring keywords to each application.")

    return tips
def calculate_ats_score(
    resume_text: str,
    resume_skills: List[str],
    resume_data: dict
) -> ATSScoreResult:
    """Calculate an ATS-style score using only resume signals (no job description)."""

    structure_score = assess_section_completeness(resume_data)
    contact_score = has_contact_info(resume_data)
    action_hits = count_action_verbs(resume_text)
    metric_hits = count_metric_statements(resume_text)

    action_verb_score = min(100, action_hits * 10)
    metrics_score = min(100, metric_hits * 15)

    ats_score = int(
        (structure_score * 0.4) +
        (contact_score * 0.2) +
        (action_verb_score * 0.2) +
        (metrics_score * 0.2)
    )

    strengths = []
    if structure_score >= 80:
        strengths.append("Solid structure and section coverage")
    if contact_score == 100:
        strengths.append("Complete contact details present")
    if action_verb_score >= 70:
        strengths.append("Good use of strong action verbs")
    if metrics_score >= 70:
        strengths.append("Achievements are quantified with metrics")
    if not strengths:
        strengths.append("Resume captured; ready for focused improvements")

    improvement_tips = generate_improvement_tips(
        structure_score,
        contact_score,
        action_verb_score,
        metrics_score
    )

    return ATSScoreResult(
        ats_score=ats_score,
        structure_score=structure_score,
        contact_score=contact_score,
        action_verb_score=action_verb_score,
        metrics_score=metrics_score,
        strengths=strengths,
        improvement_tips=improvement_tips
    )


def similarity_score(str1: str, str2: str) -> float:
    """Calculate similarity between two strings (0-100)."""
    str1 = normalize_text(str1)
    str2 = normalize_text(str2)
    ratio = SequenceMatcher(None, str1, str2).ratio()
    return int(ratio * 100)
