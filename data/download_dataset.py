from datasets import load_dataset
import pandas as pd

# Load go_emotions dataset
dataset = load_dataset("go_emotions", "simplified", split="train")
df = pd.DataFrame({"text": dataset["text"], "emotion": dataset["labels"]})

# Map numeric labels to emotion names
emotion_map = {
    0: "admiration", 1: "amusement", 2: "anger", 3: "annoyance", 4: "approval",
    5: "caring", 6: "confusion", 7: "curiosity", 8: "desire", 9: "disappointment",
    10: "disapproval", 11: "disgust", 12: "embarrassment", 13: "excitement",
    14: "fear", 15: "gratitude", 16: "grief", 17: "joy", 18: "love",
    19: "nervousness", 20: "optimism", 21: "pride", 22: "realization",
    23: "relief", 24: "remorse", 25: "sadness", 26: "surprise", 27: "neutral"
}
df["emotion"] = df["emotion"].apply(lambda x: emotion_map[x[0]] if isinstance(x, list) else emotion_map[x])

# Save to CSV
df[["text", "emotion"]].to_csv("data/emotion_dataset.csv", index=False)
print("Dataset saved to data/emotion_dataset.csv")