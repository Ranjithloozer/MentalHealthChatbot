# MindMate Chatbot Project

## Overview
MindMate is an AI-powered mental health companion that detects emotions, provides CBT-based responses, and offers mood analytics. This README provides complete instructions to run the project on any system, including fetching and downloading a dataset for training or testing the emotion model.

## Requirements
- Python 3.8 or higher
- Internet connection (for API calls, translations, and dataset download)
- Approximately 200MB free RAM and 500MB free disk space (including dataset)
- Terminal (Linux) or Command Prompt/PowerShell (Windows)

## Dataset Information
- **Source**: A sample emotion dataset (e.g., [Emotion Dataset for NLP](https://www.kaggle.com/datasets/praveengovi/emotions-dataset-for-nlp)) is used for training or testing the emotion detection model.
- **Purpose**: Contains text labeled with emotions (e.g., joy, sadness, fear) to improve or validate the `predict_emotion` model in `models/emotion_model.py`.
- **Size**: ~50MB (varies by dataset version).

## Fetching and Downloading Dataset

### For Linux
1. **Install Kaggle CLI (if not installed)**:
   Open a terminal and run:
   ```bash
   pip3 install kaggle
   ```
   - If `pip3` fails, use `python3 -m ensurepip --upgrade` and retry.

2. **Configure Kaggle API**:
   - Sign up or log in to [Kaggle](https://www.kaggle.com).
   - Go to your account > "Create New API Token" to download `kaggle.json`.
   - Move `kaggle.json` to `~/.kaggle/`:
     ```bash
     mkdir -p ~/.kaggle
     mv ~/Downloads/kaggle.json ~/.kaggle/
     chmod 600 ~/.kaggle/kaggle.json
     ```

3. **Download Dataset**:
   Navigate to the project folder and download the dataset:
   ```bash
   cd /path/to/mindmate-chatbot
   kaggle datasets download -d praveengovi/emotions-dataset-for-nlp
   ```
   - This downloads a `.zip` file (e.g., `emotions-dataset-for-nlp.zip`).

4. **Extract Dataset**:
   Unzip the file:
   ```bash
   unzip emotions-dataset-for-nlp.zip -d dataset
   ```
   - This creates a `dataset/` folder with the dataset files.

5. **Verify Dataset**:
   Check the contents:
   ```bash
   ls dataset/
   ```
   - Use the data in `models/emotion_model.py` for retraining if needed.

### For Windows
1. **Install Kaggle CLI (if not installed)**:
   Open Command Prompt or PowerShell and run:
   ```cmd
   pip install kaggle
   ```
   - If `pip` fails, use `py -m pip install kaggle` or ensure Python PATH is set.

2. **Configure Kaggle API**:
   - Sign up or log in to [Kaggle](https://www.kaggle.com).
   - Go to your account > "Create New API Token" to download `kaggle.json`.
   - Move `kaggle.json` to `%USERPROFILE%\.kaggle\`:
     ```cmd
     mkdir %USERPROFILE%\.kaggle
     move C:\Downloads\kaggle.json %USERPROFILE%\.kaggle\
     ```

3. **Download Dataset**:
   Navigate to the project folder and download the dataset:
   ```cmd
   cd C:\path\to\mindmate-chatbot
   kaggle datasets download -d praveengovi/emotions-dataset-for-nlp
   ```
   - This downloads a `.zip` file (e.g., `emotions-dataset-for-nlp.zip`).

4. **Extract Dataset**:
   Unzip the file:
   ```cmd
   tar -xf emotions-dataset-for-nlp.zip -C dataset
   ```
   - If `tar` isn’t available, use a tool like 7-Zip or WinRAR to extract to a `dataset` folder.

5. **Verify Dataset**:
   Check the contents:
   ```cmd
   dir dataset
   ```
   - Use the data in `models/emotion_model.py` for retraining if needed.

## Installation and Running Instructions

### For Linux
1. **Install Python (if not installed)**:
   Open a terminal and run:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
   - Verify with `python3 --version`.

2. **Install Dependencies**:
   Navigate to the project folder and install required libraries:
   ```bash
   cd /path/to/mindmate-chatbot
   pip3 install flask flask-sqlalchemy deep-translator gtts speechrecognition numpy requests langdetect
   ```
   - Ensure `pip3` works. If not, use `python3 -m ensurepip --upgrade` and retry.

3. **Run the Project**:
   Start the Flask server:
   ```bash
   python3 app.py
   ```
   - Open a browser and go to `http://127.0.0.1:5000`.
   - Log in with "testuser"/"password" and test the chat or voice features.

### For Windows
1. **Install Python (if not installed)**:
   Open Command Prompt or PowerShell and download from [python.org](https://www.python.org/downloads/).
   - Check "Add Python to PATH" during installation.
   - Verify with `python --version`.

2. **Install Dependencies**:
   Navigate to the project folder and install required libraries:
   ```cmd
   cd C:\path\to\mindmate-chatbot
   pip install flask flask-sqlalchemy deep-translator gtts speechrecognition numpy requests langdetect
   ```
   - If `pip` fails, use `py -m pip install` or ensure PATH is set.

3. **Run the Project**:
   Start the Flask server:
   ```cmd
   python app.py
   ```
   - Open a browser and go to `http://127.0.0.1:5000`.
   - Log in with "testuser"/"password" and test the chat or voice features.

## Project Structure
- `app.py`: Main Flask application.
- `templates/index.html`: Frontend HTML file.
- `dataset/`: Folder for the downloaded dataset (created after download).
- (Optional) `static/`: Folder for audio files (created during runtime).
- `models/`, `utils/`, `cbt/`: Supporting Python modules (included in the folder).

## Usage
- **Chat**: Type a message (e.g., "I feel anxious") and click Send.
- **Voice**: Click 🎙️, record a message, and stop with ⏹️.
- **Analytics**: Click ☰ > "Analyze Mood" after chatting.
- **Dataset**: Use `dataset/` files to retrain `predict_emotion` if needed (modify `models/emotion_model.py`).
- Default credentials: "testuser"/"password".

## Troubleshooting
- **Linux**: If "ModuleNotFoundError" occurs, re-run `pip3 install` with missing library names.
- **Windows**: If `python` fails, try `py app.py` or reinstall Python with PATH enabled.
- **Port Conflict**: If `5000` is busy, check with `lsof -i :5000` (Linux) or `netstat -aon | findstr :5000` (Windows), then kill the process (e.g., `kill -9 <PID>` or `taskkill /PID <PID> /F`).
- **Microphone**: Allow browser microphone access; test with `python3 -c "import speech_recognition as sr; r = sr.Recognizer(); with sr.Microphone() as source: print(r.record(source))"` (Linux) or similar.
- **Dataset Download**: If `kaggle` fails, ensure `kaggle.json` is correctly placed and permissions are set.
- Check terminal/console for errors and logs.

## Notes
- Move the entire `mindmate-chatbot` folder (including `dataset/` after download) to the new system.
- No additional setup is needed beyond the steps above.
- For production, disable debug mode in `app.py` (`app.run(debug=False)`) and install Tailwind CSS locally (see `index.html` comments).
- To retrain the model, update `models/emotion_model.py` with the dataset and re-run `app.py`.

## Contributing
Suggest improvements, report issues, or share better datasets!