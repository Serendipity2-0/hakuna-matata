# Technical Documentation

Status: Done
Assign: Aakash Savant
Team: Engineering

### ChitBox App Design Documentation

### Table of Contents

1. **Introduction**
2. **Phase One Features**
3. **Data Collection Justification**
4. **User Interface Design**
5. **Technical Stack**
6. **Data Privacy and Security**
7. **Conclusion**

---

### 1. Introduction

ChitBox is a digital platform aimed at simplifying and modernizing the traditional chit fund process. This document outlines the design, features for Phase One, and the rationale behind data collection from users.

### 2. Phase One Features

Phase One of ChitBox focuses on essential functionalities that enable users to join, manage, and participate in chit funds seamlessly.

### Features:

- **User Registration and Authentication**
    - Sign Up/Sign In via email or mobile number.
    - Two-factor authentication (2FA) via OTP.
    - User role selection (User/Agent).
- **KYC Verification**
    - Integration with Digilocker for document verification.
    - Collection of personal details (Name, DOB, Address).
    - Collection of identification details (Aadhar, PAN).
- **Bank Information**
    - Collection of bank details (Account number, IFSC code).
    - Verification of account ownership.
- **Chit Fund Management**
    - Viewing available chit funds.
    - Joining chit funds.
    - Viewing chit fund details (amount, premium, start date, slots).
- **Bidding System**
    - Live auction for chit funds.
    - Automatic bidding setup.
- **Notifications**
    - Real-time notifications for bids and fund status.
    - Alerts for upcoming payments and auctions.
- **User Profile Management**
    - Edit personal and bank details.
    - View linked bank accounts.
    - Manage notifications settings.

### 3. Data Collection Justification

The ChitBox app collects user data to ensure a secure and trustworthy environment for all participants. Below are the reasons for data collection and its importance:

### Personal Details:

- **Purpose:** To identify and authenticate users.
- **Why Needed:** Ensures only verified users can participate, reducing the risk of fraud.

### Bank Information:

- **Purpose:** To facilitate seamless transactions and payouts.
- **Why Needed:** Ensures the correct bank account is used for transactions, providing a secure financial process.

### Identification Documents (Aadhar, PAN):

- **Purpose:** For KYC verification to comply with legal requirements.
- **Why Needed:** Builds trust with users and ensures compliance with financial regulations.

### Contact Information:

- **Purpose:** To provide notifications and updates.
- **Why Needed:** Keeps users informed about their funds, payments, and bids.

By collecting this data, ChitBox ensures the integrity and security of its operations, fostering trust between users and the platform.

### 4. User Interface Design

The user interface (UI) design for ChitBox aims to provide an intuitive and user-friendly experience. The design focuses on clarity, simplicity, and ease of navigation.

### Key Screens:

1. **Welcome Screen**
    - Onboarding slides to introduce the app.
    - Options to Sign Up or Sign In.
2. **Registration and KYC**
    - Forms for personal details, bank information, and document upload.
    - Digilocker integration for easy verification.
3. **Dashboard**
    - Overview of active and available chit funds.
    - Navigation menu for easy access to different sections (New Chits, Active Chits, Auctions, Profile).
4. **Chit Fund Details**
    - Detailed view of chit fund information.
    - Options to join or bid in an auction.
5. **Auction Screen**
    - Live auction interface.
    - Automatic bid setup.
6. **Profile Management**
    - Options to view and edit personal and bank details.
    - Notification settings.

### 5. Technical Stack

### Backend:

- **Framework:** Django/Node.js/FastAPI
- **Database:** PostgreSQL
- **Authentication:** JWT-based authentication
- **API Integration:** Digilocker API for KYC

### Frontend:

- **Framework:** Flutter
- **Design System:** Custom UI components adhering to material design guidelines

### DevOps:

- **Containerization:** Docker
- **Hosting:** AWS/Azure
- **CI/CD:** Jenkins/GitHub Actions

### 6. Data Privacy and Security

ChitBox prioritizes user data privacy and security by implementing the following measures:

- **Encryption:** All sensitive data is encrypted using AES-256.
- **Secure Authentication:** Two-factor authentication and OAuth for third-party integrations.
- **Data Masking:** Personal data displayed in the app is masked to prevent unauthorized access.
- **Regular Audits:** Periodic security audits and compliance checks.

### 7. Conclusion

ChitBox aims to revolutionize the chit fund process by offering a secure, transparent, and user-friendly digital platform. Phase One of the app focuses on essential features that provide users with the functionality needed to manage and participate in chit funds effectively. The data collection processes ensure user trust and compliance with legal requirements, creating a safe environment for all participants.

---

### Design Documentation Templates

### 1. **User Registration and Authentication**

```markdown
### User Registration and Authentication

**Description:**
Users can sign up or log in using their email or mobile number with OTP verification.

**Components:**
- Sign Up Form
- Sign In Form
- OTP Verification

**Design:**
1. **Sign Up Screen:**
   - Input fields for email/mobile number.
   - OTP request button.
2. **Sign In Screen:**
   - Input fields for email/mobile number.
   - OTP request button.
3. **OTP Verification:**
   - Input field for OTP.
   - Resend OTP option.

**API Endpoints:**
- POST `/api/auth/signup`
- POST `/api/auth/signin`
- POST `/api/auth/verify-otp`

```

### 2. **KYC Verification**

```markdown
### KYC Verification

**Description:**
Integration with Digilocker to verify user identity.

**Components:**
- Personal Details Form
- Document Upload
- Digilocker Integration

**Design:**
1. **Personal Details Screen:**
   - Input fields for name, DOB, address, etc.
2. **Document Upload:**
   - Input fields for Aadhar, PAN.
   - Digilocker integration button.

**API Endpoints:**
- POST `/api/kyc/verify`
- GET `/api/kyc/status`

```

### 3. **Bank Information**

```markdown
### Bank Information

**Description:**
Collection and verification of user's bank details.

**Components:**
- Bank Details Form

**Design:**
1. **Bank Information Screen:**
   - Input fields for account number, IFSC code.
   - Verification button.

**API Endpoints:**
- POST `/api/bank/add`
- GET `/api/bank/verify`

```

### 4. **Chit Fund Management**

```markdown
### Chit Fund Management

**Description:**
Viewing and joining chit funds.

**Components:**
- Chit Fund List
- Chit Fund Details
- Join Chit Fund

**Design:**
1. **Chit Fund List:**
   - List of available chit funds.
   - Filter and search options.
2. **Chit Fund Details:**
   - Detailed view of chit fund information.
   - Join button.

**API Endpoints:**
- GET `/api/chitfunds`
- GET `/api/chitfunds/:id`
- POST `/api/chitfunds/join`

```

### 5. **Bidding System**

```markdown
### Bidding System

**Description:**
Live auction interface for bidding on chit funds.

**Components:**
- Live Auction Screen
- Automatic Bid Setup

**Design:**
1. **Live Auction Screen:**
   - Current highest bid.
   - Bid input field.
   - Place bid button.
2. **Automatic Bid Setup:**
   - Min and max bid input fields.
   - Save button.

**API Endpoints:**
- GET `/api/auction/:id`
- POST `/api/auction/bid`
- POST `/api/auction/auto-bid`

```

### 6. **Notifications**

```markdown
### Notifications

**Description:**
Real-time notifications for user actions and updates.

**Components:**
- Notification List
- Notification Settings

**Design:**
1. **Notification List:**
   - List of notifications.
   - Mark as read option.
2. **Notification Settings:**
   - Toggle for different notification types.

**API Endpoints:**
- GET `/api/notifications`
- POST `/api/notifications/read`

```

### 7. **User Profile Management**

```markdown
### User Profile Management

**Description:**
Manage personal and bank details, and notification settings.

**Components:**
- Profile Edit Form
- Linked Bank Accounts
- Notification Settings

**Design:**
1. **Profile Edit Screen:**
   - Input fields for personal details.
   - Save button.
2. **Linked Banks Screen:**
   - List of linked bank accounts.
   - Edit and remove options.
3. **Notification Settings:**
   - Toggle for different notification types.

**API Endpoints:**
- GET `/api/profile`
- POST `/api/profile/update`
- GET `/api/banks`
- POST `/api/banks/add`
- DELETE `/api/banks/:id`

```

---

This comprehensive design documentation outlines the key features and design elements for the ChitBox app, focusing on Phase One.