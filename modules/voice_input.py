import sounddevice as sd
import queue
import vosk
import json
import os

# 📁 Path to your Vosk speech recognition model
MODEL_PATH = "model"

# 🎤 Queue to hold audio data from mic
q = queue.Queue()

# 🎧 Callback to push mic audio into queue


def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

# ✅ Use system mic (fallback) or allow future switch


def get_working_mic_index():
    for idx, dev in enumerate(sd.query_devices()):
        name = dev['name'].lower()
        if 'microphone array' in name and dev['max_input_channels'] > 0:
            print(f"🎧 Using system mic: {dev['name']} (index {idx})")
            return idx
    print("⚠️ Defaulting to device 0")
    return 0

# 🎙️ Main Vosk listener


def listen(live_signal=None):
    if not os.path.exists(MODEL_PATH):
        print("❌ Vosk model not found. Download from https://alphacephei.com/vosk/models")
        return ""

    model = vosk.Model(MODEL_PATH)
    samplerate = 16000
    mic_index = get_working_mic_index()

    try:
        with sd.RawInputStream(device=mic_index,
                               samplerate=samplerate, blocksize=8000,
                               dtype='int16', channels=1,
                               callback=callback):
            print("🎤 Speak now...")

            rec = vosk.KaldiRecognizer(model, samplerate)
            transcript = ""
            silence_counter = 0

            while True:
                data = q.get()

                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    final = result.get("text", "")
                    if live_signal:
                        live_signal.emit("✅ " + final)
                    print(f"🧠 Final: {final}")
                    return final
                else:
                    partial = json.loads(
                        rec.PartialResult()).get("partial", "")
                    if partial:
                        transcript = partial
                        silence_counter = 0
                        if live_signal:
                            live_signal.emit(partial)
                    else:
                        silence_counter += 1

                if silence_counter > 30:
                    if live_signal:
                        live_signal.emit("✅ " + transcript)
                    return transcript
    except Exception as e:
        print(f"❌ Mic error: {e}")
        return ""
