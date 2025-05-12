import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []


def save_to_memory(question, answer):
    memory = load_memory()
    memory.append({"question": question, "answer": answer})
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)


def format_memory(memory):
    return "\n".join(
        [f"Q: {pair['question']}\nA: {pair['answer']}" for pair in memory]
    )
