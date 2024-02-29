import pandas as pd
import numpy as np
import getpass
import os
import faiss
from sentence_transformers import SentenceTransformer
import getpass
import os
import google.generativeai as genai
import re
import warnings
warnings.filterwarnings("ignore")

# Rag bot

# Reading the data
Fin_df = pd.read_csv('Combined context') # Read the preprocessed data in csv form

# # Vector encoding 
text = Fin_df['Combined_Context'] # enter the df name with the column that contains contexts

# Using all-mpnet-base-v2 for vector embedding and faiss index for vector database
encoder = SentenceTransformer("all-mpnet-base-v2",cache_folder="./working/cache/")
vectors = encoder.encode(text)
vector_dimension = 768

index = faiss.IndexFlatIP(vector_dimension)
faiss.normalize_L2(vectors)
index.add(vectors)

# Save vectors and index
np.save('Fin_vectors.npy', vectors)
faiss.write_index(index, 'Fin_index.faiss')

# Load vectors and index
loaded_vectors = np.load('FIn_vectors.npy')
loaded_index = faiss.read_index('Fin_index.faiss')

# Doing similarity search on the query
def get_content(Query):
    match = re.search(r'\b2\d{3}\b', Query) # Adding condition for year based filtering if applicable for improved results
    year = int(match.group()) if match else None

    search_vector = encoder.encode(Query)  
    distances, indices = loaded_index.search(np.array([search_vector]), k=10)
    labels = Fin_df['Combined_Context']
    
    relevant_contexts = []
    
    for idx in indices[0]:
        context = labels.iloc[idx]
        # Check if the year exists in the context
        if year and str(year) in context:
            relevant_contexts.append(context)
        
        # Check if we have collected at least 10 relevant contexts
        if len(relevant_contexts) >= 10:
            break
    
    # If no relevant contexts found, perform a normal search
    if not relevant_contexts:
        relevant_contexts = [labels.iloc[idx] for idx in indices[0][:10]]
    
    concatenated_contexts = "\n".join(relevant_contexts)
    return concatenated_contexts # Returning concatenation of top 10 relevant contexts

# Setting the GOOGLE_API_KEY environment variable 
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")
    
# Calling gemini base model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')


# Implementing response generation with history retention for upto 5 prompts
MAX_HISTORY_LENGTH = 5
conversation_history = []

def generate_text(prompt, history=[]):
    prompt_with_history = prompt

    recent_history = conversation_history[-MAX_HISTORY_LENGTH:]
    for prev_prompt, prev_response in recent_history:
        prompt_with_history = f"{prev_prompt}\n{prev_response}\n\n{prompt_with_history}"

    response = model.generate_content(prompt_with_history)
    conversation_history.append((prompt, response.text))
    conversation_history[:] = conversation_history[-MAX_HISTORY_LENGTH:]

    return response.text

# Query and prompt template with advanced prompt engineering
query = 'tell me about fidelity investments deal of infoedge'
prompt_template = f"Relevant context: {get_content(query)}\n , understand the essence of the context, \n Answer the question in detail, imagine you are a financial analyst who is conveying this information to a retail investor: {query}, you will get multiple contexts the first line of provided context has information about the deal made, about the particular investee company, followed by year summary, nation summary etc. then the second context starts similarly and so on, Based on this answer the question in brief and return part of the context that led you to the answer, remember i would rather you dont give an answer rather than giving the wrong answer, my life depends on it"

# Result
result_text = generate_text(prompt_template)