# import streamlit as st
# from utils.pdf_parser import extract_text_from_pdf, chunk_text
# from utils.api_client import extract_key_topics, generate_exam_questions

# st.set_page_config(page_title="Exam Prep AI", page_icon="📚", layout="centered")

# st.title("📚 Exam Prep AI")
# st.subheader("Upload your course materials and generate practice questions")

# # --- Session state initialization ---
# if "text_chunks" not in st.session_state:
#     st.session_state.text_chunks = None
# if "topics" not in st.session_state:
#     st.session_state.topics = None
# if "questions" not in st.session_state:
#     st.session_state.questions = None
# if "feedback_history" not in st.session_state:
#     st.session_state.feedback_history = []

# # --- Step 1: Upload PDF ---
# st.header("Step 1: Upload Your Material")
# uploaded_file = st.file_uploader("Upload a PDF (lecture slides or notes)", type="pdf")

# if uploaded_file:
#     with st.spinner("Extracting text from PDF..."):
#         raw_text = extract_text_from_pdf(uploaded_file)
#         st.session_state.text_chunks = chunk_text(raw_text)
#     st.success(f"PDF processed successfully! ({len(st.session_state.text_chunks)} sections found)")

# # --- Step 2: Extract Key Topics ---
# if st.session_state.text_chunks:
#     st.header("Step 2: Analyze Key Topics")

#     if st.button("Extract Key Topics"):
#         with st.spinner("Analyzing your material..."):
#             st.session_state.topics = extract_key_topics(st.session_state.text_chunks)
#         st.success("Topics extracted!")

#     if st.session_state.topics:
#         with st.expander("View Extracted Topics", expanded=True):
#             st.markdown(st.session_state.topics)

# # --- Step 3: Set Preferences ---
# if st.session_state.topics:
#     st.header("Step 3: Customize Your Questions")

#     col1, col2 = st.columns(2)

#     with col1:
#         question_type = st.selectbox(
#             "Question Type",
#             ["mixed", "multiple choice", "short answer", "long answer"]
#         )
#         difficulty = st.selectbox(
#             "Difficulty Level",
#             ["easy", "medium", "hard"]
#         )

#     with col2:
#         num_questions = st.slider("Number of Questions", min_value=3, max_value=15, value=5)
#         focus_areas = st.text_input("Focus Areas (optional)", placeholder="e.g. Chapter 3, derivatives, recursion")

# # --- Step 4: Generate Questions ---
# if st.session_state.topics:
#     st.header("Step 4: Generate Questions")

#     if st.button("Generate Exam Questions", type="primary"):
#         feedback_summary = " | ".join(st.session_state.feedback_history[-3:]) if st.session_state.feedback_history else ""

#         user_preferences = {
#             "question_type": question_type,
#             "difficulty": difficulty,
#             "num_questions": num_questions,
#             "focus_areas": focus_areas if focus_areas else "all topics",
#             "feedback": feedback_summary
#         }

#         with st.spinner("Generating questions..."):
#             st.session_state.questions = generate_exam_questions(
#                 st.session_state.text_chunks,
#                 st.session_state.topics,
#                 user_preferences
#             )
#         st.success("Questions generated!")

#     if st.session_state.questions:
#         st.markdown("---")
#         st.markdown(st.session_state.questions)

#         # --- Step 5: Feedback Loop ---
#         st.header("Step 5: Give Feedback")
#         st.write("Help the AI improve the next set of questions:")

#         col1, col2, col3 = st.columns(3)
#         with col1:
#             difficulty_feedback = st.selectbox("Difficulty", ["Just right", "Too easy", "Too hard"])
#         with col2:
#             coverage_feedback = st.selectbox("Topic Coverage", ["Good coverage", "Too narrow", "Too broad"])
#         with col3:
#             style_feedback = st.selectbox("Question Style", ["Good style", "Too theoretical", "Too memorization-based"])

#         if st.button("Submit Feedback & Regenerate"):
#             feedback = f"Difficulty: {difficulty_feedback}, Coverage: {coverage_feedback}, Style: {style_feedback}"
#             st.session_state.feedback_history.append(feedback)
#             st.info("Feedback saved! Click 'Generate Exam Questions' again to get improved questions.")


import json
import streamlit as st
from utils.pdf_parser import extract_text_from_pdf, chunk_text
from utils.api_client import extract_key_topics, generate_exam_questions

st.set_page_config(page_title="Exam Prep AI", page_icon="📚", layout="centered")

st.title("📚 Exam Prep AI")
st.subheader("Upload your course materials and generate practice questions")

# --- Session state initialization ---
if "text_chunks" not in st.session_state:
    st.session_state.text_chunks = None
if "topics" not in st.session_state:
    st.session_state.topics = None
if "all_question_sets" not in st.session_state:
    st.session_state.all_question_sets = []
if "feedback_history" not in st.session_state:
    st.session_state.feedback_history = []

# --- Step 1: Upload PDF ---
st.header("Step 1: Upload Your Material")
uploaded_file = st.file_uploader("Upload a PDF (lecture slides or notes)", type="pdf")

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        raw_text = extract_text_from_pdf(uploaded_file)
        st.session_state.text_chunks = chunk_text(raw_text)
    st.success(f"PDF processed successfully! ({len(st.session_state.text_chunks)} sections found)")

# --- Step 2: Extract Key Topics ---
if st.session_state.text_chunks:
    st.header("Step 2: Analyze Key Topics")

    if st.button("Extract Key Topics"):
        with st.spinner("Analyzing your material..."):
            st.session_state.topics = extract_key_topics(st.session_state.text_chunks)
        st.success("Topics extracted!")

    if st.session_state.topics:
        with st.expander("View Extracted Topics", expanded=True):
            st.markdown(st.session_state.topics)

# --- Step 3: Set Preferences ---
if st.session_state.topics:
    st.header("Step 3: Customize Your Questions")

    col1, col2 = st.columns(2)

    with col1:
        question_type = st.selectbox(
            "Question Type",
            ["mixed", "multiple choice", "short answer", "long answer"]
        )
        difficulty = st.selectbox(
            "Difficulty Level",
            ["easy", "medium", "hard"]
        )

    with col2:
        num_questions = st.slider("Number of Questions", min_value=3, max_value=15, value=5)
        focus_areas = st.text_input("Focus Areas (optional)", placeholder="e.g. Chapter 3, derivatives, recursion")

    st.session_state.last_question_type = question_type
    st.session_state.last_difficulty = difficulty
    st.session_state.last_num_questions = num_questions
    st.session_state.last_focus_areas = focus_areas if focus_areas else "all topics"   

# --- Step 4: Generate Questions ---
if st.session_state.topics:
    st.header("Step 4: Generate Questions")

    if st.button("Generate Exam Questions", type="primary"):
        feedback_summary = " | ".join(st.session_state.feedback_history[-3:]) if st.session_state.feedback_history else ""

        user_preferences = {
            "question_type": question_type,
            "difficulty": difficulty,
            "num_questions": num_questions,
            "focus_areas": focus_areas if focus_areas else "all topics",
            "feedback": feedback_summary
        }

        with st.spinner("Generating questions..."):
            raw_response = generate_exam_questions(
                st.session_state.text_chunks,
                st.session_state.topics,
                user_preferences
            )
        
        try:
            cleaned = raw_response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("```", 1)[0]
            parsed_questions = json.loads(cleaned.strip())
            st.session_state.all_question_sets.append({
                "label": f"Set {len(st.session_state.all_question_sets) + 1} — {difficulty}, {question_type}, {num_questions} questions",
                "questions": parsed_questions
            })
            st.success("Questions generated!")
        except (json.JSONDecodeError, Exception) as e:
            st.error("Something went wrong parsing the response. Please try again.")

# --- Display all question sets ---
if st.session_state.all_question_sets:
    for qset in st.session_state.all_question_sets:
        st.markdown("---")
        st.subheader(qset["label"])

        for i, q in enumerate(qset["questions"]):
            st.markdown(f"**Q{i + 1}: {q['question']}**")

            if q.get("options"):
                for opt, text in q["options"].items():
                    st.markdown(f"{opt}) {text}")

            with st.expander("View Answer & Explanation"):
                st.markdown(f"**Answer:** {q['answer']}")
                st.markdown(f"**Explanation:** {q['explanation']}")

            # Per-question feedback
            set_idx = st.session_state.all_question_sets.index(qset)
            wrong_key = f"wrong_{set_idx}_{i}"
            reason_key = f"reason_{set_idx}_{i}"

            got_wrong = st.checkbox("I got this wrong", key=wrong_key)
            if got_wrong:
                st.selectbox(
                    "Why did you get it wrong?",
                    ["Concept not understood", "Calculation error", "Misread the question"],
                    key=reason_key
                )

            st.markdown("")

    # --- Step 5: Feedback Loop ---
    st.markdown("---")
    st.header("Step 5: Give Feedback")
    st.write("Help the AI improve the next set of questions:")

    col1, col2, col3 = st.columns(3)
    with col1:
        difficulty_feedback = st.selectbox("Difficulty", ["Just right", "Too easy", "Too hard"])
    with col2:
        coverage_feedback = st.selectbox("Topic Coverage", ["Good coverage", "Too narrow", "Too broad"])
    with col3:
        style_feedback = st.selectbox("Question Style", ["Good style", "Too theoretical", "Too memorization-based"])

    if st.button("Submit Feedback"):
        wrong_questions = []
        for set_idx, qset in enumerate(st.session_state.all_question_sets):
            for i, q in enumerate(qset["questions"]):
                wrong_key = f"wrong_{set_idx}_{i}"
                reason_key = f"reason_{set_idx}_{i}"
                if st.session_state.get(wrong_key):
                    reason = st.session_state.get(reason_key, "Concept not understood")
                    wrong_questions.append(
                        f"- Q: {q['question']} | Correct answer: {q['answer']} | Reason wrong: {reason}"
                    )

        general_feedback = f"Difficulty: {difficulty_feedback}, Coverage: {coverage_feedback}, Style: {style_feedback}"
        feedback_parts = [general_feedback]

        if wrong_questions:
            feedback_parts.append("Student got the following questions wrong:\n" + "\n".join(wrong_questions))
            st.success(f"Feedback saved! {len(wrong_questions)} wrong question(s) recorded.")
        else:
            st.success("Feedback saved!")

        st.session_state.feedback_history.append("\n".join(feedback_parts))

    if st.session_state.feedback_history:
        st.markdown("---")
        if st.button("Generate Improved Questions", type="primary"):
            feedback_summary = " | ".join(st.session_state.feedback_history[-3:])
            user_preferences = {
                "question_type": st.session_state.get("last_question_type", "mixed"),
                "difficulty": st.session_state.get("last_difficulty", "medium"),
                "num_questions": st.session_state.get("last_num_questions", 5),
                "focus_areas": st.session_state.get("last_focus_areas", "all topics"),
                "feedback": feedback_summary
            }
            with st.spinner("Generating improved questions..."):
                raw_response = generate_exam_questions(
                    st.session_state.text_chunks,
                    st.session_state.topics,
                    user_preferences
                )
            
            try:
                cleaned = raw_response.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.split("\n", 1)[1]
                if cleaned.endswith("```"):
                    cleaned = cleaned.rsplit("```", 1)[0]
                parsed_questions = json.loads(cleaned.strip())
                st.session_state.all_question_sets.append({
                    "label": f"Set {len(st.session_state.all_question_sets) + 1} — improved based on feedback",
                    "questions": parsed_questions
                })
                st.rerun()
            except (json.JSONDecodeError, Exception) as e:
                st.error("Something went wrong parsing the response. Please try again.")
