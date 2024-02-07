import 'dart:async';
import 'dart:io';

import 'package:camera/camera.dart';
import 'package:camera_windows/camera_windows.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:flutter/material.dart';
import 'package:eyeagent/screens/login_screen.dart';
import 'package:flutter/material.dart';
import 'package:eyeagent/utils/constants.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:eyeagent/screens/splash_page.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Supabase.initialize(
    url: 'https://yerngrprgzhttyniubnk.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inllcm5ncnByZ3podHR5bml1Ym5rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDcxOTIwNzQsImV4cCI6MjAyMjc2ODA3NH0.JMfB2OrYlEpnoInMdS4iUWru1as7j0qfXF18dFz2BvY',
  );
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'My Chat App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const SplashPage(),
    );
  }
}

  //   /// Web Client ID that you registered with Google Cloud.
  // const webClientId = '705656740849-egjh6eaotpmd57q0m75c9ccq6ujm8j5d.apps.googleusercontent.com';

  //   /// TODO: update the iOS client ID with your own.
  //   ///
  //   /// iOS Client ID that you registered with Google Cloud.
  // const iosClientId = '705656740849-fnvoufc1evrd7amuejct0usckl80fir2.apps.googleusercontent.com';

// void main() async {
//   /// TODO: update Supabase credentials with your own
//   await Supabase.initialize(
//     url: 'https://yerngrprgzhttyniubnk.supabase.co',
//     anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inllcm5ncnByZ3podHR5bml1Ym5rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDcxOTIwNzQsImV4cCI6MjAyMjc2ODA3NH0.JMfB2OrYlEpnoInMdS4iUWru1as7j0qfXF18dFz2BvY',
//   );
//   runApp(const MyApp());
// }

// final supabase = Supabase.instance.client;

// class MyApp extends StatelessWidget {
//   const MyApp({super.key});

//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       debugShowCheckedModeBanner: false,
//       title: 'Flutter Auth',
//       theme: ThemeData(
//         colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
//         useMaterial3: true,
//       ),
//       home: const LoginScreen(),
//     );
//   }
// }

  //   TakePictureScreen(
    //       // Pass the appropriate camera to the TakePictureScreen widget.
    //       camera: firstCamera,
    //       supabase: supabase),
    // ),


// A screen that allows users to take a picture using a given camera.
