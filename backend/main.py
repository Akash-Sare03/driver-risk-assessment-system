from fastapi import FastAPI, UploadFile, File
from core.analyze import analyze_driver_image

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    return analyze_driver_image(await file.read())
