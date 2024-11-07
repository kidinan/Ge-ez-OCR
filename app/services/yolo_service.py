import os
import torch
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
yolo_model_path = os.getenv('YOLO_MODEL_PATH')

# Load YOLO model
yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path=yolo_model_path)

async def predict(file: UploadFile):
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert('RGB')
    
    # Detect lines using YOLO model
    results = yolo_model(image)
    boxes = results.xyxy[0].cpu().numpy()
    
    return results, boxes, image
