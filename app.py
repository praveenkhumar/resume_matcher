import streamlit as st
import tempfile
import os
from utils.parser import extract_text
from utils.matcher import analyze_resume_job_match

# Page configuration
st.set_page_config(
    page_title="AI Resume Skill Extractor & Job Matcher",
    page_icon="📄",
    layout="wide"
)

# Title and description
st.title("📄 AI Resume Skill Extractor & Job Matcher")
st.markdown("""
This application helps you analyze how well your resume matches a job description by:
- Extracting skills from your resume
- Comparing them with job requirements
- Providing a match score and recommendations
""")

# Sidebar for configuration
st.sidebar.header("Configuration")
extraction_method = st.sidebar.selectbox(
    "Skill Extraction Method",
    ["keyword", "ner"],
    help="Keyword: Uses predefined skill list. NER: Uses AI to detect skills."
)

# Main content
col1, col2 = st.columns(2)

with col1:
    st.header("📤 Resume Upload")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or DOCX)",
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX"
    )

    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_file_path = tmp_file.name

        try:
            # Extract text from resume
            resume_text = extract_text(temp_file_path)
            if resume_text.strip():
                st.text_area("Extracted Resume Text (Preview)", resume_text[:500] + "..." if len(resume_text) > 500 else resume_text, height=200)
            else:
                st.error("Could not extract text from the uploaded file. Please check the file format.")
                resume_text = ""
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            resume_text = ""
        finally:
            # Clean up temp file
            os.unlink(temp_file_path)
    else:
        resume_text = ""

with col2:
    st.header("💼 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="Paste the job description text here..."
    )

# Analysis button
if st.button("🔍 Analyze Match", type="primary", use_container_width=True):
    if not resume_text:
        st.error("Please upload a resume first.")
    elif not job_description.strip():
        st.error("Please enter a job description.")
    else:
        with st.spinner("Analyzing resume and job description..."):
            try:
                # Perform analysis
                results = analyze_resume_job_match(
                    resume_text,
                    job_description,
                    extraction_method=extraction_method
                )

                # Display results
                st.header("📊 Analysis Results")

                # Match Score
                col_score, col_metrics = st.columns([1, 2])

                with col_score:
                    st.metric("Match Score", f"{results['match_score']}%")

                    # Color coding for score
                    if results['match_score'] >= 80:
                        st.success("Excellent match! 🎉")
                    elif results['match_score'] >= 60:
                        st.warning("Good match, but room for improvement")
                    else:
                        st.error("Low match - consider skill development")

                with col_metrics:
                    st.metric("Resume Skills Found", len(results['resume_skills']))
                    st.metric("Job Skills Required", len(results['job_skills']))
                    st.metric("Skills Matched", len(results['matched_skills']))

                # Skills breakdown
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.subheader("✅ Matched Skills")
                    if results['matched_skills']:
                        for skill in results['matched_skills']:
                            st.success(f"✓ {skill}")
                    else:
                        st.info("No matching skills found")

                with col2:
                    st.subheader("❌ Missing Skills")
                    if results['missing_skills']:
                        for skill in results['missing_skills']:
                            st.error(f"✗ {skill}")
                    else:
                        st.success("All required skills found!")

                with col3:
                    st.subheader("📋 All Resume Skills")
                    if results['resume_skills']:
                        for skill in results['resume_skills']:
                            st.info(f"• {skill}")
                    else:
                        st.warning("No skills detected in resume")

                # Job Description Skills
                st.subheader("🎯 Job Description Skills")
                if results['job_skills']:
                    skill_cols = st.columns(min(4, len(results['job_skills'])))
                    for i, skill in enumerate(results['job_skills']):
                        col_idx = i % 4
                        with skill_cols[col_idx]:
                            if skill.lower() in [s.lower() for s in results['matched_skills']]:
                                skill_cols[col_idx].success(f"✓ {skill}")
                            else:
                                skill_cols[col_idx].error(f"✗ {skill}")
                else:
                    st.warning("No skills detected in job description")

                # Recommendations
                if results['recommendations']:
                    st.header("💡 Recommendations")
                    for rec in results['recommendations']:
                        st.info(rec)

            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.info("Please check your inputs and try again.")

# Footer
st.markdown("---")
st.markdown("""
**About this tool:**
- Uses NLP to extract skills from resumes and job descriptions
- Supports PDF and DOCX resume formats
- Provides detailed matching analysis and recommendations
- Built with Python, Streamlit, and spaCy
""")

# Hide Streamlit style
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)