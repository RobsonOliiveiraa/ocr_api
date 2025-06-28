from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import easyocr
from io import BytesIO
from PIL import Image
import numpy as np

app = FastAPI()
reader = easyocr.Reader(['pt', 'en'])

@app.post("/ocr/")
async def perform_ocr(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        image = Image.open(BytesIO(contents)).convert("RGB")
        image_np = np.array(image)
        results = reader.readtext(image_np)
        extracted_text = [" ".join([res[1]]) for res in results]
        return {"text": extracted_text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
