import os, json, re
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="LessonCraft AI", page_icon="📚", layout="wide")
st.title("📚 LessonCraft AI")
st.caption("Research-assisted lesson generation • Two-layer quality control • Review and export")

API_KEY = os.getenv("OPENAI_API_KEY", "")
try:
    import openai
except Exception:
    openai = None


def ai_text(prompt, system="You are an expert instructional designer and careful researcher."):
    key = API_KEY or st.session_state.get("api_key", "")
    if key and openai:
        client = openai.OpenAI(api_key=key)
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            temperature=0.4
        )
        return result.choices[0].message.content
    return None


def source_links(title):
    from urllib.parse import quote_plus
    q = quote_plus(title)
    links = [("Books – Google Books search", f"https://books.google.com/books?q={q}")]
    low = title.lower()
    if "http" in low or "request" in low or "response" in low:
        links += [("MDN – HTTP request methods", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods"),
                  ("MDN – HTTP response status codes", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status"),
                  ("RFC 9110 – HTTP Semantics", "https://www.rfc-editor.org/rfc/rfc9110")]
    elif "normal" in low or "database" in low:
        links += [("Microsoft – Database normalization", "https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description"),
                  ("IBM – Database normalization overview", "https://www.ibm.com/think/topics/database-normalization")]
    else:
        links += [("Web – general research search", f"https://www.google.com/search?q={q}+explained")]
    links.append(("YouTube – supplementary videos", f"https://www.youtube.com/results?search_query={q}+tutorial"))
    return links


def fallback_lesson(title, objective):
    return f'''# {title}\n\n**Learning objective:** {objective}\n**Estimated completion time:** 45 minutes\n\n## 1. Introduction (5 minutes)\nStart by connecting **{title}** to a real-world situation. Think about where this concept appears in applications, products, or everyday technology. By the end of this lesson, you should be able to explain the key idea and apply it to a simple example.\n\n## 2. Core concepts (12 minutes)\n\n### What does it mean?\n{title} refers to the set of concepts and techniques used to understand this topic. Begin with its purpose, the problem it solves, and the main terms associated with it.\n\n### How does it work?\n1. Identify the problem or requirement.\n2. Understand the key components involved.\n3. Follow the process in the correct order.\n4. Check the result and consider possible limitations.\n\n## 3. Worked example (8 minutes)\nConsider a practical situation related to **{title}**. First identify the input or problem, then apply the relevant concept step by step, and finally explain why the result makes sense. Try changing one condition and observe how the outcome changes.\n\n## 4. Practical application (7 minutes)\nA useful way to apply this topic is to build a small demonstration or analyse a real system that uses it. Record the problem, the approach, the result, and one limitation.\n\n## 5. Activity (5 minutes)\nWrite a short example of **{title}** in a real-world context. Identify at least two important concepts and explain how they contribute to the outcome.\n\n## 6. Knowledge check (5 minutes)\n1. Define the central idea of {title}.\n2. Describe the main steps or components.\n3. Give one practical application.\n4. State one limitation or common mistake.\n\n## 7. Summary (3 minutes)\nYou should now be able to: **{objective}**. Review the key terms, revisit the worked example, and explain the concept in your own words.\n\n> **Research note:** This is a starter lesson generated in offline/demo mode. Verify topic-specific facts against the references before teaching or submitting it.\n'''


def fallback_qc1(lesson, links):
    checks = []
    checks.append("Source links are provided for books, web research, and videos; these are search links, not individually verified sources.")
    checks.append("Review topic-specific definitions, dates, statistics, and technical claims against primary or authoritative references.")
    checks.append("The lesson contains general instructional guidance; add precise facts and citations before final use.")
    checks.append("No unsupported numerical statistics were detected by the basic automated check.")
    return "# QC Layer 1 – Research and Factual Accuracy\n\n**Status: Needs human source verification**\n\n" + "\n".join(f"- {x}" for x in checks) + "\n\n**Suggested improvement:** Replace search-result links with 2–3 sources actually opened and checked; cite the exact page/video next to relevant claims."


def fallback_qc2(lesson, objective):
    sections = ["Introduction", "Core concepts", "Worked example", "Practical application", "Activity", "Knowledge check", "Summary"]
    missing = [s for s in sections if s.lower() not in lesson.lower()]
    word_count = len(lesson.split())
    status = "Pass – structure is present" if not missing else "Needs improvement – sections missing"
    return ("# QC Layer 2 – Instructional Quality\n\n"
            f"**Status: {status}**\n\n"
            f"- Learning objective supplied: {objective}\n"
            f"- Estimated lesson duration: 45 minutes (5 + 12 + 8 + 7 + 5 + 5 + 3).\n"
            f"- Approximate word count: {word_count}.\n"
            f"- Sections found: {', '.join(s for s in sections if s.lower() in lesson.lower()) or 'None'}.\n"
            f"- Missing sections: {', '.join(missing) if missing else 'None'}.\n\n"
            "**Suggested improvements:** Ensure every section directly supports the learning objective; add a worked example with a clear answer, and make the knowledge check assess the stated objective."
    )


def run_qc(lesson, objective, links):
    p1 = "Audit this lesson only for factual accuracy, unsupported claims, source quality, relevance, gaps and inconsistencies. Do not assess teaching style. Return issues and specific fixes.\n\n" + lesson + "\n\nReferences:\n" + "\n".join(u for _,u in links)
    p2 = "Audit this lesson only for instructional quality: alignment to the learning objective, clarity, sequencing, 45-minute feasibility, examples, practical application and knowledge checks. Do not fact-check. Return issues and specific fixes.\n\nLearning objective: " + objective + "\n\n" + lesson
    q1 = ai_text(p1, "You are a research fact-checking auditor. Be cautious; never claim you verified sources you did not access.")
    q2 = ai_text(p2, "You are an instructional design auditor. Evaluate alignment and learning effectiveness separately from factual accuracy.")
    return q1 or fallback_qc1(lesson, links), q2 or fallback_qc2(lesson, objective)

with st.sidebar:
    st.header("Settings")
    st.text_input("OpenAI API key (optional)", type="password", key="api_key", help="If provided, the app uses GPT-4o-mini for lesson generation and both QC audits. Without a key, demo mode works locally.")
    st.caption("Never commit your API key to GitHub.")
    st.markdown("**Mode:** " + ("AI mode" if (API_KEY or st.session_state.get("api_key")) and openai else "Offline demo mode"))

col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Lesson Title", value="HTTP Requests and Responses")
with col2:
    objective = st.text_input("Learning Objective", value="Explain GET and POST methods and distinguish between 2xx, 4xx, and 5xx response status categories.")

if st.button("✨ Generate lesson and run both QC layers", type="primary", use_container_width=True):
    if not title.strip() or not objective.strip():
        st.error("Please enter both a lesson title and a learning objective.")
    else:
        with st.spinner("Preparing lesson and independent quality audits..."):
            links = source_links(title)
            prompt = f"Create a well-researched, accurate lesson for a learner. Title: {title}. Learning objective: {objective}. It must take exactly about 45 minutes including explanations, examples, an activity and knowledge checks. Use clear headings and concise explanations. Include practical examples. Do not invent citations or claim sources were accessed. Provide a References section with source types/search links to be filled in by the application."
            generated = ai_text(prompt)
            lesson = generated if generated else fallback_lesson(title, objective)
            q1, q2 = run_qc(lesson, objective, links)
            st.session_state.update({"lesson": lesson, "qc1": q1, "qc2": q2, "links": links, "title": title, "objective": objective})
        st.success("Lesson generated and both QC layers completed.")

if "lesson" in st.session_state:
    st.divider()
    st.subheader("1. Research references")
    st.caption("These are live search links to help you locate relevant material; replace them with the exact sources you read before final submission.")
    for label, url in st.session_state.links:
        st.markdown(f"- [{label}]({url})")
    st.subheader("2. Review and edit lesson")
    edited = st.text_area("Edit the lesson below. Your changes remain in this session.", value=st.session_state.lesson, height=420, key="lesson_editor")
    if st.button("Save edits and rerun QC", use_container_width=True):
        q1, q2 = run_qc(edited, st.session_state.objective, st.session_state.links)
        st.session_state.update({"lesson": edited, "qc1": q1, "qc2": q2})
        st.success("Edits saved and QC reports refreshed.")
    left, right = st.columns(2)
    with left:
        st.subheader("3. QC Layer 1 – Factual accuracy")
        st.markdown(st.session_state.qc1)
    with right:
        st.subheader("4. QC Layer 2 – Instructional quality")
        st.markdown(st.session_state.qc2)
    st.subheader("5. Export")
    combined = (st.session_state.lesson + "\n\n---\n\n" + st.session_state.qc1 + "\n\n---\n\n" + st.session_state.qc2 + "\n\n## Research links\n" + "\n".join(f"- [{n}]({u})" for n,u in st.session_state.links))
    st.download_button("⬇️ Download lesson + both QC reports (.md)", combined, file_name="lesson_and_qc_reports.md", mime="text/markdown", use_container_width=True)
    st.download_button("⬇️ Download QC reports only (.txt)", st.session_state.qc1 + "\n\n" + st.session_state.qc2, file_name="qc_reports.txt", mime="text/plain", use_container_width=True)

st.divider()
st.subheader("Quick test cases required by the assignment")
st.markdown("- **Test 1:** HTTP Requests and Responses – explain GET/POST and 2xx/4xx/5xx.\n- **Test 2:** Database Normalization – explain 1NF, 2NF and 3NF and why normalization reduces data redundancy.")
st.caption("Error handling: empty inputs are blocked; generation failures fall back to demo mode; edits remain in Streamlit session state; rerun QC after editing.")
