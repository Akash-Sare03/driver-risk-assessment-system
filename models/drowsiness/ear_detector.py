import cv2
import mediapipe as mp
import numpy as np
import os

# MediaPipe Tasks imports
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Eye landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "face_landmarker.task"
)

def calculate_ear(eye_points, landmarks, image_shape):
    h, w = image_shape[:2]
    coords = []

    for point in eye_points:
        x = landmarks[point].x * w
        y = landmarks[point].y * h
        coords.append((x, y))

    A = np.linalg.norm(np.array(coords[1]) - np.array(coords[5]))
    B = np.linalg.norm(np.array(coords[2]) - np.array(coords[4]))
    C = np.linalg.norm(np.array(coords[0]) - np.array(coords[3]))

    return (A + B) / (2.0 * C)

def detect_drowsiness(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=VisionRunningMode.IMAGE,
        num_faces=1
    )

    with FaceLandmarker.create_from_options(options) as landmarker:
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_image
        )

        result = landmarker.detect(mp_image)

        if not result.face_landmarks:
            return "No Face Detected"

        landmarks = result.face_landmarks[0]

        left_ear = calculate_ear(LEFT_EYE, landmarks, image.shape)
        right_ear = calculate_ear(RIGHT_EYE, landmarks, image.shape)

        avg_ear = (left_ear + right_ear) / 2

        print(f"Left EAR: {left_ear:.3f}, Right EAR: {right_ear:.3f}, Avg EAR: {avg_ear:.3f}")

        if avg_ear < 0.25:
            return "DROWSY"
        elif avg_ear < 0.29:
            return "POSSIBLY DROWSY"
        else:
            return "ALERT"

import cv2
import mediapipe as mp
import numpy as np
import os

# MediaPipe Tasks imports
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Eye landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "face_landmarker.task"
)

def calculate_ear(eye_points, landmarks, image_shape):
    h, w = image_shape[:2]
    coords = []

    for point in eye_points:
        x = landmarks[point].x * w
        y = landmarks[point].y * h
        coords.append((x, y))

    A = np.linalg.norm(np.array(coords[1]) - np.array(coords[5]))
    B = np.linalg.norm(np.array(coords[2]) - np.array(coords[4]))
    C = np.linalg.norm(np.array(coords[0]) - np.array(coords[3]))

    return (A + B) / (2.0 * C)

def detect_drowsiness(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=VisionRunningMode.IMAGE,
        num_faces=1
    )

    with FaceLandmarker.create_from_options(options) as landmarker:
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_image
        )

        result = landmarker.detect(mp_image)

        if not result.face_landmarks:
            return "No Face Detected"

        landmarks = result.face_landmarks[0]

        left_ear = calculate_ear(LEFT_EYE, landmarks, image.shape)
        right_ear = calculate_ear(RIGHT_EYE, landmarks, image.shape)

        avg_ear = (left_ear + right_ear) / 2

        print(f"Left EAR: {left_ear:.3f}, Right EAR: {right_ear:.3f}, Avg EAR: {avg_ear:.3f}")

        if avg_ear < 0.25:
            return "DROWSY"
        elif avg_ear < 0.29:
            return "POSSIBLY DROWSY"
        else:
            return "ALERT"

