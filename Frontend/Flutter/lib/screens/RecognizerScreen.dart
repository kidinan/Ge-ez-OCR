import 'dart:ui' as ui;
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:image_cropper/image_cropper.dart';
import '../service/api_service.dart'; // Import the API service

class RecognizerScreen extends StatefulWidget {
  final File image;
  final bool isEnglish;
  RecognizerScreen(this.image, this.isEnglish);
  @override
  _RecognizerScreenState createState() => _RecognizerScreenState();
}

class _RecognizerScreenState extends State<RecognizerScreen> with TickerProviderStateMixin {
  late File _image;
  ui.Image? uiImage;
  List<String> detectedTexts = [];
  List<Rect> textPositions = [];
  bool showExtractedText = false;
  bool isLoading = false;
  late AnimationController _controller;

  final ApiService apiService = ApiService(baseUrl: 'http://192.168.9.166:8000');

  @override
  void initState() {
    super.initState();
    _image = widget.image;
    detectedTexts = [];
    textPositions = [];
    _loadImage(_image).then((image) {
      setState(() {
        uiImage = image;
      });
    });

    _controller = AnimationController(
      duration: const Duration(seconds: 1),
      vsync: this,
    )..repeat(reverse: true);
  }

  Future<ui.Image> _loadImage(File file) async {
    final data = await file.readAsBytes();
    return decodeImageFromList(data);
  }

  Future<void> _cropImage() async {
    CroppedFile? croppedFile = await ImageCropper().cropImage(
      sourcePath: _image.path,
      uiSettings: [
        AndroidUiSettings(
          toolbarTitle: widget.isEnglish ? 'Crop Image' : 'ምስልን ቆራርጥ',
          toolbarColor: Colors.black,
          toolbarWidgetColor: Colors.white,
          initAspectRatio: CropAspectRatioPreset.original,
          lockAspectRatio: false,
        ),
        IOSUiSettings(
          minimumAspectRatio: 1.0,
        ),
      ],
    );
    if (croppedFile != null) {
      setState(() {
        _image = File(croppedFile.path);
        _loadImage(_image).then((image) {
          setState(() {
            uiImage = image;
          });
        });
      });
    }
  }

  Future<void> _detectLinesAndRecognizeText() async {
    if (uiImage == null) {
      return;  // Ensure uiImage is loaded before proceeding
    }
    setState(() {
      isLoading = true;
    });
    try {
      print("Sending request to API with image: ${_image.path}");
      String response = await apiService.detectAndRecognizeText(_image);
      print("API response received: $response");

      List<String> lines = response.split('\n');
      List<String> texts = [];
      List<Rect> positions = [];

      double scaleX = MediaQuery.of(context).size.width / uiImage!.width;
      double scaleY = (MediaQuery.of(context).size.width * uiImage!.height / uiImage!.width) / uiImage!.height;

      for (String line in lines) {
        List<String> parts = line.split('|');
        texts.add(parts[0]);
        List<String> pos = parts[1].split(',');
        positions.add(Rect.fromLTRB(
          double.parse(pos[0]) * scaleX,
          double.parse(pos[1]) * scaleY,
          double.parse(pos[2]) * scaleX,
          double.parse(pos[3]) * scaleY,
        ));
        print("Text: ${parts[0]}, Position: ${positions.last}");
      }

      setState(() {
        detectedTexts = texts;
        textPositions = positions;
        print("detectedTexts and textPositions assigned.");
        showExtractedText = true;
        isLoading = false;  // Stop the loading animation
        _controller.stop();  // Stop the animation controller
      });
    } catch (e) {
      print("Error during detection: $e");
      setState(() {
        detectedTexts = ['Error: $e'];
        showExtractedText = true;
        isLoading = false;
        _controller.stop();  // Stop the animation controller
      });
    }
  }

  void _copyText() {
    if (detectedTexts.isNotEmpty) {
      StringBuffer concatenatedText = StringBuffer();
      for (String text in detectedTexts) {
        concatenatedText.write(text);
        concatenatedText.write('\n');
      }
      Clipboard.setData(ClipboardData(text: concatenatedText.toString().trim()));  // Trim to remove the last newline
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(widget.isEnglish ? 'Text copied to clipboard' : 'ጽሑፉ ኮፒ ተደርጓል'),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(widget.isEnglish ? 'No text to copy' : 'ጽሑፍ የለም'),
        ),
      );
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        title: Text(
          widget.isEnglish ? 'Converter' : 'ቀያሪ',
          style: TextStyle(color: Colors.white),
        ),
        actions: [
          if (!showExtractedText)
            IconButton(
              icon: Icon(Icons.crop, color: Colors.blueAccent),
              onPressed: _cropImage,
            ),
        ],
      ),
      body: Container(
        color: Colors.black,  // Set overall background color to black
        padding: EdgeInsets.all(10),
        child: Center(
          child: uiImage == null
              ? CircularProgressIndicator()  // Show a loading indicator while the image is being loaded
              : Container(
            width: MediaQuery.of(context).size.width,  // Adjust to fit the screen width
            height: MediaQuery.of(context).size.width * (uiImage!.height / uiImage!.width),  // Maintain image aspect ratio
            color: Colors.white,  // Set the background color for text display
            child: Stack(
              children: [
                if (!showExtractedText)
                  Center(child: Image.file(_image, fit: BoxFit.contain)),  // Ensure the image fits within the container
                if (isLoading)
                  Positioned.fill(
                    child: AnimatedBuilder(
                      animation: _controller,
                      builder: (context, child) {
                        return CustomPaint(
                          painter: LinePainter(_controller.value),
                        );
                      },
                    ),
                  ),
                if (showExtractedText)
                  ...textPositions.asMap().entries.map((entry) {
                    int index = entry.key;
                    Rect pos = entry.value;
                    double left = pos.left;
                    double top = pos.top;
                    return Positioned(
                      left: left,
                      top: top,
                      child: GestureDetector(
                        onLongPress: () {
                          Clipboard.setData(ClipboardData(text: detectedTexts[index]));
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text(widget.isEnglish ? 'Text copied to clipboard' : 'ጽሑፉ ኮፒ ተደርጓል'),
                            ),
                          );
                        },
                        child: Container(
                          color: Colors.transparent,
                          child: SelectableText(
                            detectedTexts[index],
                            style: TextStyle(color: Colors.black, fontSize: 8),  // Adjust font size as needed
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                if (!showExtractedText)
                  Positioned(
                    bottom: 10,
                    left: 50,
                    right: 50,
                    child: ElevatedButton(
                      onPressed: () {
                        print("Extract button pressed");
                        _detectLinesAndRecognizeText();
                      },
                      child: Text(widget.isEnglish ? 'Extract' : 'ቀይር'),
                    ),
                  ),
                if (showExtractedText)
                  Positioned(
                    top: 0,
                    right: 0,
                    child: IconButton(
                      icon: Icon(Icons.copy, color: Colors.blueAccent),
                      onPressed: _copyText,
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class LinePainter extends CustomPainter {
  final double animationValue;

  LinePainter(this.animationValue);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.blueAccent
      ..strokeWidth = 4.0;

    // Draw moving lines to indicate processing
    final double y = size.height * animationValue;
    canvas.drawLine(Offset(0, y), Offset(size.width, y), paint);
  }

  @override
  bool shouldRepaint(LinePainter oldDelegate) {
    return true;
  }
}
