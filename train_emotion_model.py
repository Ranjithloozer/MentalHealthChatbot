import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# Load dataset
df = pd.read_csv("data/emotion_dataset.csv")

# Create pipelin
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000)),
    ("clf", LogisticRegression(max_iter=1000, multi_class="multinomial"))
])

# Train model
pipeline.fit(df["text"], df["emotion"])

# Save model
joblib.dump(pipeline, "models/emotion_classifier.joblib")
print("Emotion model trained and saved to models/emotion_classifier.joblib")