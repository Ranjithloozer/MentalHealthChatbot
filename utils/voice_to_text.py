import whisper

model = whisper.load_model("base")

def whisper_transcribe(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]
