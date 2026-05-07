import requests
import random

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_question(parsed_data, level="medium"):

    skills = parsed_data.get("skills", [])
    projects = parsed_data.get("projects", [])
    achievements = parsed_data.get("achievements", [])

    # Keep your context (NO REMOVAL)
    context = f"""
Skills: {skills}
Projects: {projects}
Achievements: {achievements}
"""

    # Keep your random styles
    styles = [
        "technical concept",
        "problem solving",
        "behavioral",
        "situational",
        "mixed"
    ]

    style = random.choice(styles)

    # 🔥 IMPROVED PROMPT (STRICT + RELIABLE)
    prompt = f"""
You are a professional interviewer.

Candidate background:
{context}

Interview style: {style}

Task:
Generate EXACTLY ONE short interview question.

Rules:
- Maximum 10 words
- Must end with a question mark
- No explanation
- No extra text
- Do NOT repeat the same question

Examples:
What is polymorphism?
Explain REST API?
Tell me about a challenge?

Now generate the question.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 20,
                    "temperature": 0.7
                }
            }
        )

        data = response.json()

        question = data.get("response", "").strip()

        # 🔥 SAFETY CHECK (IMPORTANT)
        if not question or len(question) < 5 or "?" not in question:
            return fallback_question()

        return question

    except Exception as e:
        print("Question generation error:", e)
        return fallback_question()


# 🔥 FALLBACK SYSTEM (NEVER FAILS)
def fallback_question():
    questions = [
        "What is polymorphism?",
        "Explain REST API?",
        "Tell me about a project?",
        "What is OOP?",
        "How do you debug code?",
        "Describe a challenging situation?",
        "What is database indexing?"
    ]
    return random.choice(questions)