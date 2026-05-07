import numpy as np


def calculate_wpm(text, duration):
    words = len(text.split())
    minutes = duration / 60 if duration > 0 else 1
    return words / minutes


def calculate_energy(audio):
    return np.mean(np.abs(audio))


def detect_pauses(audio, threshold=0.005):
    silent = np.abs(audio) < threshold
    pause_ratio = np.sum(silent) / len(audio)
    return pause_ratio


def calculate_confidence(text, audio, duration):
    wpm = calculate_wpm(text, duration)
    energy = calculate_energy(audio)
    pause_ratio = detect_pauses(audio)

    score = 0

    # 🗣️ Speech speed
    if 110 <= wpm <= 170:
        score += 4
    elif 80 <= wpm < 110:
        score += 3
    else:
        score += 2

    # 🔊 Voice energy
    if energy > 0.02:
        score += 3
    else:
        score += 2

    # ⏸️ Pauses
    if pause_ratio < 0.4:
        score += 3
    else:
        score += 1

    return round(score, 2)