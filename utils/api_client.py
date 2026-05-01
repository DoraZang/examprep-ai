import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def extract_key_topics(text_chunks):
    """
    Analyze course material and extract key topics and concepts for exam preparation.
    text_chunks: list of text chunks from the uploaded PDF
    Returns: a structured string of key topics
    """
    combined_text = "\n\n".join(text_chunks[:3])  # Use first 3 chunks to save tokens

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"""You are an expert academic tutor. Analyze the following course material and extract the most important topics and concepts that are likely to appear on an exam.

Course Material:
{combined_text}

Please provide:
1. A list of 5-8 main topics covered
2. Key concepts and definitions for each topic
3. Any formulas, theorems, or important facts mentioned

Format your response clearly with headers for each topic. For all mathematical expressions, use LaTeX notation: inline math with $...$ and block math with $$...$$."""
            }
        ]
    )

    return message.content[0].text


# def generate_exam_questions(text_chunks, topics, user_preferences):
#     """
#     Generate exam-style questions based on course material and user preferences.
#     text_chunks: list of text chunks from the uploaded PDF
#     topics: extracted key topics from extract_key_topics()
#     user_preferences: dict containing question_type, difficulty, num_questions, focus_areas
#     Returns: generated questions as a string
#     """
#     combined_text = "\n\n".join(text_chunks[:3])

#     question_type = user_preferences.get("question_type", "mixed")
#     difficulty = user_preferences.get("difficulty", "medium")
#     num_questions = user_preferences.get("num_questions", 5)
#     focus_areas = user_preferences.get("focus_areas", "all topics")
#     feedback = user_preferences.get("feedback", "")

#     feedback_context = ""
#     if feedback:
#         feedback_context = f"\n\nPrevious feedback to incorporate: {feedback}"

#     message = client.messages.create(
#         model="claude-haiku-4-5-20251001",
#         max_tokens=2000,
#         messages=[
#             {
#                 "role": "user",
#                 "content": f"""You are an expert professor creating exam questions. Generate exam questions based on the following course material and requirements.

# Course Material:
# {combined_text}

# Key Topics Identified:
# {topics}

# Requirements:
# - Number of questions: {num_questions}
# - Question type: {question_type} (options: multiple choice, short answer, long answer, mixed)
# - Difficulty level: {difficulty} (options: easy, medium, hard)
# - Focus areas: {focus_areas}{feedback_context}

# Please generate exactly {num_questions} questions. For each question:
# 1. Write the question clearly
# 2. If multiple choice, provide 4 options (A, B, C, D)
# 3. Provide the correct answer
# 4. Briefly explain why it is correct

# Match the difficulty and style to a real university exam."""
#             }
#         ]
#     )

#     return message.content[0].text

def generate_exam_questions(text_chunks, topics, user_preferences):
    """
    Generate exam-style questions based on course material and user preferences.
    Returns a JSON string of structured questions.
    """
    combined_text = "\n\n".join(text_chunks[:3])

    question_type = user_preferences.get("question_type", "mixed")
    difficulty = user_preferences.get("difficulty", "medium")
    num_questions = user_preferences.get("num_questions", 5)
    focus_areas = user_preferences.get("focus_areas", "all topics")
    feedback = user_preferences.get("feedback", "")

    feedback_context = ""
    if feedback:
        feedback_context = f"\n\nStudent performance feedback from previous set:\n{feedback}\n\nIMPORTANT: For each wrong answer, generate a similar question targeting the same concept. Prioritize these weak areas in the new question set."

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=8192,
        messages=[
            {
                "role": "user",
                "content": f"""You are an expert professor creating exam questions. Generate exam questions based on the following course material and requirements.

Course Material:
{combined_text}

Key Topics Identified:
{topics}

Requirements:
- Number of questions: {num_questions}
- Question type: {question_type} (options: multiple choice, short answer, long answer, mixed)
- Difficulty level: {difficulty} (options: easy, medium, hard)
- Focus areas: {focus_areas}{feedback_context}

Return ONLY a JSON array with no other text, no markdown, no backticks. For all mathematical expressions, use LaTeX notation: inline math with $...$ and block math with $$...$$. Each element must have:
- "question": the question text
- "options": object with keys "A", "B", "C", "D" for multiple choice, otherwise null
- "answer": the correct answer
- "explanation": brief explanation of why the answer is correct

Example format:
[{{"question": "What is X?", "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}}, "answer": "A", "explanation": "Because..."}}]

Match the difficulty and style to a real university exam. Keep each explanation concise (maximum 3 sentences)."""
            }
        ]
    )

    return message.content[0].text