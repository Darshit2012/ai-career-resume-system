"""
Resume Suggestions Page
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from resume_rewriter import generate_resume_suggestions

st.set_page_config(page_title="Resume Suggestions", page_icon="💡", layout="wide")

st.title("💡 AI Resume Improvement Suggestions")

st.markdown("""
Get AI-powered suggestions to improve your resume content, clarity, and ATS compatibility.
""")

# Check if resume is loaded
if 'parsed_resume' not in st.session_state:
    st.warning("⚠️ No resume loaded yet")
    st.info("Please upload a resume on the **Upload & Analyze** page first")
    st.stop()

parsed_resume = st.session_state.parsed_resume
resume_dict = st.session_state.resume_dict

# Get job description
st.markdown("### Enter Target Job Description")
job_description = st.text_area(
    "Paste the job description for which you want suggestions",
    height=200,
    placeholder="Copy and paste the job description here...",
    key="suggestions_jd"
)

if not job_description:
    st.info("👆 Paste a job description to get personalized suggestions")
    st.stop()

# Generate suggestions
with st.spinner("✍️ Generating improvement suggestions..."):
    feedback = generate_resume_suggestions(resume_dict, job_description)

if feedback:
    st.markdown("---")
    st.markdown("## 🎯 Improvement Suggestions")
    
    # Overall assessment
    st.markdown("### 📋 Overall Assessment")
    st.info(feedback.overall_assessment)
    
    # Top actions
    st.markdown("### 🔥 Top 3 Priority Actions")
    for i, action in enumerate(feedback.top_actions[:3], 1):
        st.markdown(f"{i}. {action}")
    
    st.markdown("---")
    
    # Specific suggestions
    st.markdown("### ✏️ Specific Improvement Suggestions")
    
    for i, suggestion in enumerate(feedback.suggestions, 1):
        with st.expander(f"💬 Suggestion {i}: {suggestion.focus_area.title()}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Original Text:**")
                st.code(suggestion.original_text, language="")
            
            with col2:
                st.markdown("**Suggested Improvement:**")
                st.code(suggestion.suggested_text, language="")
            
            st.markdown("**Why This Helps:**")
            st.info(suggestion.reason)
            
            # Action button
            if st.button(f"Copy Suggestion {i}", key=f"copy_{i}"):
                st.session_state[f"copied_{i}"] = suggestion.suggested_text
                st.success("Copied to clipboard!")
    
    st.markdown("---")
    
    # Categorized tips
    st.markdown("## 📚 Writing Tips by Category")
    
    # Categorize suggestions
    focus_areas = {}
    for suggestion in feedback.suggestions:
        area = suggestion.focus_area.title()
        if area not in focus_areas:
            focus_areas[area] = []
        focus_areas[area].append(suggestion)
    
    for area, suggestions in focus_areas.items():
        with st.expander(f"📌 {area} ({len(suggestions)} tips)"):
            for idx, sugg in enumerate(suggestions, 1):
                st.write(f"**{idx}. {sugg.reason}**")
                st.write(f"Original: {sugg.original_text[:100]}...")
                st.write(f"Improved: {sugg.suggested_text[:100]}...")
                st.divider()
    
else:
    st.error("❌ Failed to generate suggestions. Please try again.")

st.markdown("---")

# Additional tips
st.markdown("## 💡 General Resume Writing Tips")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ✨ Clarity & Professionalism")
    st.markdown("""
    - Use active voice, not passive
    - Keep sentences concise (under 20 words)
    - Avoid jargon unless it's industry-standard
    - Use professional language
    - Proofread carefully
    """)
    
    st.markdown("### 🎯 Action Verbs")
    st.markdown("""
    Start bullet points with strong verbs:
    - Developed, Created, Built
    - Managed, Led, Directed
    - Analyzed, Identified, Optimized
    - Achieved, Improved, Increased
    - Implemented, Designed, Engineered
    """)

with col2:
    st.markdown("### 📊 Quantification")
    st.markdown("""
    Add specific numbers and results:
    - Increased efficiency by 30%
    - Reduced costs by $50,000
    - Led team of 5 engineers
    - Achieved 99.9% uptime
    - Processed 1M+ transactions
    """)
    
    st.markdown("### 🔑 Keyword Optimization")
    st.markdown("""
    - Study job description keywords
    - Include relevant technical terms
    - Match industry terminology
    - Use standard job titles
    - Incorporate required skills
    """)

st.markdown("---")

# Improvement checklist
st.markdown("## ✅ Resume Improvement Checklist")

checklist = {
    "Contact Information": "Name, email, phone clearly visible",
    "Professional Summary": "Brief, impactful overview of your career",
    "Experience Section": "Clear job titles, companies, dates, achievements",
    "Education": "Degrees, institutions, graduation dates",
    "Skills Section": "Organized by category (technical, tools, soft)",
    "Quantified Results": "Include numbers, percentages, metrics",
    "Action Verbs": "Start sentences with strong verbs",
    "Keywords": "Job-relevant keywords naturally incorporated",
    "Formatting": "Clean, consistent, ATS-friendly layout",
    "Proofreading": "No spelling, grammar, or punctuation errors",
}

checked = st.session_state.get("resume_checks", {})

st.markdown("### Review Your Resume Against These Criteria:")
for item, description in checklist.items():
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        checked[item] = st.checkbox(item, value=checked.get(item, False))
    with col2:
        st.caption(description)

st.session_state.resume_checks = checked

# Summary
checked_count = sum(1 for v in checked.values() if v)
st.markdown(f"**Progress: {checked_count}/{len(checklist)} items completed**")
if checked_count == len(checklist):
    st.success("✨ Your resume is well-optimized!")
elif checked_count >= len(checklist) * 0.8:
    st.info("👍 Great progress! Keep refining.")
else:
    st.warning("⚠️ Consider working on the unchecked items.")

st.markdown("---")
st.markdown("### 🔄 Next Steps")
col1, col2 = st.columns(2)
with col1:
    st.info("🎲 Go to **Job Matching** to find suitable roles")
with col2:
    st.info("🎤 Go to **Interview Prep** to prepare for interviews")
