from langchain.prompts import PromptTemplate
# ✅ Requires: pip install langchain-deepseek
from langchain_deepseek import ChatDeepSeek

# 🔑 Insert your DeepSeek API key
llm = ChatDeepSeek(
    model="deepseek-chat",  # or "deepseek-coder" for coding tasks
    # ✅ Replace with your own key securely
    api_key="sk-0928fe9ce7114f1eb49fbb0edbf0f5f7",
    streaming=True
)

# ✅ Friendly summary prompt
summary_prompt = PromptTemplate(
    input_variables=["context"],
    template="Reply in exactly one sentence only like Jarvis from Iron Man would speak. Do not use markdown, bullet points, emojis, or styling. Keep it witty, spoken, and clean: {context}"
)

# ✅ Detailed full reply prompt
full_prompt = PromptTemplate(
    input_variables=["context"],
    template="Answer clearly and helpfully in a friendly tone, based on: {context}"
)

# ✅ Use in main.py → returns plain string (not dict)


def get_summary(context):
    result = (summary_prompt | llm).invoke({"context": context})

    # ✅ This works regardless of format
    try:
        return result.content  # If result is an AIMessage
    except:
        return str(result)

# ✅ Stream full reply as chunks (already works fine with print + save)


def stream_full_reply(context):
    return (full_prompt | llm).stream({"context": context})
