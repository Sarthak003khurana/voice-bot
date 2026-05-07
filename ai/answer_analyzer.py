import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def analyze_answer(question, answer):

    prompt = f"""
You are a strict technical interviewer.

Evaluate the candidate's answer.

Question:
{question}

Answer:
{answer}

Instructions:
- Be very concise
- Mention only mistakes or missing points
- Do NOT explain the full answer
- Max 2 short sentences
- If answer is correct, say: "Good answer, but can be more detailed."

Output only the feedback.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 40,
                    "temperature": 0.5
                }
            }
        )

        data = response.json()

        return data.get("response", "Answer lacks clarity.")

    except Exception as e:
        print("Error:", e)
        return "Could not evaluate answer."