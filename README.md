# Exam Prep AI

An intelligent exam preparation tool that transforms course materials into personalized practice questions using context engineering and iterative feedback loops.

## Motivation

Students often struggle to use AI effectively for exam preparation — either writing vague prompts that produce irrelevant questions, or failing to iterate based on their performance. This tool automates the entire workflow: from extracting key concepts to generating targeted questions based on what the student actually got wrong.

## Features

- **PDF Parsing** — Upload lecture slides or notes and automatically extract key topics
- **Customizable Question Generation** — Control question type, difficulty, number of questions, and focus areas
- **Iterative Feedback Loop** — Rate question difficulty, coverage, and style to improve the next set
- **Wrong Answer Tracking** — Mark questions you got wrong, specify why, and get similar questions targeting your weak areas
- **Session History** — All generated question sets are preserved so you can review previous practice rounds
- **LaTeX Rendering** — Mathematical expressions are rendered properly for STEM courses

## Tech Stack

- **Python** — Core application logic
- **Streamlit** — Frontend UI
- **Anthropic Claude API** — Question generation and topic extraction
- **pypdf** — PDF text extraction
- **python-dotenv** — Environment variable management

## How It Works

1. Upload a PDF of your course material
2. Extract key topics automatically using Claude
3. Customize your question preferences (type, difficulty, focus areas)
4. Generate practice questions
5. Mark wrong answers and provide feedback
6. Generate an improved set targeting your weak areas

The core of this project is a **context engineering pipeline** — rather than sending a simple prompt, the system dynamically builds a structured context for each API call that includes extracted course content, user preferences, and accumulated feedback history. This produces significantly more accurate and personalized output than a naive prompt.

## Setup

1. Clone the repository
2. Install dependencies:
```bash
   pip install anthropic streamlit pypdf python-dotenv
```
3. Create a `.env` file with your Anthropic API key:
ANTHROPIC_API_KEY=your_key_here
4. Run the app:
```bash
   streamlit run app.py
```

## Project Structure

```
exam-prep-ai/
├── app.py              # Main Streamlit application
├── utils/
│   ├── pdf_parser.py   # PDF text extraction and chunking
│   └── api_client.py   # Claude API integration and prompt engineering
├── .env                # API key (not committed)
└── README.md
```

