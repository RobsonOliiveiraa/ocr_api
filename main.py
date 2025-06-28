from fastapi import FastAPI, File, UploadFile
import easyocr
import uvicorn
import shutil
import os

app = FastAPI()
reader = easyocr.Reader(['pt'], gpu=False)

@app.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    try:
        temp_file = f"temp_{file.filename}"
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = reader.readtext(temp_file, detail=0)
        os.remove(temp_file)
        return {"text": result}

    except Exception as e:
        return {"error": str(e)}
