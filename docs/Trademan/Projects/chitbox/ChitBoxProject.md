# Chitbox Project

**System Design for User App**

## User-based Requirements

**Difference between Operator & Agent**

Only Operator can:

- Create/View/Edit/Delete all kinds of details related to Chits as well as the Users.
- Operator is the one who conducts the Auctions (Agents do not & don’t have control of it.)
- Download Company-wide reports as well as individual reports & view dashboards
    - Should be able to track all user status inlcuding well-performers, defaulters etc.
    - Agent-wise performance
    - Chit-fund wise performance
    - User-wise performance & details
    - Financial Statements

Agents can:

- Verify, Add (with approval from Operator) & View users
- Monitor/View User activity + Monitor Claims
- Ability to create chits with approval from Operator
- Perform Document verification
- Perform Distribution of Dividends
- Rewards monitoring & approval
- Download reports & view dashboards
    - Tracking monthly collections
    - Monthly disbursements of auction winners etc.
    - Financial Statements
        - Dividends
        - Auctions Stats
        - Collections
        - P&L Graphs

Users can:

- Verify their identity & KYC
- Can view their portfolio/dashboard summaries
- Can join chits, View info of chits, exit/cancel chits
- Participate in Auctions/Perform bidding in auctions
- They must be able to claim their cash prize
- View their transactions & history

## Functional Requirements

[Functional Requirements](../chitbox/projectmanagement/FunctionalRequirements.md) 

[Process Payment Sequence Diagram](https://whimsical.com/process-payment-EWWmfP2nc5M7gbC5wkMTC4@2Ux7TurymNATTiFreXdd)

[Place a Bid Sequence Diagram](https://whimsical.com/place-bid-QGqyrHwRxpHpG2SLrnn462@6HYTAunKLgTVBLRPV2D2SejJsGLik87v4uQUjiRF3JFvKsV)

[Create a chit fund Sequence Diagram](https://whimsical.com/create-chitfund-W28LcTJrQvxGzuwwboFJnA@6HYTAunKLgTVBLRPV2D2SejJsGLik87v4uQUjiRF3JFvKsV)

[User Registration Sequence Diagram](https://whimsical.com/user-registration-9Yk2JstVnVLKF8PxsmkbRR) 

[Payment Process](https://whimsical.com/payment-processing-TX1bFNZ4x7ZFJ5Mxpd3bKv)

[https://whimsical.com/bidding-system-TsNH2bxbyWhCQKPV5unjz7](https://whimsical.com/bidding-system-TsNH2bxbyWhCQKPV5unjz7)

[https://whimsical.com/chitfund-management-4WpCxSsHQvitAFsWJo9z6n](https://whimsical.com/chitfund-management-4WpCxSsHQvitAFsWJo9z6n)

[https://whimsical.com/chitfund-management-91BxVCEpVoe2YxXaMm9QM@2Ux7TurymNVSeNmuW77Z](https://whimsical.com/chitfund-management-91BxVCEpVoe2YxXaMm9QM@2Ux7TurymNVSeNmuW77Z)

[https://whimsical.com/user-registration-and-login-DvDLktgsBotTvTL5igwMAz](https://whimsical.com/user-registration-and-login-DvDLktgsBotTvTL5igwMAz)

[Chitfund System plan](https://whimsical.com/chitfund-system-plan-UMJ61pGVA7AjAXazEJTbE6)

[System Design plan](../chitbox/projectmanagement/SystemDesign.md)

## Data/User Flow Diagrams

### Todo List

- [ ]  Premium Payment, Defaulting & Joining Auction Logic is not added in the flow!
    - [ ]  If he exceeds the due date, he can’t join the Auction
    - [ ]  Logic for free loop period - 10 days.
    - [ ]  If he pays after due date+10, pay payment with penalty!
- [ ]  Notifications Design
- [ ]  

## App Flow Diagram

- Google Play Store documentation
    
    [Google playstore Account creation Account](../chitbox/projectmanagement/GooglePlaystoreAccountCreation.md)
    
- Testflight
    
    [Test flight documentation](../chitbox/projectmanagement/TestFlightDocs.md)
    
    
- API Sethu and MSG91
    
    [APi Sethu documentation](../chitbox/apisethudocs/ApiSethuDocs.md)
    
- 

[Flutter  code ](../chitbox/fluttercode/FlutterCodeReviewForm.md)

# System Design for Admin Panel Dashboard

[Admin Tab Flow](https://app.eraser.io/workspace/YfH5lFP6lZi4P95gG2zi?origin=share)

[Project Management](../chitbox/projectmanagement/ProjectManagement.md)

