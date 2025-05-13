import pyttsx3
import time


def speak_summary(summary_text):
    start_time = time.time()
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)

        # ✅ Try to set female voice
        for voice in engine.getProperty("voices"):
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break

        print(f"🗣️ Speaking: {summary_text}")
        engine.say(summary_text)
        engine.runAndWait()
        print(f"✅ Done speaking in {round(time.time() - start_time, 2)}s")

    except Exception as e:
        print(f"❌ Speaking failed: {e}")
