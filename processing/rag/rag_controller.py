from fastapi import FastAPI, File, UploadFile
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
import json
import os
# import tempfile

@app.post("/vectorize/")
async def vectorize_file(file: UploadFile = File(...)):
    """
    Receives a .txt file, processes it, and returns the vectorization status.
    """
    # Read the file content
    try:
        # Save the file temporarily
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        # Read the file content
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

        # Split the content into chunks
        docs_splits = split_text_from_file(file_content)

        # Vectorize and store embeddings in PGVector (Chroma)
        chroma = vectorizer_to_pgvector(docs_splits)

        # Respond with a success message (you can customize this response as needed)
        return {"message": "File vectorized successfully!", "collection_name": chroma.collection_name}
    
    except Exception as e:
        return {"error": str(e)}

    finally:
        # Cleanup the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)