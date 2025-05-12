import speech_recognition as sr
import pvporcupine
import pyaudio
import struct

# ✅ Detect AirPods mic index (SpeechRecognition)


def get_airpods_mic_index():
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        if "airpods" in name.lower():
            print(f"🎧 Using AirPods mic: {name} (index {i})")
            return i
    print("❌ AirPods mic not found. Using default mic.")
    return None

# ✅ Wake word detection using Google STT


def wake_with_google(wake_word="jarvis", mic_index=None):
    recognizer = sr.Recognizer()

    # If no index provided, try AirPods, then fallback
    if mic_index is None:
        mic_index = get_airpods_mic_index()

    try:
        with sr.Microphone(device_index=0) as source:
            print(f"🎧 Using mic index {mic_index} (Google STT)...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        return False

    try:
        text = recognizer.recognize_google(audio)
        print("🧠 You said:", text)
        if wake_word.lower() in text.lower():
            print("✅ Wake word detected (Google)")
            return True
        else:
            print("❌ Wake word not found.")
            return False
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError as e:
        print(f"❌ Google API error: {e}")
    return False

# ✅ Wake word detection using Porcupine


def wake_with_porcupine(keyword="jarvis"):
    try:
        porcupine = pvporcupine.create(keywords=[keyword])
    except Exception as e:
        print(f"❌ Porcupine init error: {e}")
        return False

    pa = pyaudio.PyAudio()
    airpods_index = None

    for i in range(pa.get_device_count()):
        dev = pa.get_device_info_by_index(i)
        name = dev.get("name", "").lower()
        if "airpods" in name and dev.get("maxInputChannels", 0) > 0:
            airpods_index = i
            print(f"🎧 Using AirPods mic for Porcupine: {name} (index {i})")
            break

    if airpods_index is None:
        airpods_index = pa.get_default_input_device_info().get("index", 0)
        print(f"🎙️ Falling back to system default mic (index {airpods_index})")

    try:
        stream = pa.open(rate=porcupine.sample_rate,
                         channels=1,
                         format=pyaudio.paInt16,
                         input=True,
                         input_device_index=airpods_index,
                         frames_per_buffer=porcupine.frame_length)
    except Exception as e:
        print(f"❌ Failed to open mic stream: {e}")
        return False

    print(f"🎧 Listening for '{keyword}' via Porcupine...")

    try:
        while True:
            data = stream.read(porcupine.frame_length,
                               exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, data)
            if porcupine.process(pcm) >= 0:
                print("✅ Wake word detected (Porcupine)")
                return True
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

# 🔁 Universal interface


def listen_for_wake_word(mode="google", wake_word="jarvis", mic_index=None):
    if mode == "google":
        return wake_with_google(wake_word, mic_index=mic_index)
    elif mode == "porcupine":
        return wake_with_porcupine(wake_word)
    else:
        print("❌ Invalid mode. Use 'google' or 'porcupine'.")
        return False
