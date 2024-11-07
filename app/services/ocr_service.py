import os
import torch
import torchvision.transforms as transforms
from dotenv import load_dotenv
from app.models.ocr_model import OCRModel

# Load environment variables
load_dotenv()
ocr_model_path = os.getenv('OCR_MODEL_PATH')

# Initialize OCR model
ocr_model = OCRModel(num_classes=your_num_classes)
ocr_model.load_state_dict(torch.load(ocr_model_path, map_location=torch.device('cpu')))
ocr_model.eval()

# Define transforms
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((32, 128)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# Decode predictions
def decode_predictions(preds, idx_to_char):
    preds = preds.argmax(2)
    pred_strings = []
    for pred in preds:
        pred_string = ''.join([idx_to_char[idx.item()] for idx in pred if idx.item() != 0])
        pred_strings.append(pred_string)
    return pred_strings

async def recognize_text(results, boxes, image, idx_to_char):
    lines = [image.crop((int(box[0]), int(box[1]), int(box[2]), int(box[3]))) for box in boxes]
    texts = []
    positions = []
    with torch.no_grad():
        for box, line_image in zip(boxes, lines):
            line_image_tensor = transform(line_image).unsqueeze(0)
            preds = ocr_model(line_image_tensor)
            pred_texts = decode_predictions(preds, idx_to_char)
            texts.append(pred_texts[0])
            positions.append(f"{int(box[0])},{int(box[1])},{int(box[2])},{int(box[3])}")

    response_text = '\n'.join([f"{text}|{position}" for text, position in zip(texts, positions)])
    return response_text
