import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';

import 'package:eyeagent/models/profile.dart';
import 'package:eyeagent/utils/constants.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:uuid/uuid.dart';

import 'package:camera/camera.dart';

/// Page to chat with someone.
///
/// Displays chat bubbles as a ListView and TextField to enter new chat.
class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  static Route<void> route() {
    return MaterialPageRoute(
      builder: (context) => const HomePage(),
    );
  }

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late CameraDescription firstCamera; // Declare firstCamera variable

  @override
  void initState() {
    final myUserId = supabase.auth.currentUser!.id;
    super.initState();
    getCamera();
  }

  Future<void> getCamera() async {
    final cameras = await availableCameras();

    setState(() {
      firstCamera = cameras.first;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: const Text('Home')),
        body: FutureBuilder<void>(
          future: getCamera(),
          builder: (context, snapshot) {
            if (firstCamera == null) {
              return Center(
                child: CircularProgressIndicator(),
              );
            } else {
              // Access firstCamera here
              return Container(
                child: TakePictureScreen(
                    // Pass the appropriate camera to the TakePictureScreen widget.
                    camera: firstCamera,
                    supabase: supabase),
              );
            }
          },
        ));
  }
}

class TakePictureScreen extends StatefulWidget {
  const TakePictureScreen({
    super.key,
    required this.camera,
    required this.supabase,
  });

  final CameraDescription camera;
  final SupabaseClient supabase;

  @override
  TakePictureScreenState createState() => TakePictureScreenState();
}

class TakePictureScreenState extends State<TakePictureScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;

  @override
  void initState() {
    super.initState();
    // To display the current output from the Camera,
    // create a CameraController.
    _controller = CameraController(
      // Get a specific camera from the list of available cameras.
      widget.camera,
      // Define the resolution to use.
      ResolutionPreset.medium,
    );

    // Next, initialize the controller. This returns a Future.
    _initializeControllerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    // Dispose of the controller when the widget is disposed.
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Take a picture')),
      // You must wait until the controller is initialized before displaying the
      // camera preview. Use a FutureBuilder to display a loading spinner until the
      // controller has finished initializing.
      body: FutureBuilder<void>(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            // If the Future is complete, display the preview.
            return CameraPreview(_controller);
          } else {
            // Otherwise, display a loading indicator.
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
      floatingActionButton: FloatingActionButton(
        // Provide an onPressed callback.
        onPressed: () async {
          // Take the Picture in a try / catch block. If anything goes wrong,
          // catch the error.
          try {
            // Ensure that the camera is initialized.
            await _initializeControllerFuture;

            // Attempt to take a picture and get the file `image`
            // where it was saved.
            final image = await _controller.takePicture();

            if (!mounted) return;

            // If the picture was taken, display it on a new screen.
            await Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => DisplayPictureScreen(
                  // Pass the automatically generated path to
                  // the DisplayPictureScreen widget.
                  imagePath: image.path,
                ),
              ),
            );
          } catch (e) {
            // If an error occurs, log the error to the console.
            print(e);
          }
        },
        child: const Icon(Icons.camera_alt),
      ),
    );
  }
}

class DisplayPictureScreen extends StatefulWidget {
  final String imagePath;

  const DisplayPictureScreen({Key? key, required this.imagePath})
      : super(key: key);

  @override
  _DisplayPictureScreenState createState() => _DisplayPictureScreenState();
}

// A widget that displays the picture taken by the user.
class _DisplayPictureScreenState extends State<DisplayPictureScreen> {
  final StreamController<String> _streamController =
      StreamController<String>(); // Stream controller

  @override
  void dispose() {
    _streamController
        .close(); // Close the stream controller when disposing the widget
    super.dispose();
  }

  void handleInserts(PostgresChangePayload event) {
    print(event);
    _streamController.add(event.newRecord['results'].toString());
  }

  Future<void> uploadImage() async {
    final myUserId = supabase.auth.currentUser!.id;

    var uuid = Uuid();
    var uniqueFileName =
        uuid.v4() + '.jpg'; // Generates a version 4 (random) UUID

    // Replace 'http://localhost:your_port/upload' with your server URL
    var url = Uri.parse('http://10.0.2.2:5000/storeImage');

    // Create a multipart request
    var request = http.MultipartRequest('POST', url);

    // Attach the image file to the request
    var file = File(widget
        .imagePath); // Replace 'path_to_your_image' with the actual path of the image file
    var stream = http.ByteStream(file.openRead());
    var length = await file.length();
    var multipartFile = http.MultipartFile('file', stream, length,
        filename:
            uniqueFileName); // Change 'example.jpg' to the desired filename

    request.files.add(multipartFile);
    request.fields['uuid'] = myUserId;

    // Send the request
    var response = await request.send();

    // Check the response status
    if (response.statusCode == 200) {
      print('Image uploaded successfully');
      var responseData = await response.stream.bytesToString();
      var jsonData = json.decode(responseData);
      var id = jsonData['id'];

      supabase
          .channel('Images')
          .onPostgresChanges(
              event: PostgresChangeEvent.update,
              schema: 'public',
              table: 'Images',
              filter: PostgresChangeFilter(
                type: PostgresChangeFilterType.eq,
                column: 'id',
                value: id,
              ),
              callback: handleInserts)
          .subscribe();
    } else {
      print('Failed to upload image');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Display the Picture')),
      // The image is stored as a file on the device. Use the `Image.file`
      // constructor with the given path to display the image.
      body: Column(
        children: [
          Container(child: Image.file(File(widget.imagePath))),
          ElevatedButton(
            onPressed: () {
              uploadImage();
            },
            child: const Text('Upload'),
          ),
          Expanded(
            child: StreamBuilder<String>(
              stream: _streamController.stream,
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  // Parse the JSON string
                  Map<String, dynamic> data = jsonDecode(snapshot.data!);

                  // Create a list to store UI elements
                  List<Widget> widgets = [];

                  // Loop through the JSON data and create UI elements
                  data.forEach((key, value) {
                    widgets.add(
                      ListTile(
                        title: Text(key),
                        subtitle: Text(value.toString()),
                        // Customize the ListTile UI according to your needs
                      ),
                    );
                  });
                  return ListView(
                    children: widgets,
                  );
                } else {
                  return CircularProgressIndicator();
                }
              },
            ),
          ),
        ],
      ),
    );
  }
}
