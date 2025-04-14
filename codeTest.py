import torch
import google.generativeai as genai
from transformers import AutoModelForCausalLM, AutoTokenizer
from gtts import gTTS
from playsound3 import playsound
import sys

# ✅ Option 1: Use a lightweight local model (Phi-1.5)
LOCAL_MODEL = "microsoft/phi-1_5"

def load_local_model():
    print("Loading local AI model... This may take some time.")
    device = "cpu"  # ✅ Use CPU to avoid GPU memory issues
    tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL)
    model = AutoModelForCausalLM.from_pretrained(
        LOCAL_MODEL,
        torch_dtype=torch.float32,  # ✅ Avoid float16 issues on CPU
        device_map="cpu"
    ).to(device)
    return tokenizer, model, device

def clean_response(text):
    """Remove markdown notations like asterisks and other special characters."""
    return re.sub(r'[*_`]', '', text)

def generate_response_local(prompt, tokenizer, model, device):
    """Generate a concise response using the Phi-1.5 model."""
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=256).to(device)
    output = model.generate(
        **inputs,
        max_new_tokens=50,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.2
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return clean_response(response)

def send_text_response(text) :
    return re.sub(r'[*_`]', '', text)

# ✅ Option 2: Use Google Gemini API (Requires API Key)
GEMINI_API_KEY = "AIzaSyDD7KvN-cIA1y1lbs9PGCG_uWaSk44Knnc"

def generate_response_gemini(prompt):
    """Generate a concise response using the Google Gemini API."""
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt, generation_config={"max_output_tokens": 120})
    return clean_response(response.text)

def text_to_speech(text):
    """Convert text to speech using gTTS."""
    try:
        print("Speaking:", text)
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")
        playsound("output.mp3")
    except Exception as e:
        print(f"[ERROR] TTS failed: {e}")

# ✅ Choose between local model or cloud API
use_gemini = True  # Change to False if you want to use the local model

if not use_gemini:
    tokenizer, model, device = load_local_model()
Into export                                             
if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        if use_gemini:
            response = generate_response_gemini(user_input)
        else:
            response = generate_response_local(user_input, tokenizer, model, device)

        print("Assistant:", response)
        text_to_speech(response)
        send_text_response(response.text)
    else:
        print("Usage: python3 filename.py \"Your message here\"")
