## 📱 Ge'ez OCR Frontend (Flutter App)

This is the mobile application for the Ge'ez OCR system, built using Flutter. It allows users to capture or upload images containing Ge'ez script and receive OCR-translated text via the backend API.

---

### 🚀 Features

- Capture images using the device camera
- Upload images from gallery
- Send images to the backend for OCR processing
- Display translated Ge'ez text
- Clean and responsive UI

---

### 🛠️ Setup Instructions

#### 1. Install Flutter
Make sure Flutter is installed on your system. You can check with:
```bash
flutter --version
```
If not installed, follow the [Flutter installation guide](https://docs.flutter.dev/get-started/install).

#### 2. Install Dependencies
Navigate to the app directory and run:
```bash
flutter pub get
```

#### 3. Run the App
To run on an emulator or connected device:
```bash
flutter run
```

---

### 📦 Folder Structure

```plaintext
Frontend/
└── Flutter/
    ├── lib/                # Main Dart code
    ├── android/            # Android platform config
    ├── ios/                # iOS platform config
    ├── pubspec.yaml        # Dependencies and assets
    └── README.md           # This file
```

---

### 🔗 Backend Integration

The app communicates with the FastAPI backend via HTTP. Make sure the backend is running and accessible. Update the API URL in your Dart code (usually in a config file or service class).

Example:
```dart
const String apiUrl = "http://your-backend-ip:8000/ocr";
```

---

### 📱 Platform Notes

- **Android**: Ensure camera and storage permissions are set in `AndroidManifest.xml`.
- **iOS**: Update `Info.plist` with required permissions for camera and photo access.

---

### 📄 License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.
