
import torch
import torch.nn as nn
from torchvision import models

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_smoking_model():
    model = models.mobilenet_v2(pretrained=True)

    num_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(num_features, 2)
    )

    model.load_state_dict(
        torch.load("models/smoking/smoking_mobilenetv2.pth", map_location=device)
    )

    model.to(device)
    model.eval()
    return model

import torch
import torch.nn as nn
from torchvision import models

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_smoking_model():
    model = models.mobilenet_v2(pretrained=True)

    num_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(num_features, 2)
    )

    model.load_state_dict(
        torch.load("models/smoking/smoking_mobilenetv2.pth", map_location=device)
    )

    model.to(device)
    model.eval()
    return model
