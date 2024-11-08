import torch
from app.models.ocr_model import load_ocr_model, transform, decode_predictions, idx_to_char

# Load OCR model
ocr_model_path = 'models/ocr_model.pth'
num_classes = len(idx_to_char)  # Number of classes for Geez characters
ocr_model = load_ocr_model(ocr_model_path, num_classes)

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
