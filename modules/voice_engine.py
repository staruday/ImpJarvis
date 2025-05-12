
# from edge_tts import Communicate
# import asyncio
# import threading
# from modules.audio_player import play_audio
# import os  # ✅ for file deletion

# voice = "en-US-GuyNeural"


# def speak_summary(summary_text):
#     communicator = Communicate(summary_text, voice)

#     # ✅ Create a new event loop inside the thread
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(communicator.save("summary.mp3"))

#     # ✅ Play the audio
#     play_audio("summary.mp3")

#     # ✅ Remove the mp3 after playback is complete
#     try:
#         os.remove("summary.mp3")
#     except Exception as e:
#         print(f"Warning: Could not delete summary.mp3 — {e}")
import asyncio
import threading
import os
import pyttsx3
from edge_tts import Communicate
from modules.audio_player import play_audio

voice = "en-US-GuyNeural"


def speak_summary(summary_text):
    try:
        # ✅ Online TTS using Edge
        communicator = Communicate(summary_text, voice)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(communicator.save("summary.mp3"))

        play_audio("summary.mp3")

        # ✅ Remove the file after playback
        os.remove("summary.mp3")

    except Exception as e:
        print(f"⚠️ Online TTS failed: {e}")
        print("🔁 Switching to offline TTS...")

        # ✅ Offline fallback using pyttsx3
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 175)  # Adjust speed if needed
            engine.say(summary_text)
            engine.runAndWait()
        except Exception as ex:
            print(f"❌ Offline TTS also failed: {ex}")
