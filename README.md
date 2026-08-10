# 🎓 Internship Recommendation System with Integrated QR Code Generator

A Data Science and Machine Learning-oriented web application built using **Streamlit**, **Pandas**, and **Python**. The system provides personalized internship recommendations for students based on a multi-factor weighted matching algorithm evaluating candidate **skills**, **preferred domain**, and **preferred work mode**. It also features an integrated **QR Code Generator** allowing students to instantly generate, scan, and download application link QR codes.

---

## 🌟 Key Features

- **🎯 Multi-Factor Weighted Recommendation Engine**: Calculates precise match percentages using customized domain weighting ($60\%$ Skills, $25\%$ Domain, $15\%$ Work Mode).
- **📊 Real-time Executive Summary Dashboard**: Interactive metric cards showing total dataset size, matches found, top match title, and peak match score.
- **🏷️ Dynamic Match Classification**: Color-coded categorization into **Excellent Match** ($\ge 70\%$), **Good Match** ($\ge 50\%$), and **Partial Match** ($< 50\%$).
- **📱 Integrated QR Code Generator**: Generates clean PNG QR codes containing the direct internship application URL for top-ranked matches.
- **💾 Session State Persistence**: Retains search results, summary metrics, and generated QR codes seamlessly across Streamlit reruns.
- **✨ Modern Glassmorphism UI**: Styled with custom CSS, Plus Jakarta Sans typography, skill badges, and responsive action call-to-buttons.

---

## 🧮 Recommendation Algorithm & Mathematical Formula

The system ranks available internships by computing a overall weighted match score ($M$) for each internship profile against user input details:

$$M = (\text{Skill Match} \times 0.60) + (\text{Domain Match} \times 0.25) + (\text{Work Mode Match} \times 0.15)$$

### Component Calculations:

1. **Skill Match ($S$)**:
   $$\text{Skill Match} = \left( \frac{|\text{User Skills} \cap \text{Required Skills}|}{|\text{Required Skills}|} \right) \times 100$$
   *(All skills are normalized to lowercase prior to set intersection).*

2. **Domain Match ($D$)**:
   $$\text{Domain Match} = \begin{cases} 100, & \text{if } \text{User Domain} = \text{Internship Domain} \\ 0, & \text{otherwise} \end{cases}$$

3. **Work Mode Match ($W$)**:
   $$\text{Work Mode Match} = \begin{cases} 100, & \text{if } \text{User Work Mode} = \text{Internship Work Mode} \\ 0, & \text{otherwise} \end{cases}$$

### Match Thresholds:
- **Threshold Filter**: Internships with $M < 30\%$ are excluded.
- **Ranking**: Qualifying recommendations are sorted in descending order of $M$.

---

## 📁 Project Directory Structure

```
Internship_Recommendation_System/
│
├── app.py                      # Core Streamlit Web Application & Recommendation Engine
├── app_backup.py               # Application Backup State
├── internships.csv             # Internship Dataset (20 Sample Roles)
├── top_internship_qr.png       # Sample Generated QR Code Output
├── README.md                   # Complete Project Documentation & Setup Guide
   
```

---

## 📊 Dataset Specification (`internships.csv`)

The dataset contains 20 curated internship records with the following schema:

| Column Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `title` | String | Title of the internship role | `Data Science Intern` |
| `domain` | String | Industry/Technical domain | `Data Science` |
| `skills` | String | Pipe-separated required skills | `Python\|SQL\|Pandas` |
| `work_mode` | String | Location requirement | `Remote` |
| `link` | String | Application portal URL | `https://www.linkedin.com/jobs/...` |

---

## 🚀 Installation & Local Setup

### Prerequisites
- **Python**: Version `3.8` or higher
- **pip**: Python Package Installer

### Step 1: Clone or Navigate to Project Directory
```bash
cd Internship_Recommendation_System
```

### Step 2: Install Required Dependencies
```bash
pip install streamlit pandas qrcode pillow
```

### Step 3: Launch the Application
```bash
streamlit run app.py
```

Open your browser and navigate to `http://localhost:8501` (or `http://localhost:8502`).

---

## 🧪 Sample Verification Test Profile

To test the system's exact matching accuracy, use the following test candidate profile:

- **Candidate Name**: Mallika
- **Branch**: Data Science
- **Skills**: `Python, SQL, Pandas`
- **Preferred Domain**: `Data Science`
- **Preferred Work Mode**: `Remote`

### Expected Result:
- **Top Recommendation**: Data Science Intern
- **Match Score**: `100.0%`
- **Match Classification**: 🌟 `Excellent Match`
- **Matched Skills**: `python`, `sql`, `pandas`

---

## 🔮 Future Enhancements

1. **Natural Language Processing (NLP)**: Implement TF-IDF vectorization and Cosine Similarity to handle unstructured resume text matching.
2. **Resume Parser**: PDF/DOCX resume upload to automatically extract candidate skills using `spaCy` or `PyPDF2`.
3. **Machine Learning Model**: Train a Collaborative Filtering / Content-Based Filtering recommendation model based on past applicant interaction data.
