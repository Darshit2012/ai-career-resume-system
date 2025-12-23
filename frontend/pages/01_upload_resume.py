"""
Upload & Resume Analysis Page
"""

import streamlit as st
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from resume_parser import parse_resume_from_file, detect_missing_sections, categorize_skills
from utils import resume_dict_to_text, validate_resume_data

st.set_page_config(page_title="Upload & Analyze Resume", page_icon="📄", layout="wide")

st.title("📄 Upload & Analyze Your Resume")

st.markdown("""
Upload your resume to get started. Supported formats: PDF, DOCX, TXT
""")

# File uploader
uploaded_file = st.file_uploader(
    "Choose your resume file",
    type=["pdf", "docx", "txt"],
    help="Upload a PDF, DOCX, or TXT file"
)

if uploaded_file:
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    # Parse resume
    with st.spinner("🔍 Parsing your resume..."):
        parsed_resume = parse_resume_from_file(uploaded_file)
    
    if parsed_resume:
        # Convert to dictionary for easier handling
        resume_dict = parsed_resume.model_dump()
        
        # Store in session state for other pages
        st.session_state.parsed_resume = parsed_resume
        st.session_state.resume_dict = resume_dict
        st.session_state.uploaded_file = uploaded_file
        
        # Tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Parsed Data",
            "👤 Contact Info",
            "🛠️ Skills",
            "📚 Education",
            "💼 Experience"
        ])
        
        with tab1:
            st.subheader("Resume Overview")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📝 Name", parsed_resume.name or "Not found")
            with col2:
                st.metric("🛠️ Skills Count", len(parsed_resume.skills) or 0)
            with col3:
                st.metric("📚 Education", len(parsed_resume.education) or 0)
            
            # Validation
            is_valid, missing, completeness = validate_resume_data(resume_dict)
            
            st.markdown("### Resume Completeness")
            st.progress(min(completeness / 100, 1.0))
            st.caption(f"Completeness Score: {completeness}%")
            
            if missing:
                st.warning(f"Missing sections: {', '.join(missing)}")
            else:
                st.success("All major sections are present!")
            
            # Missing sections analysis
            missing_sections = detect_missing_sections(parsed_resume)
            st.markdown("### Missing/Weak Sections")
            for section, is_missing in missing_sections.items():
                if is_missing:
                    st.info(f"⚠️ {section.replace('_', ' ').title()}: Consider adding or expanding")
        
        with tab2:
            st.subheader("Contact Information")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Name:**", parsed_resume.name or "Not found")
                st.write("**Email:**", parsed_resume.email or "Not found")
            
            with col2:
                st.write("**Phone:**", parsed_resume.phone or "Not found")
                if parsed_resume.summary:
                    st.write("**Summary:**", parsed_resume.summary)
        
        with tab3:
            st.subheader("Skills Analysis")
            
            if parsed_resume.skills:
                # Categorize skills
                skills = parsed_resume.skills
                
                # Display by category
                categorized = categorize_skills(skills)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("#### 💻 Technical Skills")
                    if categorized['technical']:
                        for skill in categorized['technical']:
                            st.write(f"• {skill}")
                    else:
                        st.caption("None found")
                
                with col2:
                    st.markdown("#### 🛠️ Tools")
                    if categorized['tools']:
                        for skill in categorized['tools']:
                            st.write(f"• {skill}")
                    else:
                        st.caption("None found")
                
                with col3:
                    st.markdown("#### 👥 Soft Skills")
                    if categorized['soft_skills']:
                        for skill in categorized['soft_skills']:
                            st.write(f"• {skill}")
                    else:
                        st.caption("None found")
                
                # All skills in tags
                st.markdown("#### All Skills")
                skills_text = ", ".join([s.name for s in skills])
                st.write(skills_text)
            else:
                st.warning("No skills found in resume")
        
        with tab4:
            st.subheader("Education")
            
            if parsed_resume.education:
                for i, edu in enumerate(parsed_resume.education, 1):
                    with st.expander(f"📚 Education {i}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Degree:**", edu.degree or "Not specified")
                            st.write("**Institution:**", edu.institution or "Not specified")
                        with col2:
                            st.write("**Graduation Year:**", edu.graduation_year or "Not specified")
                            st.write("**GPA:**", edu.gpa or "Not specified")
            else:
                st.warning("No education information found")
        
        with tab5:
            st.subheader("Work Experience")
            
            if parsed_resume.experience:
                for i, exp in enumerate(parsed_resume.experience, 1):
                    with st.expander(f"💼 Experience {i}: {exp.title}"):
                        st.write("**Position:**", exp.title or "Not specified")
                        st.write("**Company:**", exp.company or "Not specified")
                        st.write("**Duration:**", exp.duration or "Not specified")
                        if exp.description:
                            st.write("**Responsibilities:**")
                            st.write(exp.description)
            else:
                st.warning("No work experience found")
        
        # Additional sections
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if parsed_resume.certifications:
                st.markdown("### 🏆 Certifications")
                for cert in parsed_resume.certifications:
                    st.write(f"✓ {cert}")
        
        with col2:
            if parsed_resume.projects:
                st.markdown("### 🎯 Projects")
                for project in parsed_resume.projects:
                    st.write(f"• {project}")
        
        # Full resume text view
        st.markdown("---")
        with st.expander("📖 View Full Resume Text"):
            full_text = resume_dict_to_text(resume_dict)
            st.text(full_text)
        
        # Export options
        st.markdown("---")
        st.markdown("### 💾 Next Steps")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("📊 Go to **ATS Score** to analyze ATS compatibility")
        
        with col2:
            st.info("💡 Go to **Resume Suggestions** for improvement tips")
        
        with col3:
            st.info("🎲 Go to **Job Matching** to find suitable roles")
        
        # Display JSON for debugging
        with st.expander("🔧 View Parsed JSON (Debug)"):
            st.json(resume_dict)
    
    else:
        st.error("❌ Failed to parse resume. Please try a different file.")
        st.info("Ensure the file is a valid PDF, DOCX, or TXT document.")

else:
    st.info("👆 Upload a resume file to get started")
    
    # Show example format
    with st.expander("📋 What Should Your Resume Contain?"):
        st.markdown("""
        For best results, ensure your resume includes:
        
        - **Contact Information**: Name, email, phone
        - **Professional Summary**: 2-3 line career overview
        - **Work Experience**: Job title, company, duration, responsibilities
        - **Education**: Degree, institution, graduation year
        - **Skills**: Technical and soft skills
        - **Optional**: Certifications, projects, publications
        
        **Pro Tips:**
        - Keep it to 1-2 pages
        - Use clear section headings
        - Include quantifiable achievements
        - Use relevant keywords for your industry
        - Maintain consistent formatting
        """)
