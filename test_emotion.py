from models.emotion_model import predict_emotion
from utils.nlp_utils import preprocess

# Test cases covering your inputs and new emotions
test_texts = [
    "I feel really sad today",
    "i dont live in this world",
    "i need to became a developer",
    "whats ur name",
    "can i give u the name",
    "whats the time now",
    "iam getting boring",
    "whats my status",
    "I’m so anxious about my exams.",
    "I’m so grateful for your help!",
    "I don’t understand what’s happening."
]

for text in test_texts:
    clean_text = preprocess(text)
    emotion, confidence = predict_emotion(clean_text)
    print(f"Text: {text}\nEmotion: {emotion}, Confidence: {confidence:.2f}\n")