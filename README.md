# LessonCraft AI – AI-Powered Lesson Creation Tool

An AI-powered lesson creation application developed for the **Kalvium AI Research Intern Assignment**.

LessonCraft AI helps instructors create structured, engaging 45-minute lessons using a lesson title and learning objective. It includes research discovery, two independent quality-control layers, lesson editing, and export functionality.

## Features

- **Lesson Generation:** Generate structured lessons using a lesson title and learning objective.
- **Research References:** Discover relevant books, websites, and YouTube learning resources.
- **QC Layer 1 – Factual Accuracy:** Review factual claims, source reliability, and research gaps.
- **QC Layer 2 – Instructional Quality:** Evaluate learning objective alignment, clarity, examples, and lesson structure.
- **Lesson Editing:** Review and modify generated lesson content.
- **Export:** Download the lesson and both QC reports.
- **Error Handling:** Validate empty inputs and support offline demo mode.

## Technology Stack

- Python
- Streamlit
- OpenAI API (GPT-4o-mini – optional)
- Markdown

## Project Structure

```text
Kalvium-LessonCraft-AI/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Kalvium-LessonCraft-AI.git
```

### 2. Navigate to the project directory

```bash
cd Kalvium-LessonCraft-AI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open locally at:

`http://localhost:8501`

## AI Configuration

An OpenAI API key is optional.

Enter your API key in the application's sidebar to enable GPT-4o-mini-based lesson generation and both QC audits.

Without an API key, the application runs in offline demo mode using a predefined lesson structure and heuristic QC checks.

**Security:** Never upload API keys or `.env` files to GitHub.

## Test Cases

### Test Case 1: HTTP Requests and Responses

**Learning Objective:** Explain GET and POST methods and distinguish between 2xx, 4xx, and 5xx response status categories.

### Test Case 2: Database Normalization

**Learning Objective:** Explain 1NF, 2NF, and 3NF with examples and describe how normalization reduces data redundancy.

## Quality Control Approach

**QC Layer 1 – Research and Factual Accuracy**
- Review factual correctness.
- Identify unsupported claims.
- Evaluate source relevance and reliability.
- Identify research gaps.

**QC Layer 2 – Instructional Quality**
- Check learning objective alignment.
- Evaluate lesson clarity and structure.
- Review examples and practical applications.
- Identify missing instructional elements.

Both QC layers produce separate audit reports.

## Future Improvements

- Integration with live research APIs.
- Automated source verification and citation extraction.
- Persistent lesson storage.
- Additional export formats such as PDF.

## Author

Developed as part of the Kalvium AI Research Intern assignment.

