from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import io

from .ai_engine import simulate_ai_generation

app = FastAPI(title="CSR to Article API", description="Backend for processing CSR to Research Article Draft")

@app.post("/api/generate-article")
async def generate_article(file: UploadFile = File(...)):
    """
    Receives a CSR document, extracts the text (mocked for PoC),
    and returns a structured JSON with IMRaD sections.
    """
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
    
    # In a real app we'd parse the PDF/DOCX here:
    # content = await file.read()
    # text = extract_text_from_doc(content)
    # mock:
    text = "Extracting text from " + file.filename
    
    print(f"Received file: {file.filename}, simulating processing...")
    
    # Process text through AI engine
    try:
        imrad_sections = await simulate_ai_generation(text)
        return JSONResponse(content={"status": "success", "data": imrad_sections})
    except Exception as e:
        print(f"Error during AI processing: {e}")
        raise HTTPException(status_code=500, detail="Error generating article draft.")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
