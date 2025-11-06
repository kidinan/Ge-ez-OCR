import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'RecognizerScreen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ImagePicker imagePicker = ImagePicker();
  bool isFrontCamera = true;
  bool isEnglish = true; // State variable for language
  final List<String> geezFacts = [
    'The Ge\'ez language is an ancient Semitic language.',
    'Ge\'ez script is one of the oldest alphabets still in use.',
    'The Bible was translated into Ge\'ez in the 5th century.',
    'Ge\'ez is the liturgical language of the Ethiopian Orthodox Church.',
    'The Book of Enoch is written in Ge\'ez.',
    'Ge\'ez is also used by Ethiopian Jews ',
    'Ge\'ez is not a modern communication language.',
    'The Ethiopian calendar is written in Ge\'ez.',
    'Ge\'ez used mainly in ancient Axumite Kingdom',
  ];
  final List<String> geezFactsAmharic = [
    'ግዕዝ ቋንቋ ጥንታዊ ሰሜታዊ ቋንቋ ናት።',
    'መጽሃፍ ቅዱስ በ5ኛው ክፍለ ዘመን ወደ ግዕዝ ተተረጎም።',
    'ግዕዝ የኢትዮጵያ ኦርቶዶክስ ተዋህዶ ቤተ ክርስቲያን የቅዱስ ቃላት ቋንቋ ናት።',
    'የግዕዝ ፊደል አቡጊዳ ነው፣ በእሱም እያንዳንዱ ፊደል ቃላት ቁምፊ-እርስዋ ያመለክታል።',
    'መጽሐፈ ሄኖክ በግዕዝ የተትጻፈ ነው።',
    'እንዲሁም በኢትዮጵያዊት አይሁድ ይጠቀሙበታል።',
    'በአሁኑ ዘመን ለመኖርነት የማይጠቅሙ ቋንቋ ነው።',
    'የኢትዮጵያ ቀን መቁጠሪያ በግዕዝ የተጻፈ ነው።',
    'በጥንታዊው የአክሱም መንግሥት ውስጥ እንደግምት ተጠቀሙበት ነበር።',
  ];
  int currentFactIndex = 0;
  late Timer _timer;

  @override
  void initState() {
    super.initState();
    _startTimer();
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  void _startTimer() {
    _timer = Timer.periodic(Duration(seconds: 10), (Timer timer) {
      _showNextFact();
    });
  }

  void _showNextFact() {
    setState(() {
      currentFactIndex = (currentFactIndex + 1) % (isEnglish ? geezFacts.length : geezFactsAmharic.length);
    });
  }

  void _showPreviousFact() {
    setState(() {
      currentFactIndex = (currentFactIndex - 1 + (isEnglish ? geezFacts.length : geezFactsAmharic.length)) % (isEnglish ? geezFacts.length : geezFactsAmharic.length);
    });
  }

  void _toggleLanguage() {
    setState(() {
      isEnglish = !isEnglish;
    });
  }

  void _showPrompt(String title, String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          backgroundColor: Colors.grey,  // Adjust the color as needed
          title: Text(title, style: TextStyle(color: Colors.black)),
          content: Text(message, style: TextStyle(color: Colors.black)),
          actions: <Widget>[
            TextButton(
              child: const Text("OK", style: TextStyle(color: Colors.black)),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    String currentFact = isEnglish ? geezFacts[currentFactIndex] : geezFactsAmharic[currentFactIndex];

    return Container(
      color: Colors.black,
      padding: EdgeInsets.only(top: 27),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          Expanded(
            flex: 1,
            child: Card(
              color: Colors.black,
              margin: const EdgeInsets.all(2), // Thin line between cards
              child: Container(
                width: double.infinity,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    InkWell(
                      onTap: _toggleLanguage,
                      child: Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text(
                          isEnglish ? 'EN' : 'አማ',
                          style: TextStyle(color: Colors.white, fontSize: 15),
                        ),
                      ),
                    ),
                    Spacer(),
                    PopupMenuButton<String>(
                      icon: const Icon(Icons.more_vert, color: Colors.white),
                      onSelected: (value) {
                        if (value == (isEnglish ? 'About Us' : 'ስለ እኛ')) {
                          _showPrompt(
                            isEnglish ? 'About Us' : 'ስለ እኛ',
                            isEnglish
                                ? 'This app is developed by Kidist Dejene. For more information, contact: kidist338@gmail.com'
                                : 'ይህ መተግበሪያ በቅድስት ደጀኔ የተሰራ ነው። ለተጨማሪ መረጃ በዚህ ያግኙን፡ kidist338@gmail.com',
                          );
                        } else if (value == (isEnglish ? 'How to Use' : 'እንዴት እንደሚጠቀሙ')) {
                          _showPrompt(
                            isEnglish ? 'How to Use' : 'እንዴት እንደሚጠቀሙ',
                            isEnglish
                                ? 'Take a picture or choose an image from the gallary.If necessary crop the image.Then press extract button.After the text being displayed copy the texts'
                                : 'ፎቶ አንሳ ወይንም ከ ጋለሪ ምስል ምረጥ። ካስፈለገ ምስሉን ቆራርጥ። ከዛ ቀይር ሚለውን ንካ። ጽሁፉ ከመጣ በኋላ ከፈለክ ኮፒ አድርግ።',
                          );
                        }
                      },
                      itemBuilder: (BuildContext context) {
                        return {(isEnglish ? 'About Us' : 'ስለ እኛ'), (isEnglish ? 'How to Use' : 'እንዴት እንደሚጠቀሙ')}.map((String choice) {
                          return PopupMenuItem<String>(
                            value: choice,
                            child: Text(choice),
                          );
                        }).toList();
                      },
                    ),
                  ],
                ),
              ),
            ),
          ),
          Expanded(
            flex: 2,
            child: Card(
              color: Colors.black,
              margin: const EdgeInsets.symmetric(vertical: 1), // Thin line between cards
              child: Container(
                width: double.infinity,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    InkWell(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(
                            Icons.camera_rounded,
                            size: 70,
                            color: Colors.blueAccent,
                          ),
                          Text(
                            isEnglish ? 'Take Picture' : 'ፎቶ አንሳ',
                            style: const TextStyle(color: Colors.white),
                          ),
                        ],
                      ),
                      onTap: () async {
                        XFile? xfile = await imagePicker.pickImage(
                          source: ImageSource.camera,
                          preferredCameraDevice: isFrontCamera
                              ? CameraDevice.front
                              : CameraDevice.rear,
                        );
                        if (xfile != null) {
                          File image = File(xfile.path);
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (ctx) {
                              return RecognizerScreen(image, isEnglish);
                            }),
                          );
                        }
                      },
                    ),
                    const SizedBox(height: 20),
                    InkWell(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(
                            Icons.image_rounded,
                            size: 70,
                            color: Colors.green,
                          ),
                          Text(
                            isEnglish ? 'Pick from Gallery' : 'ከጋለሪ ይምረጡ',
                            style: const TextStyle(color: Colors.white),
                          ),
                        ],
                      ),
                      onTap: () async {
                        XFile? xfile = await imagePicker.pickImage(
                          source: ImageSource.gallery,
                        );
                        if (xfile != null) {
                          File image = File(xfile.path);
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (ctx) {
                              return RecognizerScreen(image, isEnglish);
                            }),
                          );
                        }
                      },
                    ),
                  ],
                ),
              ),
            ),
          ),
          Expanded(
            flex: 3,
            child: Card(
              color: Colors.black,
              margin: const EdgeInsets.symmetric(vertical: 1), // Thin line between cards
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    Text(
                      isEnglish ? 'Facts' : 'እውነታዎች',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 25,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 20),
                    Text(
                      currentFact,
                      style: const TextStyle(color: Colors.white, fontSize: 25),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 80),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        IconButton(
                          icon: const Icon(Icons.arrow_left, color: Colors.red),
                          onPressed: _showPreviousFact,
                        ),
                        IconButton(
                          icon: const Icon(Icons.arrow_right, color: Colors.red),
                          onPressed: _showNextFact,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

