from modules.llm_engine import get_summary, stream_full_reply
# Import LLM functions

from modules.voice_engine import speak_summary
# Import TTS (Text-to-Speech) function

from modules.memory_engine import load_memory, save_to_memory, format_memory
# Import memory functions

import threading
from modules.voice_input import listen
# 🟢 STEP 0: Load previous memory (this stays in memory throughout the loop)
memory = load_memory()

# 🟢 START MAIN LOOP
while True:

    # 🟢 STEP 1: Get user's question
    question = input("\nAsk your question (or type 'exit' to quit): ")
    # question = listen()

    print(f"You said: {question}")
    if question.lower() == "exit":
        print("Goodbye!")
        break

    # 🟢 STEP 2: Prepare context using past memory + new question
    chat_history = format_memory(memory)
    if chat_history:
        context = f"{chat_history}\n\nNew Question: {question}"
    else:
        context = question

    # 🟢 STEP 3: Get summary from LLM
    summary = get_summary(context)

    summary_text = summary["content"] if isinstance(
        summary, dict) and "content" in summary else str(summary)
    print("\nSummary:", summary_text)

    # 🟢 STEP 4: Speak summary without blocking
    # threading.Thread(target=speak_summary, args=(summary,)).start()

    threading.Thread(target=speak_summary, args=(summary_text,)).start()

    # 🟢 STEP 5: Stream full reply and save it live
    buffer = ""  # Will hold the full reply

    with open("full_reply.txt", "w", encoding="utf-8") as f:
        print("\nFull reply:\n")

        for chunk in stream_full_reply(context):
            text = chunk.content
            print(text, end="", flush=True)  # Print as it streams
            buffer += text  # Add to buffer
            f.write(text)  # Save to file
            f.flush()

    print("\n\nFull reply complete.")

    # 🟢 STEP 6: Save the new Q&A to memory
    save_to_memory(question, buffer)

    # Also update in-memory memory so next question uses the latest history
    memory.append({"question": question, "answer": buffer})
