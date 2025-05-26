import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';
import 'package:cross_file/cross_file.dart';
import 'package:path/path.dart' as p;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Word to PDF Converter',
      home: WordToPdfConverter(),
    );
  }
}

class WordToPdfConverter extends StatefulWidget {
  @override
  _WordToPdfConverterState createState() => _WordToPdfConverterState();
}

class _WordToPdfConverterState extends State<WordToPdfConverter> {
  File? _wordFile;
  String? _pdfPath;

  Future<void> _pickWordFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(type: FileType.custom, allowedExtensions: ['doc', 'docx']);
    if (result != null && result.files.single.path != null) {
      setState(() {
        _wordFile = File(result.files.single.path!);
      });
    }
  }

  Future<void> _convertToPdf() async {
    if (_wordFile == null) return;

    final uri = Uri.parse('http://10.90.21.218:5000/convert');
    final request = http.MultipartRequest('POST', uri)
      ..files.add(await http.MultipartFile.fromPath('file', _wordFile!.path));

    final response = await request.send();

    if (response.statusCode == 200) {
      final bytes = await response.stream.toBytes();
      final dir = await getExternalStorageDirectory();
      final outputPath = p.join(dir!.path, p.setExtension(p.basename(_wordFile!.path), '.pdf'));
      final pdfFile = File(outputPath);
      await pdfFile.writeAsBytes(bytes);

      setState(() {
        _pdfPath = outputPath;
      });

      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("PDF saved at: $_pdfPath")));
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Conversion failed.")));
    }
  }

  Future<void> _sharePDF() async {
      await Share.shareXFiles([XFile(_pdfPath!)], text: 'Here is your converted PDF!');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Word to PDF Converter')),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _pickWordFile,
              child: Text('Select Word File'),
            ),
            SizedBox(height: 10),
            Text(_wordFile != null ? "Selected: ${p.basename(_wordFile!.path)}" : "No file selected"),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _convertToPdf,
              child: Text('Convert to PDF'),
            ),
            if (_pdfPath != null) ...[
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: _sharePDF,
                child: Text('Share PDF'),
              ),
              SizedBox(height: 10),
              Text("PDF saved at: $_pdfPath", textAlign: TextAlign.center),
            ]
          ],
        ),
      ),
    );
  }
}
