import os
import torch
from dotenv import load_dotenv

def load_yolo_model():
    # Load environment variables
    load_dotenv()
    yolo_model_path = os.getenv('YOLO_MODEL_PATH')

    if not yolo_model_path:
        raise ValueError("Environment variable YOLO_MODEL_PATH is not set.")
    if not os.path.isfile(yolo_model_path):
        raise ValueError(f"Model file not found at {yolo_model_path}")
    
    print(f"Loading YOLO model from {yolo_model_path}")

    # Load YOLO model from local file
    yolo_model = torch.load(yolo_model_path, map_location=torch.device('cpu'))
    return yolo_model
