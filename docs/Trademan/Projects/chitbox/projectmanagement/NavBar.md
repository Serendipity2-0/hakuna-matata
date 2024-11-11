# Task List for Implementing and Testing Bottom Navigation Bar with Local Assets

### Main Tasks:

1. **Set Up Project Structure**
2. **Add Local Assets**
3. **Update `pubspec.yaml`**
4. **Create Reusable `BottomNavBar` Widget**
5. **Integrate `BottomNavBar` in `DashboardScreen`**
6. **Create Placeholder Screens**
7. **Test Implementation**
8. **Update Documentation**

### Subtasks:

- 1. Set Up Project Structure
    - [x]  Organize project directories.
        - [x]  Create `assets/icons` directory for storing icon images.
        - [x]  Ensure `features` and `widgets` directories are properly structured.

- 2. Add Local Assets
    - [x]  Save all required icons in `assets/icons` directory.
        - [x]  new_chits.png
        - [x]  my_chits.png
        - [x]  auction.png
        - [x]  profile.png

- 3. Update `pubspec.yaml`
- [x]  Update `pubspec.yaml` to include local assets.
        
        ```yaml
        flutter:
          assets:
            - assets/icons/
        
        ```
        
- 4. Create Reusable `BottomNavBar` Widget
    - [x]  Create `bottom_nav_bar.dart` in the `widgets` directory.

**Code**
        
        ```dart
        import 'package:flutter/material.dart';
        
        class BottomNavBar extends StatefulWidget {
          final int currentIndex;
          final Function(int) onTap;
        
          BottomNavBar({required this.currentIndex, required this.onTap});
        
          @override
          _BottomNavBarState createState() => _BottomNavBarState();
        }
        
        class _BottomNavBarState extends State<BottomNavBar> {
          @override
          Widget build(BuildContext context) {
            return BottomNavigationBar(
              currentIndex: widget.currentIndex,
              onTap: widget.onTap,
              items: [
                BottomNavigationBarItem(
                  icon: Image.asset(
                    'assets/icons/new_chits.png',
                    color: widget.currentIndex == 0 ? Colors.purple : Colors.grey,
                    height: 24,
                  ),
                  label: 'New Chits',
                ),
                BottomNavigationBarItem(
                  icon: Image.asset(
                    'assets/icons/my_chits.png',
                    color: widget.currentIndex == 1 ? Colors.purple : Colors.grey,
                    height: 24,
                  ),
                  label: 'My Chits',
                ),
                BottomNavigationBarItem(
                  icon: Image.asset(
                    'assets/icons/auction.png',
                    color: widget.currentIndex == 2 ? Colors.purple : Colors.grey,
                    height: 24,
                  ),
                  label: 'Auction',
                ),
                BottomNavigationBarItem(
                  icon: Image.asset(
                    'assets/icons/profile.png',
                    color: widget.currentIndex == 3 ? Colors.purple : Colors.grey,
                    height: 24,
                  ),
                  label: 'Profile',
                ),
              ],
              selectedItemColor: Colors.purple,
              unselectedItemColor: Colors.grey,
              showSelectedLabels: true,
              showUnselectedLabels: true,
            );
          }
        }
        
        ```
        
- 5. Integrate `BottomNavBar` in `DashboardScreen`
    - [x]  Modify `DashboardScreen` to use the new `BottomNavBar` widget.

**Code**
        
        ```dart
        import 'package:flutter/material.dart';
        import 'package:chitbox_app/widgets/bottom_nav_bar.dart';
        
        class DashboardScreen extends StatefulWidget {
          @override
          _DashboardScreenState createState() => _DashboardScreenState();
        }
        
        class _DashboardScreenState extends State<DashboardScreen> {
          int _currentIndex = 0;
        
          final List<Widget> _screens = [
            NewChitsScreen(),
            MyChitsScreen(),
            AuctionScreen(),
            ProfileScreen(),
          ];
        
          void _onTabTapped(int index) {
            setState(() {
              _currentIndex = index;
            });
          }
        
          @override
          Widget build(BuildContext context) {
            return Scaffold(
              body: IndexedStack(
                index: _currentIndex,
                children: _screens,
              ),
              bottomNavigationBar: BottomNavBar(
                currentIndex: _currentIndex,
                onTap: _onTabTapped,
              ),
            );
          }
        }
        
        ```
        
- 6. Create Placeholder Screens
    - [x]  Create placeholder screens for each tab.

**Code**
        
        ```dart
        import 'package:flutter/material.dart';
        
        class NewChitsScreen extends StatelessWidget {
          @override
          Widget build(BuildContext context) {
            return Center(
              child: Text('New Chits Screen'),
            );
          }
        }
        
        class MyChitsScreen extends StatelessWidget {
          @override
          Widget build(BuildContext context) {
            return Center(
              child: Text('My Chits Screen'),
            );
          }
        }
        
        class AuctionScreen extends StatelessWidget {
          @override
          Widget build(BuildContext context) {
            return Center(
              child: Text('Auction Screen'),
            );
          }
        }
        
        class ProfileScreen extends StatelessWidget {
          @override
          Widget build(BuildContext context) {
            return Center(
              child: Text('Profile Screen'),
            );
          }
        }
        
        ```
        
- 7. Test Implementation
    - [x]  Run the application to ensure the bottom navigation bar works correctly.
    - [x]  Verify that the correct screen is displayed when a tab is selected.
- 8. Update Documentation
    - [x]  Update the `README.md` to include instructions on how to use the `BottomNavBar` widget.
    - [x]  Document the project structure and how to add new routes and screens.

### Today's Completed Tasks:

- **Set Up Project Structure**
    - [x]  Organized project directories and ensured proper structure.
    1. **Add Local Assets**
        - [x]  Added the required icons to the `assets/icons` directory.
- **Update `pubspec.yaml`**
    - [x]  Updated the `pubspec.yaml` to include the path to local assets.
- **Create Reusable `BottomNavBar` Widget**
    - [x]  Created the `BottomNavBar` widget to use local assets for icons.
- **Integrate `BottomNavBar` in `DashboardScreen`**
    - [x]  Integrated the `BottomNavBar` widget in the `DashboardScreen`.

- **Create Placeholder Screens**
    - [x]  Created placeholder screens for each tab: New Chits, My Chits, Auction, and Profile.
- **Test Implementation**
    - [x]  Tested the application to ensure the bottom navigation bar works correctly and the correct screen is displayed when a tab is selected.
- **Update Documentation**
    - [x]  Updated the `README.md` with instructions on how to use the `BottomNavBar` widget and documented the project structure.

### Summary

Today's tasks focused on implementing a reusable bottom navigation bar using local assets. The tasks were successfully completed, and the bottom navigation bar now works as intended, providing a consistent navigation experience across the application.