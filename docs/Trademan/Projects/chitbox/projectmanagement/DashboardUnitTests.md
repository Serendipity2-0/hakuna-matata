# Detailed Documentation for Unit Test of Dashboard Bottom Navigation

### Objective

The purpose of this documentation is to provide a comprehensive guide on writing and executing unit tests for the bottom navigation bar in the `DashboardScreen` of the ChitBox application. This will ensure that the navigation works correctly and the appropriate screens are displayed when different tabs are selected.

### Prerequisites

- Flutter and Dart SDK installed
- Basic knowledge of Flutter development
- Basic knowledge of unit testing in Flutter

### Project Setup

1. **Add Dependencies**: Ensure that the necessary dependencies are added to the `pubspec.yaml` file.

**Dependencies:**
    
       yaml

    dev_dependencies:

      flutter_test:

        sdk: flutter

      mockito: ^5.0.0
    
    
2. **Create Test File**: Create a file named `dashboard_screen_test.dart` in the `test` directory.

### Test Plan

The unit tests will cover the following scenarios:

1. Verify the presence of the bottom navigation bar.
2. Verify navigation between different tabs.
3. Verify the correct screen is displayed when a tab is selected.

### Test Cases

1. **Verify the Presence of Bottom Navigation Bar**
    - Ensure that the bottom navigation bar is present in the `DashboardScreen`.
2. **Verify Navigation Between Different Tabs**
    - Check that the bottom navigation bar allows navigation between the "New Chits", "My Chits", "Auction", and "Profile" tabs.
3. **Verify the Correct Screen is Displayed When a Tab is Selected**
    - Ensure that the correct screen is displayed when each tab is selected.

### Step-by-Step Breakdown

**Subtask 1: Set Up Testing Environment**

1. **Add Dependencies in `pubspec.yaml`**:
Ensure that the `flutter_test` and `mockito` dependencies are added to the `pubspec.yaml` file under `dev_dependencies`.

**Dependencies:**
    
       yaml
    dev_dependencies:
      flutter_test:
        sdk: flutter
      mockito: ^5.0.0

    
2. **Create Test File**:
Create a file named `dashboard_screen_test.dart` in the `test` directory.
3. **Import Necessary Packages**:
Import the necessary packages at the beginning of the test file.
    
**packages:**

           dart

        import 'package:flutter/material.dart';
        import 'package:flutter_test/flutter_test.dart';
        import 'package:chitbox_app/features/home/DashboardScreen.dart';
        import 'package:chitbox_app/widgets/bottom_nav_bar.dart';


**Subtask 2: Write Test Cases for Bottom Navigation**

1. **Verify the Presence of Bottom Navigation Bar**:
This test ensures that the bottom navigation bar is present in the `DashboardScreen`.

**Code**

    dart

    testWidgets('Verify the presence of Bottom Navigation Bar', (WidgetTester tester) async {
      await tester.pumpWidget(MaterialApp(home: DashboardScreen()));
    
      expect(find.byType(BottomNavBar), findsOneWidget);
    });
    
    
2. **Verify Navigation Between Different Tabs**:
This test ensures that the bottom navigation bar allows navigation between the different tabs.

**Code**
    
    ```dart
    testWidgets('Verify navigation between tabs', (WidgetTester tester) async {
      await tester.pumpWidget(MaterialApp(home: DashboardScreen()));
    
      // Initial tab (New Chits)
      expect(find.text('New Chits Screen'), findsOneWidget);
    
      // Tap on My Chits tab
      await tester.tap(find.text('My Chits'));
      await tester.pump();
      expect(find.text('My Chits Screen'), findsOneWidget);
    
      // Tap on Auction tab
      await tester.tap(find.text('Auction'));
      await tester.pump();
      expect(find.text('Auction Screen'), findsOneWidget);
    
      // Tap on Profile tab
      await tester.tap(find.text('Profile'));
      await tester.pump();
      expect(find.text('Profile Screen'), findsOneWidget);
    });
    
    ```
    
3. **Verify the Correct Screen is Displayed When a Tab is Selected**:
This test ensures that the correct screen is displayed when each tab is selected.

**Code**
    
    ```dart
    testWidgets('Verify the correct screen is displayed when a tab is selected', (WidgetTester tester) async {
      await tester.pumpWidget(MaterialApp(home: DashboardScreen()));
    
      // Initial tab (New Chits)
      expect(find.text('New Chits Screen'), findsOneWidget);
    
      // Tap on My Chits tab
      await tester.tap(find.text('My Chits'));
      await tester.pump();
      expect(find.text('My Chits Screen'), findsOneWidget);
    
      // Tap on Auction tab
      await tester.tap(find.text('Auction'));
      await tester.pump();
      expect(find.text('Auction Screen'), findsOneWidget);
    
      // Tap on Profile tab
      await tester.tap(find.text('Profile'));
      await tester.pump();
      expect(find.text('Profile Screen'), findsOneWidget);
    });
    
    ```
    

**Subtask 3: Run and Validate Tests**

1. **Run Tests**:
Execute the test cases using the following command:

**Commands**  

    ```
    flutter test test/dashboard_screen_test.dart
    
    ```
    
2. **Validate Test Results**:
Ensure that all test cases pass successfully. If any test fails, debug and fix the issues, then re-run the tests.

**Full Test File Example**

    import 'package:flutter/material.dart';
    import 'package:flutter_test/flutter_test.dart';
    import 'package:chitbox_app/features/home/DashboardScreen.dart';
    import 'package:chitbox_app/widgets/bottom_nav_bar.dart';           
    void main() {
      testWidgets('Verify the presence of Bottom Navigation Bar', (WidgetTester tester) async {
        await tester.pumpWidget(MaterialApp(home: DashboardScreen()));
    
        expect(find.byType(BottomNavBar), findsOneWidget);
      });
    
      testWidgets('Verify navigation between tabs', (WidgetTester tester) async {
        await tester.pumpWidget(MaterialApp(home: DashboardScreen()));
    
        // Initial tab (New Chits)
        expect(find.text('New Chits Screen'), findsOneWidget);
    
        // Tap on My Chits tab
        await tester.tap(find.text('My Chits'));
        await tester.pump();
        expect(find.text('My Chits Screen'), findsOneWidget);
    
        // Tap on Auction tab
        await tester.tap(find.text('Auction'));
        await tester.pump();
        expect(find.text('Auction Screen'), findsOneWidget);
    
        // Tap on Profile tab
        await tester.tap(find.text('Profile'));
        await tester.pump();
        expect(find.text('Profile Screen'), findsOneWidget);
      });
    
      testWidgets('Verify the correct screen is displayed when a tab is selected', (WidgetTester tester) async {
        await tester.pumpWidget(MaterialApp(home: DashboardScreen()));
    
        // Initial tab (New Chits)
        expect(find.text('New Chits Screen'), findsOneWidget);
    
        // Tap on My Chits tab
        await tester.tap(find.text('My Chits'));
        await tester.pump();
        expect(find.text('My Chits Screen'), findsOneWidget);
    
        // Tap on Auction tab
        await tester.tap(find.text('Auction'));
        await tester.pump();
        expect(find.text('Auction Screen'), findsOneWidget);
    
        // Tap on Profile tab
        await tester.tap(find.text('Profile'));
        await tester.pump();
        expect(find.text('Profile Screen'), findsOneWidget);
      });
    }

### Conclusion

This detailed documentation provides a comprehensive guide on writing and executing unit tests for the bottom navigation bar in the `DashboardScreen` of the ChitBox application. By following the steps outlined in this guide, you can ensure that the navigation works correctly and the appropriate screens are displayed when different tabs are selected.