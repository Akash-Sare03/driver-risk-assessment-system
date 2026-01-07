from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
from PIL import Image
import io

from models.drowsiness.ear_detector import detect_drowsiness
from models.emotion.emotion_utils import predict_emotion
from models.seatbelt.seatbelt_utils import predict_seatbelt
from models.smoking.smoking_predictor import predict_smoking 

app = FastAPI(title="Driver Monitoring System")

@app.post("/analyze")
async def analyze_driver(file: UploadFile = File(...)):

    contents = await file.read()

    # ---------- OpenCV Image (Drowsiness) ----------
    np_array = np.frombuffer(contents, np.uint8)
    image_cv = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if image_cv is None:
        return {"error": "Invalid image"}

    # ---------- PIL Image (Emotion, Seatbelt, Smoking) ----------
    try:
        image_pil = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        return {"error": "Invalid image format"}

    # ---------- Predictions ----------
    drowsiness = detect_drowsiness(image_cv)
    emotion = predict_emotion(image_pil)
    seatbelt = predict_seatbelt(image_pil)
    smoking = predict_smoking(image_pil)   # ✅ NEW

    return {
        "drowsiness": drowsiness,

        "emotion": emotion["emotion"],
        "emotion_confidence": emotion["confidence"],

        "seatbelt_status": seatbelt["label"],
        "seatbelt_confidence": seatbelt["confidence"],

        "smoking_status": smoking["smoking_status"],         
        "smoking_confidence": smoking["confidence"] 
    }
