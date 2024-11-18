# Documentation for chitbox auction process

### **AuctionScreen Documentation**

## **Overview**

The `AuctionScreen` is a core UI component in the ChitBox app that facilitates a live auction process for chit funds. It handles user interactions, animations, sounds, bid placement, and displays real-time updates on auction status. The screen is stateful and uses multiple controllers and state management tools to manage the complex auction flow.

This documentation outlines the core components, properties, methods, and functionality of the `AuctionScreen` class.

---

## **Key Features**

- **Live Auction Interface**: Displays auction data, including current bids, group dividends, and prize money.
- **Bid Placement**: Allows users to place bids via a sliding panel and provides real-time feedback.
- **Timers and Sounds**: Handles countdown timers and plays a ticking sound to create urgency during the final seconds of the auction.
- **Dialogs and Feedback**: Presents dialogs for bid confirmation, auction results, and handling edge cases like duplicate bids.

---

## **Class Structure**

 **AuctionScreen**:

The main `AuctionScreen` class is a `StatefulWidget` that displays the auction screen UI. It consists of the following key components:

1. **State Management:**
    - `AuctionScreenState`: The state class for `AuctionScreen`, which manages the auction data, timers, bid amounts, and UI updates.
2. **Controllers:**
    - `PanelController _panelController`: Controls the sliding panel that displays bid options.
    - `PageController _pageController`: Handles navigation between different pages of the app (New Chits, My Chits, Auction, Profile).
    - `TabController _tabController`: Controls the tab switching between "Live Auction" and "Upcoming Auction."
3. **Key Variables:**
    - **Auction Variables**:
        - `double currentHighestBid`: Stores the current highest bid in the auction.
        - `double maxBidAmount`: The maximum allowed bid based on the chit amount and configured bid percentage.
        - `double groupDividend`: The calculated dividend for the group, after subtracting the foreman's commission.
        - `double prizeMoney`: The remaining prize money after the highest bid is subtracted from the chit amount.
    - **Timers & Animation**:
        - `Timer? _countdownTimer`: A countdown timer used to track remaining auction time.
        - `AudioPlayer _audioPlayer`: Manages playing of audio files (e.g., tick sound when auction is about to end).
    - **Bid Data**:
        - `List<Map<String, String>> bidTableData`: Stores the bids placed by users during the auction.

---

## **Methods**

 **1. initState**

Initializes the state of the `AuctionScreen`. It sets up the tab controller, initial bid amounts, and starts the timer and arrow animation.

**Responsibilities**:

- Initializes `TabController`.
- Sets the initial highest bid and max bid amounts.
- Starts a periodic timer that handles the countdown.
- Triggers UI updates through `setState()`.

---

**2. dispose**

Cleans up resources used by the `AuctionScreen`. This includes disposing of the countdown timer, page controller, and audio player to prevent memory leaks.

**Responsibilities**:

- Cancels timers.
- Disposes of controllers and resources.

---

**3. _calculateGroupDividendAndPrizeMoney**

Calculates the group dividend and prize money after deducting the foreman’s commission from the chit amount.

**Parameters**:

- No parameters.

**Responsibilities**:

- Uses the `Config` class to get chit amounts and commission rates.
- Updates the state with the new dividend and prize money values.

---

 **4. _startArrowAnimation**

Starts a periodic timer to toggle the visibility of an arrow animation every second. This is used to indicate the slide-up functionality for placing bids.

---

 **5. _startCountdownTimer**

Starts the auction countdown timer and plays a ticking sound when the auction is about to end (less than 10 seconds remaining).

**Responsibilities**:

- Decrements the remaining time every second.
- Plays a sound when the countdown reaches 10 seconds or less.

---

 **6. _endAuction**

Ends the auction and triggers post-auction dialogs and actions. It closes the sliding panel, marks the auction as ended, and shows a custom countdown dialog for announcing the winner.

**Responsibilities**:

- Stops the auction timer.
- Closes the slide-up panel and shows the winner countdown dialog.

---

 **7. _showCountdownDialog**

Displays a custom countdown dialog that indicates the auction has ended and a winner will be announced soon. It plays a ticking sound during the countdown.

**Responsibilities**:

- Shows a custom dialog.
- Plays a sound for each second of the countdown.

---

 **8. _announceWinner**

Determines the winner by finding the highest bid from the `bidTableData`. If no valid bids are present, it shows a "No Winner" dialog.

**Responsibilities**:

- Loops through the bid data to find the highest bid.
- Displays a dialog announcing the winner or indicating no winner.

---

 **9. _placeBid**

Places a new bid after validating the bid amount. It updates the bid table and recalculates the group dividend and prize money. Also, checks for duplicate bids.

**Responsibilities**:

- Adds a new bid entry to `bidTableData`.
- Updates the current highest bid and recalculates financial data.
- Checks for duplicate bids and shows appropriate dialogs if needed.

---

## **UI Components**

 **AppBar and Bottom Navigation**

The AppBar is dynamically rendered based on the current screen:

- On the auction page, it shows a custom title and live indicator.
- On other pages (e.g., Profile, My Chits), it shows a simple centered title.

The bottom navigation bar allows switching between the app's major screens (`New Chits`, `My Chits`, `Auction`, `Profile`).

 **SlidingUpPanel**

This panel allows users to place a bid in the live auction. It includes:

- A slider to select the bid amount.
- A button to confirm the bid.
- Bid options are limited by the max bid amount and current highest bid.

 **BidInfoCard**

Displays financial information about the auction, such as the current highest bid, prize money, and group dividend.

---

## **Event Handling**

 **AuctionBloc and Events**

The screen uses the `AuctionBloc` to manage the auction state. The bloc handles:

- Starting the auction timer.
- Managing live updates for bids.
- Handling the end of the auction and announcing winners.

## **Dialogs**

- **Bid Confirmation Dialog**: Prompts the user to confirm their bid before submitting.
- **Winner Announcement Dialog**: Displays the auction winner and offers a reward claim option.
- **Duplicate Bid Dialog**: Informs the user if they attempt to place a duplicate bid.
- **No Winner Dialog**: Shown when no valid bids were placed in the auction.

---

## **Code Dependencies**

- **Config Class**: Holds the configuration for the auction, such as chit amount, bid size, commission rate, etc.
- **AuctionBloc and AuctionEvent**: Handles business logic and event-driven state management for the auction.
- **AudioPlayer**: Responsible for playing sound effects during the auction.

---

## **Conclusion**

The `AuctionScreen` integrates multiple components to create a feature-rich auction experience. It follows key principles of separating UI, logic, and state management, making it easier to maintain and extend. However, improvements can be made by further splitting large methods and abstracting business logic from the UI.

For more efficient and scalable development, consider the following:

- **Refactor large methods**: Breaking down complex methods into smaller, single-responsibility functions can enhance readability and maintainability.
- **Separate concerns**: Move business logic (e.g., bid calculations) into services or helper classes, aligning better with the clean code principles of separation of concerns.

Calculation of bid :

 **Understanding Bid Calculation in ChitBox Auction System**

The bid calculation in the ChitBox auction system is designed to ensure a fair and transparent process for both bidders and organizers, while maintaining key principles of a chit fund. The calculation primarily revolves around determining the current highest bid, the group dividend, and the prize money, considering various factors like the chit amount and foreman commission. Here's an explanation of how the bidding system works:

---

## **Core Concepts of Bid Calculation**

 **1. Chit Amount**

The **chit amount** represents the total fund value for which the participants are bidding. In a chit fund, members contribute a fixed amount regularly, and the collected amount is auctioned among the participants. The total chit amount is the value up for bidding and serves as the base for calculating various financial outcomes during the auction.

---

 **2. Foreman Commission**

The **foreman** is the person or entity managing the chit fund, and they charge a commission for their services. In the ChitBox auction system, the foreman's commission is calculated as a percentage of the total chit amount. This commission is deducted from the current bid to determine how much of the bid will be distributed among the group participants.

- **Example**: If the foreman commission rate is 5% and the chit amount is ₹2,00,000, the foreman commission will be ₹10,000.

---

 **3. Current Highest Bid**

The **current highest bid** is the amount that a participant is willing to bid for the chit amount. This bid is essential because it determines the final prize money and group dividend. Bidders compete by offering higher bids, and the one who bids the highest by the end of the auction wins the chit.

---

 **4. Group Dividend**

The **group dividend** is the portion of the current highest bid that is distributed among the other participants (non-winners). It is calculated by subtracting the foreman’s commission from the highest bid. This incentivizes the rest of the group, as they receive a portion of the winning bid amount as compensation.

- **Formula**:
    
    `Group Dividend = Current Highest Bid - Foreman Commission`
    
    - **Example**:
    If the current highest bid is ₹50,000 and the foreman commission is ₹10,000, the group dividend would be ₹40,000. This amount is shared among the other members of the chit fund.

---

 **5. Prize Money**

The **prize money** is the amount the highest bidder takes home. It is calculated by subtracting the current highest bid from the total chit amount. The lower the winning bid, the higher the prize money the winner receives.

- **Formula**:
    
    `Prize Money = Chit Amount - Current Highest Bid`
    
    - **Example**:
    If the chit amount is ₹2,00,000 and the highest bid is ₹50,000, the winner receives ₹1,50,000 as prize money.

---

 **6. Bid Increment**

To maintain structure and prevent trivial bidding, the ChitBox auction system has a **fixed bid increment**. This means that every new bid must increase by a specific amount (in this case, ₹500). This ensures smoother and more organized bidding, reducing the chances of minor incremental bids that would slow down the auction.

---

 **7. Maximum Bid**

The **maximum bid** is a limit set to ensure that the participants do not bid too high and leave little to no prize money. In ChitBox, the maximum bid is capped at 30% of the chit amount, meaning no bid can exceed 30% of the total chit value.

- **Example**:
If the chit amount is ₹2,00,000, the maximum allowed bid is ₹60,000. This ensures that there is always a significant amount of prize money left for the winning participant.

---

## **Summary of the Bid Calculation Process**

In the ChitBox auction system:

1. The total **chit amount** is set, which is the amount participants are bidding for.
2. The **foreman commission** is deducted from the highest bid.
3. The remaining amount from the highest bid becomes the **group dividend**, distributed to non-winners.
4. The **prize money** is the chit amount minus the highest bid, which goes to the winning bidder.
5. Bids must follow a predefined **increment** and cannot exceed the **maximum bid** limit (30% of the chit amount).

By structuring the bid calculation this way, ChitBox ensures that both the foreman and the participants benefit, while maintaining a balanced and fair auction process.