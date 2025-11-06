# Ge'ez OCR

Welcome to Ge'ez OCR! This project provides a FastAPI-based backend for a text recognition application that uses YOLOv5 for line detection and an OCR model for recognizing text in images. The API is secure and can only be accessed through an API key.

## Features

- **Line Detection**: Utilizes YOLOv5 to detect lines in images.
- **Text Recognition**: Uses a fine-tuned OCR model to recognize text in detected lines.
- **API Key Authentication**: Ensures that only authorized users can access the API.

## Project Structure

Ge-ez-OCR/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   └── predict.py
│   ├── models/
│   │   ├── ocr_model.py
│   │   └── yolo_model.py
│   ├── services/
│   │   ├── yolo_service.py
│   │   └── ocr_service.py
│   ├── utils/
│   │   ├── logging.py
│   │   └── auth.py
├── models/
│   ├── yolo_model.pt
│   └── ocr_model.pth
├── .gitignore
├── requirements.txt
├── README.md
└── Dockerfile
