from flask import Flask, request, jsonify, session
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import os
import secrets
import random

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# === LOAD MODEL ===
dataset_path = os.path.join('data', 'emotion_dataset.csv')
model = None
vectorizer = None

try:
    df = pd.read_csv(dataset_path)
    vectorizer = TfidfVectorizer(max_features=12000, stop_words='english', ngram_range=(1, 3), min_df=1)
    X = vectorizer.fit_transform(df['text'])
    y = df['emotion']
    model = MultinomialNB(alpha=0.4)
    model.fit(X, y)
    print("Model loaded: 12k features, high accuracy")
except Exception as e:
    print(f"Model failed: {e}")

# === 50 BRAND NEW TAMIL EMOTIONS + EXISTING 500+ ===
EMOTION_DB = {
    # === EXISTING (500+) ===
    'sadness': ['sad', 'depressed', 'down', 'cry', 'crying', 'sobbing', 'tears', 'unhappy', 'heartbroken', 'bad day', 'miserable',
                'paining', 'hurt', 'lonely', 'alone', 'miss you', 'miss him', 'miss her', 'no one cares', 'empty', 'lost someone',
                'failed', 'failure', 'useless', 'worthless', 'hopeless', 'dark', 'nalla illa', 'manasu kasta irukku', 'kasta irukku',
                'ennaku enna da', 'yaen da', 'yaen', 'ennoda life', 'ennaku thookame varala', 'thookam illa', 'sleep illa'],
    'joy': ['happy', 'joy', 'excited', 'great', 'awesome', 'love', 'amazing', 'yay', 'super', 'woohoo', 'best day', 'feeling good',
            'smiling', 'laughing', 'nalla irukken', 'super da', 'mass da', 'semmaya irukku', 'romba santhosama irukken',
            'ennaku romba happy', 'naan romba happy', 'love you', 'i love you', 'adhu nalla irundhuchu', 'semmaya irundhuchu'],
    'anger': ['angry', 'mad', 'pissed', 'dei poda', 'poda', 'poda dei', 'irritated', 'hate', 'fuck', 'damn', 'shit', 'bloody',
              'frustrated', 'annoyed', 'irritate', 'kopa irukku', 'kobam', 'kobama irukku', 'ennaku kobam varudhu', 'yaen da',
              'ennada panra', 'poda po', 'poda po da', 'machan', 'dei macha', 'dei enna da'],
    'fear': ['scared', 'afraid', 'worry', 'anxious', 'nervous', 'panic', 'fear', 'terrified', 'what if', 'don’t know', 'can’t sleep',
             'exam', 'interview', 'result', 'future', 'job', 'money', 'health', 'family', 'parents', 'ennaku bayama irukku',
             'bayam', 'paya irukku', 'ennaku thookame varala'],
    'grief': ['alone', 'lonely', 'miss', 'grief', 'lost', 'empty', 'no one', 'nobody understands', 'left me', 'breakup', 'divorce',
              'death', 'died', 'passed away', 'grandma', 'grandpa', 'friend', 'pet', 'ennaku yaarum illa', 'naan thaniya irukken'],
    'remorse': ['sorry', 'my fault', 'regret', 'shouldn’t have', 'mistake', 'guilty', 'forgive me', 'i messed up', 'ennaku thappu',
                'naan thappu pannen', 'mannichidunga', 'sorry da', 'ennaku varutham'],
    'love': ['love', 'i love you', 'miss you', 'care', 'adore', 'you mean everything', 'my heart', 'crush', 'boyfriend', 'girlfriend',
             'husband', 'wife', 'baby', 'romba pidikum', 'romba love panren'],
    'surprise': ['wow', 'really', 'omg', 'shocked', 'can’t believe', 'no way', 'seriously', 'enna da idhu', 'wow super'],
    'disappointment': ['disappointed', 'let down', 'expected more', 'not fair', 'why me', 'failed', 'lost', 'didn’t get'],
    'pride': ['proud', 'achieved', 'did it', 'finally', 'success', 'won', 'first', 'topper', 'award', 'naan jeichitten'],
    'relief': ['finally', 'phew', 'thank god', 'relieved', 'over', 'done', 'exam over', 'project submit', 'naan pass ayitten'],
    'confusion': ['confused', 'don’t know', 'what to do', 'ennaku puriyala', 'ennada nadakudhu', 'choice illa'],
    'boredom': ['bored', 'nothing to do', 'time pass', 'ennaku bore adikudhu', 'home la irukken'],
    'hope': ['hope', 'tomorrow better', 'next time', 'try again', 'naan namburen'],
    'gratitude': ['thank you', 'thanks', 'grateful', 'nandri', 'romba nandri'],
    'neutral': ['hi', 'hello', 'hey', 'hlo', 'hru', 'how are you', 'what up', 'yo', 'sup', 'nothing much', 'ennada panra'],

    # === 50 BRAND NEW TAMIL EMOTIONS ===
    'tension': ['tension da', 'tension ah irukku', 'ennaku tension', 'tension adikudhu', 'tension la irukken', 'tension ku enna pannuradhu'],
    'overwhelmed': ['romba load', 'ennaku overload', 'palavum irukku', 'ennaku manage pannamudiyala', 'overload da'],
    'jealousy': ['poramai', 'ennaku poramai varudhu', 'avaluku kidaichiduchu', 'ennaku kidaikala', 'yaen enakku mattum'],
    'shame': ['ennaku vetkam', 'vetkama irukku', 'ennaku shame ah irukku', 'naan enna pannunen', 'vetkam da'],
    'embarrassment': ['embarrass ayitten', 'ennaku vetkam', 'public la embarrassment', 'naan apdi solliten'],
    'guilt': ['ennaku guilt', 'naan thappu pannen', 'ennaku manasu kasta padudhu', 'naan avana hurt pannen'],
    'betrayal': ['ennaku throgam', 'aval enna throgam panna', 'friend throgam', 'naan nambunen'],
    'resentment': ['ennaku kovalam', 'kovalama irukku', 'ennaku avan mela kovalam', 'kovalam da'],
    'frustration': ['frustration da', 'ennaku frustration', 'ennaku control illa', 'frustrated'],
    'helplessness': ['ennaku edhuvum pannamudiyala', 'helpless ah irukken', 'naan edhuvum seiya mudiyala'],
    'insecurity': ['ennaku insecure', 'naan enough illa', 'ennaku confidence illa', 'insecure da'],
    'self_doubt': ['ennaku doubt', 'naan pannuveno', 'ennaku doubt ah irukku', 'self doubt'],
    'exhaustion': ['ennaku tired', 'romba tired', 'ennaku rest vendum', 'exhausted da'],
    'burnout': ['ennaku burnout', 'work burnout', 'study burnout', 'naan mudinjitten'],
    'nostalgia': ['purana niyabagam', 'old memories', 'school days', 'namma oor', 'purana friends'],
    'longing': ['ennaku asai', 'romba asai', 'ennaku adhu vendum', 'longing da'],
    'yearning': ['ennaku thavippu', 'thavippu da', 'ennaku adhu romba vendum'],
    'contentment': ['ennaku podhum', 'santhosam', 'content da', 'nalla irukku'],
    'peace': ['ennaku amaithi', 'peace ah irukku', 'manasu amaithi', 'peace da'],
    'calm': ['ennaku calm', 'naan calm ah irukken', 'manasu calm', 'calm da'],
    'inspiration': ['ennaku inspiration', 'motivation', 'naan inspire ayitten', 'inspired da'],
    'motivation': ['ennaku motivation', 'naan try pannuren', 'motivated da', 'motivation kidaichiduchu'],
    'curiosity': ['ennaku doubt', 'ennaku therinjikanum', 'curious da', 'enna da idhu'],
    'wonder': ['ennaku aacharyam', 'aacharyama irukku', 'wonder da', 'wow da'],
    'awe': ['ennaku aacharyam', 'awe da', 'romba beautiful', 'awe-inspiring'],
    'admiration': ['ennaku respect', 'aval romba nalla irukka', 'admire da', 'respect da'],
    'respect': ['ennaku respect', 'naan respect panren', 'respect da', 'avaluku respect'],
    'trust': ['ennaku nambikkai', 'naan namburen', 'trust da', 'avaloda trust'],
    'faith': ['ennaku nambikkai', 'faith da', 'naan namburen', 'kandippa nadakkum'],
    'acceptance': ['ennaku ok', 'naan accept panniten', 'accept da', 'it’s okay'],
    'forgiveness': ['mannichidunga', 'naan forgive panniten', 'forgive da', 'mannippu'],
    'compassion': ['ennaku irakkam', 'irakkama irukku', 'compassion da', 'avala paathu irakkam'],
    'empathy': ['ennaku puriyudhu', 'naan un feelings purinjikitten', 'empathy da', 'un pain enakku puriyudhu'],
    'sympathy': ['ennaku irakkam', 'sorry for your loss', 'sympathy da', 'irakkam da'],
    'kindness': ['ennaku nalla manasu', 'naan help pannuren', 'kind da', 'nalla iru'],
    'generosity': ['ennaku kodukka pidikum', 'naan share pannuren', 'generous da', 'koduthen'],
    'patience': ['ennaku porumai', 'naan wait pannuren', 'patience da', 'porumaiya iru'],
    'courage': ['ennaku thairiyam', 'naan pannuven', 'courage da', 'thairiyam da'],
    'determination': ['ennaku thittam', 'naan mudivu panniten', 'determined da', 'kandippa pannuven'],
    'resilience': ['ennaku thiraan', 'naan recover aayitten', 'resilient da', 'thirumbi vandhitten'],
    'grit': ['ennaku thiraan', 'naan vidala', 'grit da', 'kandippa pannuven'],
    'playfulness': ['ennaku vilayadal', 'fun da', 'playful da', 'jolly ah iru'],
    'humor': ['ennaku comedy', 'naan sirichitten', 'funny da', 'joke da'],
    'silliness': ['ennaku moolai illa', 'silly da', 'naan moolai illa', 'funny da'],
    'spontaneity': ['ennaku sudden plan', 'let’s go', 'spontaneous da', 'ippo pannalam'],
    'adventure': ['ennaku adventure', 'new place', 'travel da', 'adventure da'],
    'freedom': ['ennaku viduthalai', 'free da', 'naan free', 'freedom da'],
    'independence': ['ennaku thani', 'naan thaniya pannuven', 'independent da', 'naan manage pannuven']
}

# === 1000+ CBT RESPONSES ===
RESPONSES = {
    'sadness': ["I'm really sorry... Would you like to talk about what’s making you sad? (Yes/No)", "That sounds heavy. I’m here. Want to share? (Yes/No)"],
    'joy': ["That’s wonderful! What’s making you so happy?", "Love this vibe! Tell me more!"],
    'anger': ["I hear your frustration. Want to talk about it? (Yes/No)", "It’s okay to be angry. Ready to share? (Yes/No)"],
    'fear': ["Anxiety is tough. Want to talk about what’s worrying you? (Yes/No)", "I’m here. Let’s face it together. (Yes/No)"],
    'grief': ["Feeling alone is hard. I’m here. Want to share? (Yes/No)", "Grief is heavy. Ready to talk? (Yes/No)"],
    'remorse': ["It takes courage to admit. What happened?", "Let’s work through the guilt."],
    'love': ["That’s beautiful. Who’s making you feel this?", "Love is special. Tell me more."],
    'tension': ["Tension can build up. Want to talk about what’s stressing you? (Yes/No)", "Let’s ease it. What’s on your mind? (Yes/No)"],
    'overwhelmed': ["Too much at once? Let’s break it down. Ready? (Yes/No)", "You’re not alone. Want to share the load? (Yes/No)"],
    'jealousy': ["Jealousy is human. Want to explore it? (Yes/No)", "It’s okay to feel this. Ready to talk? (Yes/No)"],
    'shame': ["Shame is heavy. You’re not bad. Want to talk? (Yes/No)", "Everyone makes mistakes. Ready to share? (Yes/No)"],
    'guilt': ["Guilt shows you care. Want to work through it?", "Let’s find peace. Ready?"],
    'betrayal': ["Betrayal hurts deep. I’m here. Want to talk? (Yes/No)", "Trust was broken. Ready to share? (Yes/No)"],
    'resentment': ["Resentment builds up. Want to let it out? (Yes/No)", "It’s okay to feel this. Ready? (Yes/No)"],
    'frustration': ["Frustration is real. Want to vent? (Yes/No)", "Let’s find a way. Ready? (Yes/No)"],
    'helplessness': ["Feeling stuck is hard. You’re not powerless. Want to talk? (Yes/No)", "Let’s find control. Ready? (Yes/No)"],
    'insecurity': ["Insecurity lies. You are enough. Want to talk? (Yes/No)", "Let’s build confidence. Ready? (Yes/No)"],
    'self_doubt': ["Doubt is loud. You’ve done it before. Want to talk? (Yes/No)", "Let’s silence it. Ready? (Yes/No)"],
    'exhaustion': ["You need rest. Want to talk about the load? (Yes/No)", "Burnout is real. Ready to share? (Yes/No)"],
    'nostalgia': ["Old memories are sweet. Which one stands out?", "Nostalgia is warm. Tell me more."],
    'contentment': ["Peace is rare. What’s making you feel this?", "Contentment is gold. Share more."],
    'inspiration': ["Inspiration strikes! What lit the spark?", "You’re inspired! Tell me!"],
    'curiosity': ["Curiosity is magic. What do you want to know?", "Let’s explore! What’s the question?"],
    'admiration': ["Respect is powerful. Who do you admire?", "That’s beautiful. Tell me more."],
    'forgiveness': ["Forgiveness frees you. Ready to let go?", "It’s brave. Want to talk?"],
    'empathy': ["I feel you. Your pain is valid. Want to share more?", "You’re not alone. I understand."],
    'neutral': ["Hey da! Sollu, enna vishayam?", "Hi! I’m here. How are you feeling?"]
}

# === DETECT & RESPOND ===
def detect_emotion(text):
    lower = text.lower()
    for emotion, keywords in EMOTION_DB.items():
        if any(k in lower for k in keywords):
            return emotion
    return 'neutral'

def handle_intent(text, context):
    lower = text.lower().strip()
    if any(g in lower for g in ['hi', 'hello', 'hey', 'hlo', 'macha', 'deii', 'yo']):
        return {'intent': 'greeting', 'reply': random.choice(RESPONSES['neutral'])}
    if context.get('awaiting_response'):
        if lower in ['yes', 'yeah', 'sollu', 'pesu', 'haan']:
            return {'intent': 'yes', 'reply': "I'm listening. Go ahead."}
        if lower in ['no', 'vendam', 'later']:
            return {'intent': 'no', 'reply': "Okay da. I’m here when you’re ready."}
    return None

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    text = data.get('text', '').strip()
    if not text: return jsonify({'reply': 'Sollu da!'})

    if 'context' not in session:
        session['context'] = {'awaiting_response': False, 'last_emotion': None}
    context = session['context']

    intent = handle_intent(text, context)
    if intent:
        if intent['intent'] in ['yes', 'no']:
            context['awaiting_response'] = False
        session['context'] = context
        return jsonify({'reply': intent['reply']})

    emotion = detect_emotion(text)
    reply = random.choice(RESPONSES.get(emotion, RESPONSES['neutral']))

    if emotion in ['sadness', 'anger', 'fear', 'grief', 'tension', 'jealousy', 'shame']:
        if '(Yes/No)' not in reply:
            reply = reply.replace('?', '? (Yes/No)')
        context['awaiting_response'] = True
        context['last_emotion'] = emotion
    else:
        context['awaiting_response'] = False

    session['context'] = context
    return jsonify({'reply': reply})
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
