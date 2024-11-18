# Documentation for  Implementation for  Personal Details Screen

**Documentation for Personal Details Form with Date Picker**

## Overview

This document provides a detailed explanation of implementing a Personal Details Form in a Flutter application. The form includes fields for name, date of birth (DOB), email ID, OTP, and address for communication. The DOB field opens a date picker from the bottom of the screen.

## Prerequisites

- Flutter SDK installed
- Basic understanding of Flutter and Dart programming language

## Dependencies

### Packages Required

1. **intl**: Used for formatting dates.
2. **cupertino_icons**: Contains the Cupertino icons used in iOS apps.

### Adding Dependencies

Update your `pubspec.yaml` file to include the necessary dependencies:

```yaml
name: personal_details_app
description: A new Flutter project.

publish_to: 'none' # Remove this line if you wish to publish to pub.dev

version: 1.0.0+1

environment:
  sdk: ">=2.12.0 <3.0.0"

dependencies:
  flutter:
    sdk: flutter
  intl: ^0.17.0
  cupertino_icons: ^1.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter

flutter:
  uses-material-design: true

  assets:
    - assets/logos/account_icon.png

```

After updating `pubspec.yaml`, run the following command to get the packages:

```
flutter pub get

```

## Project Structure

Ensure you have the following folder structure for your assets:

```
chitbox_app/
|-- assets/
|   |-- logos/
|       |-- account_icon.png
|-- lib/features/auth/pages
|   |-- Personal_Details.dart
|-- pubspec.yaml

```

## Main Code Implementation

Create a `main.dart` file under the `lib` directory with the following content:

```dart
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:flutter/cupertino.dart';

class PersonalDetailsScreen extends StatefulWidget {
  @override
  _PersonalDetailsScreenState createState() => _PersonalDetailsScreenState();
}

class _PersonalDetailsScreenState extends State<PersonalDetailsScreen> {
  TextEditingController dobController = TextEditingController();
  DateTime selectedDate = DateTime.now();

  Future<void> _selectDate(BuildContext context) async {
    showModalBottomSheet(
      context: context,
      builder: (BuildContext builder) {
        return Container(
          height: MediaQuery.of(context).size.height / 3,
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Text('Date Picker', style: TextStyle(fontSize: 18)),
                  ),
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: TextButton(
                      onPressed: () {
                        Navigator.pop(context);
                      },
                      child: Text(
                        DateFormat('MMM dd, yyyy').format(selectedDate),
                        style: TextStyle(color: Color(0xFF8551ED), fontSize: 18),
                      ),
                    ),
                  ),
                ],
              ),
              Divider(height: 1),
              Expanded(
                child: CupertinoDatePicker(
                  initialDateTime: selectedDate,
                  onDateTimeChanged: (DateTime newDate) {
                    setState(() {
                      selectedDate = newDate;
                      dobController.text = DateFormat('dd MMMM, yyyy').format(selectedDate);
                    });
                  },
                  maximumDate: DateTime.now(),
                  mode: CupertinoDatePickerMode.date,
                ),
              ),
              ElevatedButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                child: Text('Done'),
                style: ElevatedButton.styleFrom(
                  primary: Color(0xFF8551ED), // Button color
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () {},
        ),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Image.asset(
                  'assets/logos/account_icon.png',
                  width: 24,
                  height: 24,
                ),
                SizedBox(width: 8),
                RichText(
                  text: TextSpan(
                    children: [
                      TextSpan(
                        text: 'Personal ',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF8551ED),
                        ),
                      ),
                      TextSpan(
                        text: 'Details',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.black,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            SizedBox(height: 8),
            Text(
              'Please provide your personal details to continue.',
              style: TextStyle(color: Colors.grey),
            ),
            SizedBox(height: 24),
            TextFormField(
              decoration: InputDecoration(
                labelText: 'Name as per Aadhar card',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15),
                ),
                contentPadding: EdgeInsets.symmetric(vertical: 20, horizontal: 12),
              ),
              style: TextStyle(fontSize: 16, height: 1.5),
            ),
            SizedBox(height: 16),
            TextFormField(
              controller: dobController,
              readOnly: true,
              onTap: () => _selectDate(context),
              decoration: InputDecoration(
                labelText: 'DOB',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15),
                ),
                suffixIcon: Icon(Icons.calendar_today),
                contentPadding: EdgeInsets.symmetric(vertical: 20, horizontal: 12),
              ),
              style: TextStyle(fontSize: 16, height: 1.5),
            ),
            SizedBox(height: 16),
            TextFormField(
              decoration: InputDecoration(
                labelText: 'Email ID',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15),
                ),
                suffixIcon: Icon(Icons.send, color: Color(0xFF8551ED)),
                contentPadding: EdgeInsets.symmetric(vertical: 20, horizontal: 12),
              ),
              style: TextStyle(fontSize: 16, height: 1.5),
            ),
            SizedBox(height: 16),
            TextFormField(
              decoration: InputDecoration(
                labelText: 'Enter OTP',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15),
                ),
                suffixIcon: Icon(Icons.check_circle, color: Colors.green),
                contentPadding: EdgeInsets.symmetric(vertical: 20, horizontal: 12),
              ),
              style: TextStyle(fontSize: 16, height: 1.5),
            ),
            SizedBox(height: 16),
            TextFormField(
              maxLines: 3,
              decoration: InputDecoration(
                labelText: 'Address for communication',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15),
                ),
                contentPadding: EdgeInsets.symmetric(vertical: 20, horizontal: 12),
              ),
              style: TextStyle(fontSize: 16, height: 1.5),
            ),
            SizedBox(height: 24),
            Align(
              alignment: Alignment.center,
              child: Container(
                width: 200, // Adjust the width as needed
                height: 50,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(15),
                  gradient: LinearGradient(
                    colors: [Color(0xFF8551ED), Color(0xFF8E2DE2)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                ),
                child: ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.transparent,
                    shadowColor: Colors.transparent,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(15),
                    ),
                    padding: EdgeInsets.symmetric(horizontal: 20, vertical: 15),
                  ),
                  child: Text(
                    'Proceed',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

void main() {
  runApp(MaterialApp(
    home: PersonalDetailsScreen(),
  ));
}

```

## Detailed Explanation

### 1. App Structure

The app consists of a single screen that contains a form for collecting personal details. The form includes fields for name, date of birth, email ID, OTP, and address.

### 2. Initializing State

The state for the `PersonalDetailsScreen` is initialized with a `TextEditingController` for the DOB field and a `DateTime` object to store the selected date.

### 3. Date Picker

The `_selectDate` method shows a modal bottom sheet containing a `CupertinoDatePicker`. When the user selects a date, it updates the `selectedDate` and `dobController` fields.

### 4. User Interface

The user interface consists of a `SingleChildScrollView` that contains a `Column` with several `TextFormField` widgets for input. Each input field has customized styling, including border radius and padding to match

the desired appearance.

### 5. Submit Button

The form includes a "Proceed" button that is styled with a gradient background and rounded corners. When the button is pressed, it doesn't perform any action as the `onPressed` callback is currently empty.

## Conclusion

This documentation provides a comprehensive overview of how to implement a personal details form in a Flutter application, including setting up the project, adding dependencies, and writing the main implementation code. By following these instructions, you can create a similar form with a bottom sheet date picker in your Flutter app.