import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image

from .seatbelt_model import load_seatbelt_model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

CLASS_NAMES = ["no_seatbelt", "seatbelt"]

# Load model ONCE
model = load_seatbelt_model()
model.load_state_dict(
    torch.load("models/seatbelt/seatbelt_mobilenet.pth", map_location=device)
)
model.to(device)
model.eval()

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def predict_seatbelt(image_pil: Image.Image):
    image = transform(image_pil).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        probs = F.softmax(outputs, dim=1)
        confidence, pred = torch.max(probs, 1)

    return {
        "label": CLASS_NAMES[pred.item()],
        "confidence": round(confidence.item(), 3)
    }
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image

from .seatbelt_model import load_seatbelt_model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

CLASS_NAMES = ["no_seatbelt", "seatbelt"]

# Load model ONCE
model = load_seatbelt_model()
model.load_state_dict(
    torch.load("models/seatbelt/seatbelt_mobilenet.pth", map_location=device)
)
model.to(device)
model.eval()

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def predict_seatbelt(image_pil: Image.Image):
    image = transform(image_pil).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        probs = F.softmax(outputs, dim=1)
        confidence, pred = torch.max(probs, 1)

    return {
        "label": CLASS_NAMES[pred.item()],
        "confidence": round(confidence.item(), 3)
    }
