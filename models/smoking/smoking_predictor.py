
import torch
from torchvision import transforms
from PIL import Image
from .smoking_model import load_smoking_model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = load_smoking_model()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

label_map = {0: "Not Smoking", 1: "Smoking"}

def predict_smoking(image_pil: Image.Image):
    image = transform(image_pil).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        probs = torch.softmax(output, dim=1)
        confidence, pred = torch.max(probs, 1)

    return {
        "smoking_status": label_map[pred.item()],
        "confidence": round(confidence.item(), 3)
    }

import torch
from torchvision import transforms
from PIL import Image
from .smoking_model import load_smoking_model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = load_smoking_model()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

label_map = {0: "Not Smoking", 1: "Smoking"}

def predict_smoking(image_pil: Image.Image):
    image = transform(image_pil).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        probs = torch.softmax(output, dim=1)
        confidence, pred = torch.max(probs, 1)

    return {
        "smoking_status": label_map[pred.item()],
        "confidence": round(confidence.item(), 3)
    }
