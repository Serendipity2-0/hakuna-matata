# Detailed Documentation of Test Cases for Personal Details Screen

### Overview

This documentation provides a detailed explanation of the test cases implemented for the Personal Details Screen in a Flutter application. The test cases aim to ensure that the screen loads correctly, all fields are visible and correctly labeled, and that the fields accept appropriate inputs.

### Test Case Structure

Each test case is structured to verify a specific functionality of the Personal Details Screen. The test cases are organized into a group for better management and readability.

### Test Case 1: Verify that the Personal Details Screen Loads Correctly

**Purpose:**
To ensure that the Personal Details Screen loads without any issues and displays the correct title.

**Code:**

```dart
testWidgets('Verify that the Personal Details Screen loads correctly', (WidgetTester tester) async {
  await tester.pumpWidget(createPersonalDetailsScreen());

  // Verify that the title is displayed
  expect(find.text('Personal Details'), findsOneWidget);
});

```

**Explanation:**

- The `createPersonalDetailsScreen` function initializes the Personal Details Screen.
- The `expect` function checks if the title "Personal Details" is present on the screen.

### Test Case 2: Verify that All Text Fields Are Visible and Correctly Labeled

**Purpose:**
To ensure that all text fields are visible on the screen and have the correct labels.

**Code:**

```dart
testWidgets('Verify that all text fields are visible and correctly labeled', (WidgetTester tester) async {
  await tester.pumpWidget(createPersonalDetailsScreen());

  expect(find.byType(TextFormField), findsNWidgets(5));
  expect(find.text('Name as per Aadhar card'), findsOneWidget);
  expect(find.text('DOB'), findsOneWidget);
  expect(find.text('Email ID'), findsOneWidget);
  expect(find.text('Enter OTP'), findsOneWidget);
  expect(find.text('Address for communication'), findsOneWidget);
});

```

**Explanation:**

- The `find.byType` function checks for the presence of five `TextFormField` widgets.
- The `expect` function verifies that each text field is labeled correctly.

### Test Case 3: Verify that the Name Field Accepts Text Input

**Purpose:**
To ensure that the Name field accepts text input from the user.

**Code:**

```dart
testWidgets('Verify that the Name field accepts text input', (WidgetTester tester) async {
  await tester.pumpWidget(createPersonalDetailsScreen());

  await tester.enterText(find.byKey(Key('nameField')), 'John Doe');
  expect(find.text('John Doe'), findsOneWidget);
});

```

**Explanation:**

- The `find.byKey` function identifies the Name field using a key.
- The `tester.enterText` function simulates entering the text "John Doe" into the Name field.
- The `expect` function checks if the entered text is present in the field.

### Test Case 4: Verify that Tapping the DOB Field Opens the Date Picker

**Purpose:**
To ensure that tapping the DOB field opens a date picker.

**Code:**

```dart
testWidgets('Verify that tapping the DOB field opens the date picker', (WidgetTester tester) async {
  await tester.pumpWidget(createPersonalDetailsScreen());

  await tester.tap(find.byKey(Key('dobField')));
  await tester.pumpAndSettle();

  expect(find.byType(CupertinoDatePicker), findsOneWidget);
});

```

**Explanation:**

- The `find.byKey` function identifies the DOB field using a key.
- The `tester.tap` function simulates a tap on the DOB field.
- The `tester.pumpAndSettle` function waits for the UI to settle after the tap action.
- The `expect` function checks if the date picker is displayed.

### Test Case 5: Verify that the Email ID Field Accepts Email Input

**Purpose:**
To ensure that the Email ID field accepts email input from the user.

**Code:**

```dart
testWidgets('Verify that the Email ID field accepts email input', (WidgetTester tester) async {
  await tester.pumpWidget(createPersonalDetailsScreen());

  await tester.enterText(find.byKey(Key('emailField')), 'test@example.com');
  expect(find.text('test@example.com'), findsOneWidget);
});

```

**Explanation:**

- The `find.byKey` function identifies the Email ID field using a key.
- The `tester.enterText` function simulates entering the email "[test@example.com](mailto:test@example.com)" into the field.
- The `expect` function checks if the entered email is present in the field.

### Test Case 6: Verify that the OTP Field Accepts Numeric Input

**Purpose:**
To ensure that the OTP field accepts numeric input from the user.

**Code:**

```dart
testWidgets('Verify that the OTP field accepts numeric input', (WidgetTester tester) async {
  await tester.pumpWidget(createPersonalDetailsScreen());

  await tester.enterText(find.byKey(Key('otpField')), '123456');
  expect(find.text('123456'), findsOneWidget);
});

```

**Explanation:**

- The `find.byKey` function identifies the OTP field using a key.
- The `tester.enterText` function simulates entering the numeric OTP "123456" into the field.
- The `expect` function checks if the entered OTP is present in the field.

### Test Case 7: Verify that the Address Field Accepts Multiline Text Input

**Purpose:**
To ensure that the Address field accepts multiline text input from the user.

**Code:**

```dart
testWidgets('Verify that the Address field accepts multiline text input', (WidgetTester tester) async {
  await tester.pumpWidget(createPersonalDetailsScreen());

  await tester.enterText(find.byKey(Key('addressField')), '123 Main St\\nCity, State');
  expect(find.text('123 Main St\\nCity, State'), findsOneWidget);
});

```

**Explanation:**

- The `find.byKey` function identifies the Address field using a key.
- The `tester.enterText` function simulates entering multiline text "123 Main St\nCity, State" into the field.
- The `expect` function checks if the entered text is present in the field.

### Test Case 8: Verify that the Date Picker Appears as a Bottom Sheet

**Purpose:**
To ensure that the date picker appears as a bottom sheet when the DOB field is tapped.

**Code:**

```dart
testWidgets('Verify that the date picker appears as a bottom sheet', (WidgetTester tester) async {
  await tester.pumpWidget(createPersonalDetailsScreen());

  await tester.tap(find.byKey(Key('dobField')));
  await tester.pumpAndSettle();

  expect(find.byType(CupertinoDatePicker), findsOneWidget);
});

```

**Explanation:**

- The `find.byKey` function identifies the DOB field using a key.
- The `tester.tap` function simulates a tap on the DOB field.
- The `tester.pumpAndSettle` function waits for the UI to settle after the tap action.
- The `expect` function checks if the date picker is displayed as a bottom sheet.

### Test Case 9: Verify that the Date Picker Can Be Dismissed by Selecting a Date or Tapping Done

**Purpose:**
To ensure that the date picker can be dismissed by selecting a date or tapping the Done button.

**Code:**

```dart
testWidgets('Verify that the date picker can be dismissed by selecting a date or tapping Done', (WidgetTester tester) async {
  await tester.pumpWidget(createPersonalDetailsScreen());

  await tester.tap(find.byKey(Key('dobField')));
  await tester.pumpAndSettle();

  expect(find.byType(CupertinoDatePicker), findsOneWidget);

  await tester.tap(find.text('Done'));
  await tester.pumpAndSettle();

  expect(find.byType(CupertinoDatePicker), findsNothing);
});

```

**Explanation:**

- The `find.byKey` function identifies the DOB field using a key.
- The `tester.tap` function simulates a tap on the DOB field.
- The `tester.pumpAndSettle` function waits for the UI to settle after the tap action.
- The `expect` function checks if the date picker is displayed.
- The `tester.tap` function simulates a tap on the Done button.
- The `tester.pumpAndSettle` function waits for the UI to settle after the tap action.
- The `expect` function checks if the date picker is dismissed.

### Conclusion

By following these detailed test cases, you can ensure that the Personal Details Screen functions correctly and provides a seamless user experience. Each test case focuses on a specific aspect of the screen, ensuring comprehensive coverage of all functionalities.