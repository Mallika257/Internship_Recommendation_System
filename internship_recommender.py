```python
import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Internship Recommendation System",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# LOAD INTERNSHIP DATA
# =========================================================

df = pd.read_csv("internships.csv")

internships = df.to_dict("records")


# =========================================================
# SESSION STATE
# =========================================================

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []


# =========================================================
# TITLE
# =========================================================

st.title("🎓 Internship Recommendation System")

st.write(
    "Enter your profile details and find internships "
    "that best match your skills and preferences."
)

st.divider()


# =========================================================
# STUDENT DETAILS
# =========================================================

st.subheader("👤 Student Profile")

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
        ]
    )


# =========================================================
# WORK MODE
# =========================================================

work_mode = st.selectbox(
    "Preferred Work Mode",
    [
        "Remote",
        "Hybrid",
        "On-site"
    ]
)


st.divider()


# =========================================================
# FIND INTERNSHIPS
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
            "⚠️ Please fill in your name, branch and skills."
        )

    else:

        recommendations = []


        # -------------------------------------------------
        # STUDENT SKILLS
        # -------------------------------------------------

        student_skills = [
            skill.strip().lower()
            for skill in skills.split(",")
            if skill.strip()
        ]


        # -------------------------------------------------
        # CHECK EACH INTERNSHIP
        # -------------------------------------------------

        for internship in internships:

            # ---------------------------------------------
            # REQUIRED SKILLS
            # ---------------------------------------------

            required_skills = [
                skill.strip().lower()
                for skill in str(
                    internship["skills"]
                ).split("|")
                if skill.strip()
            ]


            # ---------------------------------------------
            # MATCHED SKILLS
            # ---------------------------------------------

            matched_skills = []

            for skill in required_skills:

                if skill in student_skills:
                    matched_skills.append(skill)


            # ---------------------------------------------
            # SKILL MATCH
            # ---------------------------------------------

            if required_skills:

                skill_match = (
                    len(matched_skills)
                    / len(required_skills)
                ) * 100

            else:

                skill_match = 0


            # ---------------------------------------------
            # DOMAIN MATCH
            # ---------------------------------------------

            if (
                domain.strip().lower()
                == str(
                    internship["domain"]
                ).strip().lower()
            ):

                domain_match = 100

            else:

                domain_match = 0


            # ---------------------------------------------
            # WORK MODE MATCH
            # ---------------------------------------------

            if (
                work_mode.strip().lower()
                == str(
                    internship["work_mode"]
                ).strip().lower()
            ):

                work_mode_match = 100

            else:

                work_mode_match = 0


            # ---------------------------------------------
            # FINAL MATCH SCORE
            # ---------------------------------------------

            match_percentage = (
                (skill_match * 0.60)
                + (domain_match * 0.25)
                + (work_mode_match * 0.15)
            )


            # ---------------------------------------------
            # MATCH LEVEL
            # ---------------------------------------------

            if match_percentage >= 70:

                match_level = "Excellent Match"

            elif match_percentage >= 50:

                match_level = "Good Match"

            else:

                match_level = "Partial Match"


            # ---------------------------------------------
            # ADD RECOMMENDATION
            # ---------------------------------------------

            if match_percentage >= 30:

                recommendations.append({

                    "title": internship["title"],

                    "domain": internship["domain"],

                    "work_mode": internship["work_mode"],

                    "matched_skills": matched_skills,

                    "match": match_percentage,

                    "match_level": match_level,

                    "link": internship.get(
                        "link",
                        ""
                    )

                })


        # -------------------------------------------------
        # SORT RECOMMENDATIONS
        # -------------------------------------------------

        recommendations.sort(
            key=lambda x: x["match"],
            reverse=True
        )


        # -------------------------------------------------
        # SAVE TO SESSION STATE
        # -------------------------------------------------

        st.session_state.recommendations = recommendations


        # =================================================
        # DISPLAY RESULTS
        # =================================================

        st.subheader("🎯 Recommended Internships")


        if recommendations:

            st.success(
                f"✅ Found {len(recommendations)} "
                "internship(s) matching your profile!"
            )


            # ---------------------------------------------
            # DISPLAY EACH RECOMMENDATION
            # ---------------------------------------------

            for i, recommendation in enumerate(
                recommendations,
                start=1
            ):

                st.markdown(
                    f"### {i}. "
                    f"{recommendation['title']}"
                )


                col1, col2 = st.columns(2)


                with col1:

                    st.write(
                        "🏢 **Domain:**",
                        recommendation["domain"]
                    )


                with col2:

                    st.write(
                        "💼 **Work Mode:**",
                        recommendation["work_mode"]
                    )


                # -----------------------------------------
                # MATCH SCORE
                # -----------------------------------------

                match = round(
                    recommendation["match"],
                    2
                )


                st.write(
                    f"🎯 **Match Score: {match}%**"
                )


                st.progress(
                    min(
                        int(match),
                        100
                    )
                )


                # -----------------------------------------
                # MATCH LEVEL
                # -----------------------------------------

                if (
                    recommendation["match_level"]
                    == "Excellent Match"
                ):

                    st.success(
                        "🌟 Excellent Match"
                    )


                elif (
                    recommendation["match_level"]
                    == "Good Match"
                ):

                    st.info(
                        "👍 Good Match"
                    )


                else:

                    st.warning(
                        "⚡ Partial Match"
                    )


                # -----------------------------------------
                # MATCHED SKILLS
                # -----------------------------------------

                matched = recommendation[
                    "matched_skills"
                ]


                if matched:

                    st.write(
                        "🛠️ **Matched Skills:**",
                        ", ".join(matched)
                    )

                else:

                    st.write(
                        "🛠️ **Matched Skills:** None"
                    )


                # -----------------------------------------
                # APPLICATION LINK
                # -----------------------------------------

                if recommendation["link"]:

                    st.markdown(
                        f"🔗 **[Apply for this internship]"
                        f"({recommendation['link']})**"
                    )


                st.divider()


        else:

            st.warning(
                "No suitable internships found. "
                "Try adding more skills or changing "
                "your preferred domain."
            )


# =========================================================
# QR CODE SECTION
# =========================================================

if st.session_state.recommendations:

    st.divider()

    st.subheader("📱 Generate QR Code")

    st.write(
        "Generate a QR code containing the details "
        "of your top recommended internship."
    )


    if st.button(
        "📱 Generate QR Code",
        use_container_width=True
    ):

        top_internship = (
            st.session_state.recommendations[0]
        )


        # ---------------------------------------------
        # QR DATA
        # ---------------------------------------------

        qr_data = f"""
===== INTERNSHIP RECOMMENDATION =====

Internship:
{top_internship['title']}

Domain:
{top_internship['domain']}

Work Mode:
{top_internship['work_mode']}

Match Score:
{round(top_internship['match'], 2)}%

Recommendation:
{top_internship['match_level']}

Matched Skills:
{", ".join(top_internship['matched_skills'])}

Apply Here:
{top_internship['link']}

Generated by:
Internship Recommendation System
"""


        # ---------------------------------------------
        # GENERATE QR
        # ---------------------------------------------

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )


        qr.add_data(qr_data)

        qr.make(
            fit=True
        )


        qr_image = qr.make_image()


        # ---------------------------------------------
        # STORE IMAGE IN MEMORY
        # ---------------------------------------------

        buffer = BytesIO()

        qr_image.save(
            buffer,
            format="PNG"
        )

        buffer.seek(0)


        # ---------------------------------------------
        # DISPLAY QR
        # ---------------------------------------------

        st.success(
            "✅ QR Code generated successfully!"
        )


        st.image(
            buffer,
            caption=(
                "Top Recommended Internship"
            ),
            width=300
        )


        # ---------------------------------------------
        # DOWNLOAD QR
        # ---------------------------------------------

        st.download_button(
            label="⬇️ Download QR Code",
            data=buffer.getvalue(),
            file_name="top_internship_qr.png",
            mime="image/png",
            use_container_width=True
        )
```
