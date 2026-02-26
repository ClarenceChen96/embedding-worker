"""RunPod serverless handler for embeddinggemma-300m embeddings."""

import os

from huggingface_hub import login

# Authenticate with HuggingFace before loading model
hf_token = os.environ.get("HF_TOKEN")
if hf_token:
    login(token=hf_token)
    print("HuggingFace authentication successful")

import runpod
from sentence_transformers import SentenceTransformer

MODEL_NAME = os.environ.get("MODEL_NAME", "google/embeddinggemma-300m")

print(f"Loading model: {MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME, trust_remote_code=True)
dim = model.get_sentence_embedding_dimension()
print(f"Model loaded. Dimension: {dim}")


def handler(event):
    """Handle embedding requests in OpenAI-compatible format."""
    input_data = event["input"]

    texts = input_data.get("input", [])
    if isinstance(texts, str):
        texts = [texts]

    if not texts:
        return {"data": [], "model": MODEL_NAME, "usage": {"prompt_tokens": 0, "total_tokens": 0}}

    embeddings = model.encode(texts)

    data = [
        {"embedding": emb.tolist(), "index": i, "object": "embedding"}
        for i, emb in enumerate(embeddings)
    ]

    return {
        "object": "list",
        "model": MODEL_NAME,
        "data": data,
        "usage": {
            "prompt_tokens": sum(len(t.split()) for t in texts),
            "total_tokens": sum(len(t.split()) for t in texts),
        },
    }


runpod.serverless.start({"handler": handler})
