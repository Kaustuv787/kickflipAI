import streamlit as st
import faiss
import pickle
import numpy as np
import os
import boto3
import json
import numpy as np
# Load FAISS index
index = faiss.read_index("faiss_index.bin")

# Load metadata
with open("metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

videos = metadata["videos"]
captions = metadata["captions"]


# Initialize Bedrock Runtime client
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

# Titan Embedding model ID
model_id = "amazon.titan-embed-text-v2:0"

# Function to get Titan embedding for a string
def titan_embed(text: str) -> list:
    payload = {"inputText": text}
    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        body=json.dumps(payload),
        contentType="application/json"
    )
    result = json.loads(response["body"].read())
    return result["embedding"]

# For multiple captions
def encode_captions(captions: list[str]) -> np.ndarray:
    print("in app.py")
    embeddings = [titan_embed(text) for text in captions]
    return np.array(embeddings, dtype="float32")


# Load embedding model
#text_encoder = SentenceTransformer("all-MiniLM-L6-v2")

# Streamlit UI
st.title("🎥 Video Retrieval System")
st.write("Search for a video by entering a relevant description!")

# User input for search
query = st.text_input("Enter search query:", "")

if query:
    # Compute query embedding
    #query_emb = text_encoder.encode([query])
    # Compute text embeddings using Titan
    query_emb = encode_captions(captions)


    # Search FAISS for closest match
    _, indices = index.search(np.array(query_emb), k=1)  # Get top match
    best_video = videos[indices[0][0]]
    best_caption = captions[indices[0][0]]

    # Display results
    st.write(f"**Best Match Caption:** {best_caption}")

    video_path = os.path.join(best_video)

    if os.path.exists(video_path):
        st.video(video_path)
    else:
        st.write("Video not found!")
