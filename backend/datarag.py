import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
import getpass
import os
import warnings
warnings.filterwarnings("ignore")

# Read the dataframe
df = pd.read_csv('data/output.csv')

# Vector encoding 
text = df['Big_context'] # enter the df name
encoder = SentenceTransformer("all-mpnet-base-v2",cache_folder="./working/cache/")
vectors = encoder.encode(text)

vector_dimension = 768
index = faiss.IndexFlatIP(vector_dimension)
faiss.normalize_L2(vectors)
index.add(vectors)

np.save('vectors.npy', vectors)
faiss.write_index(index, 'index.faiss')


def get_content(Query):
    search_vector = encoder.encode(Query)  
    distances, indices = index.search(np.array([search_vector]), k=10)
    labels = df['Big_context']
    top_10_contexts = [labels.iloc[idx] for idx in indices[0][:10]]    
    concatenated_contexts = "\n".join(top_10_contexts)
    return concatenated_contexts

# Apply the Gemini API Key
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("AIzaSyA_tac4MMAy4HHpL26QgBD3ZGccHgyGu9A",)

llm = ChatGoogleGenerativeAI(model="gemini-pro")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Generating answers
def generate_text(prompt):

    response = model.generate_content(prompt)

    return response.text

# Query and prompt generation
query = 'tell me something about the Snapdeal investment of blackrock'
prompt_template = f"Relevant context: {get_content(query)}\n\n Answer the question in detail: {query}"

# Answer generation
generate_text(prompt_template)