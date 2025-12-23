"""
AI-Based Career & Resume Optimization System
Main Streamlit Application
"""

import streamlit as st
import google.generativeai as genai
import os

# Configure page
st.set_page_config(
    page_title="AI Career & Resume Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure API
@st.cache_resource
def init_api():
    """Initialize Google Gemini API."""
    try:
        GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            # Try to load from environment variable
            GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        
        if GOOGLE_API_KEY:
            genai.configure(api_key=GOOGLE_API_KEY)
            return True
        else:
            return False
    except Exception as e:
        st.error(f"API Configuration Error: {e}")
        return False


# Initialize API
if not init_api():
    st.error("⚠️ Google API Key not configured!")
    st.info("""
    **Setup Instructions:**
    
    1. Create a `.streamlit/secrets.toml` file in your project root
    2. Add your Google API key: `GOOGLE_API_KEY = "your-key-here"`
    3. Restart the Streamlit app
    
    **Get an API Key:**
    - Visit: https://makersuite.google.com/app/apikey
    - Sign in with your Google account
    - Create an API key
    """)
    st.stop()


# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .metric-card {
        background-color: #e7f3ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #e7f5e7;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">🚀 AI Career & Resume Optimizer</div>
<div class="subtitle">Elevate Your Career with AI-Powered Resume Analysis</div>
""", unsafe_allow_html=True)

# Introduction tabs
tab1, tab2, tab3 = st.tabs(["📌 Overview", "🎯 Features", "📊 How It Works"])

with tab1:
    st.markdown("""
    ## Welcome! 👋
    
    This comprehensive platform helps both **recruiters** and **job seekers** make better hiring and career decisions using AI-powered analysis.
    
    ### For Job Seekers 🧑‍💼
    - **Resume Analysis**: Get detailed feedback on your resume quality
    - **ATS Score**: Know how well your resume will pass automated screening
    - **Smart Suggestions**: Receive AI-powered improvement recommendations
    - **Job Matching**: Find roles that align with your skills
    - **Interview Prep**: Practice with AI-generated interview questions
    
    ### For Recruiters 👔
    - **Batch Screening**: Analyze multiple resumes against a job description
    - **Skill Matching**: Identify the best candidates automatically
    - **Interview Questions**: Generate tailored questions for candidates
    """)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 💼 Candidate Tools
        
        - **Resume Upload & Parsing**: Upload PDF/DOCX resumes
        - **ATS Score Analysis**: See your resume's ATS compatibility
        - **Skill Assessment**: Get detailed skill breakdown
        - **Content Suggestions**: Improve bullet points and wording
        """)
    
    with col2:
        st.markdown("""
        ### 👔 Recruiter Tools
        
        - **Batch Analysis**: Process multiple resumes quickly
        - **Job Description Matching**: Compare resumes to job specs
        - **Candidate Ranking**: Automatic scoring and ranking
        - **Interview Questions**: Generate role-specific questions
        """)

with tab3:
    st.markdown("""
    ### System Architecture
    
    ```
    Resume Upload → Parse & Extract → Analyze & Score → Generate Insights
         ↓              ↓                    ↓                ↓
       PDF/DOCX    Extract Skills    ATS Score         Suggestions
                   Extract Exp       Skill Match       Match Score
                   Extract Edu       Completeness      Interview Q's
    ```
    
    ### Key Technologies
    - **Google Gemini API**: Intelligent content parsing and analysis
    - **NLP Processing**: Keyword extraction and text analysis
    - **Rule-Based Scoring**: ATS compatibility assessment
    - **Streamlit**: Interactive user interface
    """)

# Navigation
st.sidebar.markdown("---")
st.sidebar.title("🗂️ Navigation")

pages = {
    "📄 Upload & Analyze": "pages/01_upload_resume.py",
    "🎯 ATS Score": "pages/02_ats_score.py",
    "💡 Resume Suggestions": "pages/03_resume_suggestions.py",
    "🎲 Job Matching": "pages/04_job_matching.py",
    "🎤 Interview Prep": "pages/05_interview_prep.py",
}

selected_page = st.sidebar.radio("Choose an option:", list(pages.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📚 About This Project
**AI-Based Career & Resume Optimization System**

A comprehensive final-year B.Tech project designed to help:
- Job seekers optimize their resumes
- Recruiters screen candidates efficiently
- Both parties make better career decisions

**Technology Stack:**
- Python, Streamlit, Google Gemini API
- NLP, Text Analysis, ML-based scoring
""")

# Main content area
st.markdown("---")

st.markdown("""
### Getting Started 🚀

1. **For Job Seekers**: Go to "Upload & Analyze" to start your resume analysis
2. **Check ATS Score**: See how well your resume performs in automated screening
3. **Get Suggestions**: Receive AI-powered recommendations for improvement
4. **Match Jobs**: Find roles that align with your skills
5. **Interview Prep**: Practice with AI-generated interview questions

### Key Insights
- Your resume is often screened by ATS (Applicant Tracking Systems) before humans see it
- Average ATS parse failure rate: 25% of resumes
- Keywords matter: 60% of hiring decisions depend on relevant keywords
- Optimization can increase your chances by up to 40%
""")

st.markdown("---")

# Footer
col1, col2, col3 = st.columns(3)
with col1:
    st.info("💡 **Tip**: Use realistic job descriptions for accurate analysis")
with col2:
    st.success("✅ **Data Privacy**: Your data is processed locally and not stored")
with col3:
    st.warning("⚠️ **Accuracy**: AI scores are estimations, not guarantees")
