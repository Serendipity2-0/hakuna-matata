# LISKOV Substitution Principle Explained “L” in “SOLID”

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

### Liskov Substitution Principle (LSP)

### Explanation of Liskov Substitution Principle (LSP)

**Liskov Substitution Principle (LSP)** states that objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program. This means that subclasses should extend the functionality of the parent class without changing its behavior.

**Use Case Example: Restaurant Management System**

- **Scenario**: A restaurant has different types of employees: chefs, waiters, and managers. Each employee has common attributes like name and salary and common methods like `work()`.
- **Current System**: The system has a base class `Employee` and subclasses `Chef`, `Waiter`, and `Manager` that inherit from `Employee`.
- **Problem**: If the `work()` method in the `Waiter` subclass is changed to something that is not compatible with the base class `Employee`, it could break the functionality when using polymorphism.

**Solution**: Ensure that the subclasses do not alter the expected behavior of the `work()` method. The `Chef`, `Waiter`, and `Manager` subclasses should implement the `work()` method in a way that does not change its base behavior.

### Problem in the Given Codebase

In the provided code, the `AccountCreatedScreen` class handles both UI logic and navigation logic. While it might not seem like a direct violation of LSP, we should ensure that any subclass of a screen widget should not alter the fundamental behavior of navigation and UI rendering.

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

### Checklist for LSP

- [ ]  Can derived classes be substituted for their base classes without affecting the correctness of the program? **(No)**
- [ ]  Do subclasses override methods to maintain the behavior expected from the base class? **(No)**
- [ ]  Are subclasses able to be used interchangeably with their base classes? **(No)**

### Refactoring to Adhere to LSP

We can refactor the code by separating the navigation logic into a separate service. This way, the `AccountCreatedScreen` class will only be responsible for UI logic, and the navigation logic can be handled by another class, maintaining the expected behavior of the base class.

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

- [x]  Can derived classes be substituted for their base classes without affecting the correctness of the program? **(Yes)**
- [x]  Do subclasses override methods to maintain the behavior expected from the base class? **(Yes)**
- [x]  Are subclasses able to be used interchangeably with their base classes? **(Yes)**

### Benefits of LSP

1. **Predictability**: Ensures that derived classes can be used as their base types without unexpected behavior.
2. **Maintainability**: Simplifies the code by ensuring that subclasses do not alter the behavior of the base class, making the code easier to understand and maintain.
3. **Extensibility**: Allows new functionalities to be added by creating new subclasses without modifying the existing base class.

## Action Items

- [ ]  Review the refactored code to ensure it adheres to LSP.
- [ ]  Identify other parts of the codebase that may benefit from applying LSP.
- [ ]  Plan a refactoring strategy to gradually improve the codebase.

## Additional Notes

By applying the Liskov Substitution Principle, we ensure that our codebase remains predictable, maintainable, and extensible. Each subclass maintains the expected behavior of the base class, making the system easier to understand and extend without introducing bugs or unexpected behavior.