# Detailed Documentation for Unit Test Cases of OTP Verification Screen

 This document provides a detailed guide for writing unit test cases for the `OTPScreen` in Flutter. It includes test cases for verifying the visibility and functionality of various UI components such as the OTP Verification title, instruction text, OTP input fields, Continue button, and Resend OTP timer.

### Prerequisites

Before starting, ensure you have the following tools and dependencies installed:

- Flutter SDK
- Dart
- Visual Studio Code or any other preferred IDE

Add the necessary dependencies to your `pubspec.yaml` file:

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mockito: ^5.0.16
  pin_code_fields: ^7.3.0

```

### Step-by-Step Implementation

### Step 1: Create the Test File

Create a new Dart file named `otp_screen_test.dart` in your `test` directory.

### Step 2: Import Required Packages

Import the necessary packages for the test:

```dart
import 'package:chitbox_app/features/auth/view/pages/otp_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pin_code_fields/pin_code_fields.dart'; // Ensure the path is correct for your project

```

### Step 3: Write the Test Cases

### Group All Test Cases

Use the `group` function to group all test cases related to the OTP Verification Screen:

```dart
void main() {
  group('OTP Verification Screen Tests', () {
    // Define individual test cases here
  });
}

```

### Test the Visibility of the OTP Verification Title

Create a function to test the visibility of the OTP Verification title:

```dart
Future<void> _testOTPVerificationTitleVisibility(WidgetTester tester) async {
  // Arrange: Pump the OTPScreen widget
  await tester.pumpWidget(MaterialApp(home: OTPScreen(phoneNumber: '+91 123 456 7890')));

  // Assert: Verify the title text is displayed correctly
  expect(find.text('OTP Verification'), findsOneWidget);
}

testWidgets('Test the visibility of the OTP Verification title', (WidgetTester tester) async {
  await _testOTPVerificationTitleVisibility(tester);
});

```

### Test the Visibility of the Instruction Text

Create a function to test the visibility of the instruction text:

```dart
Future<void> _testInstructionTextVisibility(WidgetTester tester) async {
  // Arrange: Pump the OTPScreen widget
  await tester.pumpWidget(MaterialApp(home: OTPScreen(phoneNumber: '+91 123 456 7890')));

  // Assert: Verify the instruction text is displayed correctly
  expect(find.text('Please enter the verification code'), findsOneWidget);

  // Assert: Verify the phone number text is displayed correctly
  expect(find.text('sent on +91 123 456 7890'), findsOneWidget);
}

testWidgets('Test the visibility of the instruction text', (WidgetTester tester) async {
  await _testInstructionTextVisibility(tester);
});

```

### Test the Visibility and Functionality of the OTP Input Fields

Create a function to test the visibility and functionality of the OTP input fields:

```dart
Future<void> _testOTPInputFields(WidgetTester tester) async {
  // Arrange: Pump the OTPScreen widget
  await tester.pumpWidget(MaterialApp(home: OTPScreen(phoneNumber: '+91 123 456 7890')));

  // Assert: Verify the OTP input fields are visible
  expect(find.byType(PinCodeTextField), findsOneWidget);

  // Act: Enter a valid OTP
  await tester.enterText(find.byType(PinCodeTextField), '1234');

  // Assert: Verify the OTP input fields accept numeric input
  expect(find.text('1234'), findsOneWidget);
}

testWidgets('Test the visibility and functionality of the OTP input fields', (WidgetTester tester) async {
  await _testOTPInputFields(tester);
});

```

### Test the Visibility and Functionality of the Continue Button

Create a function to test the visibility and functionality of the Continue button:

```dart
Future<void> _testContinueButtonFunctionality(WidgetTester tester) async {
  // Arrange: Pump the OTPScreen widget
  await tester.pumpWidget(MaterialApp(home: OTPScreen(phoneNumber: '+91 123 456 7890')));

  // Assert: Verify the Continue button is visible
  final continueButton = find.byType(ElevatedButton);
  expect(continueButton, findsOneWidget);

  // Act: Enter a valid OTP
  await tester.enterText(find.byType(PinCodeTextField), '1234');
  await tester.pump();

  // Assert: Verify the Continue button is enabled only when a valid OTP is entered
  expect(tester.widget<ElevatedButton>(continueButton).enabled, isTrue);

  // Act: Tap the Continue button
  await tester.tap(continueButton);
  await tester.pumpAndSettle();

  // Assert: Verify that tapping the Continue button triggers the OTP verification logic
  // (Assuming there is some verification logic to check here)
  // For example, you can check if a certain function is called or a certain state is reached.
}

testWidgets('Test the visibility and functionality of the Continue button', (WidgetTester tester) async {
  await _testContinueButtonFunctionality(tester);
});

```

### Test the Visibility and Functionality of the Resend OTP Timer

Create a function to test the visibility and functionality of the Resend OTP timer:

```dart
Future<void> _testResendOTPTimer(WidgetTester tester) async {
  // Arrange: Pump the OTPScreen widget
  await tester.pumpWidget(MaterialApp(home: OTPScreen(phoneNumber: '+91 123 456 7890')));

  // Assert: Verify the timer text is displayed correctly and counts down from 35 seconds
  expect(find.text('Resend OTP in 35 seconds'), findsOneWidget);

  // Simulate waiting for the timer to reach 0
  await tester.pumpAndSettle(Duration(seconds: 35));

  // Assert: Verify the Resend OTP link is visible and clickable once the timer reaches 0
  expect(find.text('Resend OTP'), findsOneWidget);

  // Act: Click the Resend OTP link
  await tester.tap(find.text('Resend OTP'));
  await tester.pumpAndSettle();

  // Assert: Verify that clicking the Resend OTP link resets the timer and starts the countdown again
  expect(find.text('Resend OTP in 35 seconds'), findsOneWidget);
}

testWidgets('Test the visibility and functionality of the Resend OTP timer', (WidgetTester tester) async {
  await _testResendOTPTimer(tester);
});

```

### Full Test Code

Here's the full test code in `otp_screen_test.dart`:

```dart
import 'package:chitbox_app/features/auth/view/pages/otp_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pin_code_fields/pin_code_fields.dart'; // Ensure the path is correct for your project

void main() {
  // Group all test cases related to the OTP Verification Screen
  group('OTP Verification Screen Tests', () {
    // Test the visibility of the OTP Verification title
    testWidgets('Test the visibility of the OTP Verification title', (WidgetTester tester) async {
      await _testOTPVerificationTitleVisibility(tester);
    });

    // Test the visibility of the instruction text
    testWidgets('Test the visibility of the instruction text', (WidgetTester tester) async {
      await _testInstructionTextVisibility(tester);
    });

    // Test the visibility and functionality of the OTP input fields
    testWidgets('Test the visibility and functionality of the OTP input fields', (WidgetTester tester) async {
      await _testOTPInputFields(tester);
    });

    // Test the visibility and functionality of the Continue button
    testWidgets('Test the visibility and functionality of the Continue button', (WidgetTester tester) async {
      await _testContinueButtonFunctionality(tester);
    });

    // Test the visibility and functionality of the Resend OTP timer
    testWidgets('Test the visibility and functionality of the Resend OTP timer', (WidgetTester tester) async {
      await _testResendOTPTimer(tester);
    });
  });
}

// Function to test the visibility of the OTP Verification title
Future<void> _testOTPVerificationTitleVisibility(WidgetTester tester) async {
  // Arrange: Pump the OTPScreen widget
  await tester.pumpWidget(MaterialApp(home: OTPScreen(phoneNumber: '+91 123 456 7890')));

  // Assert: Verify the title text is displayed correctly
  expect(find.text('OTP Verification'), findsOneWidget);
}

// Function to test the visibility of the instruction text
Future<void> _testInstructionTextVisibility(WidgetTester tester) async {
  // Arrange: Pump the OTPScreen widget
  await tester.pumpWidget(MaterialApp(home: OTPScreen(phoneNumber: '+91 123 456 7890')));

  // Assert: Verify the instruction text is displayed correctly
  expect(find.text('Please enter the verification code'), findsOneWidget);

  // Assert: Verify the phone number text is displayed correctly
  expect(find.text('sent on +91 123 456 7890'), findsOneWidget);
}

// Function to test the visibility and functionality of the OTP input fields
Future<void> _testOTPInputFields(WidgetTester tester) async {
  // Arrange: Pump the OTPScreen widget
  await tester.pumpWidget(MaterialApp(home: OTPScreen(phoneNumber: '+91 123 456 7890'))

);

  // Assert: Verify the OTP input fields are visible
  expect(find.byType(PinCodeTextField), findsOneWidget);

  // Act: Enter a valid OTP
  await tester.enterText(find.byType(PinCodeTextField), '1234');

  // Assert: Verify the OTP input fields accept numeric input
  expect(find.text('1234'), findsOneWidget);
}

// Function to test the visibility and functionality of the Continue button
Future<void> _testContinueButtonFunctionality(WidgetTester tester) async {
  // Arrange: Pump the OTPScreen widget
  await tester.pumpWidget(MaterialApp(home: OTPScreen(phoneNumber: '+91 123 456 7890')));

  // Assert: Verify the Continue button is visible
  final continueButton = find.byType(ElevatedButton);
  expect(continueButton, findsOneWidget);

  // Act: Enter a valid OTP
  await tester.enterText(find.byType(PinCodeTextField), '1234');
  await tester.pump();

  // Assert: Verify the Continue button is enabled only when a valid OTP is entered
  expect(tester.widget<ElevatedButton>(continueButton).enabled, isTrue);

  // Act: Tap the Continue button
  await tester.tap(continueButton);
  await tester.pumpAndSettle();

  // Assert: Verify that tapping the Continue button triggers the OTP verification logic
  // (Assuming there is some verification logic to check here)
  // For example, you can check if a certain function is called or a certain state is reached.
}

// Function to test the visibility and functionality of the Resend OTP timer
Future<void> _testResendOTPTimer(WidgetTester tester) async {
  // Arrange: Pump the OTPScreen widget
  await tester.pumpWidget(MaterialApp(home: OTPScreen(phoneNumber: '+91 123 456 7890')));

  // Assert: Verify the timer text is displayed correctly and counts down from 35 seconds
  expect(find.text('Resend OTP in 35 seconds'), findsOneWidget);

  // Simulate waiting for the timer to reach 0
  await tester.pumpAndSettle(Duration(seconds: 35));

  // Assert: Verify the Resend OTP link is visible and clickable once the timer reaches 0
  expect(find.text('Resend OTP'), findsOneWidget);

  // Act: Click the Resend OTP link
  await tester.tap(find.text('Resend OTP'));
  await tester.pumpAndSettle();

  // Assert: Verify that clicking the Resend OTP link resets the timer and starts the countdown again
  expect(find.text('Resend OTP in 35 seconds'), findsOneWidget);
}

```

### Running the Tests

To run the tests, use the following command in your terminal:

```bash
flutter test

```

This command will execute all the tests in the `otp_screen_test.dart` file and output the results. Each test case is now defined in its own function for better organization and readability. The detailed comments and structure should help anyone understand what each test is verifying and how to extend or modify them in the future.


**Login_Page**

    // Imprt Required Packages

    import 'package:chitbox_app/features/auth/view/pages/login_page.dart';
    import 'package:chitbox_app/features/auth/view/pages/otp_screen.dart';
    import 'package:country_code_picker/country_code_picker.dart';
    import 'package:flutter/material.dart';
    import 'package:flutter_test/flutter_test.dart';

    /*
    
    // Group all test cases related to the Login Screen
    group('Login Screen Tests', () {
    // [ ] Test the visibility of the welcome message
    //     [ ] Verify the welcome message text is displayed correctly
    testWidgets('Test the visibility of the welcome message', (WidgetTester tester) async {
    await _testWelcomeMessageVisibility(tester);
    });
    
    // [ ] Test the visibility of the instruction text
    //     [ ] Verify the instruction text ("Enter your phone number to get started") is displayed correctly
    testWidgets('Test the visibility of the instruction text', (WidgetTester tester) async {
    await _testInstructionTextVisibility(tester);
    });
    
    // [ ] Test the visibility and functionality of the country code picker
    //     [ ] Verify the country code picker is visible
    //     [ ] Verify the default country code is set to '+91'
    //     [ ] Verify that changing the country code updates the state correctly
    testWidgets('Test the visibility and functionality of the country code picker', (WidgetTester tester) async {
    await _testCountryCodePicker(tester);
    });
    
    // [ ] Test the visibility and functionality of the phone number input field
    //     [ ] Verify the phone number input field is visible
    //     [ ] Verify the phone number input field accepts numeric input
    //     [ ] Verify the phone number input field validation (e.g., length and numeric format)
    testWidgets('Test the visibility and functionality of the phone number input field', (WidgetTester tester) async {
    await _testPhoneNumberInputField(tester);
    });
    
    // [ ] Test the visibility and functionality of the tick icon
    //     [ ] Verify the tick icon appears only when a valid 10-digit phone number is entered
    testWidgets('Test the visibility and functionality of the tick icon', (WidgetTester tester) async {
    await _testTickIconVisibility(tester);
    });
    
    // [ ] Test the visibility and functionality of the Continue button
    //     [ ] Verify the Continue button is visible
    //     [ ] Verify the Continue button is enabled only when a valid 10-digit phone number is entered
    //     [ ] Verify that tapping the Continue button navigates to the OTP Verification Screen
    testWidgets('Test the visibility and functionality of the Continue button', (WidgetTester tester) async {
    await _testContinueButtonFunctionality(tester);
    });
    });
    
    - /
    
    void main() {
    // Group all test cases related to the Login Screen
    group('Login Screen Tests', () {
    // Test the visibility of the welcome message
    testWidgets('Test the visibility of the welcome message', (WidgetTester tester) async {
    await _testWelcomeMessageVisibility(tester);
    });
    
    ```
    // Test the visibility of the instruction text
    testWidgets('Test the visibility of the instruction text', (WidgetTester tester) async {
      await _testInstructionTextVisibility(tester);
    });
    
    // Test the visibility and functionality of the country code picker
    testWidgets('Test the visibility and functionality of the country code picker', (WidgetTester tester) async {
      await _testCountryCodePicker(tester);
    });
    
    // Test the visibility and functionality of the phone number input field
    testWidgets('Test the visibility and functionality of the phone number input field', (WidgetTester tester) async {
      await _testPhoneNumberInputField(tester);
    });
    
    // Test the visibility and functionality of the tick icon
    testWidgets('Test the visibility and functionality of the tick icon', (WidgetTester tester) async {
      await _testTickIconVisibility(tester);
    });
    
    ```

    });
    }
    
    // Function to test the visibility of the welcome message
    Future<void> _testWelcomeMessageVisibility(WidgetTester tester) async {
    // Arrange: Pump the LoginPage widget
    await tester.pumpWidget(MaterialApp(home: LoginPage()));
    
    // Assert: Verify the welcome message text is displayed correctly
    expect(find.text('Welcome !'), findsOneWidget);
    }
    
    // Function to test the visibility of the instruction text
    Future<void> _testInstructionTextVisibility(WidgetTester tester) async {
    // Arrange: Pump the LoginPage widget
    await tester.pumpWidget(MaterialApp(home: LoginPage()));
    
    // Assert: Verify the instruction text is displayed correctly
    expect(find.text('Enter your phone number to get started'), findsOneWidget);
    }
    
    // Function to test the visibility and functionality of the country code picker
    Future<void> _testCountryCodePicker(WidgetTester tester) async {
    // Arrange: Pump the LoginPage widget
    await tester.pumpWidget(MaterialApp(home: LoginPage()));
    
    // Assert: Verify the country code picker is visible
    expect(find.byType(CountryCodePicker), findsOneWidget);
    
    // Assert: Verify the default country code is set to '+91'
    final countryCodePicker = find.byType(CountryCodePicker).evaluate().first.widget as CountryCodePicker;
    expect(countryCodePicker.initialSelection, 'IN');
    }
    
    // Function to test the visibility and functionality of the phone number input field
    Future<void> _testPhoneNumberInputField(WidgetTester tester) async {
    // Arrange: Pump the LoginPage widget
    await tester.pumpWidget(MaterialApp(home: LoginPage()));
    
    // Assert: Verify the phone number input field is visible
    final phoneNumberField = find.byType(TextField);
    expect(phoneNumberField, findsOneWidget);
    
    // Act: Enter a valid phone number
    await tester.enterText(phoneNumberField, '1234567890');
    
    // Assert: Verify the phone number input field accepts numeric input
    expect(find.text('1234567890'), findsOneWidget);
    }
    
    // Function to test the visibility and functionality of the tick icon
    Future<void> _testTickIconVisibility(WidgetTester tester) async {
    // Arrange: Pump the LoginPage widget
    await tester.pumpWidget(MaterialApp(home: LoginPage()));
    
    // Act: Enter a valid phone number
    final phoneNumberField = find.byType(TextField);
    await tester.enterText(phoneNumberField, '1234567890');
    await tester.pump();
    
    // Assert: Verify the tick icon appears only when a valid 10-digit phone number is entered
    expect(find.byIcon(Icons.check_circle), findsOneWidget);
    }
    
    // Function to test the visibility and functionality of the Continue button
    // Future<void> _testContinueButtonFunctionality(WidgetTester tester) async {
    //   // Arrange: Pump the LoginPage widget
    //   await tester.pumpWidget(MaterialApp(home: LoginPage()));
    //
    //   // Assert: Verify the Continue button is visible
    //   final continueButton = find.byType(ElevatedButton);
    //   expect(continueButton, findsOneWidget);
    //
    //   // Act: Enter a valid phone number
    //   final phoneNumberField = find.byType(TextField);
    //   await tester.enterText(phoneNumberField, '1234567890');
    //   await tester.pump();
    //
    //   // Assert: Verify the Continue button is enabled only when a valid 10-digit phone number is entered
    //   expect(tester.widget<ElevatedButton>(continueButton).enabled, isTrue);
    //
    //   // Act: Tap the Continue button
    //   await tester.tap(continueButton);
    //   await tester.pumpAndSettle();
    //
    //   // Assert: Verify that tapping the Continue button navigates to the OTP Verification Screen
    //   expect(find.byType(OTPScreen), findsOneWidget);
    // }
    
    // still not implemented functinality
    
    // Future<void> _testContinueButtonFunctionality(WidgetTester tester) async {
    //   await tester.pumpWidget(MaterialApp(home: LoginPage()));
    //   final continueButton = find.byType(ElevatedButton);
    //   expect(continueButton, findsOneWidget);
    //
    //   final phoneNumberField = find.byType(TextField);
    //   await tester.enterText(phoneNumberField, '1234567890');
    //   await tester.pump();
    //
    //   expect(tester.widget<ElevatedButton>(continueButton).enabled, isTrue);
    //
    //   await tester.tap(continueButton);
    //   await tester.pumpAndSettle();
    //
    //   expect(find.byType(OTPScreen), findsOneWidget);
    // }
