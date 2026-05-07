import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import time
from faster_whisper import WhisperModel

# 🔥 Load model once
model = WhisperModel("tiny", device="cpu", compute_type="int8")


def listen(
    samplerate=16000,
    silence_threshold=0.005,     # 🔥 lowered
    silence_duration=1.5,
    start_threshold=0.008,       # 🔥 lowered
    max_wait_time=5              # 🔥 NEW (prevents infinite wait)
):
    print("🎤 Waiting for speech...")

    chunk_duration = 0.3
    chunk_size = int(samplerate * chunk_duration)

    audio_data = []
    silence_time = 0
    speaking_started = False

    start_time = time.time()

    stream = sd.InputStream(samplerate=samplerate, channels=1)
    stream.start()

    try:
        while True:
            chunk, _ = stream.read(chunk_size)
            chunk = chunk.flatten()

            volume = np.linalg.norm(chunk) / len(chunk)

            # 🔥 DEBUG (see mic sensitivity)
            # print(f"Volume: {volume:.5f}")

            # 🔥 TIMEOUT FIX (very important)
            if not speaking_started and (time.time() - start_time > max_wait_time):
                print("⚠️ No speech detected, forcing recording...")
                speaking_started = True

            # 🔥 Detect speech start
            if not speaking_started:
                if volume > start_threshold:
                    speaking_started = True
                    print("🗣️ Speech detected... Recording")
                    audio_data.append(chunk)
                continue

            # After speech starts
            audio_data.append(chunk)

            # 🔥 Detect silence
            if volume < silence_threshold:
                silence_time += chunk_duration
            else:
                silence_time = 0

            # Stop when silence detected
            if silence_time > silence_duration:
                print("🛑 Silence detected, stopping...")
                break

    finally:
        stream.stop()
        stream.close()

    # No speech case
    if not audio_data:
        return "No speech detected.", np.array([]), 0

    # Combine audio
    audio = np.concatenate(audio_data)

    duration = len(audio) / samplerate

    # Save temp file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav.write(f.name, samplerate, audio)

        print("🧠 Transcribing...")

        segments, _ = model.transcribe(f.name)
        text = " ".join([seg.text for seg in segments])

    text = text.strip() if text else "No response detected."

    return text, audio, duration