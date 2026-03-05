import joblib

# Load the trained model
try:
    model = joblib.load("models/emotion_classifier.joblib")
except FileNotFoundError:
    raise FileNotFoundError("Model file not found. Please run train_emotion_model.py first.")

def predict_emotion(text):
    # Predict emotion and confidence
    emotion = model.predict([text])[0]
    confidence = model.predict_proba([text])[0].max()
    return emotion, confidence