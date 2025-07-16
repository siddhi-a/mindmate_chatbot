import streamlit as st
import random
from textblob import TextBlob
from datetime import datetime
import csv

# Optional GPT support
import openai
import streamlit as st

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]



# Try loading from secrets, else fallback to manual input
api_key = st.secrets.get("openai", {}).get("openai_key", "")
if not api_key:
    api_key = st.text_input("🔐 Enter your OpenAI API key (optional)", type="password")

if api_key:
    openai.api_key = api_key

# Mood & emoji mapping
mood_emojis = {
    "positive": "😊",
    "sad": "😔",
    "anxious": "😰",
    "angry": "😡",
    "neutral": "😐",
    "crisis": "🚨"
}

self_care_tips = {
    "anxious": ["Try 4-7-8 breathing 🌬️", "Take a mindful walk 🚶‍♀️", "Write down 3 things you're grateful for 📝"],
    "sad": ["Listen to soothing music 🎶", "Talk to someone you trust 🧑‍🤝‍🧑", "Try journaling your emotions 📓"],
    "angry": ["Take a short break 🛑", "Splash cold water 💦", "Write your feelings out ✍️"],
    "neutral": ["Drink water 🥤", "Stretch for 5 mins 🧘", "Step away from your screen 📴"],
    "positive": ["Keep smiling 😄", "Share your joy 💬", "Celebrate small wins 🎉"]
}

crisis_keywords = [
    "i want to die", "kill myself", "suicide", "i can't go on", "give up",
    "end my life", "no reason to live", "i’m done", "i hate living"
]

def analyze_mood(text):
    text = text.lower()
    for phrase in crisis_keywords:
        if phrase in text:
            return "crisis"
    if any(word in text for word in ["anxious", "nervous", "worried", "panic"]):
        return "anxious"
    if any(word in text for word in ["sad", "lonely", "down", "cry", "hopeless"]):
        return "sad"
    if any(word in text for word in ["angry", "mad", "furious", "frustrated"]):
        return "angry"
    if any(word in text for word in ["happy", "great", "excited", "joy", "grateful"]):
        return "positive"
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.3:
        return "positive"
    elif polarity < -0.1:
        return "sad"
    else:
        return "neutral"

def generate_response(text, use_gpt=False):
    mood = analyze_mood(text)
    emoji = mood_emojis.get(mood, "🙂")

    if mood == "crisis":
        return emoji, (
            "**🚨 Crisis Alert**\n\n"
            "I'm really sorry you're feeling this way. You're not alone.\n\n"
            "**India Helpline:** 9152987821 (iCall)\n"
            "**Visit:** [https://icallhelpline.org](https://icallhelpline.org)\n\n"
            "_Please speak to someone — you matter deeply._"
        )

    if use_gpt and api_key:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a compassionate mental wellness assistant."},
                    {"role": "user", "content": text}
                ]
            )
            return emoji, response['choices'][0]['message']['content']
        except Exception:
            return emoji, "Oops! GPT failed. Reverting to basic response."

    # Fallback response
    suggestion = random.choice(self_care_tips.get(mood, self_care_tips["neutral"]))
    templates = {
        "positive": f"That's wonderful to hear! {emoji} Keep holding on to the joy you feel.",
        "sad": f"I'm sorry you're feeling down. {emoji} Maybe try this: {suggestion}",
        "anxious": f"It's okay to feel anxious. {emoji} Try this to feel grounded: {suggestion}",
        "angry": f"That sounds tough. {emoji} Consider doing this: {suggestion}",
        "neutral": f"Thanks for sharing. {emoji} Here's something for today: {suggestion}"
    }
    return emoji, templates.get(mood, "I'm here for you.")

def log_interaction(user_input, mood):
    with open("chat_log.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), user_input, mood])

# Streamlit App UI
st.set_page_config(page_title="MindMate – AI Mental Wellness Chatbot", page_icon="🧠")
st.title("🧠 MindMate – AI Mental Wellness Chatbot")
st.write("Hi! I'm MindMate. Share how you're feeling today.")

# Initialize session history
if "messages" not in st.session_state:
    st.session_state.messages = []

use_gpt = st.toggle("Use GPT for replies (optional, needs API key)", value=False)
user_input = st.text_input("Your thoughts", "", key="user_input")

if st.button("Send") and user_input.strip():
    mood = analyze_mood(user_input)
    emoji, response = generate_response(user_input, use_gpt)
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append((f"MindMate {emoji}", response))
    log_interaction(user_input, mood)

# Display full conversation history
for sender, message in st.session_state.messages:
    if "MindMate" in sender:
        st.chat_message("assistant").markdown(message)
    else:
        st.chat_message("user").markdown(message)
