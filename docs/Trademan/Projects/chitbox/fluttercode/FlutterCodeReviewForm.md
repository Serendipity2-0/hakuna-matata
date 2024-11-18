# Flutter Code Review Form - Action Required(SRP)

[Prompt](./Prompt.md)

[Open/closed Principle in SOLID](./OpenClosedPrinciple.md
)

[LISKOV Substitution Principle Explained “L” in “SOLID”](./LISKOVPrinciple.md)

## Project Details

- [**Repository Link**:](https://github.com/ChitBox/chitbox-app-frontend)
- Brief Description of Main Code Flow: The `AccountCreatedScreen` displays a success message after an account is created and navigates to the dashboard after a 5-second delay using a timer.

## Agenda:

1. Introduction (2 min)

2. Code walkthrough (15-20 min)

3. Discussion of concerns and improvements (10-15 min)

4. Action items and next steps (5 min)

## Topics for Review

**Single Responsibility Principle (SRP)**

### Explanation of SRP

- *Single Responsibility Principle (SRP)** states that a class should have only one reason to change, meaning it should have only one job or responsibility.
- *Use Case Example: Restaurant Management System**
- **Kitchen Staff**: Responsible for cooking and preparing food.
- **Wait Staff**: Responsible for taking orders and serving food.
- **Cashier**: Responsible for billing and handling payments.

Each role has a single responsibility. If we ask the kitchen staff to also handle payments, it could lead to inefficiency and errors.

### Problem in the Given Codebase

In the provided code, the `AccountCreatedScreen` class is handling both UI logic and navigation logic. This violates the SRP as the class has more than one reason to change.

- *Original Code**

```python
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

1. UI Logic: The class is responsible for rendering the UI.

2. Navigation Logic: The class is also responsible for handling the navigation after a delay.

 Checklist for SRP

- Does each class have only one reason to change? **(No)**
- Is each class responsible for only one functionality? **(No)**
- Are responsibilities clearly separated across different classes? **(No)**

### Refactoring to Adhere to SRP

We can refactor the code by separating the navigation logic into a separate service. This way, the `AccountCreatedScreen` class will only be responsible for UI logic.

- *Refactored Code**
- *navigation_service.dart**

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

- *account_created_screen.dart**

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

### Checklist After Refactoring

- [ ]  Does each class have only one reason to change? **(Yes)**
- [ ]  Is each class responsible for only one functionality? **(Yes)**
- [ ]  Are responsibilities clearly separated across different classes? **(Yes)**

### Benefits of SRP

1. Flexibility: By separating responsibilities, classes can be reused more easily.

2. Maintainability: The code is easier to maintain and understand because each class has a single responsibility.

3. Testability: The class dependencies can be easily mocked, making unit testing simpler and more effective.

## Action Items

- Review the refactored code to ensure it adheres to SRP.
- Identify other parts of the codebase that may benefit from applying SRP.
- Plan a refactoring strategy to gradually improve the codebase.

## Additional Notes

By applying the Single Responsibility Principle, we make our codebase more flexible, maintainable, and easier to extend. Each class or module focuses on a single responsibility, making it easier to reason about, test, and debug.