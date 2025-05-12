# import sys
# import threading
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLabel,
#     QTextEdit, QPushButton, QHBoxLayout
# )
# from PyQt5.QtCore import Qt, QTimer, pyqtSignal
# from PyQt5.QtGui import QFont

# # 🧠 Your modules
# from modules.voice_input import listen
# from modules.voice_engine import speak_summary
# from modules.llm_engine import get_summary, stream_full_reply
# from modules.memory_engine import load_memory, save_to_memory, format_memory
# from vision import emotion_state, start_observer
# from modules.wake_word_engine import start_wake_listener


# class JarvisGUI(QWidget):
#     # ✅ Signals to safely update GUI from threads
#     update_summary_signal = pyqtSignal(str)
#     append_full_signal = pyqtSignal(str)
#     clear_full_signal = pyqtSignal()

#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("JARVIS - Iron Mode")
#         self.setGeometry(300, 100, 700, 600)
#         self.init_ui()
#         self.memory = load_memory()
#         start_observer()  # Start emotion observer
#         start_wake_listener(self.ask_jarvis)

#         # 🔁 Connect signals
#         self.update_summary_signal.connect(self.summary_text.setText)
#         self.clear_full_signal.connect(self.clear_full_reply)
#         self.append_full_signal.connect(self.append_full_reply)

#         # Start emotion label updater
#         self.update_emotion()

#     def init_ui(self):
#         self.setStyleSheet("background-color: #0A0F1C; color: #00F0FF;")
#         font = QFont("Consolas", 11)

#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         # 😐 Emotion label
#         self.emotion_label = QLabel("Emotion: Loading...")
#         self.emotion_label.setFont(QFont("Consolas", 12, QFont.Bold))
#         layout.addWidget(self.emotion_label)

#         # 🔊 Summary
#         self.summary_box = QLabel("Summary:")
#         self.summary_box.setFont(font)
#         self.summary_text = QLabel("")
#         self.summary_text.setWordWrap(True)
#         self.summary_text.setFont(font)
#         layout.addWidget(self.summary_box)
#         layout.addWidget(self.summary_text)

#         # 📜 Full Reply
#         self.full_label = QLabel("Full Reply:")
#         self.full_label.setFont(font)
#         self.full_text = QTextEdit()
#         self.full_text.setReadOnly(True)
#         self.full_text.setFont(font)
#         layout.addWidget(self.full_label)
#         layout.addWidget(self.full_text)

#         # 🎤 Buttons
#         button_row = QHBoxLayout()
#         self.ask_button = QPushButton("🎤 Ask Jarvis")
#         self.ask_button.clicked.connect(self.ask_jarvis)
#         button_row.addWidget(self.ask_button)

#         self.exit_button = QPushButton("🛑 Exit")
#         self.exit_button.clicked.connect(self.close)
#         button_row.addWidget(self.exit_button)

#         layout.addLayout(button_row)

#         # 🔁 Timer to update emotion label
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_emotion)
#         self.timer.start(8000)

#     def update_emotion(self):
#         # Get emotion from vision thread
#         mood = emotion_state.get("current", "neutral")
#         self.emotion_label.setText(f"Emotion: {mood.capitalize()}")

#     def ask_jarvis(self):
#         # Start background thread for LLM + voice
#         threading.Thread(target=self.process_question, daemon=True).start()

#     def process_question(self):
#         # 🎤 Listen to user
#         question = listen()
#         self.update_summary_signal.emit("You said: " + question)

#         # 🧠 Add memory context
#         chat_history = format_memory(self.memory)
#         context = f"{chat_history}\n\nNew Question: {question}" if chat_history else question

#         # 🧠 Get summary & speak it
#         summary = get_summary(context)
#         self.update_summary_signal.emit(summary)
#         threading.Thread(target=speak_summary, args=(
#             summary,), daemon=True).start()

#         # 🧠 Clear previous full reply
#         self.clear_full_signal.emit()

#         # 📜 Stream and update chunk by chunk
#         buffer = ""
#         for chunk in stream_full_reply(context):
#             text = chunk.content if hasattr(chunk, "content") else str(chunk)
#             buffer += text
#             # 💥 GUI updates with every chunk
#             self.append_full_signal.emit(buffer)

#         # 💾 Save to memory
#         save_to_memory(question, buffer)
#         self.memory.append({"question": question, "answer": buffer})

#     # 🧼 Clears the full_text box
#     def clear_full_reply(self):
#         self.full_text.clear()

#     # 🧩 Appends latest chunk to full_text box
#     def append_full_reply(self, full_text):
#         self.full_text.setPlainText(full_text)


# # 🚀 Run GUI
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = JarvisGUI()
#     window.show()
#     sys.exit(app.exec_())

import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QTextEdit, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont

# 🧠 Import necessary internal modules
from modules.voice_input import listen
from modules.voice_engine import speak_summary
from modules.llm_engine import get_summary, stream_full_reply
from modules.memory_engine import load_memory, save_to_memory, format_memory
from vision import emotion_state, start_observer
from modules.wake_word_engine import start_wake_listener


class JarvisGUI(QWidget):
    # ✅ Qt signals to update GUI safely from other threads
    update_summary_signal = pyqtSignal(str)
    append_full_signal = pyqtSignal(str)
    clear_full_signal = pyqtSignal()
    transcript_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS - Iron Mode")
        self.setGeometry(300, 100, 700, 600)
        self.init_ui()

        # 📦 Load previous session memory
        self.memory = load_memory()

        # 🧠 Start background vision/emotion observer
        start_observer()

        # 🎤 Start listening for wake word "Hey Jarvis"
        start_wake_listener(self.ask_jarvis)

        # 🔗 Connect update signals to their respective methods
        self.update_summary_signal.connect(self.summary_text.setText)
        self.clear_full_signal.connect(self.clear_full_reply)
        self.append_full_signal.connect(self.append_full_reply)
        self.transcript_signal.connect(self.update_transcript)

        # ⏱ Start emotion polling
        self.update_emotion()

    def init_ui(self):
        self.setStyleSheet("background-color: #0A0F1C; color: #00F0FF;")
        font = QFont("Consolas", 11)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # 😐 Display detected emotion
        self.emotion_label = QLabel("Emotion: Loading...")
        self.emotion_label.setFont(QFont("Consolas", 12, QFont.Bold))
        layout.addWidget(self.emotion_label)

        # 🗣️ Live transcript label for voice input
        self.transcript_label = QLabel("🗣 Awaiting voice...")
        self.transcript_label.setFont(QFont("Consolas", 10))
        layout.addWidget(self.transcript_label)

        # 🧠 Summary section (short reply)
        self.summary_box = QLabel("Summary:")
        self.summary_box.setFont(font)
        self.summary_text = QLabel("")
        self.summary_text.setWordWrap(True)
        self.summary_text.setFont(font)
        layout.addWidget(self.summary_box)
        layout.addWidget(self.summary_text)

        # 📜 Full detailed reply from LLM
        self.full_label = QLabel("Full Reply:")
        self.full_label.setFont(font)
        self.full_text = QTextEdit()
        self.full_text.setReadOnly(True)
        self.full_text.setFont(font)
        layout.addWidget(self.full_label)
        layout.addWidget(self.full_text)

        # 🎛 Buttons to trigger assistant or exit
        button_row = QHBoxLayout()
        self.ask_button = QPushButton("🎤 Ask Jarvis")
        self.ask_button.clicked.connect(self.ask_jarvis)
        button_row.addWidget(self.ask_button)

        self.exit_button = QPushButton("🛑 Exit")
        self.exit_button.clicked.connect(self.close)
        button_row.addWidget(self.exit_button)

        layout.addLayout(button_row)

        # ⏱ Refresh emotion label every 8 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_emotion)
        self.timer.start(8000)

    def update_emotion(self):
        # ⏳ Get emotion from vision observer
        mood = emotion_state.get("current", "neutral")
        self.emotion_label.setText(f"Emotion: {mood.capitalize()}")

    def ask_jarvis(self):
        # 🧵 Run LLM + voice in background
        threading.Thread(target=self.process_question, daemon=True).start()

    def process_question(self):
        # 🎤 Start listening and show transcript live
        question = listen(live_signal=self.transcript_signal)
        self.update_summary_signal.emit("You said: " + question)

        # 🧠 Combine memory + question into full prompt
        chat_history = format_memory(self.memory)
        context = f"{chat_history}\n\nNew Question: {question}" if chat_history else question

        # ✨ Get summary (short reply) and speak it
        summary = get_summary(context)
        self.update_summary_signal.emit(summary)
        threading.Thread(target=speak_summary, args=(
            summary,), daemon=True).start()

        # 🧽 Clear old full reply box
        self.clear_full_signal.emit()

        # 📜 Stream full answer and show progressively
        buffer = ""
        for chunk in stream_full_reply(context):
            text = chunk.content if hasattr(chunk, "content") else str(chunk)
            buffer += text
            self.append_full_signal.emit(buffer)

        # 💾 Save to memory for future follow-ups
        save_to_memory(question, buffer)
        self.memory.append({"question": question, "answer": buffer})

    def clear_full_reply(self):
        self.full_text.clear()

    def append_full_reply(self, full_text):
        self.full_text.setPlainText(full_text)

    def update_transcript(self, text):
        # 🖥 Show partial speech-to-text
        self.transcript_label.setText(f"🗣 {text}")


# 🚀 Main runner
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisGUI()
    window.show()
    sys.exit(app.exec_())
