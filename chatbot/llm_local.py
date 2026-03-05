from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Loading LLM model...")
MODEL_NAME = "distilgpt2"
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    logger.info("LLM model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise

def generate_reply(prompt, max_length=150):  # Increased for coherence
    logger.info(f"Generating reply for prompt: {prompt[:50]}...")
    try:
        inputs = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors="pt", truncation=True, max_length=512)
        outputs = model.generate(
            inputs,
            max_length=max_length,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            top_p=0.9,
            temperature=0.7,
            no_repeat_ngram_size=2  # Prevent repetition
        )
        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
        reply = decoded[len(prompt):].strip()
        if not reply or len(reply) < 5:  # Handle empty/short outputs
            reply = "I'm here to help. Could you share a bit more about how you're feeling?"
        logger.info(f"Reply generated: {reply[:50]}...")
        return reply
    except Exception as e:
        logger.error(f"Error generating reply: {e}")
        return "I'm here to help. Could you share a bit more about how you're feeling?"