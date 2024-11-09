import torch
import os

def load_yolo_model():
    # Load environment variables
    yolo_model_path = os.getenv('YOLO_MODEL_PATH')

    if not yolo_model_path:
        raise ValueError("Environment variable YOLO_MODEL_PATH is not set.")
    if not os.path.isfile(yolo_model_path):
        raise ValueError(f"Model file not found at {yolo_model_path}")
    
    print(f"Loading YOLO model from {yolo_model_path}")

    # Load YOLO model
    yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path=yolo_model_path)
    
    return yolo_model
