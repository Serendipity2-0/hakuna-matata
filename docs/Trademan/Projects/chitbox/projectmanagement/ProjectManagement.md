# Project Management

We are brainstorming all the tasks.

We have created 2 sections where both Suraj and Aakash can list down all the tasks that are to be implemented.

Aakash Savant - Brainstorm Task Ideas

## App Features/Functionalities

- User Registration
    - [ ]  Entering Invite code receive from Operator
    - [ ]  Verify Invite Code
    
    User Profile Management
    
    - [ ]  Creating a Profile (Name,Email,Communication Address)
- Basic Ekyc
    - [ ]  Entering Aadhar & Pancard  API
    - [ ]  Verifying using Aadhar and Pancard
    - [ ]  Authenticating using mobile number
- Message for creating account and kyc done
    - User will be confirm with confirmation that “you kyc is created and account verified sucessfully”
    - User will be redirected to New Chits  screen so that he can get started chit fund journey
- New Chits
    - User can able to see all list of chitfund in this screen
    - User cam view chit fund , Agreements of chit-fund and also about breakup charges and also join chit fund,download chit agreements and licenses supported to that chit fund
    - User chooses with chitfund plan and proceed further
        - [ ]  View and Download Agreement
        - [ ]  Accept licenses and Agreement
        - [ ]  Invoice breakup plan for chitfund
            - [ ]  User will proceeding to payment
            - [ ]  on sucessfull payment redirect to join auction and do bidding  depending on chit plan
- Login
    - User will enter Registered mobile number
    - System will validates mobile number will generates otp  he enters otp   if valid and registered  user then redirect to mychits
    - In my chits he can get details about chit fund details  that he joined in Earlier & also get details premium for chit plan
    - From my chits itself he can join auction performing bidding in auction ,setup automatic bid
    - for winners  : User can claim prize
        - Step 1 : Upload KYC Details
        - Step 2 : Upload cancelled cheques
        - Step 3: Physical Verification
        - Step 4: Reinbursement of prize amount

- Done
    
    Screen done upto Invitation Screen 
    
    - [x]  Splash Screen
    - [x]  Onboarding Screen about chitbox (3 Slliders)
    - [x]  Create Account info screen
    - [x]  Invitation Screen
- 1st july 2024 Monday Task
    - Designing an Personal Details Screen for mobile app
        - [x]  Creating an widget for
            - [x]  Creating an design for Personal Details
                - [x]  Done
                    - [x]  Name (Text )
                    - [x]  DOB
                    - [x]  Email Id
                    - [x]  Enter Otp  for verifying email
                    - [x]  Address for communication
            - In Pipeline
                - [x]  Fixing Bottom render flow error
                - [x]  working on  colour and alignment parts  for Personal Details Screen
            - Done  with  Personal Details Screen
                
                [Documentation for  Implementation for  Personal Details Screen](./PersonalDetailsForm.md)
                
    - Testcase
        - General Test Cases
            - [ ]  Verify that all text fields are visible and correctly labeled.
            - [ ]  Verify that the Personal Details Screen loads correctly.
        - Name Field
            - [ ]  Verify that the Name field shows an error for invalid input (if applicable).
            - [ ]  Verify that the Name field accepts text input.
        - DOB Field
            - [ ]  Verify that tapping the DOB field opens the date picker.
            - [ ]  Verify that the date picker allows selection of dates.
            - [ ]  Verify that the selected date is displayed correctly in the DOB field.
        - Email ID Field
            - [ ]  Verify that the Email ID field shows an error for invalid email format.
            - [ ]  Verify that the Email ID field accepts email input.
        - Enter OTP Field
            - [ ]  Verify that the OTP field shows an error for invalid input (if applicable).
            - [ ]  Verify that the OTP field accepts numeric input.
        - Address for Communication Field
            - [ ]  Verify that the Address field shows an error for invalid input (if applicable).
            - [ ]  Verify that the Address field accepts multiline text input.
        - Submit Button
            - [ ]  Verify that the Proceed button is visible and enabled when all fields are filled correctly.
            - [ ]  Verify that the Proceed button is disabled when required fields are empty or invalid.
            - [ ]  Verify that tapping the Proceed button submits the form (assuming further action is implemented).
        - Bottom Sheet Date Picker
            - [ ]  Verify that the date picker appears as a bottom sheet.
            - [ ]  Verify that the date picker can be dismissed by selecting a date or tapping Done.
            - [ ]  Verify that the selected date is displayed in the correct format.
        - Color and Alignment
            - [x]  Verify that the colors of the text fields, buttons, and background are as per design specifications.
            - [x]  Verify that all elements are properly aligned and spaced according to the design.
        - Error Handling
            - [x]  Verify that appropriate error messages are displayed for invalid inputs.
            - [x]  Verify that the form does not submit if there are validation errors.
        - Performance
            - [x]  Verify that the screen loads quickly without lag.
            - [x]  Verify that the bottom sheet date picker opens and closes smoothly.
        - Documentation
            - [x]  Ensure that the code is well-commented and documentation is up-to-date.
            
            [Detailed Documentation of Test Cases for Personal Details Screen](./PersonalDetailsTestCases.md)
            
        - Complete task:
            
            ### Tasks Completed Today
            
            - [x]  Implemented Personal Details Screen
            - [x]  Created test cases to validate the functionality of the Personal Details Screen
            
            ### Detailed Test Cases Completed
            
            - [x]  Verified that the Personal Details Screen loads correctly.
            - [x]  Verified that all text fields are visible and correctly labeled.
            - [x]  Verified that the Name field accepts text input.
            - [x]  Verified that tapping the DOB field opens the date picker.
            - [x]  Verified that the Email ID field accepts email input.
            - [x]  Verified that the OTP field accepts numeric input.
            - [x]  Verified that the Address field accepts multiline text input.
            - [x]  Verified that the date picker appears as a bottom sheet.
            - [x]  Verified that the date picker can be dismissed by selecting a date or tapping Done.
            
            ### Summary
            
             implemented the Personal Details Screen and created comprehensive test cases to ensure its functionality. Each aspect of the screen, including the visibility and functionality of text fields and the date picker, was thoroughly tested 
            
        
    - TODO List: Completed Test Cases
        1. **General Test Cases**
            - [x]  Verify that the Personal Details Screen loads correctly.
            - [x]  Verify that all text fields are visible and correctly labeled.
        2. **Specific Field Test Cases**
            - [x]  Verify that the Name field accepts text input.
            - [x]  Verify that tapping the DOB field opens the date picker.
            - [x]  Verify that the Email ID field accepts email input.
            - [x]  Verify that the OTP field accepts numeric input.
            - [x]  Verify that the Address field accepts multiline text input.
        3. **Date Picker Test Cases**
            - [x]  Verify that the date picker appears as a bottom sheet.
            - [x]  Verify that the date picker can be dismissed by selecting a date or tapping Done.
        
        For a detailed description of each test case, please refer to the documentation provided in the Notion link below:
        
        [Detailed Documentation of Test Cases for Personal Details Screen](./PersonalDetailsTestCases.md)
        
        completed writing and verifying the test cases for the Personal Details Screen. The detailed documentation of the test cases includes the following:
        
- 2nd july Tuesday Task
    - Dev
        - Design Login Screen
            - **Create Login Screen UI**
                - [x]  Create a new Dart file for the Login Screen (e.g., `login_screen.dart`).
                - [x]  Add a `Text` widget for the welcome message.
                - [x]  Add a dropdown or a country code picker for selecting the country code.
                - [x]  Add a `TextField` for phone number entry.
                - [x]  Add a `Button` for continuing to OTP Verification Screen.
                - [x]  Implement the number pad for phone number entry.
            - **Style the Login Screen**
                - [x]  Apply appropriate colors, fonts, and padding/margins to match the design.
                - [x]  Ensure the layout is responsive and handles different screen sizes.
        - Design OTP Verification Screen
            - **Create OTP Verification Screen UI**
                - [x]  Create a new Dart file for the OTP Verification Screen (e.g., `otp_verification_screen.dart`).
                - [x]  Add a `Text` widget for the OTP verification message.
                - [x]  Add `TextField` or OTP input fields for entering the OTP.
                - [x]  Add a `Button` for submitting the OTP.
                - [x]  Add a resend OTP timer and button.
            - **Style the OTP Verification Screen**
                - [x]  Apply appropriate colors, fonts, and padding/margins to match the design.
                - [x]  Ensure the layout is responsive and handles different screen sizes.
        - Fix RenderFlex Overflow Issue
            - [x]  **Debug and Fix Layout Overflow**
                - [x]  Identify the widget causing the RenderFlex overflow by analyzing the layout structure.
                - [x]  Adjust the layout to prevent overflow, possibly by using `Expanded`, `Flexible`, or adjusting padding/margins.
                - [x]  Test the screen on various devices to ensure the issue is resolved.
                - [x]  Bottom Over flow issue fixed by 199 pixels
        - Documentation
            
            [Detailed Documentation for `login_page.dart` and `otp_verification.dart`](./LoginPageandOTP.md)
            
    - Testing
        - Adding Relevant Test Cases
            - [ ]  **Write Unit Tests**
            - Task Breakdown  for this
                
                ### To-Do List for Writing Unit Tests
                
                - [ ]  **Write Unit Tests**
                    - [x]  **Login Screen**
                        - [ ]  Test the visibility of the welcome message.
                            - [ ]  Verify the welcome message text is displayed correctly.
                        - [x]  Test the visibility of the instruction text.
                            - [ ]  Verify the instruction text ("Enter your phone number to get started") is displayed correctly.
                        - [ ]  Test the visibility and functionality of the country code picker.
                            - [ ]  Verify the country code picker is visible.
                            - [ ]  Verify the default country code is set to '+91'.
                            - [ ]  Verify that changing the country code updates the state correctly.
                        - [ ]  Test the visibility and functionality of the phone number input field.
                            - [ ]  Verify the phone number input field is visible.
                            - [ ]  Verify the phone number input field accepts numeric input.
                            - [ ]  Verify the phone number input field validation (e.g., length and numeric format).
                        - [ ]  Test the visibility and functionality of the tick icon.
                            - [ ]  Verify the tick icon appears only when a valid 10-digit phone number is entered.
                        - [ ]  Test the visibility and functionality of the Continue button.
                            - [ ]  Verify the Continue button is visible.
                            - [ ]  Verify the Continue button is enabled only when a valid 10-digit phone number is entered.
                            - [ ]  Verify that tapping the Continue button navigates to the OTP Verification Screen.
                    - [x]  **OTP Verification Screen**
                        - [ ]  Test the visibility of the OTP Verification title.
                            - [ ]  Verify the title ("OTP Verification") is displayed correctly.
                        - [ ]  Test the visibility of the instruction text.
                            - [ ]  Verify the instruction text ("Please enter the verification code") is displayed correctly.
                            - [ ]  Verify the phone number text ("sent on +91 XXX XXX XXXX") is displayed correctly.
                        - [ ]  Test the visibility and functionality of the OTP input fields.
                            - [ ]  Verify the OTP input fields are visible.
                            - [ ]  Verify the OTP input fields accept numeric input.
                            - [ ]  Verify the OTP input fields' validation (e.g., length and numeric format).
                        - [ ]  Test the visibility and functionality of the Continue button.
                            - [ ]  Verify the Continue button is visible.
                            - [ ]  Verify the Continue button is enabled only when a valid OTP is entered.
                            - [ ]  Verify that tapping the Continue button triggers the OTP verification logic.
                        - [ ]  Test the visibility and functionality of the Resend OTP timer.
                            - [ ]  Verify the timer text ("Resend OTP in X seconds") is displayed correctly and counts down from 35 seconds.
                            - [ ]  Verify the Resend OTP link is visible and clickable once the timer reaches 0.
                            - [ ]  Verify that clicking the Resend OTP link resets the timer and starts the countdown again
                    
                    [Detailed Documentation for Unit Test Cases of OTP Verification Screen](./OTPUnitTests.md)
                    
    - Navigation
        - [x]  **Login Text Navigation**
            - [x]  Implement navigation logic from Login Text to Login Screen.
    
- 3rd July Wednesday
    
    ### Tasks Completed Today
    
    ### 1. Implemented the eKYC Verification Screen UI
    
    - **Sub-tasks**:
        - [x]  Designed the UI layout with appropriate text and icons.
        - [x]  Added input fields for PAN and Aadhaar numbers.
        - [x]  Ensured correct padding and alignment for all UI elements.
        - [x]  Applied necessary styles for text, buttons, and other UI components.
    
    ### 2. Implemented Input Validation
    
    - **Sub-tasks**:
        
        
        - [x]  Created validation logic for PAN number to be 10 characters long and alphanumeric.
        - [x]  Created validation logic for Aadhaar number to be exactly 12 digits long.
        - [x]  Added listeners to input fields to dynamically validate input.
    
    ### 3. Integrated Suffix Icons
    
    - **Sub-tasks**:
        
        
        - [x]  Added logic to show a green check mark icon when PAN input is valid.
        - [x]  Added logic to show a green check mark icon when Aadhaar input is valid.
        - [x]  Ensured that icons dynamically appear and disappear based on validation results.
        
    
    ### 4. Implemented Conditional Button Enabling
    
    - **Sub-tasks**:
        - [x]  Added logic to enable the "Verify & continue" button only when both PAN and Aadhaar inputs are valid.
        - [x]  Ensured that the button is initially disabled and only becomes enabled when the inputs meet the validation criteria.
    
    ### 5. Ensured Proper Navigation
    
    - **Sub-tasks**:
        - [x]  Implemented navigation to the next screen (eKYCVerificationScreen) upon successful validation and button click.
        - [x]  Ensured that invalid inputs prevent navigation and prompt users to correct their inputs.
    
    [eKYC Verification Screen Development Documentation](./eKYCVerificationScreen.md)
    
    - Account created Ui Design
        - [x]  UI Implementation:
            - [x]  Styled the "Verify & continue" button to enable only when both inputs are valid.
            Success Dialog:
            - [x]  Created a success dialog that displays a confirmation message after verification.
            - [x]  Implemented navigation to the Dashboard screen after displaying the success dialog for 15 seconds.
            - [x]  Dashboard Screen:
                - [x]  Designed a simple dashboard screen that users are navigated to after the success dialog.
            
            [Detailed Documentation: Creating Account Created Success Dialog](./CreatingAccountCreated.md)
            
    - Testing
        
        [Documentation: Step-by-Step Implementation and Unit Testing for eKYC Verification Screen](./eKYCImplementationAndUT.md)
        
- 4th July Thursday
    
    Dashboard UI Design 
    
    - [ ]  Bottom Navigation
    
    [Task List for Implementing and Testing Bottom Navigation Bar with Local Assets](./NavBar.md)
    
    - [ ]  Testing
    
    [Detailed Documentation for Unit Test of Dashboard Bottom Navigation](./DashboardUnitTests.md)
    
- 5th july friday
    - Today's Task List
        - Main Task: Restructuring Code and Modularizing
            1. **Restructuring Code and Modularizing Code as Suggested**
                - [ ]  Review current code structure.
                - [ ]  Identify common components and utilities.
                - [ ]  Create a modular structure for the project.
                - [ ]  Move common components to a separate folder (e.g., `widgets`).
                - [ ]  Move utility functions to a separate folder (e.g., `utils`).
                - [ ]  Update import statements to reflect new structure.
                - [ ]  Test the application to ensure no functionality is broken.
            2. **Creating Separate Branch for Development and Main**
                - [ ]  Switch to the `main` branch.
                - [ ]  Create a new branch named `dev`.
                - [ ]  Push the new branch to the remote repository.
                - [ ]  Update the project documentation to reflect the new branching strategy.
            3. **Implementing Validation Factory Pattern**
                - [ ]  Research and understand the validation factory pattern.
                - [ ]  Identify validation logic currently used in the project.
                - [ ]  Create a validation factory class.
                - [ ]  Implement the factory pattern for validation logic.
                - [ ]  Update existing validation code to use the factory pattern.
                - [ ]  Test the application to ensure validation works correctly.
            4. **Division for Common Structure for Widgets**
                - [ ]  Identify reusable widgets in the project.
                - [ ]  Create separate files for each reusable widget (e.g., `CustomButton`, `TitleWidget`, `DescriptionWidget`).
                - [ ]  Move reusable widget code to respective files.
                - [ ]  Update import statements to use the new widget files.
                - [ ]  Test the application to ensure widgets are working as expected.
        - Detailed Task Breakdown
            - 1. Restructuring Code and Modularizing Code as Suggested
                - **Review Current Code Structure**
                    - [ ]  Analyze the existing directory structure and files.
                    - [ ]  Make a list of common components and utilities.
                - **Create Modular Structure**
                    - [ ]  Create directories for `widgets`, `utils`, `services`, and `models`.
                    - [ ]  Move files to appropriate directories.
                - **Update Import Statements**
                - [ ]  Refactor import statements in all files to match the new structure.
                - **Test Application**
                - [ ]  Run the application to ensure everything is functioning as expected.
            - 2. Creating Separate Branch for Development and Main
                - **Create New Branch**
                    - [ ]  Use Git to create a new branch named `dev`.
                - **Push Branch to Remote**
                    - [ ]  Push the `dev` branch to the remote repository.
                - **Update Documentation**
                - [ ]  Add branching strategy to the `README.md`.
            - 3. Implementing Validation Factory Pattern
                - **Research Validation Factory Pattern**
                    - [ ]  Understand how the validation factory pattern works.
                - **Identify Validation Logic**
                    - [ ]  Locate all validation logic in the project.
                - **Create Validation Factory**
                    - [ ]  Create a `ValidationFactory` class.
                    - [ ]  Implement validation methods within the factory.
                - **Update Validation Code**
                    - [ ]  Replace existing validation logic with factory methods.
                - **Test Application**
                    - [ ]  Run tests to ensure validation is functioning correctly.
            - 4. Division for Common Structure for Widgets
                - **Identify Reusable Widgets**
                    - [ ]  List all widgets that are reused across the project.
                - **Create Separate Files**
                    - [ ]  Create individual files for each widget in the `widgets` directory.
                - **Move Widget Code**
                    - [ ]  Move code to respective files and clean up old references.
                - **Update Import Statements**
                    - [ ]  Ensure all files import the widgets from the new files.
                - **Test Application**
                    - [ ]  Verify that all widgets are displaying correctly and functioning as expected.
        
    - Complete tasks
        
        ### Today's Tasks Completed ✅
        
        1. **Restructured Code for Modularity** 📂
            - Organized project directories.
            - Created separate folders for core functionalities and widgets.
        2. **Created Separate Branches** 🌿
            - Set up `dev` and `main` branches for better version control.
        3. **Implemented Validation Factory Pattern** 🏭
            - Added a `ValidationFactory` class to handle input validation.
        4. **Developed Common UI Components** 🧩
            - Created reusable widgets: `CustomButton`, `TitleWidget`, `DescriptionWidget`, and `CodeBox`.
            - Ensured these components are customizable and reusable.
        5. **Enhanced Personal Details Screen** 📄
            - Added validation for Name, Email, Address, and Date of Birth (DOB).
            - Created a separate widget for DOB selection.
        6. **Improved Login Page** 📱
            - Added validation for mobile number input to ensure it's a 10-digit number.
        7. **Introduced Logging Functionality** 📝
            - Implemented a `LoggerUtil` class for logging messages, warnings, and errors.
            - Added logging to `CreateAccount` and `LoginPage`.
        8. **Configured GitHub Actions for CI/CD** 🔄
            - Set up a CI workflow to automate tests and log outputs.
            - Ensured logs are saved as artifacts for easy access and debugging.
        9. **Tested and Verified All Changes** 🔍
            - Ran unit tests for new and existing components.
            - Validated that the modularized code structure works as expected.
        
        [Detailed Documentation for Today's Tasks](./TodayTaskDocs.md)
        

Note:

This template is template  for timeline that may vary from implementation

Tasks and subtasks will change according to our  discussion related to project

# Project Management Plan for Chit-Box

---

- Timeline: 3 Months
    - Month 1: Initial Setup and Core Features Development
        - Week 1: Project Setup
            - **Project Initialization**
                - [ ]  Set up version control with Git and GitHub
                - [ ]  Set up project structure for FastAPI, PostgreSQL, and ReactJS
                - [ ]  Configure development environment
            - **Database Setup**
                - [ ]  Design database schema using SQLAlchemy
                - [ ]  Set up PostgreSQL database
                - [ ]  Implement initial database models
        - Week 2: User Authentication and Profile Management
            - [ ]  **Backend**
                - [ ]  Implement user registration and login endpoints (FastAPI)
                    - [ ]  Set up JWT authentication
                    - [ ]  Implement profile management endpoints
                - [ ]  **Frontend**
                    - [ ]  Develop user registration and login forms (ReactJS)
                    - [ ]  Create profile management page
                    - [ ]  Integrate frontend with authentication APIs
        - Week 3: Chit Fund Management
            - [ ]  **Backend**
                - [ ]  Implement endpoints for viewing, joining, and managing chit funds
                - [ ]  Create models for chit funds and user participation
            - [ ]  **Frontend**
                - [ ]  Develop chit fund listing and details pages
                - [ ]  Implement functionality to join chit funds
        - Week 4: Payment Integration
            - [ ]  **Backend**
                - [ ]  Integrate payment gateway (e.g., Stripe, Razorpay)
                - [ ]  Implement endpoints for handling payments
            - [ ]  **Frontend**
                - [ ]  Develop payment forms and UI
                - [ ]  Integrate frontend with payment APIs
    - Month 2: Advanced Features and Admin Panel
        
        ### Week 5: Auction Management
        
        - [ ]  **Backend**
            - [ ]  Implement endpoints for auction management (creating, viewing, bidding)
            - [ ]  Create models for auctions and bids
        - [ ]  **Frontend**
            - [ ]  Develop auction listing and details pages
            - [ ]  Implement bidding functionality
        
        ### Week 6: Notifications and User Feedback
        
        - [ ]  **Backend**
            - [ ]  Implement endpoints for push notifications and email alerts
            - [ ]  Create user feedback and rating endpoints
        - [ ]  **Frontend**
            - [ ]  Develop notification UI and integration
            - [ ]  Implement review and rating system (Screen 9242)
        
        ### Week 7: Admin Panel - User and Chit Fund Management
        
        - [ ]  **Backend**
            - [ ]  Implement admin endpoints for managing users and chit funds
            - [ ]  Set up role-based access control
        - [ ]  **Frontend**
            - [ ]  Develop admin panel UI for user management
            - [ ]  Implement admin functionality for managing chit funds
        
        ### Week 8: Admin Panel - Transactions and Reporting
        
        - [ ]  **Backend**
            - [ ]  Implement endpoints for viewing and approving transactions
            - [ ]  Develop reporting endpoints for financial data
        - [ ]  **Frontend**
            - [ ]  Develop admin panel UI for transaction management
            - [ ]  Create reporting and analytics dashboards
    - Month 3: Final Integration and Testing
        - Week 9: Integration and Testing - Part 1
            - [ ]  **Integration**
                - [ ]  Integrate all backend and frontend components
                - [ ]  Ensure seamless communication between APIs and UI
            - [ ]  **Testing**
                - [ ]  Write unit and integration tests for backend (FastAPI)
                - [ ]  Conduct frontend testing (ReactJS)
        - Week 10: Integration and Testing - Part 2
            - [ ]  **Performance Testing**
                - [ ]  Conduct performance and load testing on APIs
                - [ ]  Optimize database queries and API endpoints
            - [ ]  **User Acceptance Testing**
                - [ ]  Conduct UAT with a small group of users
                - [ ]  Collect feedback and make necessary adjustments
        - Week 11: Final Adjustments and Documentation
            - [ ]  **Final Adjustments**
                - [ ]  Address any remaining bugs and issues
                - [ ]  Finalize UI/UX based on feedback
                - [ ]  **Documentation**
                    - [ ]  Create comprehensive documentation for APIs
                    - [ ]  Develop user guides for the admin panel
        - Week 12: Deployment and Launch
            - [ ]  **Deployment**
                - [ ]  Set up production environment
                - [ ]  Deploy backend (FastAPI) and frontend (ReactJS) applications
                - [ ]  **Launch Preparation**
                    - [ ]  Finalize marketing and launch strategies
                    - [ ]  Conduct final review and launch ChitBox
        - Screens Mapping to Features
            - **User Registration and Login (Screens 9032 to 9060)**
            - **User Profile Management (Screen 9049)**
            - **Chit Fund Management (Screens 5, 6, 7**
            - Auction Management (Screens 8, 9, 9218,
            
            9245, 9248)**
            
            - **Payment Integration (Screens 9245, 9076, 9077)**
            - **Review and Rating (Screen 9242)**
            - **Upcoming Auctions (Screen 9246)**
            - **Charges and Claim Status (Screens 9238, 9241)**
            - **Chit History and Rewards (Screens 9233, 9236)**
            - **OTP Verification (Screens 9237, 9239, 9240, 9054, 9159)**
            - **Admin Panel Features (General overview, transaction management, user management)**

---

## Admin Panel Features/Functionalities

- [ ]  

## Backend Functionalities

- Invite User Logic
    - Generate Invitation Code
        - [x]  Username and mobile number sending  invitation code through sms
    - Verifying the invitation code
        - [x]  we will going to validate mobile number and invtation code
            - [x]  if already generated  sending invitation code via mobile number through sms
            - [x]  if not  system will generates invitation code and then send  invite code through sms
- Approval for Acessing Api for Sms & Aceesing KYC API
    - API Sethu
        - [ ]  Creating  Account and Activating for API Sethu
        - [ ]  1-week for approval from goverment (API Sethu)
        - [ ]  will have Acess to thousands of api
    - Sms & OTP
        - [ ]  Creating an Account
        - [ ]  Creating an Templete for sms and OTP (Design an message and otp message)
        - [ ]  DLT service for sms and otp
    - Payment  Gateway
        - [ ]  Creating and  completing overall process

## Other Tasks & Discussions

- [ ]  

---

---

# Suraj Donthi - Brainstorm Task & Ideas

## App Features/Functionalities

- Sign Up & Login-flow - Larger Module
    - Login with Mob. - Module
        - [ ]  Implement Mobile Login
            - [ ]  Mobile Form Field
            - [ ]  OTP Generation
            - [ ]  Sending SMS &
            - [ ]  Verification
    - Sign-Up with Invitation code - Module
        - [ ]  Mobile & Invite Code Verification - Task
            - [ ]  If mobile no. is not added by Operator, then send the message “Unrecognized number. Share your interest to operator?” - Sub-task
        - [ ]  Aadhaar and PAN Card eKYC - Task
        - [ ]  Enter Personal Details in Form - Task
            - Fields:
                - Name
                - DoB (Date Picker)
                - Email
                - Current Address
            - [ ]  AutoPopulate from eKYC APIs - Sub-Task
- New Chit Funds-flow - Larger Module
    - [ ]  List Chits in My Chits Page (Screen 9070)
    - [ ]  Implement Chit Details Page
    - [ ]  Joining Chit Fund Flow
        - [ ]  Implement Declarations Page
        - [ ]  Implement Charge Breakup Page
        - [ ]  Implement Invoice Page
            - [ ]  Implement Default Payment Method Slider
        - [ ]  Integrate Payment Gateway
- My Chit Funds-flow - Larger Module
    - [ ]  Implement Claim Status in the Page
    - [ ]  Implement Join Auction-flow
        - [ ]  
- [ ]  

## Admin Panel Features/Functionalities

- Designing Admin Panel
    - Design **Chit Funds Tab**
        - Chit Funds Table
        - Design Chit Fund Details Page
            
            The Chit Fund details page should show a summary of all the details of the chit fund.
            
            - Summary Sub-Tab
                1. Chit Fund Metrics
                    1. Amount to be Collected / Monthly Collection, Eg: 80,000 / 100,000
                    2. Monthly Payout
                    3. Dividend & Dividend %
                    4. Auction Prize Money?
                    5. 
                2. Chit Fund Attributes/details & Auction details (PSO Number, Chit Amount, Principal Amount, Empty Slots, Installments left, Installment Complete, etc.)
                    1. PSO Number
                    2. Chit Amount
                    3. Premium
                    4. No. of Members: 20/20
                    5. No. of Installments: 5/20
                    6. Chit Type: Auction | Fixed
                    7. Auction Frequency: Monthly | Weekly | Daily
                    8. Chit Start Date
                    9. Chit End Date (Automatically calculated based on # Installments & Frequency)
                    10. Next Auction Date can be given with an edit date. 
                3. Unpaid Members Section
                    1. Profile Photo
                    2. Name
                    3.  Amount
                    4. Phone & WhatsApp Icons (For directly calling & contacting)
                4. Auction Winners
                    1.  Profile Photo
                    2. Name
                    3. Prize Amount
                    4. Month/Auction Installment Won
                    5. CTA Button: Verify Documents / Approve Disbursal / Paid
                    6. Those whose (all) documents are verified can be given a **Green Tick**.
                    7. Those whose documents aren’t uploaded or not yet verified can be given a **yellow badge or tick**.
                5. Auction History Graph (Summary)
            - Members Sub-tab
                - Multiple Groups/Filters:
                    - All
                    - Unpaid Members
                    - Auction Winners
                    - Inactive Members
                - Table of members (with option on the top-right to Add/Remove Members)
                    - Add Option will get disabled once all the slots are filled!
                - 
            - Transactions Histroy Sub-Tab
                - Auctions History
                - Activity History
                - Payments & Collections History??
                    - Multiple Sub-Tabs:
                        - All
                        - Collections
                        - Dividend Disbursed
                        - Prize Money Disbursed
                        - Prize Money Approved (Not Disbursed yet)
                - Verifications History??
                    - Multiple Sub-Tabs:
                        - All
                        - Claims Verification Requests
                        - Full KYC Requests
                        - Claims Verified
                        - Full KYC Verified
                        - Documents Not Uploaded
                        - Rejected
            - Settings Sub-Tab
                
                Change settings/details of the Chit Fund
                
                - 
    - Design **Members Tab**
        - Members Table View
            - Sub-Tabs/Filters:
                - All
                - Active Members
                - Inactive Members
            - Buttons:
                - Add Members Manually
                    - Bulk Add Members
                - Invite Members
                    - Bulk Invite Members
            - Actions:
                - Verify Documents
                - Edit Member Details
                - Remove Member
                - Block Member
            - Checkbox
            - Full Name
            - Chits Subscribed
            - Auctions Won
            - Total Amount Invested
            - Total Rewards Claimed
        - Member Detailed View
            - Basic Details Section:
                - Full Name
                - Mobile Number
                - Email
                - Permanent Address
                - Current Address
            - Activities Section (Right Side)??
                - Track of Activities performed by the User
            - Verification Section:
                - Documents Uploaded
                - Button: Verify Documents, **Disburse Payment Putton**
            - Chit Funds Section:
                - Chit Funds Subscribed
                - Auctions Won
                - Payment Defaults etc.
    - Design Claims & Verifications Tab
        
        Claims and verifications entail all the verifications to be done for Full KYC & Claims Verifications
        
        - Table View:
            - Sub-Tabs:
                - All
                - Claims
                - Full KYC Verification
            - Actions:
                - Verify Documents
                - Disapprove Documents
                - Request Documents
            - Fields:
                - Checkbox
                - Name
                - Claim request for: #1234 ChitFund
    - Design **Auctions Tab**
        - [ ]  Design Live Auctions Page
        - [ ]  Design Past Auctions Page

## Backend Functionalities

- [ ]  Database Design
    - [ ]  Design Schema for Chit Funds
    - [ ]  Design Schema for Customer/Members
    - [ ]  Design Schema for Payments
    - [ ]  Design Schema for Auctions
    - [ ]  Design Schema for Administrators

