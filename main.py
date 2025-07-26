import os
from http.client import responses
from fastapi import FastAPI
#from openai import AzureOpenAI, api_version, embeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from contextlib import asynccontextmanager
from app.utils import format_docs
from app.prompts import prompt
from app.logger import Logger
from dotenv import load_dotenv
from typing_extensions import override
from groq import Groq
from langchain_aws import ChatBedrock, BedrockEmbeddings
from langchain_community.llms import Bedrock
import numpy as np
import boto3

load_dotenv(override=True)

vectorstore_db=None
logger=Logger()

# API_KEY = "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"

# client = Groq(
#     api_key=API_KEY,
# )


# embeddings = HuggingFaceEmbeddings(
#     model_name = 'paraphrase-MiniLM-L6-v2',
#     model_kwargs = {'device':'cpu'}
# )
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

# Claude Instant (LLM) via Bedrock
llm = ChatBedrock(
    client=bedrock_runtime,
    model_id="anthropic.claude-instant-v1",  # or use claude-3-haiku if you prefer
    model_kwargs={"temperature": 0.7}
)

# Titan Embeddings via Bedrock
embeddings = BedrockEmbeddings(
    client=bedrock_runtime,
    model_id="amazon.titan-embed-text-v2:0"
)

# Load embedding model
#text_encoder = SentenceTransformer("paraphrase-MiniLM-L6-v2", device="cpu")

@asynccontextmanager
async def lifespan(app: FastAPI) :
    global vectorstore_db
    loader = CSVLoader(file_path = "app/data/EventData.csv")
    documents = loader.load()
    print("Building the vector db")
    # we have created the vector database from the csv file
    vectorstore_db = FAISS.from_documents(documents,embeddings)
    print("its done")
    yield

app = FastAPI(lifespan = lifespan)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Event API"}

@app.get("/answer")
async def answer_question(query: str):
    try:
       # print(f"Received query: {query}")

        if not vectorstore_db:
            # Possibly failed to load in lifespan
            return {"error": "Vectorstore not initialized."}

        docs = vectorstore_db.similarity_search(query, k=5)
        #print(f"Docs: {docs}")

        if not docs:
            return {"error": "No documents found for this query."}

        docs_formatted = format_docs(docs)
        #print(f"Formatted Docs: {docs_formatted}")

        base_prompt = prompt()
       # print(f"Base prompt: {base_prompt}")

        prompt_text = base_prompt.format(docs_formatted)
        #print(f"Final prompt text: {prompt_text}")

        response = llm.invoke(
            prompt_text + query
        )

        #print(f"API Response: {response}")
        return {"answer": response.content}

    except Exception as e:
        # Temporarily expose the error to debug
        return {"error": f"An error occurred: {str(e)}"}


@app.get("/retrieve")
async def retrieve_video(query: str):
    #print(f"Received query and inside retrieve part: {query}")
    try:
        import faiss
        import pickle

        index = faiss.read_index("VideoRetrievalPrototype/faiss_index.bin")
        #print(f"Received query and inside retrieve part: {query}")
        # Load metadata
        with open("VideoRetrievalPrototype/metadata.pkl", "rb") as f:
            metadata = pickle.load(f)
        #print(metadata)
        videos = metadata["videos"]
        captions = metadata["captions"]

        # Compute query embedding
        query_emb = embeddings.embed_query(query)  # Fix input type
        query_emb = np.array([query_emb])  # Fix shape for FAISS
        print("query embedding is ",query_emb.shape)
        # Search FAISS for closest match
        _, indices = index.search(query_emb, k=1)  # Get top match
        print(indices)
        best_video = videos[indices[0][0]]
        best_caption = captions[indices[0][0]]
        print("seraching best video complete")
        print(best_video)
        print(best_caption)
        # Return video path
        video_path = os.path.join("VideoRetrievalPrototype", best_video)
        return {"video_path": video_path, "caption": best_caption}

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
