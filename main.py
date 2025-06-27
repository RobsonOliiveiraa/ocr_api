from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import easyocr
import tempfile

app = FastAPI()
reader = easyocr.Reader(['pt'])

@app.post("/ocr")
async def perform_ocr(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        result = reader.readtext(tmp_path, detail=0, paragraph=True)
        return JSONResponse(content={"text": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)