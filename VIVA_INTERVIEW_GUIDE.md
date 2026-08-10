# 🎓 Internship Recommendation System: Viva & Interview Guide

This guide contains everything you need to showcase, present, and answer viva/interview questions about your **Internship Recommendation System**.

---

## 📝 1. Resume Project Description

Copy and paste these bullet points into your **Resume / CV**:

### **AI-Powered Internship Recommendation System & Resume Parser**
*Tech Stack: Python, Streamlit, Pandas, pypdf (NLP), Data Science, QR Code Engine, Custom CSS*

- **Engineered an interactive data science web application** using **Streamlit**, **Pandas**, and **pypdf** to match candidate profiles with internship positions based on a multi-factor weighted scoring algorithm ($60\%$ skills, $25\%$ domain, $15\%$ work mode).
- **Architected an Automated Resume PDF Parser** using string extraction and NLP keyword matching to extract technical skillsets directly from PDF/TXT resume files, reducing manual entry friction.
- **Implemented a Real-time Skill Gap Analysis Engine** comparing candidate skills against internship requirements to highlight **Matched Skills** vs. **Skills to Learn (Gaps)** for candidate career path guidance.
- **Managed Streamlit Session State (`st.session_state`) lifecycle**, ensuring search results, executive metrics dashboard, interactive bar chart, and generated QR codes persist seamlessly across browser reruns.
- **Integrated a dynamic QR Code Generator** allowing candidates to instantly generate, preview, and download application link QR codes for top-ranked internships.

---

## 🎤 2. Project Explanation for Interviews & Presentations

### **A. 30-Second Elevator Pitch (Short)**
> *"I built an AI-assisted Streamlit Internship Recommendation System with an integrated Resume Parser and Skill Gap Analysis engine. Candidates can upload their PDF resume to auto-extract technical skills. The system matches them against internships using a weighted scoring model (60% skills, 25% domain, 15% work mode), displays interactive match comparison charts, highlights missing skills candidates need to learn, and generates downloadable application QR codes."*

### **B. 2-Minute Technical Explanation (Detailed for Technical Round / Viva)**
> *"The application is structured into four main technical layers: Resume Parsing & NLP Extraction, Candidate Input Normalization, Weighted Recommendation & Skill Gap Engine, and the Streamlit UX Layer.*
>
> 1. *First, when a candidate uploads a PDF resume, `pypdf` extracts raw text, which is parsed using keyword extraction against a technical taxonomy matrix to auto-populate the skills input.*
> 2. *The system iterates through `internships.csv`, performing set-intersection matching for skills while calculating set-difference to identify **Skill Gaps** (missing skills to learn).*
> 3. *The match score is calculated mathematically: Skill Match is weighted at 60%, Domain Match at 25%, and Work Mode Match at 15%. Roles scoring above a 30% threshold are filtered and sorted.*
> 4. *To ensure optimal UX, **Streamlit Session State** retains recommendation lists, metrics dashboards, bar charts, and in-memory `BytesIO` QR PNG buffers across reruns."*

---

## ❓ 3. Top 15 Viva & Technical Interview Questions (With Complete Answers)

### **Q1: How does your Resume Parser extract skills from a PDF file?**
**Answer:**
Using `pypdf.PdfReader`, the app iterates through each page of the uploaded PDF, extracts raw unformatted text into memory, converts it to lowercase, and performs keyword taxonomy matching against standard data science and software engineering technical skills.

---

### **Q2: What is Skill Gap Analysis and how is it calculated in code?**
**Answer:**
Skill Gap Analysis identifies the specific required skills a candidate lacks for a target role. In Python, it is calculated using set subtraction / list comprehension:
```python
missing_skills = [skill for skill in required_skills if skill not in student_skills]
```
This is displayed as amber tags (`⚠️ Pandas`) on recommendation cards to provide actionable learning guidance.

---

### **Q3: Why did you choose a 60/25/15 weighting ratio for the scoring algorithm?**
**Answer:**
- **Skills (60%)**: Technical skills are the primary prerequisite for job performance.
- **Domain (25%)**: Preferred domain ensures student career interest alignment.
- **Work Mode (15%)**: Location/remote preference addresses logistical feasibility.

---

### **Q4: How does skill matching work under the hood?**
**Answer:**
Student skills are normalized to lowercase and split by comma, while CSV required skills are pipe-separated (`|`). Set intersection determines matched skills:
$$\text{Skill Match} = \left( \frac{|\text{Matched Skills}|}{|\text{Required Skills}|} \right) \times 100$$

---

### **Q5: Why was Streamlit Session State (`st.session_state`) required?**
**Answer:**
Streamlit re-executes Python scripts top-to-bottom on every user interaction. Without `st.session_state`, previous recommendation calculations and generated QR code images would be lost whenever a user clicks a button or dropdown.

---

### **Q6: How did you fix the `NameError: name 'recommendations' is not defined` bug?**
**Answer:**
The display code was originally outside the button block. I resolved it by wrapping display logic inside `if st.session_state.search_done:` and reading `st.session_state.recommendations`.

---

### **Q7: How does the QR Code generation work in Python?**
**Answer:**
Using `qrcode.QRCode()`:
1. `qr.add_data(top_internship_link)` attaches the URL.
2. `qr.make_image()` renders the PNG image.
3. The image is saved into an in-memory `BytesIO` buffer, stored in session state, and rendered via `st.image()` & `st.download_button()`.

---

### **Q8: What is `BytesIO` and why use it instead of saving files to disk?**
**Answer:**
`BytesIO` creates an in-memory binary stream. Saving temporary QR images to disk causes unnecessary disk I/O overhead and permission errors during cloud deployment. `BytesIO` keeps operations fast in RAM.

---

### **Q9: How does your dataset store required skills and why pipe-separated (`|`)?**
**Answer:**
Skills inside CSV cells contain commas (e.g. `"Python, SQL"`). Using commas inside cells can break CSV parsing unless quoted. Pipe (`|`) provides clean, unambiguous parsing via `.split("|")`.

---

### **Q10: How do you filter out weak recommendations?**
**Answer:**
Recommendations with a total weighted score below **30%** are filtered out using `if match_percentage >= 30:`.

---

### **Q11: How are recommendations sorted?**
**Answer:**
Using Python's built-in `sort()` with a lambda key:
```python
recommendations.sort(key=lambda x: x["match"], reverse=True)
```
This orders the list in descending order of match percentage in $O(N \log N)$ time.

---

### **Q12: How fixed input autocomplete bug in Streamlit?**
**Answer:**
Assigning unique `key` parameters (e.g. `key="student_name"`, `key="student_skills"`) locks widget state bound explicitly to Streamlit's session dictionary.

---

### **Q13: How would you scale this project to handle 100,000 internships?**
**Answer:**
1. **Database Migration**: Move from `internships.csv` to PostgreSQL / SQLite.
2. **Vector Indexing**: Use TF-IDF vectors or embeddings for job descriptions.
3. **Pagination**: Implement paginated display in Streamlit (10 roles per page).

---

### **Q14: How can Machine Learning / NLP enhance this system further?**
**Answer:**
- **TF-IDF & Cosine Similarity**: Compute semantic similarity between unstructured resume text and job descriptions.
- **Transformer Embeddings (BERT / Word2Vec)**: Capture contextual relevance (e.g., recognizing that `"Deep Learning"` connects to `"PyTorch"`).

---

### **Q15: What is the computational time complexity of your algorithm?**
**Answer:**
For $N$ internships and average $K$ skills per role:
- Skill parsing & matching: $O(N \cdot K)$
- Sorting: $O(N \log N)$
- Overall time complexity: $O(N \cdot K + N \log N)$, executing in under 5 milliseconds for typical datasets.
