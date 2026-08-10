# 🎓 Internship Recommendation System: Viva & Interview Guide

This guide contains everything you need to showcase, present, and answer viva/interview questions about your **Internship Recommendation System**.

---

## 📝 1. Resume Project Description

Copy and paste these bullet points into your **Resume / CV**:

### **Internship Recommendation System with QR Integration**
*Tech Stack: Python, Streamlit, Pandas, Data Science, QR Code Engine, Custom CSS*

- **Engineered an interactive data science web application** using **Streamlit** and **Pandas** to match student candidate profiles with relevant internship positions based on a multi-factor weighted scoring algorithm ($60\%$ skills, $25\%$ domain, $15\%$ work mode).
- **Implemented a robust data parsing & normalization engine** to evaluate candidate skills against pipe-separated CSV metadata, classifying matches into **Excellent** ($\ge 70\%$), **Good** ($\ge 50\%$), and **Partial** ($< 50\%$) categories.
- **Architected Streamlit Session State (`st.session_state`) lifecycle management**, ensuring search results, summary metrics dashboard, and generated QR codes persist seamlessly across user UI interactions.
- **Integrated a dynamic QR Code Generator** allowing candidates to instantly generate, preview, and download application link QR codes for top-ranked internships.

---

## 🎤 2. Project Explanation for Interviews & Presentations

### **A. 30-Second Elevator Pitch (Short)**
> *"I built a Streamlit-based Internship Recommendation System designed to help students discover relevant internship opportunities tailored to their specific skillset, preferred domain, and work mode. The app uses a weighted scoring algorithm where skills carry 60% weight, domain carries 25%, and work mode carries 15%. It features a real-time summary dashboard, skill match visualization, and an integrated QR Code generator that lets candidates scan or download application links directly."*

### **B. 2-Minute Technical Explanation (Detailed for Technical Round / Viva)**
> *"The application is structured into four main layers: Data Ingestion, Candidate Input Normalization, Weighted Recommendation Engine, and the Streamlit UI Layer.*
>
> 1. *First, the dataset of internships is loaded from `internships.csv` using **Pandas** and converted into dictionary records.*
> 2. *When a candidate enters their details, skills are cleaned and converted to lowercase. The system iterates through the dataset, parsing pipe-separated required skills and finding the set intersection with user skills.*
> 3. *The match score is calculated mathematically: Skill Match is weighted at 60%, Domain Match at 25%, and Work Mode Match at 15%. Roles scoring above a 30% threshold are filtered and sorted in descending order.*
> 4. *To ensure optimal UX, I utilized **Streamlit Session State** so recommendations and QR codes persist during browser reruns. Finally, the top recommendation's link is converted into a PNG QR Code using the `qrcode` library and served via an in-memory `BytesIO` buffer for instant download."*

---

## ❓ 3. Top 15 Viva & Technical Interview Questions (With Complete Answers)

### **Q1: What is the core problem your project solves?**
**Answer:**
Many job portals rely on basic keyword searches that often return irrelevant results. This system uses a multi-factor weighted matching algorithm to evaluate candidates based on skill coverage, domain interest, and logistical feasibility (work mode), providing ranked, personalized recommendations.

---

### **Q2: Why did you choose a 60/25/15 weighting ratio for the scoring algorithm?**
**Answer:**
- **Skills (60%)**: Technical skills are the primary prerequisite for job performance.
- **Domain (25%)**: Preferred domain ensures student career interest alignment.
- **Work Mode (15%)**: Location/remote preference addresses logistical feasibility without overly penalizing a strong technical match.

---

### **Q3: How does skill matching work under the hood?**
**Answer:**
Student skills are comma-separated strings (e.g., `"Python, SQL, Pandas"`), while CSV internship skills are pipe-separated (e.g., `"Python|SQL|Pandas"`). Both inputs are normalized to lowercase and stripped of whitespace. The algorithm computes:
$$\text{Skill Match} = \left( \frac{|\text{Matched Skills}|}{|\text{Required Skills}|} \right) \times 100$$

---

### **Q4: Why was Streamlit Session State (`st.session_state`) required?**
**Answer:**
Streamlit executes Python scripts top-to-bottom on every user interaction (widget state change). Without `st.session_state`, previous recommendation calculations and generated QR code images would be lost whenever a user interacts with buttons or inputs. Session state retains these variables across reruns.

---

### **Q5: What caused the `NameError: name 'recommendations' is not defined` bug and how did you resolve it?**
**Answer:**
The recommendation display code was placed at the top-level script scope outside the button block. When the app first loaded, `recommendations` was never created, triggering a `NameError`. I resolved it by wrapping the display logic inside `if st.session_state.search_done:` and reading `st.session_state.recommendations`.

---

### **Q6: How does the QR Code generation work in Python?**
**Answer:**
Using the `qrcode` module:
1. `qr = qrcode.QRCode(version=1, box_size=10, border=5)` initializes the matrix.
2. `qr.add_data(link)` attaches the top internship application link.
3. `qr.make_image()` renders the PNG pixel image.
4. The PNG data is saved into an in-memory `BytesIO` buffer and stored in session state for display and download.

---

### **Q7: What is `BytesIO` and why use it instead of saving files to disk?**
**Answer:**
`BytesIO` creates an in-memory binary stream. Saving temporary QR images to disk causes unnecessary disk I/O overhead, file system latency, and permission errors during cloud deployment (e.g., Streamlit Community Cloud). `BytesIO` keeps operations fast and stateless in RAM.

---

### **Q8: How does your dataset store required skills and why pipe-separated (`|`)?**
**Answer:**
Skill lists inside CSVs often contain commas (e.g., `"Python, Pandas"`). Using a comma inside a CSV cell can cause parsing ambiguity if not quoted properly. Using pipe (`|`) as a delimiter provides clean, unambiguous parsing via `.split("|")`.

---

### **Q9: How do you filter out weak recommendations?**
**Answer:**
Recommendations with a total weighted score below **30%** are filtered out using `if match_percentage >= 30:`. This ensures only meaningful matches appear to the student.

---

### **Q10: How are recommendations sorted?**
**Answer:**
Using Python's built-in `sort()` with a lambda key:
```python
recommendations.sort(key=lambda x: x["match"], reverse=True)
```
This orders the list in descending order of match percentage in $O(N \log N)$ time complexity.

---

### **Q11: Why is this project classified as a medium-level Data Science project?**
**Answer:**
It moves beyond basic CLI scripts by incorporating structured data ingestion, string normalization, mathematical weighting models, threshold filtering, session lifecycle management, UI design system with CSS, dynamic data visualizations (metrics, progress bars), and third-party API integration (QR generation).

---

### **Q12: How fixed input autocomplete bug in Streamlit?**
**Answer:**
Streamlit input widgets can conflict when browser autocomplete fills form fields. Assigning unique `key` parameters (e.g. `key="student_name"`, `key="student_skills"`) locks widget state bound explicitly to Streamlit's session dictionary.

---

### **Q13: How would you scale this project to handle 100,000 internships?**
**Answer:**
1. **Database Migration**: Move from `internships.csv` to PostgreSQL / SQLite database with indexed columns.
2. **Vector Search / Indexing**: Pre-calculate TF-IDF vectors or embeddings for internship skills.
3. **Pagination**: Implement paginated display in Streamlit to render 10-20 recommendations per page instead of all matches at once.

---

### **Q14: How could Machine Learning / NLP enhance this system in the future?**
**Answer:**
- **TF-IDF & Cosine Similarity**: Measure semantic similarity between user resumes and job descriptions.
- **Word Embeddings (BERT / Word2Vec)**: Capture contextual skill relevance (e.g., recognizing that `"Deep Learning"` is strongly related to `"PyTorch"`).
- **Collaborative Filtering**: Recommend internships based on similar candidates' application history.

---

### **Q15: What is the computational time complexity of your recommendation algorithm?**
**Answer:**
For $N$ internships in the dataset and average $K$ skills per role:
- Skill parsing & matching: $O(N \cdot K)$
- Sorting: $O(N \log N)$
- Overall time complexity: $O(N \cdot K + N \log N)$

For $N = 20$, computation executes in under 5 milliseconds.
