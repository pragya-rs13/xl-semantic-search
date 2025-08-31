from fastapi import APIRouter, Form, UploadFile, File
from typing import Optional
from schemas.llm_schema import SearchRequest
from usecases.uploads import handle_uploaded_csv, handle_uploaded_excel
from usecases.search import searchPipeline


router = APIRouter()

@router.post("/search")
async def search(
    query: str = Form(...),  # query comes as a form field
    file: UploadFile = File(...)
):
    
    # detect extension
    filename = file.filename.lower()
    if filename.endswith(".csv"):
        jsonl_path = handle_uploaded_csv(file)
    elif filename.endswith((".xls", ".xlsx")):
        jsonl_path = handle_uploaded_excel(file)
    else:
        return {"error": "Unsupported file type"}
    

    # Pass JSONL file into your pipeline (expand → rank → validate etc.)
    results = searchPipeline(request=query, jsonl_document=jsonl_path)
    
    response = {"size": len(results), "results": results}
    return response
