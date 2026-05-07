import requests
import random

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_followup(question, answer):

    prompt = f"""
You are a professional interviewer.

Original Question:
{question}

Candidate Answer:
{answer}

Task:
Ask ONE follow-up question.

Rules:
- Maximum 10 words
- Must be related to the same topic
- Must go deeper into the concept
- Do NOT repeat the original question
- No explanation
- Only return the question
- Must end with a question mark

Examples:
What happens internally?
Can you give a real example?
How does it work in practice?

Now generate the follow-up question.
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
        followup = data.get("response", "").strip()

        # 🔥 Safety check
        if not followup or len(followup) < 5 or "?" not in followup:
            return fallback_followup()

        return followup

    except Exception as e:
        print("Follow-up generation error:", e)
        return fallback_followup()


# 🔥 Fallback (never fails)
def fallback_followup():
    questions = [
        "Can you explain that further?",
        "What happens internally?",
        "Can you give an example?",
        "Why is this important?",
        "How does it work?"
    ]
    return random.choice(questions)