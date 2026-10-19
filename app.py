import re
from io import BytesIO

import streamlit as st
from pypdf import PdfReader

# ---------------------------------------------------------
# AI-Assisted Skill Assessment Tool for Recognition of Prior
# Learning (RPL) - Student Hackathon Prototype
# ---------------------------------------------------------

st.set_page_config(
    page_title="RPL Skill Assessment",
    page_icon="🎓",
    layout="wide",
)

# Simple, predefined skill list for the demo.
# Add or edit keywords to suit your chosen RPL domain.
REQUIRED_SKILLS = {
    "Python Programming": ["python", "python programming", "pandas", "numpy"],
    "Web Development": ["html", "css", "javascript", "streamlit", "web development"],
    "Database Management": ["sql", "mysql", "postgresql", "database", "database management"],
    "Communication": ["communication", "presentation", "client interaction", "team communication"],
    "Problem Solving": ["problem solving", "troubleshooting", "debugging", "analytical"],
    "Project Management": ["project management", "planning", "scheduling", "project coordination"],
    "Data Analysis": ["data analysis", "excel", "power bi", "data visualization"],
    "Teamwork": ["teamwork", "team collaboration", "collaborated", "worked in a team"],
}


def extract_pdf_text(uploaded_file):
    """Extract selectable text from an uploaded PDF."""
    try:
        reader = PdfReader(BytesIO(uploaded_file.getvalue()))
        pages_text = []
        for page in reader.pages:
            pages_text.append(page.extract_text() or "")
        return "\n".join(pages_text).strip(), None
    except Exception as error:
        return "", f"Could not read this PDF: {error}"


def identify_skills(text):
    """Identify skills by checking predefined keywords in the text."""
    searchable_text = re.sub(r"\s+", " ", text.lower())
    matched = []
    missing = []

    for skill, keywords in REQUIRED_SKILLS.items():
        found = any(keyword.lower() in searchable_text for keyword in keywords)
        if found:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing


# -------------------------- Styling --------------------------
st.markdown(
    """
    <style>
    .stApp { background: #ffffff; }
    h1, h2, h3 { color: #12315a !important; }
    .subtitle { color: #52657d; font-size: 1.05rem; }
    .info-card {
        background: #f4f7fb;
        border: 1px solid #dce5f0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
    }
    .small-note { color: #52657d; font-size: 0.88rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("AI-Assisted Skill Assessment Tool")
st.subheader("Recognition of Prior Learning (RPL)")
st.markdown(
    '<p class="subtitle">A simple prototype that identifies skills from a CV '
    'and work-experience description, then compares them with a predefined skill list.</p>',
    unsafe_allow_html=True,
)

st.info(
    "Hackathon demo: this prototype uses keyword matching, not a trained AI model. "
    "Results are indicative and should be reviewed by a human assessor."
)

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("### 1. Provide your details")
    uploaded_cv = st.file_uploader(
        "Upload CV (PDF only)",
        type=["pdf"],
        help="Upload a PDF CV with selectable text. Scanned/image-only PDFs may not be readable.",
    )
    experience = st.text_area(
        "Work experience",
        placeholder=(
            "Example: I used Python to build a Streamlit website, worked with SQL databases, "
            "analysed data in Excel, and collaborated with a team to solve problems."
        ),
        height=180,
    )
    assess_clicked = st.button("Assess Skills", type="primary", use_container_width=True)

with right:
    st.markdown("### 2. Required skills")
    st.markdown(
        '<div class="info-card">The demo compares the CV and work-experience text '
        'against these skill areas:</div>',
        unsafe_allow_html=True,
    )
    for skill in REQUIRED_SKILLS:
        st.markdown(f"- {skill}")

if assess_clicked:
    cv_text = ""
    pdf_error = None

    if uploaded_cv is not None:
        cv_text, pdf_error = extract_pdf_text(uploaded_cv)

    combined_text = f"{cv_text}\n{experience}".strip()

    if pdf_error:
        st.warning(pdf_error)

    if not combined_text:
        st.warning("Please upload a readable PDF CV or enter your work experience before assessing.")
    else:
        matched_skills, missing_skills = identify_skills(combined_text)
        total_skills = len(REQUIRED_SKILLS)
        score = round((len(matched_skills) / total_skills) * 100) if total_skills else 0

        st.divider()
        st.header("Skill Assessment Report")

        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Skills Matched", len(matched_skills))
        metric2.metric("Skills to Develop", len(missing_skills))
        metric3.metric("Coverage (demo)", f"{score}%")

        st.progress(score / 100)

        match_col, missing_col = st.columns(2, gap="large")
        with match_col:
            st.markdown("### ✅ Matching skills")
            if matched_skills:
                for skill in matched_skills:
                    st.success(skill)
            else:
                st.write("No matching skills were detected from the supplied text.")

        with missing_col:
            st.markdown("### 📌 Missing / not detected")
            if missing_skills:
                for skill in missing_skills:
                    st.warning(skill)
            else:
                st.success("All predefined skills were detected.")

        st.markdown("### Summary")
        if matched_skills:
            st.write(
                "The supplied information mentions "
                + ", ".join(matched_skills)
                + "."
            )
        else:
            st.write("The supplied information did not contain the configured skill keywords.")

        st.caption(
            "Important: 'Missing / not detected' means the keyword was not found in the supplied text. "
            "It does not prove that the applicant lacks the skill. The coverage percentage is a simple "
            "demo indicator, not an official RPL score or qualification decision."
        )

st.divider()
st.caption("Smart India Hackathon 2026 | Student prototype | Python + Streamlit")
