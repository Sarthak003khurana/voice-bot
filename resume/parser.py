import re

def parse_resume(text):

    text_lower = text.lower()

    # -------- SKILLS --------
    common_skills = [
        "python", "java", "c++", "javascript",
        "react", "flask", "django", "node",
        "machine learning", "deep learning",
        "sql", "mongodb", "git", "docker"
    ]

    skills = [s.capitalize() for s in common_skills if s in text_lower]

    # -------- PROJECTS --------
    project_keywords = ["project", "developed", "built", "created"]
    projects = []

    for line in text.split("\n"):
        line_clean = line.strip()
        if any(word in line_clean.lower() for word in project_keywords):
            if len(line_clean) > 20:
                projects.append(line_clean)

    # -------- ACHIEVEMENTS --------
    achievement_keywords = ["achieved", "award", "won", "rank", "certified"]
    achievements = []

    for line in text.split("\n"):
        line_clean = line.strip()
        if any(word in line_clean.lower() for word in achievement_keywords):
            achievements.append(line_clean)

    return {
        "skills": list(set(skills)),
        "projects": projects[:3],        # limit
        "achievements": achievements[:3],
        "raw_text": text
    }