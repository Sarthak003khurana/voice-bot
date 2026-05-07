from resume.extractor import extract_resume_text
from resume.parser import parse_resume
from speech.tts import speak
from speech.stt import listen
from ai.question_generator import generate_question
from ai.answer_analyzer import analyze_answer
from ai.followup_generator import generate_followup
from analysis.eye_contact import check_eye_contact

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import threading
import time
import requests


def is_weak_answer(feedback):
    keywords = ["lack", "incorrect", "missing", "weak", "unclear"]
    return any(word in feedback.lower() for word in keywords)


def run_intro_round():
    speak("Please introduce yourself.")
    time.sleep(0.3)

    print("\n🎤 Listening for your introduction...")
    intro = listen()

    print("\nCandidate Intro:", intro)

    feedback = analyze_answer("Introduce yourself", intro)

    return intro, feedback


def run_interview():
    try:
        Tk().withdraw()

        resume_path = askopenfilename(
            title="Upload Resume",
            filetypes=[("Resume Files", "*.pdf *.jpg *.jpeg *.png")]
        )

        if not resume_path:
            print("No resume selected.")
            return

        print("\nSelected resume:", resume_path)

        text = extract_resume_text(resume_path)
        parsed = parse_resume(text)

        speak("Welcome to your AI interview.")
        time.sleep(0.5)

        # ============================
        # INTRO ROUND
        # ============================
        speak("We will begin with your introduction.")
        time.sleep(0.5)

        intro_text, intro_feedback = run_intro_round()

        speak("Now we will begin the technical interview.")
        time.sleep(0.5)

        # ============================
        # QUESTIONS
        # ============================
        question = generate_question(parsed)
        num_questions = 3
        interview_data = []

        for i in range(num_questions):

            print(f"\n--- Question {i+1} ---")

            speak(question)
            time.sleep(0.3)

            eye_score = 0

            def run_eye():
                nonlocal eye_score
                eye_score = check_eye_contact(duration=3)

            thread = threading.Thread(target=run_eye)
            thread.start()

            print("\n🎤 Listening for your answer...")
            answer = listen()

            thread.join()

            print("\nCandidate:", answer)
            print(f"👁 Eye Contact Score: {eye_score}/10")

            feedback = analyze_answer(question, answer)

            # FOLLOW-UP (with evaluation)
            if is_weak_answer(feedback):
                speak("Let me ask a follow-up question.")
                time.sleep(0.3)

                follow_q = generate_followup(question, answer)
                speak(follow_q)

                print("\n🎤 Listening for follow-up answer...")
                follow_answer = listen()

                print("\nFollow-up Answer:", follow_answer)

                follow_feedback = analyze_answer(follow_q, follow_answer)

                answer += f" | Follow-up: {follow_answer} ({follow_feedback})"

            interview_data.append({
                "question": question,
                "answer": answer,
                "eye_score": eye_score,
                "feedback": feedback
            })

            if i < num_questions - 1:
                speak("Next question.")
                time.sleep(0.3)
                question = generate_question(parsed)

        # ============================
        # FINAL FEEDBACK
        # ============================
        speak("Here is your interview feedback.")
        time.sleep(0.5)

        full_report = f"Introduction:\n{intro_text}\n"

        speak("Feedback for your introduction.")
        speak(intro_feedback)

        total_eye = 0

        for i, item in enumerate(interview_data):
            feedback = item["feedback"]
            total_eye += item["eye_score"]

            speak(f"For question {i+1}.")
            speak(feedback)
            speak(f"Eye contact score was {item['eye_score']} out of 10.")

            full_report += f"""
Question {i+1}: {item['question']}
Answer: {item['answer']}
"""

        avg_eye = total_eye / len(interview_data) if interview_data else 0

        speak(f"Your average eye contact score is {round(avg_eye, 2)}.")

        # ============================
        # FINAL RESULT
        # ============================
        final_prompt = f"""
You are an interviewer.

Based on this interview:

{full_report}

Average eye contact: {avg_eye}

Give:
1. Short summary
2. Final decision: PASS or FAIL

Return:
Summary:
Decision:
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": final_prompt,
                "stream": False
            }
        )

        result = response.json().get("response", "").strip()

        if not result:
            result = "Summary: Average performance.\nDecision: PASS"

        print("\n===== FINAL RESULT =====")
        print(result)

        speak("Here is your final result.")
        speak(result)

        speak("Thank you for attending the interview.")

    except Exception as e:
        print("Error:", e)