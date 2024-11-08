import torch
from PIL import Image
from io import BytesIO
from fastapi import UploadFile
from app.models.yolo_model import load_yolo_model

# Load YOLO model
yolo_model = load_yolo_model()

async def predict(file: UploadFile):
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert('RGB')
    
    # Detect lines using YOLO model
    results = yolo_model(image)
    boxes = results.xyxy[0].cpu().numpy()
    
    return results, boxes, image
