from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import uvicorn
import shutil
import os
import uuid

app = FastAPI()

# CORS - Permite que o frontend acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Substitua por seu domínio específico em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o leitor EasyOCR
reader = easyocr.Reader(['pt'], gpu=False)

@app.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    try:
        ext = os.path.splitext(file.filename)[1]
        temp_filename = f"temp_{uuid.uuid4()}{ext}"

        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = reader.readtext(temp_filename, detail=0)
        os.remove(temp_filename)
        return {"text": result}

    except Exception as e:
        return {"error": str(e)}

