from fastapi.responses import JSONResponse
from fastapi import HTTPException
from rag.rag_service import split_text_from_file, vectorizer_to_pgvector 

@app.post("/vectorize/")
async def rag_vectorize_file(file: UploadFile = File(...)):
    allowed_extensions = {".xlsx", ".pdf", ".txt", ".json"}
    file_extension = file.filename.split('.')[-1]
    if f".{file_extension}" not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: .{file_extension}. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    try:
        file_content = (await file.read()).decode("utf-8")
        docs_splits = split_text_from_file(file_content)
        chroma = vectorizer_to_pgvector(docs_splits)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "File vectorized successfully!", 
                "collection_name": chroma.collection_name
            }
        )
    except ValueError as ve:
        return JSONResponse(
            status_code=422,
            content={
                "status": "error", 
                "message": "A message error occurred.", 
                "details": str(ve)
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error", 
                "message": "An unexpected error occurred.", 
                "details": str(e)
            }
        )

async def save_question_answer_as_document() -> None:
    return 