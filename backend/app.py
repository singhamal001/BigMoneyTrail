# app.py
import numpy as np
import faiss
from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import getpass
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

# Read the dataframe
df = pd.read_csv('data/output.csv')

# Vector encoding 
text = df['Big_context']

# llm = ChatGoogleGenerativeAI(model="gemini-pro")

genai.configure(api_key="AIzaSyA_tac4MMAy4HHpL26QgBD3ZGccHgyGu9A")
model = genai.GenerativeModel('gemini-pro')

# Load vectors and index
loaded_vectors = np.load('vectors.npy')
loaded_index = faiss.read_index('index.faiss')
encoder = SentenceTransformer("all-mpnet-base-v2",cache_folder="./working/cache/")

def get_content(Query):
    search_vector = encoder.encode(Query)  
    distances, indices = loaded_index.search(np.array([search_vector]), k=10)
    labels = df['Big_context']
    top_10_contexts = [labels.iloc[idx] for idx in indices[0][:10]]    
    concatenated_contexts = "\n".join(top_10_contexts)
    return concatenated_contexts

def generate_text(prompt):

    response = model.generate_content(prompt)

    return response.text

@app.route('/process', methods=['POST'])

def process_input():
    data = request.json
    user_input = data['input']

    # Generate the context using your retrieval function
    context = get_content(user_input)

    # Generate the augmented prompt
    prompt_template = f"Using this Relevant context Answer the question in detail, Based on this context if you have some valuable additions then please add that as well:\n Context: {context}\n Question\n  {user_input} "

    # Call the LLM API with the augmented prompt
    response_text = generate_text(prompt_template)

    # Form the response to send back to the frontend
    response = {
        "response": response_text
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)