import tkinter as tk
from tkinter import scrolledtext
import nltk
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Define chatbot concepts, tasks, and responses with answers and explanations
concepts = {
    "NLP_BASICS": {
        "name": "NLP Basics",
        "explanation": "NLP basics involve transforming human language into data that computers can understand and process. This includes tokenization, stemming, and lemmatization.",
        "task": "Explain how NLP helps computers understand text and speech.",
        "answer": "NLP techniques like tokenization and lemmatization help break down and understand text structure and meaning.",
        "explanation_answer": "NLP enables computers to process text by breaking it down into manageable parts (like tokens) and finding the base meaning (like with lemmatization)."
    },
    "TOKENIZATION": {
        "name": "Tokenization",
        "explanation": "Tokenization splits text into individual words or phrases, allowing for better analysis and manipulation of text.",
        "task": "Please tokenize this sentence: 'Text analysis splits text into manageable parts.'",
        "answer": ["Text", "analysis", "splits", "text", "into", "manageable", "parts"],
        "explanation_answer": "Tokenization splits the sentence into individual words or tokens, helping us analyze each component."
    },
    "STEMMING": {
        "name": "Stemming",
        "explanation": "Stemming reduces words to their root form. For example, 'running' becomes 'run'. This helps with matching words to their base meaning.",
        "task": "What is the stem of 'running' and 'happily'?",
        "answer": ["run", "happili"],
        "explanation_answer": "Stemming reduces words to their base form by removing suffixes. 'Running' becomes 'run', and 'happily' becomes 'happili'."
    },
    "LEMMATIZATION": {
        "name": "Lemmatization",
        "explanation": "Lemmatization reduces words to their dictionary form. Unlike stemming, it returns valid words (e.g., 'better' -> 'good').",
        "task": "What is the lemmatized form of 'better' and 'children'?",
        "answer": ["good", "child"],
        "explanation_answer": "Lemmatization finds the dictionary form of words: 'better' becomes 'good' and 'children' becomes 'child'."
    },
    "SENTIMENT_ANALYSIS": {
        "name": "Sentiment Analysis",
        "explanation": "Sentiment Analysis determines the sentiment behind text, such as positive, negative, or neutral tones, often used in customer feedback and reviews.",
        "task": "Analyze the sentiment of: 'This product is amazing!'",
        "answer": "Positive",
        "explanation_answer": "The phrase contains positive words ('amazing') indicating a positive sentiment."
    },
    "SPEECH_RECOGNITION": {
        "name": "Speech Recognition",
        "explanation": "Speech Recognition converts spoken language into text, enabling voice-activated applications.",
        "task": "Describe an example of where speech recognition is used in daily life.",
        "answer": "Virtual assistants like Siri or Alexa",
        "explanation_answer": "Speech recognition powers virtual assistants like Siri, which convert spoken commands into text to execute actions."
    }
}

emotional_responses = {
    "STRESS": [
        "I understand that learning new concepts can be overwhelming. Take it one step at a time; you're doing great!",
        "Feeling stressed is normal. Break things down and focus on one small task at a time.",
        "Remember to take deep breaths. It's okay to take breaks and come back when you're ready."
    ],
    "FRUSTRATION": [
        "Frustration is part of the learning process. Let's review the basics if it feels too hard.",
        "Don't worry about mistakes; they’re part of learning. What specific part is confusing you?",
        "Feeling stuck? Try breaking the problem into smaller steps. You've got this!"
    ],
    "MOTIVATION": [
        "Keep going! You're making progress with each attempt.",
        "It's okay if it feels challenging. Small, consistent efforts lead to mastery.",
        "Remember why you started. You're closer to your goal with each step."
    ],
    "CONFIDENCE": [
        "Believe in your abilities! Each step forward is a win.",
        "You're capable of amazing things! Learning takes time, and you're on the right path.",
        "Remember, even experts started as beginners. Keep going, and you'll see improvement!"
    ]
}

# Chatbot processing logic
lemmatizer = WordNetLemmatizer()
current_concept = None

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return tokens

def get_response(user_message):
    global current_concept

    user_message = user_message.lower()

    if "teach me the basics" in user_message:
        concepts_list = "\n- ".join([concept["name"] for concept in concepts.values()])
        return f"These are the basic concepts in Text and Speech Analysis:\n- {concepts_list}\nWhich concept would you like to learn about?"
    
    elif user_message in [concept["name"].lower() for concept in concepts.values()]:
        for concept_name, details in concepts.items():
            if user_message == details["name"].lower():
                current_concept = concept_name
                return f"{details['explanation']}\nTask: {details['task']}"
    
    elif user_message == "hint" and current_concept:
        return f"Hint: {concepts[current_concept]['explanation']}"

    elif user_message == "answer" and current_concept:
        answer = concepts[current_concept]["answer"]
        explanation = concepts[current_concept]["explanation_answer"]
        current_concept = None
        return f"The answer is: {answer}\nExplanation: {explanation}"

    elif current_concept:
        # Check if the user's answer matches the concept's expected answer
        if str(concepts[current_concept]["answer"]).lower() == user_message:
            response = f"Correct! {concepts[current_concept]['explanation_answer']}"
            current_concept = None
            return response
        else:
            return "That's not quite right. Try again or type 'hint' for help, or 'answer' for the solution and explanation."
    
    # Emotional support check
    for emotion, responses in emotional_responses.items():
        if any(word in user_message for word in ["stressed", "frustrated", "motivation", "confidence"]):
            return random.choice(responses)

    return "I'm here to help! Type 'teach me the basics' to start learning or ask for 'hint' if you need help."

# GUI setup
def send_message():
    user_message = user_input.get()
    chat_display.insert(tk.END, f"You: {user_message}\n")
    user_input.delete(0, tk.END)

    response = get_response(user_message)
    chat_display.insert(tk.END, f"Chatbot: {response}\n\n")
    chat_display.yview(tk.END)

# Initialize the GUI
root = tk.Tk()
root.title("Text and Speech Analysis Chatbot")

chat_display = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD, state="normal")
chat_display.pack(pady=10)

user_input = tk.Entry(root, width=55)
user_input.pack(side=tk.LEFT, padx=10, pady=10)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=10, pady=10)

# Run the chatbot GUI
root.mainloop()
