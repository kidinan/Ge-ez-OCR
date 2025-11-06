import 'dart:io';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:geezz/screens/HomeScreen.dart'; // Ensure to replace with your actual imports

void startLocalServer() async {
  final directory = await getApplicationDocumentsDirectory();
  final serverPath = "${directory.path}/app"; // Path to your executable

  if (Platform.isAndroid || Platform.isLinux || Platform.isWindows) {
    Process.start(serverPath, []);
  }
}

void main() {
  runApp(MyApp());
  startLocalServer();
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: HomeScreen(),
    );
  }
}
