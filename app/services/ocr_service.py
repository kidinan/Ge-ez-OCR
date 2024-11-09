import torch
from PIL import Image
from io import BytesIO
from fastapi import UploadFile
import torchvision.transforms as transforms
from app.models.ocr_model import load_ocr_model, decode_predictions, idx_to_char,char_to_idx

# Load OCR model
ocr_model = load_ocr_model('OCR_MODEL_PATH', num_classes=len(char_to_idx))

transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((32, 128)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

async def predict(file: UploadFile):
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert('RGB')
    
    # Preprocess image and make predictions
    image_tensor = transform(image).unsqueeze(0)
    preds = ocr_model(image_tensor)
    pred_texts = decode_predictions(preds, idx_to_char)
    
    return pred_texts[0]
