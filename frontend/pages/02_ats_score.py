"""
ATS Score Analysis Page
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from ats_analyzer import calculate_ats_score
from utils import format_ats_score_display

st.set_page_config(page_title="ATS Score", page_icon="🎯", layout="wide")

st.title("🎯 ATS Health Check")

st.markdown(
    """
Run a quick ATS-style check of your resume structure, contact info, action verbs, and quantified impact. 
No job description needed—this focuses on making the resume itself scanner-friendly.
"""
)

st.markdown(
    """
    <style>
        .metric-card {background: #0f172a0d; padding: 1rem 1.2rem; border-radius: 12px; border: 1px solid #e2e8f0;}
        .section-card {background: #ffffff; padding: 1.2rem 1.2rem; border-radius: 14px; border: 1px solid #e2e8f0; box-shadow: 0 4px 10px rgba(15,23,42,0.06);}
    </style>
    """,
    unsafe_allow_html=True,
)

# Check if resume is loaded
if 'parsed_resume' not in st.session_state:
    st.warning("⚠️ No resume loaded yet")
    st.info("Please upload a resume on the **Upload & Analyze** page first")
    st.stop()

parsed_resume = st.session_state.parsed_resume
resume_dict = st.session_state.resume_dict

with st.spinner("📊 Calculating ATS score..."):
    resume_text = " ".join([
        str(parsed_resume.name or ""),
        str(parsed_resume.email or ""),
        str(parsed_resume.phone or ""),
        str(parsed_resume.summary or ""),
        " ".join([s.name for s in parsed_resume.skills]) if parsed_resume.skills else "",
        " ".join([e.description or "" for e in parsed_resume.experience]) if parsed_resume.experience else "",
        " ".join([e.degree or "" for e in parsed_resume.education]) if parsed_resume.education else "",
        " ".join(parsed_resume.certifications) if parsed_resume.certifications else "",
        " ".join(parsed_resume.projects) if parsed_resume.projects else "",
    ])

    resume_skills = [s.name for s in parsed_resume.skills] if parsed_resume.skills else []

    ats_result = calculate_ats_score(
        resume_text,
        resume_skills,
        resume_dict
    )

# Display ATS Score
st.markdown("---")
st.markdown("## 📊 ATS Analysis Results")

card1, card2, card3, card4 = st.columns(4)

with card1:
    emoji, color, assessment = format_ats_score_display(ats_result.ats_score)
    st.markdown(f"<div class='metric-card'><h4>Overall ATS</h4><h2>{ats_result.ats_score}/100</h2><p>{emoji} {assessment}</p></div>", unsafe_allow_html=True)

with card2:
    st.markdown(f"<div class='metric-card'><h4>Structure</h4><h2>{ats_result.structure_score}%</h2><p>Section completeness</p></div>", unsafe_allow_html=True)

with card3:
    st.markdown(f"<div class='metric-card'><h4>Action Verbs</h4><h2>{ats_result.action_verb_score}%</h2><p>Impactful openings</p></div>", unsafe_allow_html=True)

with card4:
    st.markdown(f"<div class='metric-card'><h4>Quantified Impact</h4><h2>{ats_result.metrics_score}%</h2><p>Numbers & metrics</p></div>", unsafe_allow_html=True)

# Detailed breakdown
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📈 Score Breakdown", "✅ Strengths", "💡 Improvement Plan"])

with tab1:
    st.markdown("### Score Components")
    with st.container():
        st.write("**Structure & Sections**")
        st.progress(ats_result.structure_score / 100)
        st.write(f"{ats_result.structure_score}%")

        st.write("**Contact Readiness**")
        st.progress(ats_result.contact_score / 100)
        st.write(f"{ats_result.contact_score}%")

        st.write("**Action Verbs**")
        st.progress(ats_result.action_verb_score / 100)
        st.write(f"{ats_result.action_verb_score}%")

        st.write("**Quantified Impact**")
        st.progress(ats_result.metrics_score / 100)
        st.write(f"{ats_result.metrics_score}%")

    st.markdown("### Score Interpretation")
    if ats_result.ats_score >= 80:
        st.success("🟢 Excellent — resume is ATS-friendly and impact-focused")
    elif ats_result.ats_score >= 60:
        st.info("🟡 Good — tighten action verbs and metrics")
    elif ats_result.ats_score >= 40:
        st.warning("🟠 Fair — add clearer sections and quantified results")
    else:
        st.error("🔴 Needs Improvement — fill missing sections and contact details")

with tab2:
    st.markdown("### ✅ Resume Strengths")
    if ats_result.strengths:
        for strength in ats_result.strengths:
            st.success(strength)
    else:
        st.info("Continue refining impact statements and structure")

with tab3:
    st.markdown("### 💡 Targeted Fixes")
    for tip in ats_result.improvement_tips:
        st.info(tip)
    if ats_result.ats_score < 70:
        st.markdown("---")
        st.markdown("**Fast wins:** add metrics to top 3 bullets, start each with an action verb, and ensure email + phone are in the header.")

# Additional insights
st.markdown("---")
st.markdown("## 📚 Quick Tips")

tip_col1, tip_col2, tip_col3 = st.columns(3)

with tip_col1:
    st.info("""
    **Format**
    - Clear section headers
    - Consistent bullet style
    - Standard fonts (no images)
    """)

with tip_col2:
    st.info("""
    **Impact**
    - Lead with verbs
    - Add metrics (% or #)
    - Highlight top skills early
    """)

with tip_col3:
    st.info("""
    **Contact**
    - Email + phone in header
    - Location (city, country)
    - LinkedIn (optional)
    """)

# Save results to session
st.session_state.ats_result = ats_result

st.markdown("---")
st.markdown("### 🔄 Next Steps")
col1, col2 = st.columns(2)
with col1:
    st.info("💡 Go to **Resume Suggestions** for improvement tips")
with col2:
    st.info("🎲 Go to **Job Matching** to find similar jobs")
