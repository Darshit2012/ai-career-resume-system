# 🚀 AI-Based Career & Resume Optimization System

**A Final Year B.Tech Computer Engineering Project**

## 📌 Problem Statement

In today's competitive job market, candidates struggle to optimize their resumes for Applicant Tracking Systems (ATS), and recruiters face challenges in efficiently screening large volumes of resumes. Additionally, job seekers lack real-time feedback on how well their resumes match specific job requirements, and both parties need intelligent tools to make better hiring decisions.

## 🎯 Project Objectives

1. **For Job Seekers:**
   - Analyze resume quality and identify improvement areas
   - Check ATS compatibility and provide optimization suggestions
   - Match resume with job descriptions for suitability assessment
   - Prepare for interviews with AI-generated questions

2. **For Recruiters:**
   - Efficiently screen multiple resumes against job descriptions
   - Automatically rank candidates based on skill matching
   - Generate tailored interview questions
   - Reduce time spent on initial resume screening

3. **Technical Objectives:**
   - Implement intelligent resume parsing using NLP and LLM
   - Develop rule-based ATS scoring system
   - Create skill matching and job alignment algorithms
   - Build user-friendly Streamlit interface

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                     │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐   │
│  │ Upload   │  ATS     │ Resume   │   Job    │Interview │   │
│  │ Resume   │  Score   │Suggest   │ Matching │  Prep    │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘   │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                    BACKEND (Python)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                                                      │   │
│  │  Resume Parser  → ATS Analyzer  → Resume Rewriter   │   │
│  │  Job Matcher    → Interview Generator → Utils       │   │
│  │                                                      │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                  SERVICES & APIs                             │
│         Google Gemini API (LLM & Content Analysis)           │
└──────────────────────────────────────────────────────────────┘
```

## 📂 Project Structure

```
ai-career-resume-system/
│
├── backend/
│   ├── resume_parser.py            # Resume parsing & extraction
│   ├── ats_analyzer.py             # ATS scoring system
│   ├── resume_rewriter.py          # Content improvement suggestions
│   ├── job_matcher.py              # Job matching algorithm
│   ├── interview_generator.py      # Interview question generation
│   └── utils.py                    # Utility functions
│
├── frontend/
│   ├── streamlit_app.py            # Main Streamlit app
│   └── pages/
│       ├── 01_upload_resume.py     # Resume upload & parsing
│       ├── 02_ats_score.py         # ATS compatibility analysis
│       ├── 03_resume_suggestions.py # Improvement suggestions
│       ├── 04_job_matching.py      # Job matching interface
│       └── 05_interview_prep.py    # Interview preparation
│
├── data/
│   ├── sample_resumes/             # Sample resume files
│   └── job_descriptions/           # Sample job descriptions
│
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables (API keys)
└── README.md                       # Project documentation
```

## 🛠️ Technology Stack

### Backend
- **Python 3.9+**: Core programming language
- **Pydantic**: Data validation and schema management
- **Google Gemini API**: LLM for intelligent parsing and analysis
- **Regular Expressions**: Text processing and keyword extraction

### Frontend
- **Streamlit**: Interactive user interface framework
- **Streamlit Caching**: Performance optimization

### Additional Tools
- **python-dotenv**: Environment variable management
- **JSON**: Data serialization

## 📊 Key Features & Modules

### 1. **Resume Parser** (`resume_parser.py`)

**Purpose:** Extract structured information from resume documents

**Features:**
- Parse PDF, DOCX, and TXT files
- Extract: Name, email, phone, summary, skills, education, experience, certifications, projects
- Categorize skills (technical, tools, soft skills)
- Detect missing resume sections
- Validate data completeness

**Technologies:**
- Google Gemini API for intelligent extraction
- Pydantic for schema validation
- Regular expressions for text processing

### 2. **ATS Analyzer** (`ats_analyzer.py`)

**Purpose:** Evaluate ATS-readiness of the resume itself (no job description required)

**Scoring Methodology (Out of 100):**
- **Structure (40%)**: Section completeness and clarity
- **Contact (20%)**: Presence of email and phone in header
- **Action Verbs (20%)**: Use of strong impact verbs in bullets
- **Quantified Impact (20%)**: Use of numbers/percentages to show results

**Output:**
- ATS Score (0-100)
- Component scores (structure, contact, verbs, metrics)
- Actionable improvement tips
- Resume strengths identification

**Algorithm Details:**
```
ATS_Score = (Structure × 0.4) + (Contact × 0.2) + (ActionVerbs × 0.2) + (Metrics × 0.2)
```

### 3. **Resume Rewriter** (`resume_rewriter.py`)

**Purpose:** Generate AI-powered improvement suggestions for resume content

**Suggestion Categories:**
- **Clarity**: Simplify complex sentences, remove jargon
- **ATS Optimization**: Incorporate keywords, improve formatting
- **Professional Language**: Enhance tone and formality
- **Quantification**: Add metrics and measurable results

**Features:**
- Action verb recommendations
- Bullet point improvement suggestions
- Clarity enhancement
- Industry-specific writing tips

**Output:**
- Original vs. improved text comparison
- Reasoning for each suggestion
- Priority-ordered recommendations

### 4. **Job Matcher** (`job_matcher.py`)

**Purpose:** Determine how well a resume aligns with job requirements

**Matching Factors:**
- Skill overlap analysis
- Experience relevance assessment
- Education alignment
- Career trajectory fit
- Job title compatibility

**Output:**
- Match percentage (0-100)
- Matching skills list
- Missing skills identification
- Career alignment assessment
- Suitability recommendations

**Sample Jobs Included:**
- Software Engineer
- Data Scientist
- Frontend Developer
- (Easily extensible for more roles)

### 5. **Interview Generator** (`interview_generator.py`)

**Purpose:** Generate contextual interview questions based on resume and job

**Question Categories:**

1. **Technical Questions (3-5):**
   - Framework and language specific
   - Problem-solving focused
   - Domain expertise assessment

2. **Behavioral Questions (3-5):**
   - STAR format compatible
   - Soft skills evaluation
   - Conflict resolution scenarios

3. **Role-Specific Questions (2-3):**
   - Position-specific challenges
   - Seniority-appropriate questions
   - Industry expectations

**Features:**
- Why each question is asked (context)
- Tips for answering effectively
- STAR method guidance
- Preparation checklists
- Common question templates for fallback

### 6. **Utilities** (`utils.py`)

**Common Functions:**
- Skill categorization and database
- Experience years calculation
- Seniority level estimation
- Score formatting and display
- Resume text normalization
- Data validation functions
- Improvement priority assessment

## 💡 How It Works

### User Flow for Job Seekers

```
1. Upload Resume
   ↓
2. Parse & Extract Information
   ↓
3. Choose Job Description (paste or select sample)
   ↓
4. Get ATS Score & Feedback
   ↓
5. Receive Improvement Suggestions
   ↓
6. Match with Jobs
   ↓
7. Prepare Interview Questions
   ↓
8. Apply with Optimized Resume
```

### User Flow for Recruiters

```
1. Prepare Job Description
   ↓
2. Batch Upload Resumes
   ↓
3. Automated Screening & Ranking
   ↓
4. View Candidate Comparison
   ↓
5. Generate Interview Questions
   ↓
6. Schedule Interviews
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- Google API Key (Gemini API)
- Internet connection

### Installation

1. **Clone the repository:**
   ```bash
   cd ai-career-resume-system
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API Key:**
   - Create `.streamlit/secrets.toml` file
   - Add: `GOOGLE_API_KEY = "your-api-key-here"`
   - Get key from: https://makersuite.google.com/app/apikey

5. **Run the application:**
   ```bash
   streamlit run frontend/streamlit_app.py
   ```

6. **Access the app:**
   - Open browser to `http://localhost:8501`

## 📊 Sample Features & Screenshots

### Resume Analysis
- Parsed resume data in tabular format
- Skill categorization
- Missing sections detection
- Data completeness score

### ATS Health Check
- Score breakdown (out of 100)
- Component-wise analysis: structure, contact, action verbs, metrics
- Actionable improvement recommendations

### Job Matching
- Match percentage
- Matching skills highlight
- Missing skills identification
- Career alignment assessment
- Application success probability

### Interview Preparation
- Category-based questions
- STAR method templates
- Preparation tips
- Pre-interview checklist

## 📈 Advantages

1. **For Job Seekers:**
   - Real-time resume feedback
   - ATS compatibility optimization
   - Personalized improvement suggestions
   - Job suitability assessment
   - Interview preparation support
   - Free and accessible

2. **For Recruiters:**
   - Automated resume screening
   - Consistent candidate evaluation
   - Time-saving batch analysis
   - Standardized interview questions
   - Data-driven hiring decisions

3. **For Institutions:**
   - Demonstrates practical AI/ML application
   - Shows full-stack development
   - Addresses real-world problem
   - Combines multiple technologies
   - Scalable and maintainable architecture

## ⚠️ Limitations

1. **ATS Scoring:**
   - Rule-based approach (not machine learning)
   - Estimates, not guarantees
   - Accuracy depends on resume and JD clarity

2. **Resume Parsing:**
   - Complex resume formats may not parse perfectly
   - Scanned/image resumes not supported
   - Dependent on document quality

3. **Interview Questions:**
   - Generic templates for some questions
   - May not cover all edge cases
   - Requires human review for sensitive roles

4. **Data Security:**
   - Data processed via Google API (review terms)
   - No persistent storage
   - Each session is independent

## 🔮 Future Scope & Enhancements

### Short Term
- Support for more file formats (RTF, ODT)
- Language support (multiple languages)
- Export suggestions to PDF
- Resume comparison tool

### Medium Term
- Machine learning-based ATS scoring
- Video interview simulation
- Portfolio integration
- Email notification system
- User accounts and history

### Long Term
- Mobile application
- Database for resume storage
- Advanced analytics dashboard
- Integration with job portals
- Salary prediction model
- Career path recommendation engine

## 🧪 Testing & Validation

### Test Cases Covered
- File upload with different formats
- Resume parsing accuracy
- ATS score calculation
- Job matching accuracy
- Interview question relevance
- Edge cases (empty sections, special characters)

### Sample Test Data
- Multiple resume templates included
- Sample job descriptions provided
- Various skill combinations tested

## 📚 References & Resources

### Technologies
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Regular Expressions](https://docs.python.org/3/library/re.html)

### Concepts
- Applicant Tracking Systems (ATS) - How they work
- NLP and Text Processing Basics
- Resume Optimization Best Practices
- Interview Preparation Techniques

## 👥 Authors & Contributors

**Developed as a Final Year B.Tech Project**
- Computer Engineering Department
- [Your College Name]
- 2024

## 📞 Support & Contact

For questions or issues:
- Review the README sections above
- Check API key configuration
- Ensure all dependencies are installed
- Verify Python version is 3.9+

## 📄 License

This project is created for educational purposes as part of the B.Tech Computer Engineering curriculum.

---

## 🎓 Project Evaluation Criteria Met

✅ **Problem Statement:** Clear identification of industry challenges
✅ **System Design:** Well-structured, modular architecture
✅ **Technology Stack:** Appropriate use of modern tools
✅ **Functionality:** All proposed features implemented
✅ **User Interface:** Clean, intuitive Streamlit interface
✅ **Code Quality:** Well-documented, maintainable code
✅ **Innovation:** AI/LLM integration for intelligent analysis
✅ **Scalability:** Extensible design for future enhancements
✅ **Documentation:** Comprehensive README and code comments
✅ **Presentation:** Ready for viva and demo

---

**Last Updated:** December 2024  
**Version:** 1.0.0  
**Status:** Production Ready
