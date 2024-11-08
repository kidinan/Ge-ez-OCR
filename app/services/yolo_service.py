import os
import torch
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from fastapi import UploadFile
import urllib.error
import time

# Load environment variables
load_dotenv()
yolo_model_path = os.getenv('YOLO_MODEL_PATH')

def load_yolo_model_with_retries(repo, model, path, retries=3, delay=5):
    for attempt in range(retries):
        try:
            model = torch.hub.load(repo, model, path=path, trust_repo=True)
            return model
        except urllib.error.HTTPError as e:
            if e.code == 403 and 'rate limit exceeded' in str(e):
                print(f'Rate limit exceeded, retrying in {delay} seconds...')
                time.sleep(delay)
            else:
                raise e
    raise Exception('Failed to load model after multiple retries')

# Load YOLO model with retry mechanism
yolo_model = load_yolo_model_with_retries('ultralytics/yolov5', 'custom', path=yolo_model_path)

async def predict(file: UploadFile):
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert('RGB')
    
    # Detect lines using YOLO model
    results = yolo_model(image)
    boxes = results.xyxy[0].cpu().numpy()
    
    return results, boxes, image
