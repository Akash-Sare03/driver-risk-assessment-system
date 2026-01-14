import cv2
import numpy as np
from PIL import Image
import io

from models.drowsiness.ear_detector import detect_drowsiness
from models.emotion.emotion_utils import predict_emotion
from models.seatbelt.seatbelt_utils import predict_seatbelt
from models.smoking.smoking_predictor import predict_smoking


def analyze_driver_image(image_bytes):
    # ---- OpenCV image (drowsiness) ----
    np_array = np.frombuffer(image_bytes, np.uint8)
    image_cv = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if image_cv is None:
        return {"error": "Invalid image"}

    # ---- PIL image (DL models) ----
    image_pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # ---- Predictions ----
    drowsiness = detect_drowsiness(image_cv)
    emotion = predict_emotion(image_pil)
    seatbelt = predict_seatbelt(image_pil)
    smoking = predict_smoking(image_pil)

    return {
        "drowsiness": drowsiness,

        "emotion": emotion["emotion"],
        "emotion_confidence": emotion["confidence"],

        "seatbelt_status": seatbelt["label"],
        "seatbelt_confidence": seatbelt["confidence"],

        "smoking_status": smoking["smoking_status"],
        "smoking_confidence": smoking["confidence"],
    }
