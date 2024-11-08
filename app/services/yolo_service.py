import os
import torch
import boto3
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from fastapi import UploadFile

# Load environment variables
load_dotenv()
s3_bucket_name = os.getenv('S3_BUCKET_NAME')
s3_model_path = os.getenv('S3_MODEL_PATH')
local_model_path = '/tmp/yolo_model.pt'  # Temporary path to save the model

def download_model_from_s3():
    s3 = boto3.client('s3')
    s3.download_file(s3_bucket_name, s3_model_path, local_model_path)

# Download YOLO model from S3
download_model_from_s3()
yolo_model = torch.load(local_model_path)

async def predict(file: UploadFile):
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert('RGB')
    
    # Detect lines using YOLO model
    results = yolo_model(image)
    boxes = results.xyxy[0].cpu().numpy()
    
    return results, boxes, image
