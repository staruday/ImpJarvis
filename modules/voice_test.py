import speech_recognition as sr

recognizer = sr.Recognizer()
mic_index = 0  # Use the one that worked for you

with sr.Microphone(device_index=mic_index) as source:
    print(f"🎧 Using mic index {mic_index}")
    recognizer.adjust_for_ambient_noise(source)
    print("🎙 Speak clearly now...")
    audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

print("📦 Audio length:", len(audio.frame_data))
with open("test_audio.wav", "wb") as f:
    f.write(audio.get_wav_data())  # Optional: save for verification

try:
    text = recognizer.recognize_google(audio)
    print("🧠 Recognized:", text)
except sr.UnknownValueError:
    print("❌ Google could not understand the speech.")
except sr.RequestError as e:
    print(f"❌ Google API error: {e}")
