import streamlit as st
from textblob import TextBlob
import random

# Self-care suggestions
self_care_tips = {
    "anxious": ["Try 4-7-8 breathing 😌", "Take a short mindful walk 🍃", "Write down 3 things you're grateful for 📝"],
    "sad": ["Listen to soothing music 🎧", "Talk to a friend you trust 🤝", "Do a simple creative activity 🎨"],
    "angry": ["Take a 5-minute break 🕒", "Splash cold water on your face 🚿", "Try journaling your thoughts ✍️"],
    "neutral": ["Drink a glass of water 💧", "Do a light stretch 🧘", "Go offline for 10 minutes 🔌"]
}

crisis_keywords = [
    "i want to die", "kill myself", "suicide", "i can't go on", "give up", 
    "end my life", "no reason to live", "i’m done", "i hate living"
]

def analyze_mood(text):
    text = text.lower()

    # Crisis check
    for phrase in crisis_keywords:
        if phrase in text:
            return "crisis"

    # Mood keyword detection
    if any(word in text for word in ["anxious", "nervous", "worried", "panic"]):
        return "anxious"
    if any(word in text for word in ["sad", "lonely", "down", "cry", "hopeless"]):
        return "sad"
    if any(word in text for word in ["angry", "mad", "furious", "frustrated"]):
        return "angry"
    if any(word in text for word in ["happy", "great", "excited", "joy", "grateful"]):
        return "positive"

    # Sentiment fallback
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.3:
        return "positive"
    elif polarity < -0.1:
        return "sad"
    else:
        return "neutral"

def generate_response(text):
    mood = analyze_mood(text)

    if mood == "crisis":
        return (
            "⚠️ I'm really sorry you're feeling this way.\n\n"
            "You are not alone, and help is available. 💙\n\n"
            "**India Helpline:** 9152987821 (iCall) 📞\n"
            "Visit: [https://icallhelpline.org](https://icallhelpline.org)\n\n"
            "_Please reach out. You matter more than you know._"
        )

    if mood == "positive":
        return "That's wonderful to hear! 😊 Keep holding on to the things that bring you joy."

    # Suggest based on mood
    if mood in self_care_tips:
        suggestion = random.choice(self_care_tips[mood])
    else:
        suggestion = random.choice(self_care_tips["neutral"])

    if mood == "sad":
        return (
            "I'm sorry you're feeling low. 💙 I'm here with you.\n\n"
            f"Here’s something you can try right now: {suggestion}"
        )
    elif mood == "anxious":
        return (
            "It’s okay to feel anxious sometimes. 🌊 Let’s slow down together.\n\n"
            f"Try this to feel a bit better: {suggestion}"
        )
    elif mood == "angry":
        return (
            "That sounds really frustrating. 😠 It's healthy to express emotions.\n\n"
            f"Maybe this can help: {suggestion}"
        )
    elif mood == "neutral":
        return (
            "Thanks for sharing how you're feeling. 🌱 Small steps matter.\n\n"
            f"Here’s a calming tip for today: {suggestion}"
        )
    else:
        return (
            "Thank you for opening up. If you're unsure how you feel, that’s okay too. 🌼\n\n"
            f"Here’s something that might help: {suggestion}"
        )

# Streamlit UI
st.set_page_config(page_title="MindMate – Mental Wellness Chatbot", page_icon="🧠")
st.title("🧠 MindMate – AI Mental Wellness Chatbot")
st.write("Hi there! I'm here to listen. How are you feeling today?")

user_input = st.text_area("Your thoughts:", "")

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter your thoughts so I can respond.")
    else:
        response = generate_response(user_input)
        st.success("MindMate says:")
        st.info(response)
