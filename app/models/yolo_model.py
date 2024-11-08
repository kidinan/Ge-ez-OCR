import torch
import os
import pickle

def load_yolo_model():
    # Load environment variables
    yolo_model_path = os.getenv('YOLO_MODEL_PATH')

    if not yolo_model_path:
        raise ValueError("Environment variable YOLO_MODEL_PATH is not set.")
    if not os.path.isfile(yolo_model_path):
        raise ValueError(f"Model file not found at {yolo_model_path}")
    
    print(f"Loading YOLO model from {yolo_model_path}")

    # Custom unpickler to handle the 'models' module and persistent load
    class CustomUnpickler(pickle.Unpickler):
        def find_class(self, module, name):
            if module == 'models':
                module = 'app.models'
            return super().find_class(module, name)
        
        def persistent_load(self, pid):
            # Implement the function to handle persistent IDs
            raise pickle.UnpicklingError("Persistent ID not supported: {}".format(pid))

    with open(yolo_model_path, 'rb') as f:
        yolo_model = CustomUnpickler(f).load()
    
    return yolo_model
