import os
import asyncio
import torch
import faiss
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
from sentence_transformers import SentenceTransformer, CrossEncoder
from transformers import AutoModelForCausalLM, AutoTokenizer
import edge_tts
from colorama import Fore, Style, init

init(autoreset=True)

# ------------------- GLOBALS -------------------
bi_encoder = None
cross_encoder = None
chunk_map = {}
index = None

# ------------------- SPEAK FUNCTION -------------------
async def speak(text):
    tts = edge_tts.Communicate(text, "en-US-AvaNeural")
    filename = "response.mp3"
    await tts.save(filename)
    audio = AudioSegment.from_file(filename, format="mp3")
    play(audio)

# ------------------- LOAD + EMBEDDINGS -------------------
def init_models_and_index():
    global bi_encoder, cross_encoder, chunk_map, index

    bi_encoder = SentenceTransformer("intfloat/e5-large-v2")
    cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    with open("./Newdata.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    chunks = []
    for i in range(len(lines)):
        if lines[i].startswith("User"):
            user_query = lines[i].replace("User", "").strip()
            ai_response = []
            j = i + 1
            while j < len(lines) and lines[j].startswith("AI"):
                ai_response.append(lines[j].replace("AI", "").strip())
                j += 1
            full_chunk = f"User: {user_query}\nAI: {' '.join(ai_response)}"
            chunks.append(full_chunk)

    chunk_embeddings = bi_encoder.encode(chunks, convert_to_tensor=False, show_progress_bar=True)
    chunk_embeddings = np.array(chunk_embeddings).astype("float32")

    dimension = chunk_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(chunk_embeddings)
    chunk_map = {i: chunks[i] for i in range(len(chunks))}

# ------------------- RETRIEVAL -------------------
def retrieve_top_chunk(query):
    query_embedding = bi_encoder.encode(query, convert_to_tensor=False).astype("float32")
    D, I = index.search(np.array([query_embedding]), 10)
    candidate_chunks = [chunk_map[i] for i in I[0]]
    scores = cross_encoder.predict([[query, c] for c in candidate_chunks])
    sorted_chunks = sorted(zip(candidate_chunks, scores), key=lambda x: x[1], reverse=True)
    return sorted_chunks[0][0]

def get_ai_response(user_input):
    top_chunk = retrieve_top_chunk(user_input)
    lines = top_chunk.split("\n")
    ai_line = next((line.replace("AI:", "").strip() for line in lines if line.startswith("AI:")), "Let me help you.")
    return ai_line

# ------------------- MAIN ENTRY -------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 2 and sys.argv[1] == "ask":
        user_question = sys.argv[2]
        init_models_and_index()
        ai_response = get_ai_response(user_question)
        print(f"{ai_response}")
        asyncio.run(speak(ai_response))
