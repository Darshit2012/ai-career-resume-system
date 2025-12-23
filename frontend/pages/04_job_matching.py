"""
Job Matching Page
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from job_matcher import (
    match_resume_with_job,
    get_sample_jobs,
    get_sample_job_by_index,
    calculate_simple_skill_match
)
from utils import format_match_percentage, estimate_application_success

st.set_page_config(page_title="Job Matching", page_icon="🎲", layout="wide")

st.title("🎲 Job Matching & Fit Analysis")

st.markdown("""
Find and analyze how well your resume matches specific job roles.
""")

# Check if resume is loaded
if 'parsed_resume' not in st.session_state:
    st.warning("⚠️ No resume loaded yet")
    st.info("Please upload a resume on the **Upload & Analyze** page first")
    st.stop()

parsed_resume = st.session_state.parsed_resume
resume_dict = st.session_state.resume_dict

# Choose input method
st.markdown("### 📋 Select a Job")

input_method = st.radio(
    "How would you like to provide job information?",
    ["Use Sample Jobs", "Paste Custom Job Description"],
    horizontal=True
)

job_description = None
job_title = None
company_name = None

if input_method == "Use Sample Jobs":
    st.markdown("#### Sample Job Descriptions")
    sample_jobs = get_sample_jobs()
    
    job_options = {f"{job.title} at {job.company}": i for i, job in enumerate(sample_jobs)}
    selected_job = st.selectbox("Choose a job:", list(job_options.keys()))
    
    if selected_job:
        job_index = job_options[selected_job]
        sample_job = get_sample_job_by_index(job_index)
        
        if sample_job:
            job_description = sample_job.description
            job_title = sample_job.title
            company_name = sample_job.company
            
            st.success(f"✅ Selected: {job_title} at {company_name}")

else:
    st.markdown("#### Custom Job Description")
    job_title = st.text_input("Job Title (optional)")
    company_name = st.text_input("Company Name (optional)")
    job_description = st.text_area(
        "Paste the full job description",
        height=250,
        placeholder="Copy and paste the job description here...",
        key="match_jd"
    )

if not job_description:
    st.info("👆 Select or paste a job description to proceed")
    st.stop()

# Perform matching
with st.spinner("🔍 Analyzing job match..."):
    match_result = match_resume_with_job(resume_dict, job_description)

if match_result:
    st.markdown("---")
    st.markdown("## 📊 Job Matching Results")
    
    # Overall match score
    col1, col2, col3 = st.columns(3)
    
    with col1:
        emoji, assessment = format_match_percentage(match_result.match_percentage)
        st.metric(
            "Overall Match",
            f"{match_result.match_percentage}%",
            delta=assessment,
            delta_color="inverse"
        )
    
    with col2:
        if job_title:
            st.metric("Position", job_title)
    
    with col3:
        if company_name:
            st.metric("Company", company_name)
    
    # Suitability assessment
    st.markdown("---")
    st.markdown("### 🎯 Suitability Assessment")
    
    # Color-code the assessment
    if match_result.match_percentage >= 80:
        st.success(match_result.suitability_assessment)
    elif match_result.match_percentage >= 60:
        st.info(match_result.suitability_assessment)
    elif match_result.match_percentage >= 40:
        st.warning(match_result.suitability_assessment)
    else:
        st.error(match_result.suitability_assessment)
    
    # Career alignment
    st.markdown("### 📈 Career Alignment")
    st.info(match_result.career_alignment)
    
    # Application success estimate
    st.markdown("### 💼 Application Success Estimate")
    success_estimate = estimate_application_success(
        match_result.match_percentage,
        match_result.match_percentage  # Using match percentage as proxy for ATS score
    )
    st.markdown(success_estimate)
    
    st.markdown("---")
    
    # Detailed breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Matching Skills")
        if match_result.matching_skills:
            for skill in match_result.matching_skills:
                st.write(f"✓ {skill}")
        else:
            st.caption("No matching skills identified")
        
        st.markdown("### 📚 Matching Experience")
        if match_result.matching_experience:
            for exp in match_result.matching_experience:
                st.write(f"• {exp}")
        else:
            st.caption("No matching experience found")
    
    with col2:
        st.markdown("### ⚠️ Missing Skills")
        if match_result.missing_skills:
            for skill in match_result.missing_skills:
                st.write(f"✗ {skill}")
        else:
            st.success("✓ No major skills missing!")
        
        st.markdown("### 🎯 Growth Areas")
        if match_result.growth_areas:
            for area in match_result.growth_areas:
                st.write(f"→ {area}")
        else:
            st.caption("No identified growth areas")
    
    st.markdown("---")
    
    # Recommendations
    st.markdown("## 📝 Recommendations")
    
    if match_result.match_percentage >= 80:
        st.success("""
        ### 🎉 Excellent Match!
        This role aligns very well with your background. Consider applying!
        
        **Next Steps:**
        1. Tailor your cover letter to highlight matching skills
        2. Prepare specific examples from your experience
        3. Research the company and role thoroughly
        4. Review the job requirements one more time
        """)
    
    elif match_result.match_percentage >= 60:
        st.info("""
        ### 👍 Good Match
        You have a solid foundation for this role. With some preparation, you can succeed.
        
        **Next Steps:**
        1. Focus on the missing skills in your application
        2. Highlight all matching experience
        3. Explain how you'll learn required skills
        4. Show enthusiasm for the role
        """)
    
    elif match_result.match_percentage >= 40:
        st.warning("""
        ### 🎯 Partial Match
        You have some relevant experience, but there are notable gaps.
        
        **Consider:**
        1. Whether you're willing to learn the missing skills
        2. How to position your existing skills
        3. If there are similar roles that match better
        4. Your long-term interest in this field
        """)
    
    else:
        st.error("""
        ### ❌ Limited Match
        This role may not be a good fit at this time.
        
        **Suggestions:**
        1. Look for entry-level or junior positions
        2. Develop the key missing skills first
        3. Find roles that value your current expertise
        4. Consider related positions in adjacent fields
        """)
    
    st.markdown("---")
    
    # Similar roles suggestion
    st.markdown("## 🔍 Skills Analysis")
    
    # Extract skills from resume and job
    resume_skills = [s.name for s in parsed_resume.skills] if parsed_resume.skills else []
    
    st.markdown("### Your Skills vs. Job Requirements")
    st.caption("Skills you have that are relevant:")
    st.write(", ".join(match_result.matching_skills[:5]) if match_result.matching_skills else "None identified")
    
    st.caption("Skills you should develop:")
    st.write(", ".join(match_result.missing_skills[:5]) if match_result.missing_skills else "None identified")

else:
    st.error("❌ Failed to analyze job match. Please try again.")

st.markdown("---")

# Additional features
st.markdown("## 📚 Understanding Job Fit")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **🎯 Match Percentage**
    
    Indicates how well your resume aligns with the job requirements:
    - 80%+: Excellent fit
    - 60-80%: Good fit
    - 40-60%: Partial fit
    - <40%: Limited fit
    """)

with col2:
    st.info("""
    **💼 Matching Skills**
    
    Skills you have that the job requires. The more matches, the better
    your chances of success in the role.
    """)

with col3:
    st.info("""
    **📈 Growth Areas**
    
    Skills to develop to be more competitive
    for this role or similar positions.
    """)

st.markdown("---")

# Save results
st.session_state.match_result = match_result

st.markdown("### 🔄 Next Steps")
col1, col2 = st.columns(2)
with col1:
    st.info("🎤 Go to **Interview Prep** to prepare for interviews")
with col2:
    st.info("📄 Upload a new resume or try other jobs")
