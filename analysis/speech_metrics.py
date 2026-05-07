import time

# 1️⃣ Speaking speed
def calculate_wpm(text, duration):
    words = len(text.split())
    minutes = duration / 60
    if minutes == 0:
        return 0
    return int(words / minutes)


# 2️⃣ Filler words detection
def count_filler_words(text):
    fillers = ["um", "uh", "like", "you know", "basically", "actually"]
    count = 0

    text_lower = text.lower()

    for filler in fillers:
        count += text_lower.count(filler)

    return count


# 3️⃣ Confidence score
def calculate_confidence(wpm, filler_count, eye_score):

    score = 0

    # WPM scoring
    if 120 <= wpm <= 180:
        score += 4
    elif 90 <= wpm < 120:
        score += 3
    else:
        score += 2

    # filler penalty
    score += max(0, 3 - filler_count)

    # eye contact contribution
    score += eye_score / 2

    return round(score, 2)