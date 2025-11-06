import torch
import torchvision.transforms as transforms
from PIL import Image
from io import BytesIO

def get_image_transform():
    """Defines the image transformations for the OCR model."""
    return transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((32, 128)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

def load_ocr_model(model_path, num_classes, device='cpu'):
    """Loads the OCR model."""
    model = OCRModel(num_classes=num_classes)
    model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
    model.eval()
    return model

def decode_predictions(preds, idx_to_char):
    """Decodes the predictions from the OCR model."""
    preds = preds.argmax(2)  # Get the index of the max log-probability
    pred_strings = []
    for pred in preds:
        pred_string = ''.join([idx_to_char[idx.item()] for idx in pred if idx.item() != 0])
        pred_strings.append(pred_string)
    return pred_strings

def process_ocr(ocr_model, transform, lines, idx_to_char):
    """Processes the OCR predictions."""
    texts = []
    with torch.no_grad():
        for line_image in lines:
            line_image_tensor = transform(line_image).unsqueeze(0)
            preds = ocr_model(line_image_tensor)
            pred_texts = decode_predictions(preds, idx_to_char)
            texts.append(pred_texts[0])
    return texts
