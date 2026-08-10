import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
import pypdf


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Internship Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# =========================================================
# HELPER: RESUME PARSER (NLP KEYWORD EXTRACTOR)
# =========================================================

def extract_skills_from_resume(uploaded_file):
    extracted_text = ""
    try:
        if uploaded_file.name.endswith(".pdf"):
            reader = pypdf.PdfReader(uploaded_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + " "
        else:
            extracted_text = uploaded_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading resume file: {e}")
        return []

    KNOWN_SKILLS = [
        "python", "sql", "pandas", "numpy", "java", "c++", "c#", "machine learning",
        "data analysis", "data science", "html", "css", "javascript", "react",
        "node", "django", "flask", "power bi", "tableau", "aws", "cloud", "docker",
        "kubernetes", "cybersecurity", "database", "git", "nlp", "deep learning",
        "computer vision", "tensorflow", "pytorch", "excel", "r", "spark", "hadoop",
        "bash", "linux", "scikit-learn", "matplotlib", "seaborn"
    ]

    extracted_skills = []
    text_lower = extracted_text.lower()
    for s in KNOWN_SKILLS:
        if s in text_lower and s not in extracted_skills:
            extracted_skills.append(s)

    return extracted_skills


# =========================================================
# MODERN CUSTOM CSS STYLING
# =========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .sub-header {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }

    .skill-tag {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 6px;
        margin-top: 4px;
    }

    .skill-gap-tag {
        display: inline-block;
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 6px;
        margin-top: 4px;
    }

    .badge-excellent {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 700;
    }

    .badge-good {
        display: inline-block;
        background: rgba(59, 130, 246, 0.15);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 700;
    }

    .badge-partial {
        display: inline-block;
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 700;
    }

    .apply-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: #ffffff !important;
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: 600;
        text-decoration: none !important;
        font-size: 0.9rem;
        box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.39);
        transition: all 0.2s ease;
        margin-top: 10px;
    }
    
    .apply-btn:hover {
        transform: scale(1.03);
        box-shadow: 0 6px 20px 0 rgba(79, 70, 229, 0.55);
    }

    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 16px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD INTERNSHIP DATA
# =========================================================

df = pd.read_csv("internships.csv")
internships = df.to_dict("records")


# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

if "search_done" not in st.session_state:
    st.session_state.search_done = False

if "qr_bytes" not in st.session_state:
    st.session_state.qr_bytes = None


# =========================================================
# TITLE & HEADER
# =========================================================

st.markdown('<div class="main-header">🎓 Internship Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Enter your profile details or upload your resume to discover personalized internship opportunities tailored to your skills and preferences.</div>', unsafe_allow_html=True)

st.divider()


# =========================================================
# STUDENT DETAILS FORM
# =========================================================

st.subheader("👤 Student Profile")

# Resume File Uploader Feature
uploaded_file = st.file_uploader(
    "📄 Upload Resume (PDF or TXT) to Auto-Extract Skills",
    type=["pdf", "txt"],
    key="resume_uploader"
)

default_skills = ""
if uploaded_file is not None:
    extracted = extract_skills_from_resume(uploaded_file)
    if extracted:
        default_skills = ", ".join(extracted)
        st.info(f"✨ Auto-extracted {len(extracted)} skills from resume: **{default_skills}**")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "Enter your name",
        key="student_name"
    )

    branch = st.text_input(
        "Enter your branch",
        key="student_branch"
    )

with col2:
    skills = st.text_input(
        "Enter your skills",
        value=default_skills if default_skills else st.session_state.get("student_skills", ""),
        placeholder="Example: Python, SQL, Pandas",
        key="student_skills"
    )

    domain = st.selectbox(
        "Preferred Domain",
        [
            "Data Science",
            "Data Analytics",
            "Machine Learning",
            "Artificial Intelligence",
            "Web Development",
            "Software Development",
            "Database",
            "Data Engineering",
            "Cloud Computing",
            "Cybersecurity"
        ],
        key="student_domain"
    )

work_mode = st.selectbox(
    "Preferred Work Mode",
    [
        "Remote",
        "Hybrid",
        "On-site"
    ],
    key="student_work_mode"
)

st.divider()


# =========================================================
# FIND INTERNSHIPS BUTTON & LOGIC
# =========================================================

if st.button(
    "🔍 Find Internships",
    use_container_width=True
):
    # -----------------------------------------------------
    # VALIDATE INPUT
    # -----------------------------------------------------
    if not name.strip() or not branch.strip() or not skills.strip():
        st.warning(
            "⚠️ Please fill in your name, branch, and skills (or upload a resume)."
        )
    else:
        recommendations = []

        # Parse student skills (lowercase & trimmed)
        student_skills = [
            skill.strip().lower()
            for skill in skills.split(",")
            if skill.strip()
        ]

        # Evaluate each internship in dataset
        for internship in internships:
            # Parse required internship skills (pipe-separated)
            required_skills = [
                skill.strip().lower()
                for skill in str(internship["skills"]).split("|")
                if skill.strip()
            ]

            # Find matched skills
            matched_skills = [
                skill for skill in required_skills
                if skill in student_skills
            ]

            # Find missing skills (Skill Gap Analysis)
            missing_skills = [
                skill for skill in required_skills
                if skill not in student_skills
            ]

            # 1. Skill Match (60% weight)
            if required_skills:
                skill_match = (len(matched_skills) / len(required_skills)) * 100
            else:
                skill_match = 0

            # 2. Domain Match (25% weight)
            if domain.strip().lower() == str(internship["domain"]).strip().lower():
                domain_match = 100
            else:
                domain_match = 0

            # 3. Work Mode Match (15% weight)
            if work_mode.strip().lower() == str(internship["work_mode"]).strip().lower():
                work_mode_match = 100
            else:
                work_mode_match = 0

            # Final Weighted Match Score
            match_percentage = (
                (skill_match * 0.60)
                + (domain_match * 0.25)
                + (work_mode_match * 0.15)
            )

            # Match Level Determination
            if match_percentage >= 70:
                match_level = "Excellent Match"
            elif match_percentage >= 50:
                match_level = "Good Match"
            else:
                match_level = "Partial Match"

            # Threshold Filter: match_percentage >= 30%
            if match_percentage >= 30:
                recommendations.append({
                    "title": internship["title"],
                    "domain": internship["domain"],
                    "work_mode": internship["work_mode"],
                    "matched_skills": matched_skills,
                    "missing_skills": missing_skills,
                    "match": match_percentage,
                    "match_level": match_level,
                    "link": internship.get("link", "")
                })

        # Sort recommendations descending by match percentage
        recommendations.sort(
            key=lambda x: x["match"],
            reverse=True
        )

        # Store results in Session State
        st.session_state.recommendations = recommendations
        st.session_state.search_done = True
        st.session_state.qr_bytes = None  # Reset previous QR code on new search


# =========================================================
# DISPLAY RESULTS & SUMMARY (AFTER SEARCH IS DONE)
# =========================================================

if st.session_state.search_done:
    recommendations = st.session_state.recommendations

    # -----------------------------------------------------
    # 📊 RECOMMENDATION SUMMARY
    # -----------------------------------------------------
    st.subheader("📊 Recommendation Summary")

    col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)

    with col_sum1:
        st.metric("Total Internships", len(internships))

    with col_sum2:
        st.metric("Matches Found", len(recommendations))

    with col_sum3:
        best_title = recommendations[0]["title"] if recommendations else "None"
        st.metric("Best Match", best_title)

    with col_sum4:
        best_score = f"{round(recommendations[0]['match'], 1)}%" if recommendations else "0%"
        st.metric("Highest Match Score", best_score)

    st.divider()

    # -----------------------------------------------------
    # 📈 TOP MATCHES COMPARISON CHART
    # -----------------------------------------------------
    if recommendations:
        st.subheader("📈 Top Matches Comparison")
        chart_df = pd.DataFrame({
            "Internship Title": [r["title"] for r in recommendations[:5]],
            "Match Score (%)": [round(r["match"], 1) for r in recommendations[:5]]
        }).set_index("Internship Title")
        st.bar_chart(chart_df)

    st.divider()

    # -----------------------------------------------------
    # 🎯 RECOMMENDED INTERNSHIPS LIST
    # -----------------------------------------------------
    st.subheader("🎯 Recommended Internships")

    if recommendations:
        st.success(
            f"✅ Found {len(recommendations)} internship(s) matching your profile!"
        )

        for i, recommendation in enumerate(recommendations, start=1):
            with st.container():
                st.markdown(f"### {i}. {recommendation['title']}")

                col1, col2 = st.columns(2)
                with col1:
                    st.write("🏢 **Domain:**", recommendation["domain"])
                with col2:
                    st.write("💼 **Work Mode:**", recommendation["work_mode"])

                match = round(recommendation["match"], 2)
                st.write(f"🎯 **Match Score: {match}%**")
                st.progress(min(int(match), 100))

                if recommendation["match_level"] == "Excellent Match":
                    st.markdown('<span class="badge-excellent">🌟 Excellent Match</span>', unsafe_allow_html=True)
                elif recommendation["match_level"] == "Good Match":
                    st.markdown('<span class="badge-good">👍 Good Match</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-partial">⚡ Partial Match</span>', unsafe_allow_html=True)

                st.write("")

                matched = recommendation["matched_skills"]
                missing = recommendation.get("missing_skills", [])

                col_sk1, col_sk2 = st.columns(2)

                with col_sk1:
                    if matched:
                        skills_html = "".join([f'<span class="skill-tag">✓ {s}</span>' for s in matched])
                        st.markdown(f"**🛠️ Matched Skills:**<br>{skills_html}", unsafe_allow_html=True)
                    else:
                        st.write("🛠️ **Matched Skills:** None")

                with col_sk2:
                    if missing:
                        gap_html = "".join([f'<span class="skill-gap-tag">⚠️ {s}</span>' for s in missing])
                        st.markdown(f"**💡 Skill Gap (Need to Learn):**<br>{gap_html}", unsafe_allow_html=True)
                    else:
                        st.markdown("**💡 Skill Gap:** <span style='color:#34d399; font-weight:600;'>None - Complete Match! 🎉</span>", unsafe_allow_html=True)

                st.write("")

                if recommendation["link"]:
                    st.markdown(
                        f'<a href="{recommendation["link"]}" target="_blank" class="apply-btn">🚀 Apply for Internship 🔗</a>',
                        unsafe_allow_html=True
                    )

                st.divider()

    else:
        st.warning(
            "No suitable internships found. Try adding more skills or changing your preferred domain."
        )

    # -----------------------------------------------------
    # 📱 QR CODE GENERATION SECTION
    # -----------------------------------------------------
    if recommendations:
        st.subheader("📱 Generate QR Code")
        st.write(
            "Generate a QR code containing the application link for your top recommended internship."
        )

        if st.button("📱 Generate QR Code", use_container_width=True):
            top_internship = recommendations[0]
            qr_data = top_internship["link"]

            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            qr_image = qr.make_image()

            buffer = BytesIO()
            qr_image.save(buffer, format="PNG")
            st.session_state.qr_bytes = buffer.getvalue()

        if st.session_state.qr_bytes is not None:
            st.success("✅ QR Code generated successfully!")
            st.image(
                st.session_state.qr_bytes,
                caption="Top Recommended Internship Application Link",
                width=300
            )
            st.download_button(
                label="⬇️ Download QR Code",
                data=st.session_state.qr_bytes,
                file_name="top_internship_qr.png",
                mime="image/png",
                use_container_width=True
            )
