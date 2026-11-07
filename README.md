# LessonCraft AI – Kalvium AI Research Intern Task

A local Streamlit prototype for generating 45-minute lessons, providing research discovery links, running two separate quality-control audits, reviewing/editing content, and exporting the lesson and QC reports.

## Features
- Lesson title and learning objective inputs
- AI generation and separate AI prompts for factual/research QC and instructional QC when an OpenAI API key is supplied
- Offline demo mode so the workflow can still be demonstrated without an API key
- Research discovery links for Google Books, web search, and YouTube
- Editable lesson, rerunnable QC, Markdown/TXT export
- Empty-input validation and session-state preservation during the running session

## Setup
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Run `python -m venv .venv`
4. Activate it:
   - Windows: `.venv\\Scripts\\activate`
   - macOS/Linux: `source .venv/bin/activate`
5. Run `pip install -r requirements.txt`
6. Optional AI mode: set `OPENAI_API_KEY` in your terminal. Do not upload the key to GitHub.
   - PowerShell: `$env:OPENAI_API_KEY="your-key"`
   - macOS/Linux: `export OPENAI_API_KEY="your-key"`
7. Run `streamlit run app.py`

Without a key, the app runs in offline demo mode. In that mode, the lesson is a structured starter template and the QC reports are heuristic checks, not independent AI verification. The research URLs are search links, not sources already verified. For a real lesson, open the links, select credible sources, and cite the exact pages/videos.

## Test workflow
**Test 1 (required):** HTTP Requests and Responses; objective: Explain GET and POST methods and distinguish between 2xx, 4xx, and 5xx response status categories.

**Test 2:** Database Normalization; objective: Explain 1NF, 2NF and 3NF and why normalization reduces data redundancy.

For each test, generate a lesson, inspect the references, review both QC reports, edit the lesson, rerun QC, and download the Markdown export.

## Technical decisions
- Streamlit was selected for fast local development and a simple instructor-facing interface.
- OpenAI GPT-4o-mini is optional for lesson generation and two independent audit prompts.
- QC Layer 1 focuses on factual claims and source reliability; QC Layer 2 focuses on objective alignment and teaching design.
- Search URLs are used as research discovery starting points; they must be replaced with verified source citations before the lesson is treated as final.
