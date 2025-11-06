## 📝 Ge'ez OCR — End-to-End Optical Character Recognition System

Ge'ez OCR is a full-stack system for recognizing and translating Ge'ez script from images. It combines a mobile app for image capture, a FastAPI backend for processing, and a two-stage model pipeline using YOLO and PyTorch.

---

### 🧠 Architecture Overview

1. **Line Detection**  
   - Uses **YOLOv5** to detect lines of Ge'ez script in images.
   - Crops each line for character-level processing.

2. **Character Recognition**  
   - Custom **CNN model built with PyTorch**.
   - Outputs text predictions for each cropped line.

3. **Backend API**  
   - Built with **FastAPI**.
   - Accepts image uploads, runs detection + recognition, and returns extracted text.

4. **Mobile App**  
   - Built with **Flutter**.
   - Captures or uploads images and displays OCR results.

---

### 📦 Project Structure

```plaintext
Ge-ez-OCR/
├── Frontend/           # Flutter mobile app
├── Backend/
│   └── Fast-api/       # FastAPI backend server
├── models/             # YOLO + PyTorch model code and checkpoints
├── .gitignore
├── LICENSE
├── README.md           # This file
```

---

### 🚀 Getting Started

#### 1. Clone the Repository
```bash
git clone https://github.com/kidinan/Ge-ez-OCR.git
cd Ge-ez-OCR
```

#### 2. Set Up the Backend
```bash
cd Backend/Fast-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### 3. Run the Mobile App
```bash
cd Frontend/GEEZZ
flutter pub get
flutter run
```

#### 4. Load Models
Ensure your YOLOv5 weights and PyTorch character recognition model are placed in the appropriate folders under `models/`. Update paths in your backend code if needed.

### 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

