"""
Interview Preparation Page
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from interview_generator import (
    generate_interview_questions,
    generate_simple_questions
)

st.set_page_config(page_title="Interview Prep", page_icon="🎤", layout="wide")

st.title("🎤 Interview Preparation")

st.markdown("""
Prepare for interviews with AI-generated questions tailored to your background and target role.
""")

# Check if resume is loaded
if 'parsed_resume' not in st.session_state:
    st.warning("⚠️ No resume loaded yet")
    st.info("Please upload a resume on the **Upload & Analyze** page first")
    st.stop()

parsed_resume = st.session_state.parsed_resume
resume_dict = st.session_state.resume_dict

# Get job information
st.markdown("### 🎯 Provide Job Information")

col1, col2 = st.columns(2)

with col1:
    job_title = st.text_input(
        "Job Title",
        placeholder="e.g., Senior Software Engineer",
        value=st.session_state.get('interview_job_title', '')
    )
    st.session_state.interview_job_title = job_title

with col2:
    company_name = st.text_input(
        "Company Name (optional)",
        placeholder="e.g., Tech Corp",
        value=st.session_state.get('interview_company', '')
    )
    st.session_state.interview_company = company_name

job_description = st.text_area(
    "Job Description (optional)",
    height=200,
    placeholder="Paste the job description for more targeted questions...",
    key="interview_jd"
)

if not job_title:
    st.info("👆 Enter at least a job title to proceed")
    st.stop()

# Generate questions
with st.spinner("🎤 Generating interview questions..."):
    if job_description:
        # Use AI-generated questions if job description is provided
        interview_set = generate_interview_questions(
            resume_dict,
            job_description,
            job_title,
            company_name
        )
    else:
        # Use template-based questions
        skills = [s.name for s in parsed_resume.skills] if parsed_resume.skills else []
        interview_set = generate_simple_questions(skills, job_title)

if interview_set:
    st.markdown("---")
    st.markdown(f"## 🎤 Interview Questions for {job_title}")
    
    if company_name:
        st.markdown(f"**Company:** {company_name}")
    
    # Tabs for question categories
    tab1, tab2, tab3, tab4 = st.tabs([
        f"💻 Technical ({len(interview_set.technical_questions)})",
        f"👥 Behavioral ({len(interview_set.behavioral_questions)})",
        f"🎯 Role-Specific ({len(interview_set.role_specific_questions)})",
        f"📋 Preparation Tips"
    ])
    
    with tab1:
        st.markdown("### 💻 Technical Questions")
        st.markdown("""
        Technical questions assess your knowledge, problem-solving abilities, and expertise in relevant technologies.
        
        **Tips for answering:**
        - Explain your thinking process clearly
        - Don't just give answers, show how you solve problems
        - Use real examples from your experience
        - Ask for clarification if needed
        """)
        
        for i, question in enumerate(interview_set.technical_questions, 1):
            with st.expander(f"Q{i}: {question.question[:60]}..."):
                st.markdown("**Question:**")
                st.write(question.question)
                
                st.markdown("**Why this is asked:**")
                st.info(question.why_asked)
                
                if question.tip:
                    st.markdown("**Tip for answering:**")
                    st.success(question.tip)
                
                # Answer space
                st.markdown("---")
                answer = st.text_area(
                    "Your answer (practice):",
                    height=100,
                    key=f"tech_answer_{i}",
                    placeholder="Type your answer here to practice..."
                )
                if answer:
                    st.success("✓ Keep this answer prepared!")
    
    with tab2:
        st.markdown("### 👥 Behavioral Questions")
        st.markdown("""
        Behavioral questions use the STAR method to understand how you've handled situations.
        
        **STAR Method:**
        - **Situation:** Set the context
        - **Task:** Explain what was needed
        - **Action:** Describe what you did
        - **Result:** Share the outcome and learnings
        """)
        
        for i, question in enumerate(interview_set.behavioral_questions, 1):
            with st.expander(f"Q{i}: {question.question[:60]}..."):
                st.markdown("**Question:**")
                st.write(question.question)
                
                st.markdown("**Why this is asked:**")
                st.info(question.why_asked)
                
                if question.tip:
                    st.markdown("**Tip for answering:**")
                    st.success(question.tip)
                
                # STAR template
                st.markdown("---")
                st.markdown("**STAR Template:**")
                col1, col2 = st.columns(2)
                with col1:
                    situation = st.text_area(
                        "Situation:",
                        height=80,
                        key=f"star_s_{i}",
                        placeholder="What was the context?"
                    )
                    task = st.text_area(
                        "Task:",
                        height=80,
                        key=f"star_t_{i}",
                        placeholder="What did you need to do?"
                    )
                
                with col2:
                    action = st.text_area(
                        "Action:",
                        height=80,
                        key=f"star_a_{i}",
                        placeholder="What did you do?"
                    )
                    result = st.text_area(
                        "Result:",
                        height=80,
                        key=f"star_r_{i}",
                        placeholder="What was the outcome?"
                    )
    
    with tab3:
        st.markdown("### 🎯 Role-Specific Questions")
        st.markdown("""
        These questions are tailored to your specific role and background.
        """)
        
        for i, question in enumerate(interview_set.role_specific_questions, 1):
            with st.expander(f"Q{i}: {question.question[:60]}..."):
                st.markdown("**Question:**")
                st.write(question.question)
                
                st.markdown("**Why this is asked:**")
                st.info(question.why_asked)
                
                if question.tip:
                    st.markdown("**Tip for answering:**")
                    st.success(question.tip)
                
                # Answer space
                st.markdown("---")
                answer = st.text_area(
                    "Your answer (practice):",
                    height=100,
                    key=f"role_answer_{i}",
                    placeholder="Type your answer here to practice..."
                )
                if answer:
                    st.success("✓ Great! Practice this answer multiple times.")
    
    with tab4:
        st.markdown("### 📋 Interview Preparation Tips")
        
        st.markdown("#### General Preparation")
        st.markdown("""
        - Research the company: mission, values, products, recent news
        - Study the job description thoroughly
        - Prepare stories from your experience (use STAR)
        - Practice your answers out loud (not just in your head)
        - Have questions ready to ask them
        - Get good sleep before the interview
        """)
        
        st.markdown("#### Interview Preparation Tips")
        for tip in interview_set.preparation_tips:
            st.success(tip)
        
        st.markdown("#### Day Before Checklist")
        
        checklist_items = [
            ("Research company thoroughly", ""),
            ("Review job description", ""),
            ("Prepare 2-3 success stories", ""),
            ("Organize documents (resume, certifications, portfolio)", ""),
            ("Plan your route to the interview location", ""),
            ("Prepare professional outfit", ""),
            ("Get questions ready to ask", ""),
            ("Test video/audio if it's virtual", ""),
            ("Get good sleep", ""),
            ("Eat a good breakfast", ""),
        ]
        
        st.markdown("**Day Before Checklist:**")
        checklist_state = st.session_state.get("interview_checklist", {})
        
        for item, _ in checklist_items:
            checklist_state[item] = st.checkbox(item, value=checklist_state.get(item, False))
        
        st.session_state.interview_checklist = checklist_state
        
        checked = sum(1 for v in checklist_state.values() if v)
        st.caption(f"Completed: {checked}/{len(checklist_items)}")
        
        st.markdown("---")
        
        st.markdown("#### Common Questions to Ask the Interviewer")
        st.markdown("""
        Always prepare thoughtful questions:
        
        1. **About the role:**
            - "What does a typical day look like?"
            - "What are the biggest challenges in this role?"
            - "How does this role contribute to the team/company?"
        
        2. **About the team:**
            - "What's the team size and structure?"
            - "How do you measure success in this position?"
            - "What's the culture like on this team?"
        
        3. **About career growth:**
            - "What are opportunities for professional development?"
            - "How often do performance reviews happen?"
            - "What's the typical career progression?"
        
        4. **About the company:**
            - "What's the company's vision for the next 3-5 years?"
            - "What sets your company apart from competitors?"
            - "What do you enjoy most about working here?"
        
        **Avoid asking about:**
        - Salary or benefits (until an offer)
        - Company problems you haven't researched
        - Information easily found online
        """)

else:
    st.error("❌ Failed to generate interview questions. Please try again.")

st.markdown("---")

# Interview tips
st.markdown("## 📚 Interview Success Tips")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **⏱️ Timing**
    
    - Arrive 10-15 minutes early
    - Aim for 30-60 min duration
    - Answer questions concisely (2-3 min)
    - Ask 2-3 questions at the end
    """)

with col2:
    st.info("""
    **💬 Communication**
    
    - Speak clearly and confidently
    - Make eye contact
    - Listen carefully to questions
    - Ask for clarification if needed
    - Avoid filler words ("um", "uh")
    """)

with col3:
    st.info("""
    **📊 Demonstration**
    
    - Show enthusiasm for the role
    - Provide specific examples
    - Quantify your achievements
    - Show growth mindset
    - Express willingness to learn
    """)

st.markdown("---")

st.markdown("## 🎯 Post-Interview")

st.markdown("""
After the interview:

1. **Send a thank you email** (within 24 hours)
   - Reference specific points from the conversation
   - Reiterate your interest in the role
   - Add any additional information you forgot to mention

2. **Reflect and improve**
   - What went well?
   - What could be improved?
   - Did you answer all questions adequately?

3. **Wait for feedback**
   - Companies typically respond within 1-2 weeks
   - Follow up if you don't hear back after a week

4. **Continue applying**
   - Don't put all eggs in one basket
   - Keep applying to other positions
   - Interview with other companies
""")

st.markdown("---")

st.markdown("### 💪 You've Got This!")
st.balloons()

st.success("""
Remember:
- Interviews are conversations, not interrogations
- They want to like you as much as you want to work there
- Preparation builds confidence
- Practice makes perfect

Good luck with your interview! 🚀
""")
