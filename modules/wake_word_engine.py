import os
import queue
import sounddevice as sd
import vosk
import json
import threading

# ✅ Function to detect AirPods microphone index


# def get_airpods_input_device():
#     """Find the index of an input device that matches 'AirPods' or fallback."""
#     for idx, dev in enumerate(sd.query_devices()):
#         name = dev['name'].lower()
#         if 'airpods' in name and dev['max_input_channels'] > 0:
#             print(f"🎧 Using AirPods mic: {dev['name']} (index {idx})")
#             return idx
#     print("❌ AirPods mic not found. Using system default microphone.")
#     return None  # fallback to system default


# 🔁 Callback function to trigger when wake word is detected
wake_trigger = None  # will be set from gui.py

# 🧠 Wake-word detection loop


def wake_word_listener(wake_word="hey jarvis", model_path="model"):
    global wake_trigger

    if not os.path.exists(model_path):
        print("❌ Vosk model folder not found.")
        print("Download from: https://alphacephei.com/vosk/models")
        return

    model = vosk.Model(model_path)
    q = queue.Queue()
   # mic_index = get_airpods_input_device()  # 🔍 Find AirPods or fallback

    # 🎙 Microphone callback for Vosk
    def audio_callback(indata, frames, time, status):
        if status:
            print("[WakeWord] Audio error:", status)
        q.put(bytes(indata))

    # 🎧 Start continuous input stream
    with sd.RawInputStream(device=0,
                           samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        print("[WakeWord] Listening for:", wake_word)
        rec = vosk.KaldiRecognizer(model, 16000)

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                print("[WakeWord] Heard:", text)
                if wake_word.lower() in text.lower():
                    print("✅ Wake word detected!")
                    if wake_trigger:
                        wake_trigger()

# 🚀 Start wake-word listener as a background thread


def start_wake_listener(trigger_function, model_path="model"):
    global wake_trigger
    wake_trigger = trigger_function
    threading.Thread(target=wake_word_listener, args=(
        "hey jarvis", model_path), daemon=True).start()
