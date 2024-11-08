import os
import torch
from dotenv import load_dotenv

def load_yolo_model():
    # Load environment variables
    load_dotenv()
    yolo_model_path = os.getenv('YOLO_MODEL_PATH')

    # Load YOLO model from local file
    yolo_model = torch.load(yolo_model_path, map_location=torch.device('cpu'))
    return yolo_model
