import streamlit as st
from textblob import TextBlob
import random

# Self-care suggestions
self_care_tips = [
    "Take a 10-minute walk in nature 🍃",
    "Try 4-7-8 breathing to relax 😌",
    "Write down 3 things you're grateful for 📝",
    "Listen to your favorite music 🎵",
    "Try a short guided meditation 🧘",
    "Drink a glass of water and stretch 💧"
]

# Sentiment analysis function
def analyze_mood(text):
    text = text.lower()
    if any(word in text for word in ["sad", "depressed", "not good", "anxious", "tired", "hopeless", "stressed", "alone", "down", "angry"]):
        return "negative"
    
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.3:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"


# Chatbot response logic
def generate_response(user_input):
    text = user_input.lower()

    # 🔴 Crisis detection
    crisis_keywords = [
        "i want to die", "i just want to die", "suicide", "kill myself",
        "ending it all", "can't go on", "give up", "end my life", "i'm done"
    ]
    for phrase in crisis_keywords:
        if phrase in text:
            return (
                "⚠️ I'm really sorry you're feeling this way.\n\n"
                "You are not alone, and help is available. 💙\n"
                "Please consider reaching out to a mental health professional or a helpline immediately.\n\n"
                "**India Helpline:** 9152987821 (iCall) 📞\n"
                "Or visit [https://icallhelpline.org](https://icallhelpline.org)\n\n"
                "_You matter, and your life is important._"
            )

    # ✅ Proceed with normal analysis
    mood = analyze_mood(text)

    if mood == "positive":
        return "That's great to hear! 😊 Keep doing what makes you happy!"
    elif mood == "negative":
        return (
            "I'm really sorry you're feeling this way. 💙 "
            f"Here’s something you can try: {random.choice(self_care_tips)}"
        )
    else:
        return (
            "Thanks for sharing. If you're unsure how you feel, take a moment to breathe. 🌱 "
            f"Here’s a tip for today: {random.choice(self_care_tips)}"
        )


# Streamlit UI
st.set_page_config(page_title="MindMate – Mental Wellness Chatbot", page_icon="🧠")

st.title("🧠 MindMate – AI Mental Wellness Chatbot")
st.write("Hi there! I'm here to listen. Tell me how you're feeling today:")

user_input = st.text_area("Your thoughts:", "")

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter something so I can help you.")
    else:
        response = generate_response(user_input)
        st.success("MindMate says:")
        st.info(response)
