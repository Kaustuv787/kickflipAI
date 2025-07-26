import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
import boto3
import json
# Define video directory
VIDEO_DIR = "videos"  # Folder where videos are stored

# Sample dataset (video filenames and captions)
videos = [
    "videos/video1.mp4", "videos/video2.mp4", "videos/video3.mp4",
    "videos/video4.mp4", "videos/video5.mp4", "videos/video6.mp4",
    "videos/video7.mp4"
]

captions = ["Ed Sheeran and Diljit Dosanjh perform 'Shape of You' & 'Naina', live from Birmingham on 22nd September 2024.",
            "Ed Sheeran performs 'Perfect' live from Kaunas, Lithuania as part of the Mathematics Tour 2024", 
            "Ed Sheeran performing Give me love live on his X Album Release Party",
            "Guns N' Roses - Knockin' On Heaven's Door (The Freddie Mercury Tribute Concert)",
            "Guns N' Roses - November Rain  (Tokyo 1992)  HD Remastered",
            "Ozzy Osbourne performing “Crazy Train” Live",
            "Black Sabbath perform Paranoid live at the O2 Academy in Birmingham."]

# Load embedding model
# text_encoder = SentenceTransformer("all-MiniLM-L6-v2")

# # Compute text embeddings
# text_embeddings = text_encoder.encode(captions)

# # Save metadata (video paths and captions)
# metadata = {"videos": videos, "captions": captions}

# with open("metadata.pkl", "wb") as f:
#     pickle.dump(metadata, f)

# # Store in FAISS index
# d = text_embeddings.shape[1]  # Dimensionality
# index = faiss.IndexFlatL2(d)
# index.add(np.array(text_embeddings))

# # Save FAISS index
# faiss.write_index(index, "faiss_index.bin")


# print("✅ FAISS index and metadata saved successfully!")



#---------------------------------TITAN EMBEDDINGS START HERE-----------------------------------


# Create Bedrock client (adjust region as needed)
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Titan Embedding model ID
model_id = "amazon.titan-embed-text-v2:0"
def get_titan_embedding(text):
    payload = {"inputText": text}
    print("generating the captions embeddings")
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(payload),
        contentType="application/json"
    )
    result = json.loads(response['body'].read())
    return result["embedding"]

# Encode all captions with Titan
text_embeddings = [get_titan_embedding(caption) for caption in captions]
text_embeddings = np.array(text_embeddings).astype("float32")  # FAISS needs float32

# Save metadata
metadata = {"videos": videos, "captions": captions}
with open("metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

# Create and populate FAISS index
embedding_dim = text_embeddings.shape[1]
print("embedding dimension is ",embedding_dim)
index = faiss.IndexFlatL2(embedding_dim)
index.add(text_embeddings)
faiss.write_index(index, "faiss_index.bin")
