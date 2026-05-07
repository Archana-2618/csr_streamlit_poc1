from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from backend.ai_engine import simulate_ai_generation

app = FastAPI(
    title="CSR to Article API",
    description="Backend for processing CSR to Research Article Draft"
)

@app.get("/")
def health_check():
    return {"status": "Backend is running"}

@app.post("/api/generate-article")
async def generate_article(file: UploadFile = File(...)):

    # Validate file type
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    try:
        # Mock text extraction (replace later with real parser)
        text = f"Extracting text from {file.filename}"

        print(f"Received file: {file.filename}, processing...")

        # AI processing
        imrad_sections = await simulate_ai_generation(text)

        return JSONResponse(
            content={
                "status": "success",
                "data": imrad_sections
            }
        )

    except Exception as e:
        print(f"Error during processing: {e}")

        raise HTTPException(
            status_code=500,
            detail="Error generating article draft."
        )
