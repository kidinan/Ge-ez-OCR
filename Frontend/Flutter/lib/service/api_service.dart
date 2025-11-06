import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl;

  ApiService({required this.baseUrl});

  Future<String> detectAndRecognizeText(File image) async {
    var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/predict'));
    request.files.add(await http.MultipartFile.fromPath('file', image.path));
    var response = await request.send();

    if (response.statusCode == 200) {
      var responseData = await http.Response.fromStream(response);
      return responseData.body; // Return the plain text response
    } else {
      throw Exception('Failed to load text');
    }
  }
}
