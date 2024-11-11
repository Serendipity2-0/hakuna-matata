# Detailed Documentation for login_page.dart and otp_verification.dart

This document provides a detailed implementation guide for creating a Login Page and OTP Verification screen in Flutter.

### Prerequisites

Ensure you have the following tools and dependencies installed:

- Flutter SDK
- Dart
- Visual Studio Code or any other preferred IDE

Add the necessary dependencies to your `pubspec.yaml` file:

```yaml
dependencies:
  flutter:
    sdk: flutter
  country_code_picker: ^2.0.2
  pin_code_fields: ^7.0.1

```

### `login_page.dart`

### 1. Create the `login_page.dart` File

Create a new Dart file named `login_page.dart` in your project directory.

### 2. Import Required Packages

```dart
import 'package:flutter/material.dart';
import 'package:country_code_picker/country_code_picker.dart';
import 'otp_screen.dart'; // Ensure you have this import to navigate to the OTP screen

```

### 3. Define the `LoginPage` Widget

Create a stateful widget for the Login page:

```dart
class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

```

### 4. Define the State Class `_LoginPageState`

In this class, we manage the state of the login page, including user input validation and navigation.

```dart
class _LoginPageState extends State<LoginPage> {
  TextEditingController phoneController = TextEditingController();
  String countryCode = '+91';
  bool isPhoneValid = false;

  void _onPhoneChanged() {
    final phone = phoneController.text;
    setState(() {
      isPhoneValid = countryCode == '+91' && phone.length == 10 && RegExp(r'^[0-9]+$').hasMatch(phone);
    });
  }

  @override
  void initState() {
    super.initState();
    phoneController.addListener(_onPhoneChanged);
  }

  @override
  void dispose() {
    phoneController.removeListener(_onPhoneChanged);
    phoneController.dispose();
    super.dispose();
  }

```

### 5. Build the UI

Use the `build` method to construct the UI of the Login page:

```dart
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(height: 16),
            Text(
              'Welcome !',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            Text(
              'Enter your phone number to get started',
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
            SizedBox(height: 32),
            Container(
              padding: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.grey),
              ),
              child: Row(
                children: [
                  CountryCodePicker(
                    onChanged: (code) {
                      setState(() {
                        countryCode = code.dialCode ?? '+91';
                        _onPhoneChanged();
                      });
                    },
                    initialSelection: 'IN',
                    favorite: ['+91', 'IN'],
                    showCountryOnly: false,
                    showOnlyCountryWhenClosed: false,
                    alignLeft: false,
                  ),
                  Expanded(
                    child: TextField(
                      controller: phoneController,
                      keyboardType: TextInputType.phone,
                      decoration: InputDecoration(
                        hintText: 'Phone number',
                        border: InputBorder.none,
                      ),
                    ),
                  ),
                  if (isPhoneValid)
                    Icon(Icons.check_circle, color: Colors.green),
                ],
              ),
            ),
            Spacer(),
            Center(
              child: Container(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: isPhoneValid ? () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => OTPScreen(phoneNumber: '$countryCode ${phoneController.text}'),
                      ),
                    );
                  } : null,
                  style: ElevatedButton.styleFrom(
                    primary: Color(0xFF8E2DE2),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                  child: Text(
                    'Continue',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                    ),
                  ),
                ),
              ),
            ),
            SizedBox(height: 16),
          ],
        ),
      ),
    );
  }
}

```

### Explanation of the UI Components

1. **AppBar**: Contains a back button to navigate back to the previous screen.
2. **SingleChildScrollView**: Ensures the content is scrollable to avoid overflow errors.
3. **Column**: Contains all the widgets in a vertical layout.
4. **CountryCodePicker**: Allows the user to select their country code.
5. **TextField**: Allows the user to input their phone number.
6. **Icon**: Displays a green check mark when the phone number is valid.
7. **ElevatedButton**: The "Continue" button to navigate to the OTP screen when the phone number is valid.

### Running the Code

To run the code, make sure you have set up your Flutter environment correctly. Use the following command in your terminal:

```bash
flutter run

```

### Asset Configuration

Ensure that the image asset is correctly added to your project, and your `pubspec.yaml` file includes the necessary configuration:

```yaml
flutter:
  assets:
    - assets/images/otp_verification.png

```

### `otp_screen.dart`

### 1. Create the `otp_screen.dart` File

Create a new Dart file named `otp_screen.dart` in your project directory.

### 2. Import Required Packages

```dart
import 'package:flutter/material.dart';
import 'package:pin_code_fields/pin_code_fields.dart';
import 'dart:async'; // Importing for Timer

```

### 3. Define the `OTPScreen` Widget

Create a stateful widget for the OTP screen:

```dart
class OTPScreen extends StatefulWidget {
  final String phoneNumber;

  OTPScreen({required this.phoneNumber});

  @override
  _OTPScreenState createState() => _OTPScreenState();
}

```

### 4. Define the State Class `_OTPScreenState`

In this class, we manage the state of the OTP screen, including the timer and user input.

```dart
class _OTPScreenState extends State<OTPScreen> {
  TextEditingController otpController = TextEditingController();
  late Timer _timer;
  int _start = 35;

  void startTimer() {
    const oneSec = const Duration(seconds: 1);
    _timer = Timer.periodic(
      oneSec,
      (Timer timer) {
        if (_start == 0) {
          setState(() {
            timer.cancel();
          });
        } else {
          setState(() {
            _start--;
          });
        }
      },
    );
  }

  void resetTimer() {
    setState(() {
      _start = 35;
    });
    startTimer();
  }

  @override
  void initState() {
    super.initState();
    startTimer();
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

```

### 5. Build the UI

Use the `build` method to construct the UI of the OTP screen:

```dart
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        elevation: 0,
      ),
      body: SingleChildScrollView( // Added SingleChildScrollView
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Center(
                child: Image.asset(
                  'assets/images/otp_verification.png', // Add your image asset here
                  height: 150,
                ),
              ),
              SizedBox(height: 32),
              Center(
                child: RichText(
                  textAlign: TextAlign.center,
                  text: TextSpan(
                    text: 'OTP ',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF8E2DE2),
                    ),
                    children: <TextSpan>[
                      TextSpan(
                        text: 'Verification',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.black,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              SizedBox(height: 8),
              Center(
                child: Column(
                  children: [
                    Text(
                      'Please enter the verification code',
                      style: TextStyle(fontSize: 16, color: Colors.grey),
                      textAlign: TextAlign.center,
                    ),
                    Text(
                      'sent on ${widget.phone

Number}',
                      style: TextStyle(fontSize: 16, color: Colors.grey),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
              SizedBox(height: 32),
              PinCodeTextField(
                appContext: context,
                length: 4,
                keyboardType: TextInputType.number,
                pinTheme: PinTheme(
                  shape: PinCodeFieldShape.box,
                  borderRadius: BorderRadius.circular(5),
                  fieldHeight: 50,
                  fieldWidth: 40,
                  activeFillColor: Colors.white,
                  selectedFillColor: Colors.white,
                  inactiveFillColor: Colors.white,
                  inactiveColor: Colors.grey,
                  selectedColor: Color(0xFF8E2DE2),
                  activeColor: Colors.grey,
                ),
                controller: otpController,
                onChanged: (value) {},
              ),
              SizedBox(height: 24),
              Center(
                child: Container(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton(
                    onPressed: () {
                      // Handle OTP verification here
                    },
                    style: ElevatedButton.styleFrom(
                      primary: Color(0xFF8E2DE2),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                    ),
                    child: Text(
                      'Continue',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                      ),
                    ),
                  ),
                ),
              ),
              SizedBox(height: 16),
              Center(
                child: GestureDetector(
                  onTap: _start == 0 ? resetTimer : null, // Add gesture detection for resetting the timer
                  child: Text(
                    _start == 0 ? 'Resend OTP' : 'Resend OTP in $_start Seconds',
                    style: TextStyle(fontSize: 16, color: Color(0xFF8E2DE2)),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

```

### Explanation of the UI Components

1. **AppBar**: Contains a back button to navigate back to the previous screen.
2. **SingleChildScrollView**: Ensures the content is scrollable to avoid overflow errors.
3. **Column**: Contains all the widgets in a vertical layout.
4. **Image.asset**: Displays an image for the OTP verification process.
5. **RichText**: Combines different styles for the "OTP Verification" text.
6. **PinCodeTextField**: Custom text field for entering the OTP code.
7. **ElevatedButton**: The "Continue" button to proceed after entering the OTP.
8. **GestureDetector**: Detects taps on the "Resend OTP" text to reset the timer.

### Running the Code

To run the code, make sure you have set up your Flutter environment correctly. Use the following command in your terminal:

```bash
flutter run

```

### Asset Configuration

Ensure that the image asset is correctly added to your project, and your `pubspec.yaml` file includes the necessary configuration:

```yaml
flutter:
  assets:
    - assets/images/otp_verification.png

```

### Testing

Ensure that the timer counts down correctly, the "Resend OTP" functionality works, and the OTP input field accepts input properly.

### Summary

This documentation provides a comprehensive guide to implementing the Login page and OTP verification screen with a timer and resend functionality. Follow the steps carefully to set up your project and ensure all dependencies are correctly added to your `pubspec.yaml` file.