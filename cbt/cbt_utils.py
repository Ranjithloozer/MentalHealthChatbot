CBT_TEMPLATES = {
    "admiration": "Wow, that’s inspiring! What’s sparking this admiration? Let’s explore what makes it special.",
    "amusement": "That sounds like fun! What’s making you smile? Want to share the moment?",
    "anger": "It sounds like you’re really upset. Anger can be tough. Let’s take a moment to breathe and explore what’s triggering this.",
    "annoyance": "It sounds like something’s getting under your skin. Let’s pinpoint what’s causing this annoyance and find ways to address it.",
    "approval": "That’s great to hear! What’s got you feeling so positive? Let’s build on that vibe!",
    "caring": "Your caring nature is beautiful! Want to talk about who or what you’re feeling this way about?",
    "confusion": "It’s okay to feel confused. Let’s break things down together. Can you share more about what’s unclear?",
    "curiosity": "I love your curiosity! What’s sparking your interest? Let’s dive deeper into that topic.",
    "desire": "It’s great to have goals! Tell me more about what you’re aiming for, and we can explore steps to get there.",
    "disappointment": "I’m sorry you’re feeling disappointed. Let’s explore what happened and find a positive perspective.",
    "disapproval": "It sounds like something’s not sitting right with you. Want to talk about what’s bothering you?",
    "disgust": "That sounds really unpleasant. Let’s explore what’s causing this feeling and how to move forward.",
    "embarrassment": "Feeling embarrassed can be tough. I’m here for you. Want to share what happened?",
    "excitement": "You’re buzzing with excitement! That’s awesome. Tell me more about what’s got you so energized!",
    "fear": "Feeling scared can be overwhelming. I’m here to listen. Would you like to talk about what’s worrying you?",
    "gratitude": "That’s wonderful! Gratitude can be so uplifting. Want to share more about what you’re thankful for?",
    "grief": "I’m so sorry you’re going through this. Grief is heavy. Would you like to share more or try a comforting exercise?",
    "joy": "That’s so great to hear! What’s making you feel so happy? Let’s celebrate this moment!",
    "love": "Feeling love is beautiful! Want to share more about who or what’s in your heart?",
    "nervousness": "I hear you’re feeling anxious. That can feel intense. Would you like to try a grounding exercise?",
    "optimism": "Your positivity is infectious! What’s got you feeling so hopeful? Let’s explore that!",
    "pride": "That’s amazing! What are you proud of? Let’s celebrate your achievement!",
    "realization": "That sounds like a big moment! What did you just realize? Let’s explore what it means for you.",
    "relief": "Phew, that must feel good! What brought on this relief? Let’s savor it.",
    "remorse": "Feeling regret can be heavy. It’s great that you’re reflecting. Would you like to talk about how to move forward?",
    "sadness": "I’m really sorry you’re feeling sad. It’s okay to feel this way sometimes. Would you like to share more?",
    "surprise": "Wow, that sounds unexpected! What happened? Let’s talk about it.",
    "neutral": "Thanks for sharing! I’m here to listen. What’s on your mind today?"
}

def get_cbt_prompt(emotion):
    return CBT_TEMPLATES.get(emotion, CBT_TEMPLATES["neutral"])