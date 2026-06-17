import time
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

print("Starting model load...", flush=True)

start = time.time()
model = SentenceTransformer(MODEL_NAME, device="cpu")
print(f"Model loaded in {round(time.time() - start, 2)} seconds.", flush=True)

texts = [
    "I was charged twice for my order.",
    "I cannot login to my account.",
    "I want to cancel my subscription."
]

print("Creating embeddings...", flush=True)
embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

print("Embeddings shape:", embeddings.shape, flush=True)
print("Test completed successfully.", flush=True)