import torch
from torchvision import transforms
from PIL import Image
from .emotion_model import EmotionCNN

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Label map
EMOTION_LABELS = {
    0: "Angry",
    1: "Fear",
    2: "Happy",
    3: "Neutral",
    4: "Sad"
}

# Load model
model = EmotionCNN(num_classes=5).to(device)
model.load_state_dict(
    torch.load("models/emotion/emotion_cnn.pth", map_location=device)
)
model.eval()

# Transform (MUST match training)
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((48, 48)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])

def predict_emotion(image: Image.Image):
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        probs = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probs, 1)

    return {
        "emotion": EMOTION_LABELS[predicted.item()],
        "confidence": round(confidence.item(), 3)
    }
