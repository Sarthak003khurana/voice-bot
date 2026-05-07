def speak(text):
    try:
        import pyttsx3

        engine = pyttsx3.init()
        engine.setProperty("rate", 160)

        text = str(text).strip()

        print("\nBot:", text)

        engine.say(text)
        engine.runAndWait()

        engine.stop()

    except Exception as e:
        print("TTS Error:", e)