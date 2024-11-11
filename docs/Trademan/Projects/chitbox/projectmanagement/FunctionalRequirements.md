# Functional Requirements

## Main Panel - Tabs

### User Tab - Managing User Accounts

- Functional Specification:
    - Bulk Invite users Button - Create users in bulk by uploading a CSV file with user details.
    - Invite/Add User Button - Create individual users manually with required information.
    - Users Table
        - Multiple tabs/Filters
        - For each User
            - **Customer Details**
                - KYC Status
                - ID
                - Name
                - Email
                - Mobile
                - Address
                - eKYC - Electronic KYC - Show Green Ticks against the fields
                    - Adhaar,
                    - PAN Card
                    - Mobile ()
                    - Email
                    - Face Verification
            - **Full KYC Verification Status & Details**
            - **List of All Chits Enrolled**
                - Tabs/Filters:
                    - Active Chits
                    - Claimed Chits
                    - Unclaimed Chits
                    - Past Chits
                    - Cancelled Chits
                    - etc.

### Chit fund management

- Overview pointers of the functionality:
    - Create new chit funds.
    - Bulk Create Chits??
    - Modify existing chit funds??
        - What parameters can be changed & what cannot be? @Chitbox 07
    - Close chit funds when necessary.
    - Approve chit proposals from agencies.

### Verification, Approval & Claims

- Overview pointers of the functionality:
    - Common Process for Verification and KYC - Establish a standardized process for verification and KYC across all users
    accounts.
    - Utilize third-party services or manual approval by the admin for verification.
    - Verify KYC details for individual users during account creation or update.
    - Initiate KYC verification for bulk users and process verification using a common
    process.
    - Verify physical documents and checks for user accounts and transactions.
    - Track claiming processes, procedures, and rewards processes.

### Reporting and analysis

- Generate financial reports.
- Analyze operational data.
- Monitor user and agency activity.
- Track KYC verification status and compliance.

### Data Processing

- The system processes admin actions and updates the database accordingly.
- Payments, verifications, and user interactions are recorded and managed.

### Support and communication

- Communicate with agencies, operators, and users regarding KYC verification and
other account-related matters.
- Receive notifications for important events such as approvals, verifications, and
support tickets.

### Notification and Feedback

- Provide feedback on system functionalities or raise issues for resolution.

## Settings

### Role-based Access Control

- Manage user accounts, permissions, and roles.
    - SuperAdmin
    - Operator (Next Phase)
    - **Agents**
    - Managers
    - Verification Agent
    - Accountant

---

# **Admin Panel High-level Functionalities**

- **User Management**
    - View user profiles
    - Approve/Reject user registrations
    - Assign roles (Admin, Manager, Member)
    - Deactivate/Activate users
- **ChitFund Management**
    - Create new ChitFunds
    - Update ChitFund details (amount, duration, members)
    - View active and completed ChitFunds
    - Manage member participation in ChitFunds
- **Bidding Management**
    - Monitor live bidding sessions
    - Approve/Reject bids
    - View bid history
- **Payment Management**
    - Configure payment gateways
    - Monitor transactions
    - Approve/Reject payments
    - View transaction history
- **Reporting and Analytics**
    - Generate performance reports
    - View financial reports
    - User activity reports
- **Notification Management**
    - Configure notification settings
    - Send custom notifications to users
    - View notification history