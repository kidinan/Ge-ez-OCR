import torch
import gdown
import os
from app.models.yolov5.models.common import DetectMultiBackend
from app.models.yolov5.utils import TryExcept  # Ensure correct import

def load_yolo_model(weights_path):
    if not os.path.exists(weights_path):
        # Google Drive file ID
        file_id = '1r8CErVpjZdX58y1FzpV4admydQE4Th9a'
        # Create the download URL
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, weights_path, quiet=False)
    
    # Load the YOLOv5 model directly using DetectMultiBackend
    model = DetectMultiBackend(weights_path, device='cpu')
    return model

def detect_lines(yolo_model, image):
    results = yolo_model(image)
    return results.xyxy[0].cpu().numpy()
