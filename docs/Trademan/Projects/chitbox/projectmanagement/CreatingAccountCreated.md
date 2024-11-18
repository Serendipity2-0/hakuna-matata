# Detailed Documentation: Creating Account Created Success Dialog

### Introduction

This document provides a comprehensive overview of the process involved in creating an "Account Created" success dialog for the eKYC verification screen in the Chitbox application. It includes the steps taken, the code used, and the challenges faced during the implementation.

### Objective

The main objective was to create a success dialog that appears after the successful verification of PAN and Aadhaar details. The dialog displays a confirmation message and then automatically redirects the user to the Dashboard screen after a short delay.

### Steps to Implementation

### Step 1: Setting Up the Project

First, ensure that the Flutter project is set up and that the necessary dependencies are added to the `pubspec.yaml` file.

```yaml
dependencies:
  flutter:
    sdk: flutter

```

### Step 2: Creating the eKYC Verification Screen

**Code:**

```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class eKYCVerificationScreen extends StatefulWidget {
  @override
  _eKYCVerificationScreenState createState() => _eKYCVerificationScreenState();
}

class _eKYCVerificationScreenState extends State<eKYCVerificationScreen> {
  final _panController = TextEditingController();
  final _aadhaarController = TextEditingController();

  bool isPanValid = false;
  bool isAadhaarValid = false;

  @override
  void initState() {
    super.initState();
    _panController.addListener(_validatePan);
    _aadhaarController.addListener(_validateAadhaar);
  }

  void _validatePan() {
    final panRegex = RegExp(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$');
    setState(() {
      isPanValid = panRegex.hasMatch(_panController.text);
    });
  }

  void _validateAadhaar() {
    final aadhaarRegex = RegExp(r'^\\d{12}$');
    setState(() {
      isAadhaarValid = aadhaarRegex.hasMatch(_aadhaarController.text);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text('Verify PAN and Aadhaar', style: TextStyle(color: Colors.black)),
        centerTitle: true,
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.verified_user, color: Colors.black, size: 30),
                SizedBox(width: 8),
                RichText(
                  text: TextSpan(
                    children: [
                      TextSpan(
                        text: 'Verify ',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.black,
                        ),
                      ),
                      TextSpan(
                        text: 'PAN ',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.blue,
                        ),
                      ),
                      TextSpan(
                        text: 'and ',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.black,
                        ),
                      ),
                      TextSpan(
                        text: 'Aadhaar',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.blue,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            SizedBox(height: 16),
            Text(
              'Kindly provide your PAN',
              style: TextStyle(fontSize: 16, color: Colors.grey[600]),
            ),
            Text(
              'and Aadhaar information for KYC',
              style: TextStyle(fontSize: 16, color: Colors.grey[600]),
            ),
            SizedBox(height: 24),
            TextField(
              controller: _panController,
              decoration: InputDecoration(
                labelText: 'PAN Number',
                suffixIcon: isPanValid ? Icon(Icons.check_circle, color: Colors.green) : null,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15.0),
                ),
              ),
              inputFormatters: [
                FilteringTextInputFormatter.allow(RegExp(r'[A-Z0-9]')),
                LengthLimitingTextInputFormatter(10),
              ],
              textCapitalization: TextCapitalization.characters,
            ),
            SizedBox(height: 16),
            TextField(
              controller: _aadhaarController,
              decoration: InputDecoration(
                labelText: 'Aadhaar Number',
                suffixIcon: isAadhaarValid ? Icon(Icons.check_circle, color: Colors.green) : null,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15.0),
                ),
              ),
              keyboardType: TextInputType.number,
              inputFormatters: [
                FilteringTextInputFormatter.digitsOnly,
                LengthLimitingTextInputFormatter(12),
              ],
            ),
            SizedBox(height: 24),
            Align(
              alignment: Alignment.center,
              child: SizedBox(
                width: 250,
                height: 60,
                child: ElevatedButton(
                  child: Text(
                    'Verify & continue',
                    style: TextStyle(
                      fontFamily: 'Roboto', // Change this to your desired font family
                      fontSize: 18,
                      color: Colors.white, // Change the text color to white
                    ),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.purple,
                    padding: EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30), // Oval corners
                    ),
                  ),
                  onPressed: isPanValid && isAadhaarValid ? () {
                    Navigator.push(context, MaterialPageRoute(builder: (_) => AccountCreatedScreen()));
                  } : null,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _panController.dispose();
    _aadhaarController.dispose();
    super.dispose();
  }
}

```

### Step 3: Creating the Account Created Success Dialog

**Code:**

```dart
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:chitbox_app/features/home/DashboardScreen.dart';

class AccountCreatedScreen extends StatefulWidget {
  const AccountCreatedScreen({super.key});

  @override
  _AccountCreatedScreenState createState() => _AccountCreatedScreenState();
}

class _AccountCreatedScreenState extends State<AccountCreatedScreen> {
  @override
  void initState() {
    super.initState();
    Timer(const Duration(seconds: 15), () {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (context) => DashboardScreen()),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color.fromARGB(255, 68, 63, 63), // Light grey background
      body: Center(
        child: Dialog(
          backgroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
          child: Container(
            padding: const EdgeInsets.all(20),
            height: 400,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  width: 200,
                  height: 200,
                  decoration: const BoxDecoration(
                    image: DecorationImage(
                      image: AssetImage('assets/logos/success_information.png'),
                      fit: BoxFit.cover,
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                const Text(
                  'Your account has been created\\nand KYC verified successfully.',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
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

```

### Step 4: Create the Dashboard Screen

**Code:**

```dart
import 'package:flutter/material.dart';

class DashboardScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dashboard'),
      ),
      body: Center(
        child: Text(
          'Welcome to the Dashboard!',
          style: TextStyle(fontSize: 18),
        ),
      ),
    );
  }
}

```

### Hurdles Faced

1. **Validation Issues**:
    - **Problem**: Ensuring that the validation for PAN and Aadhaar numbers was accurate and that the green tick mark appeared correctly.
    - **Solution**: Implemented regular expressions for validation and updated the state accordingly to display the green tick mark.
2. **UI Alignment and Design**:
    - **Problem**: Aligning the elements correctly within the dialog and ensuring a consistent design across different screen sizes.
    - **Solution**: Used `SizedBox`, `Container`, and `Padding` widgets to achieve proper alignment and consistent design.
3. **Navigation**:
    - **Problem**: Implementing a smooth transition from the success dialog to the Dashboard screen.
    - **Solution**: Utilized the `Navigator.pushReplacement` method to ensure the transition was seamless.
4. **Timer Implementation**:
    - **Problem**: Ensuring the dialog displayed for the correct amount of time before navigating to the

Dashboard.

- **Solution**: Used the `Timer` class from Dart's `async` library to manage the duration.

### Future Integration with API Setu

In future iterations, we plan to integrate the eKYC verification process with API Setu to perform real-time verification of PAN and Aadhaar details. This integration will enhance the security and accuracy of the KYC process.

### Complete Code

Here is the complete code for the implementation:

**eKYC Verification Screen**:

```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class eKYCVerificationScreen extends StatefulWidget {
  @override
  _eKYCVerificationScreenState createState() => _eKYCVerificationScreenState();
}

class _eKYCVerificationScreenState extends State<eKYCVerificationScreen> {
  final _panController = TextEditingController();
  final _aadhaarController = TextEditingController();

  bool isPanValid = false;
  bool isAadhaarValid = false;

  @override
  void initState() {
    super.initState();
    _panController.addListener(_validatePan);
    _aadhaarController.addListener(_validateAadhaar);
  }

  void _validatePan() {
    final panRegex = RegExp(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$');
    setState(() {
      isPanValid = panRegex.hasMatch(_panController.text);
    });
  }

  void _validateAadhaar() {
    final aadhaarRegex = RegExp(r'^\\d{12}$');
    setState(() {
      isAadhaarValid = aadhaarRegex.hasMatch(_aadhaarController.text);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text('Verify PAN and Aadhaar', style: TextStyle(color: Colors.black)),
        centerTitle: true,
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.verified_user, color: Colors.black, size: 30),
                SizedBox(width: 8),
                RichText(
                  text: TextSpan(
                    children: [
                      TextSpan(
                        text: 'Verify ',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.black,
                        ),
                      ),
                      TextSpan(
                        text: 'PAN ',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.blue,
                        ),
                      ),
                      TextSpan(
                        text: 'and ',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.black,
                        ),
                      ),
                      TextSpan(
                        text: 'Aadhaar',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.blue,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            SizedBox(height: 16),
            Text(
              'Kindly provide your PAN',
              style: TextStyle(fontSize: 16, color: Colors.grey[600]),
            ),
            Text(
              'and Aadhaar information for KYC',
              style: TextStyle(fontSize: 16, color: Colors.grey[600]),
            ),
            SizedBox(height: 24),
            TextField(
              controller: _panController,
              decoration: InputDecoration(
                labelText: 'PAN Number',
                suffixIcon: isPanValid ? Icon(Icons.check_circle, color: Colors.green) : null,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15.0),
                ),
              ),
              inputFormatters: [
                FilteringTextInputFormatter.allow(RegExp(r'[A-Z0-9]')),
                LengthLimitingTextInputFormatter(10),
              ],
              textCapitalization: TextCapitalization.characters,
            ),
            SizedBox(height: 16),
            TextField(
              controller: _aadhaarController,
              decoration: InputDecoration(
                labelText: 'Aadhaar Number',
                suffixIcon: isAadhaarValid ? Icon(Icons.check_circle, color: Colors.green) : null,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15.0),
                ),
              ),
              keyboardType: TextInputType.number,
              inputFormatters: [
                FilteringTextInputFormatter.digitsOnly,
                LengthLimitingTextInputFormatter(12),
              ],
            ),
            SizedBox(height: 24),
            Align(
              alignment: Alignment.center,
              child: SizedBox(
                width: 250,
                height: 60,
                child: ElevatedButton(
                  child: Text(
                    'Verify & continue',
                    style: TextStyle(
                      fontFamily: 'Roboto', // Change this to your desired font family
                      fontSize: 18,
                      color: Colors.white, // Change the text color to white
                    ),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.purple,
                    padding: EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30), // Oval corners
                    ),
                  ),
                  onPressed: isPanValid && isAadhaarValid ? () {
                    Navigator.push(context, MaterialPageRoute(builder: (_) => AccountCreatedScreen()));
                  } : null,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _panController.dispose();
    _aadhaarController.dispose();
    super.dispose();
  }
}

```

**Account Created Screen**:

```dart
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:chitbox_app/features/home/DashboardScreen.dart';

class AccountCreatedScreen extends StatefulWidget {
  const AccountCreatedScreen({super.key});

  @override
  _AccountCreatedScreenState createState() => _AccountCreatedScreenState();
}

class _AccountCreatedScreenState extends State<AccountCreatedScreen> {
  @override
  void initState() {
    super.initState();
    Timer(const Duration(seconds: 15), () {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (context) => DashboardScreen()),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color.fromARGB(255, 68, 63, 63), // Light grey background
      body: Center(
        child: Dialog(
          backgroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
          child: Container(
            padding: const EdgeInsets.all(20),
            height: 400,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  width: 200,
                  height: 200,
                  decoration: const BoxDecoration(
                    image: DecorationImage(
                      image: AssetImage('assets/logos/success_information.png'),
                      fit: BoxFit.cover,
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                const Text(
                  'Your account has been created\\nand KYC verified successfully.',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
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

```

**Dashboard Screen**:

```dart
import 'package:flutter/material.dart';

class DashboardScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dashboard'),
      ),
      body: Center(
        child: Text(
          'Welcome to the Dashboard!',
          style: TextStyle(fontSize: 18),
        ),
      ),
    );
  }
}

```

### Conclusion

This documentation provides a step-by-step guide to implementing the eKYC verification screen, success dialog, and navigation to the dashboard. It includes the complete code and explains the challenges faced and how they were resolved. Future integration with API Setu will enhance the security and accuracy of the KYC process.