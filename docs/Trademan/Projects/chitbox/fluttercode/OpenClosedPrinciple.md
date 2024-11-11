# Open/closed Principle in SOLID

**Flutter Code Review Form - Action Required**

## Project Details

- **Repository Link**: [Insert GitHub/GitLab/Bitbucket link here]
- **Brief Description of Main Code Flow**: The `AccountCreatedScreen` displays a success message after an account is created and navigates to the dashboard after a 5-second delay using a timer.

## Agenda:

1. Introduction (2 min)
2. Code walkthrough (15-20 min)
3. Discussion of concerns and improvements (10-15 min)
4. Action items and next steps (5 min)

## Topics for Review

### Open/Closed Principle (OCP)

### Explanation of Open/Closed Principle (OCP)

**Open/Closed Principle (OCP)** states that software entities (classes, modules, functions, etc.) should be open for extension but closed for modification.

**Use Case Example: Restaurant Management System**

- **Scenario**: A restaurant's billing system calculates the bill based on different types of discounts (e.g., seasonal discounts, membership discounts).
- **Current System**: The billing system has a method that calculates the total bill with hardcoded discount logic.
- **Problem**: Adding a new type of discount requires modifying the existing method, which could introduce bugs and affect existing functionality.

**Solution**: The billing system should be designed in a way that allows new discount types to be added without modifying the existing bill calculation logic. This can be achieved by using interfaces or abstract classes for discounts and implementing new discount types as separate classes.

### Problem in the Given Codebase

In the provided code, the `AccountCreatedScreen` class is handling both UI logic and navigation logic directly within the same class. This violates the OCP as any changes in navigation logic would require modifying this class, which might introduce bugs.

**Original Code**

```dart
import 'dart:async';
import 'package:chitbox_app/routes/app_routes.dart';
import 'package:chitbox_app/utils/strings.dart';
import 'package:flutter/material.dart';
import '../widgets/success_dialog.dart';

class AccountCreatedScreen extends StatefulWidget {
  const AccountCreatedScreen({super.key});

  @override
  _AccountCreatedScreenState createState() => _AccountCreatedScreenState();
}

class _AccountCreatedScreenState extends State<AccountCreatedScreen> {
  @override
  void initState() {
    super.initState();
    Timer(const Duration(seconds: 5), () {
      Navigator.of(context).pushReplacementNamed(AppRoutes.getRoutePath(AppRoute.dashboard));
    });
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: Color.fromARGB(255, 68, 63, 63),
      body: Center(
        child: SuccessDialog(
          message: AppStrings.accountCreatedMessage,
        ),
      ),
    );
  }
}

```

**Issues in the Code:**

1. **UI Logic**: The class is responsible for rendering the UI.
2. **Navigation Logic**: The class is also responsible for handling the navigation after a delay.

### Checklist for OCP

- [ ]  Can new functionalities be added without modifying existing code? **(No)**
- [ ]  Are classes and methods designed to be extended without modification? **(No)**
- [ ]  Is there a clear separation between core logic and extension points? **(No)**

### Refactoring to Adhere to OCP

We can refactor the code by separating the navigation logic into a separate service. This way, the `AccountCreatedScreen` class will only be responsible for UI logic, and the navigation logic can be extended without modifying the screen class.

**Refactored Code**

**navigation_service.dart**

```dart
import 'package:flutter/material.dart';

class NavigationService {
  final BuildContext context;

  NavigationService(this.context);

  void navigateToDashboard() {
    Navigator.of(context).pushReplacementNamed('/dashboard');
  }
}

```

**account_created_screen.dart**

```dart
import 'dart:async';
import 'package:chitbox_app/routes/app_routes.dart';
import 'package:chitbox_app/utils/strings.dart';
import 'package:chitbox_app/services/navigation_service.dart';
import 'package:flutter/material.dart';
import '../widgets/success_dialog.dart';

class AccountCreatedScreen extends StatefulWidget {
  const AccountCreatedScreen({super.key});

  @override
  _AccountCreatedScreenState createState() => _AccountCreatedScreenState();
}

class _AccountCreatedScreenState extends State<AccountCreatedScreen> {
  late NavigationService _navigationService;

  @override
  void initState() {
    super.initState();
    _navigationService = NavigationService(context);
    Timer(const Duration(seconds: 5), () {
      _navigationService.navigateToDashboard();
    });
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: Color.fromARGB(255, 68, 63, 63),
      body: Center(
        child: SuccessDialog(
          message: AppStrings.accountCreatedMessage,
        ),
      ),
    );
  }
}

```

**Checklist After Refactoring**

- [x]  Can new functionalities be added without modifying existing code? **(Yes)**
- [x]  Are classes and methods designed to be extended without modification? **(Yes)**
- [x]  Is there a clear separation between core logic and extension points? **(Yes)**

### Benefits of OCP

1. **Flexibility**: By separating responsibilities, classes can be reused more easily.
2. **Maintainability**: The code is easier to maintain and understand because each class has a single responsibility.
3. **Testability**: The class dependencies can be easily mocked, making unit testing simpler and more effective.

## Action Items

- [ ]  Review the refactored code to ensure it adheres to OCP.
- [ ]  Identify other parts of the codebase that may benefit from applying OCP.
- [ ]  Plan a refactoring strategy to gradually improve the codebase.

## Additional Notes

By applying the Open/Closed Principle, we make our codebase more flexible, maintainable, and easier to extend. Each class or module focuses on a single responsibility, making it easier to reason about, test, and debug.