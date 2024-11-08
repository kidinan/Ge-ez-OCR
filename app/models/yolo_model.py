import torch
import os
from app.models.yolo import YOLOModel  # Adjust this import to match your model location

def load_yolo_model():
    # Load environment variables
    yolo_model_path = os.getenv('YOLO_MODEL_PATH')

    if not yolo_model_path:
        raise ValueError("Environment variable YOLO_MODEL_PATH is not set.")
    if not os.path.isfile(yolo_model_path):
        raise ValueError(f"Model file not found at {yolo_model_path}")
    
    print(f"Loading YOLO model from {yolo_model_path}")

    # Initialize model
    model = YOLOModel()
    # Load model state_dict
    model.load_state_dict(torch.load(yolo_model_path, map_location=torch.device('cpu')))
    
    return model
