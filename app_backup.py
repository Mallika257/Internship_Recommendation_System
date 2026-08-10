import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO

df = pd.read_csv("internships.csv")
internships = df.to_dict("records")
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

# Page/UI
st.set_page_config(
    page_title="Internship Recommendation System",
    page_icon="🎓"
)

st.title("🎓 Internship Recommendation System")

name = st.text_input("Enter your name")
branch = st.text_input("Enter your branch")
skills = st.text_input("Enter your skills")

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
    ]
)

work_mode = st.selectbox(
    "Preferred Work Mode",
    ["Remote", "Hybrid", "On-site"]
)


if st.button("🔍 Find Internships", use_container_width=True):

    if not name or not branch or not skills:
        st.warning("Please fill in all the required fields.")

    else:

        # IMPORTANT
        recommendations = []

        student_skills = [
            skill.strip().lower()
            for skill in skills.split(",")
        ]

        for internship in internships:

            required_skills = [
                skill.strip().lower()
                for skill in internship["skills"].split("|")
                if skill.strip()
            ]

            matched_skills = []

            for skill in required_skills:
                if skill in student_skills:
                    matched_skills.append(skill)

            if required_skills:
                skill_match = (
                    len(matched_skills) /
                    len(required_skills)
                ) * 100
            else:
                skill_match = 0

            if domain.lower() == internship["domain"].lower():
                domain_match = 100
            else:
                domain_match = 0

            if work_mode.lower() == internship["work_mode"].lower():
                work_mode_match = 100
            else:
                work_mode_match = 0

            match_percentage = (
                skill_match * 0.60
                + domain_match * 0.25
                + work_mode_match * 0.15
            )

            if match_percentage >= 70:
                match_level = "Excellent Match"
            elif match_percentage >= 50:
                match_level = "Good Match"
            else:
                match_level = "Partial Match"

            if match_percentage >= 30:
                recommendations.append({
                    "title": internship["title"],
                    "domain": internship["domain"],
                    "work_mode": internship["work_mode"],
                    "matched_skills": matched_skills,
                    "match": match_percentage,
                    "match_level": match_level
                })

        recommendations.sort(
            key=lambda x: x["match"],
            reverse=True
        )

        st.session_state.recommendations = recommendations

        # DISPLAY RESULTS
        st.subheader("🎯 Recommended Internships")

        if recommendations:

            for i, recommendation in enumerate(
                recommendations,
                start=1
            ):

                st.markdown(
                    f"### {i}. {recommendation['title']}"
                )

                st.write(
                    "**Domain:**",
                    recommendation["domain"]
                )

                st.write(
                    "**Work Mode:**",
                    recommendation["work_mode"]
                )

                st.write(
                    "**Match:**",
                    f"{round(recommendation['match'], 2)}%"
                )

                st.write(
                    "**Matched Skills:**",
                    ", ".join(
                        recommendation["matched_skills"]
                    )
                )

                st.write(
                    "**Recommendation:**",
                    recommendation["match_level"]
                )

                st.divider()

                       # QR CODE
st.subheader("📱 Generate QR Code")

if st.button("Generate QR Code"):

    if len(st.session_state.recommendations) > 0:

        top_internship = st.session_state.recommendations[0]

        qr_data = f"""
===== INTERNSHIP RECOMMENDATION =====

Internship: {top_internship['title']}
Domain: {top_internship['domain']}
Work Mode: {top_internship['work_mode']}
Match Score: {round(top_internship['match'], 2)}%
Recommendation: {top_internship['match_level']}

Matched Skills:
{", ".join(top_internship['matched_skills'])}
"""

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
        buffer.seek(0)

        st.success("✅ QR Code generated!")

        st.image(
            buffer,
            caption="Top Recommended Internship",
            width=300
        )

    else:
        st.warning("Please click 'Find Internships' first.")