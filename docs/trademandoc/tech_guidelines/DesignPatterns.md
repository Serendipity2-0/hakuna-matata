# Design Patterns: Singleton Pattern

## Agenda
1. **What is the concept?**
2. **Why is it important?**
3. **How does it work?**
4. **What problems does the Singleton Pattern solve?**
5. **When should we use it?**

This guide also includes a Zerodha-based use case, with code examples in Django, Flutter, Next.js, Python, JavaScript, Dart, and TypeScript.

---

## Singleton Pattern

### 1. **What is the concept?**
The Singleton Pattern is a design pattern that ensures a class has only **one instance** and provides a global point of access to that instance. It restricts the creation of multiple objects of the same class and returns the same instance every time it’s called.

### 2. **Why is it important?**
   - **Control resource usage**: Singleton is useful when you want to limit resource consumption, like managing database connections or logging systems.
   - **Consistency**: Ensures consistent access to shared resources. For example, in an application that interacts with an API, only one instance manages that communication.
   - **Global access**: Provides easy global access to objects from different parts of an application.

### 3. **How does it work?**
To implement the Singleton pattern:
   - Make the constructor **private** or **restricted**.
   - Use a static method to **create** or **return** the instance.
   - Ensure the class can’t be instantiated more than once.

### 4. **Problem Statement**
Suppose you’re building a trading platform (like Zerodha). You only need **one database connection** shared across your entire application to maintain efficiency and reduce costs. Opening multiple connections for each user session could overload the database server.

### 5. **When should we use it?**
   - **Database connection pools**: As in Zerodha's case, where one shared database connection reduces resource load.
   - **Logging systems**: One logger instance that writes to a file or console suffices.
   - **Configuration managers**: A single object can manage the application’s settings.


- Code Examples
    - **Django (Python)**:
        
    python

        class DatabaseConnection:
            _instance = None
        
            def __new__(cls):
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    # Initialize the database connection here
                return cls._instance
        
        # Using Singleton
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        
        print(db1 == db2)  # True, both instances are the same
        
    - **Flutter (Dart)**:    
    
    Dart

        class DatabaseConnection {
            static final DatabaseConnection _instance = DatabaseConnection._internal();

            factory DatabaseConnection() {
              return _instance;
            }
        
            DatabaseConnection._internal();  // Private constructor
        }
        
        // Using Singleton
        final db1 = DatabaseConnection();
        final db2 = DatabaseConnection();
        
        print(db1 == db2);  // True

    - **Next.js (JavaScript/TypeScript)**:
    
    JavaScript/TypeScript

        class DatabaseConnection {
            static instance;
        
            constructor() {
                if (!DatabaseConnection.instance) {
                    this.connection = "DB connection";
                    DatabaseConnection.instance = this;
                }
                return DatabaseConnection.instance;
            }
        }

       const db1 = new DatabaseConnection();
       const db2 = new DatabaseConnection();
        
       console.log(db1 === db2);  // True

---

## Builder Pattern
### 1. **What is the concept?**
The Builder Pattern is a design pattern used to construct complex objects step by step. Unlike the Singleton, it doesn’t restrict you to a single instance, but instead provides a way to construct an object by separating its construction logic from its representation.
        
### 2. **Why is it important?**
 - **Simplifies complex object creation**: If an object has multiple optional properties or settings, Builder Pattern simplifies object creation by making it readable and flexible.
- **Separation of concerns**: It separates the logic of object construction from the actual object itself.
- **Fluent interface**: You can build objects step by step in a readable and intuitive way.

### 3. **How does it work?**
        
In the Builder pattern:
        
- You create a **builder class** that has methods to set the various attributes of the object.
- Once all parts of the object are set, you **build** the final object.

### 4. **Problem statement**:
        
Imagine Zerodha wants to create a trade order where users can set a variety of properties (e.g., buy/sell, stock symbol, limit price, stop loss, etc.). A simple constructor might not handle all of these options in an intuitive way. The Builder Pattern allows you to gradually set up the trade order with optional configurations before finalizing it.
        
### 5. **When should we use it?**
- **Complex objects** with lots of optional properties.
- **Fluent API design**: If you want a clean, step-by-step object creation process.
- **Immutable objects**: You can use a builder to create objects and ensure they are immutable once built.


- Code Examples
    - **Django (Python)**:
        
    python

        class TradeOrder:
            def __init__(self, stock_symbol, quantity, order_type, price=None):
                self.stock_symbol = stock_symbol
                self.quantity = quantity
                self.order_type = order_type
                self.price = price
        
        class TradeOrderBuilder:
            def __init__(self):
                self._stock_symbol = None
                self._quantity = None
                self._order_type = None
                self._price = None
        
            def set_stock_symbol(self, symbol):
                self._stock_symbol = symbol
                return self
        
            def set_quantity(self, quantity):
                self._quantity = quantity
                return self
        
            def set_order_type(self, order_type):
                self._order_type = order_type
                return self
        
            def set_price(self, price):
                self._price = price
                return self
        
            def build(self):
                return TradeOrder(self._stock_symbol, self._quantity, self._order_type, self._price)
        
        # Usage:
        builder = TradeOrderBuilder()
        order = builder.set_stock_symbol('AAPL').set_quantity(100).set_order_type('buy').set_price(150).build()
        print(order.__dict__)
        
    - **Flutter (Dart)**:
    
    Dart

        class TradeOrder {
            String stockSymbol;
            int quantity;
            String orderType;
            double? price;
        
            TradeOrder({required this.stockSymbol, required this.quantity, required this.orderType, this.price});
        }
        
        class TradeOrderBuilder {
            String? _stockSymbol;
            int? _quantity;
            String? _orderType;
            double? _price;
        
            TradeOrderBuilder setStockSymbol(String symbol) {
                _stockSymbol = symbol;
                return this;
            }
        
            TradeOrderBuilder setQuantity(int quantity) {
                _quantity = quantity;
                return this;
            }
        
            TradeOrderBuilder setOrderType(String orderType) {
                _orderType = orderType;
                return this;
            }
        
            TradeOrderBuilder setPrice(double price) {
                _price = price;
                return this;
            }
        
            TradeOrder build() {
                return TradeOrder(
                    stockSymbol: _stockSymbol!, quantity: _quantity!, orderType: _orderType!, price: _price);
            }
        }
        
        // Usage
        final order = TradeOrderBuilder()
            .setStockSymbol('AAPL')
            .setQuantity(100)
            .setOrderType('buy')
            .setPrice(150)
            .build();                                
        
        print(order);
        
    - **Nextjs (JavaScript/TypeScript)**:
    
    JavaScript/TypeScript

        class TradeOrder {
            constructor(public stockSymbol: string, public quantity: number, public orderType: string, public price?: number) {}
        }
        
        class TradeOrderBuilder {
            private stockSymbol: string | null = null;
            private quantity: number | null = null;
            private orderType: string | null = null;
            private price?: number;
        
            setStockSymbol(symbol: string): this {
                this.stockSymbol = symbol;
                return this;
            }
        
            setQuantity(quantity: number): this {
                this.quantity = quantity;
                return this;
            }
        
            setOrderType(orderType: string): this {
                this.orderType = orderType;
                return this;
            }
        
            setPrice(price: number): this {
                this.price = price;
                return this;
            }
        
            build(): TradeOrder {
                return new TradeOrder(this.stockSymbol!, this.quantity!, this.orderType!, this.price);
            }
        }
        
        // Usage:
        const order = new TradeOrderBuilder()
            .setStockSymbol("AAPL")
            .setQuantity(100)
            .setOrderType("buy")
            .setPrice(150)
            .build();
        
        console.log(order);


### Prompt used
    can you structures this one with this  below structureAgenda :
    what is concept
    why
    how
    what problem statement  that 2. Singleton Pattern
    3. Builder Pattern   solves   in which scenerio we have to use
    
    Problrm  statement of usecase
    Discuss each topic in detail what is  and why we have to take decission to use this pattern single patterns and builder pattern  only
    what concept is all about and then talk problem in usecse what is 2. Singleton Pattern
    3. Builder Pattern hoow can we utilize this : 2. Singleton Pattern
    3. Builder Pattern   and what problems solves with usecase one by one with  what is 2. Singleton Pattern
    3. Builder Pattern how can we use 2. Singleton Pattern
    3. Builder Pattern to utilize this pattern
    
    can you  discuss Zerodha usecase  for this pattern
    with code examples  discussing frameworks and language
    real world example in django,  Flutter , Nextjs and  as well as python ,js and dart and typescript
    make it  very and laymann terms so that everyone can understand about this in 20 minutes wee discuss about this pattern

---

## Bridge Pattern
### 1. **What is the concept?**
The Bridge Pattern is a structural design pattern that decouples an abstraction from its implementation, allowing them to vary independently. Essentially, it separates the "interface" from the "implementation" and allows the two to evolve separately without affecting each other.

### 2. **Why is it important?**
- **Flexibility**: It allows you to change both the abstraction (interface) and implementation independently, which is useful when you have many possible classes or implementations that need to interact with each other.
- **Maintainability**: By separating the abstraction and implementation, changes to one side don’t affect the other, making the code easier to maintain.
- **Reduces complexity**: In systems where both abstraction and implementation can have multiple variations, it helps reduce the complexity of class hierarchies.

### 3. **How does it work?**
The Bridge Pattern works by creating two separate class hierarchies:
        
- **Abstraction hierarchy**: Defines the high-level control interface.
- **Implementation hierarchy**: Defines the low-level operations.
        
The abstraction has a reference to an object in the implementation hierarchy, and it can delegate work to the implementation. This way, you can mix and match implementations without rewriting code

### 4. **Problem statement**:
Let’s say you are building a **payment gateway** in an e-commerce platform (like Amazon). You need different types of payment methods like **credit card, bank transfer, and digital wallets**. You also want to support different platforms such as **web and mobile apps**. Without the Bridge Pattern, you would need to create a separate class for each combination of payment method and platform, leading to a bloated and complex class structure

### 5. **When should we use it?**
- When both the abstraction and the implementation can evolve independently.
- When you want to avoid a proliferation of classes.
- When your code has complex hierarchies of classes with multiple variations.

- Code Examples        
    - **Django (Python)**:
        
    python

        class PaymentMethod:
            def __init__(self, name, description):
                self.name = name
                self.description = description
        
        class CreditCard(PaymentMethod):
            def __init__(self, name, description, card_number, expiry_date):
                super().__init__(name, description)
                self.card_number = card_number
                self.expiry_date = expiry_date
        
        class BankTransfer(PaymentMethod):
            def __init__(self, name, description, account_number, routing_number):
                super().__init__(name, description)
                self.account_number = account_number
                self.routing_number = routing_number
        
        # Abstraction hierarchy
        class PaymentProcessor:
            def __init__(self, payment_method):
                self.payment_method = payment_method
        
            def pay(self, amount):
                return self.payment_gateway.
                process_payment(amount)

        # Usage
        payment_method = PaymentProcessor(CreditCardPayment())
        print(payment_method.pay(1000))  # Processing credit card payment of 1000    
        
    - **Flutter (Dart)**:                        
    
    Dart

            // Implementation Hierarchy
            abstract class PaymentGateway {
              String processPayment(double amount);
            }
            
            class CreditCardPayment implements PaymentGateway {
              @override
              String processPayment(double amount) => "Processing credit card payment of $amount";
            }
            
            class BankTransferPayment implements PaymentGateway {
              @override
              String processPayment(double amount) => "Processing bank transfer payment of $amount";
            }
            
            // Abstraction Hierarchy
            class PaymentProcessor {
              final PaymentGateway paymentGateway;
            
              PaymentProcessor(this.paymentGateway);
            
              String pay(double amount) {
                return paymentGateway.processPayment(amount);
              }
            }
            
            // Usage
            final paymentProcessor = PaymentProcessor(CreditCardPayment());
            print(paymentProcessor.pay(1000));  // Processing credit card payment of 1000                       
            
    - **Nextjs (JavaScript/TypeScript)**:
    
    JavaScript/TypeScript 
        
                        // Implementation Hierarchy
            interface PaymentGateway {
              processPayment(amount: number): string;
            }
            
            class CreditCardPayment implements PaymentGateway {
              processPayment(amount: number): string {
                return `Processing credit card payment of ${amount}`;
              }
            }
            
            class BankTransferPayment implements PaymentGateway {
              processPayment(amount: number): string {
                return `Processing bank transfer payment of ${amount}`;
              }
            }
            
            // Abstraction Hierarchy
            class PaymentProcessor {
              constructor(private paymentGateway: PaymentGateway) {}
            
              pay(amount: number): string {
                return this.paymentGateway.processPayment(amount);
              }
            }
            
            // Usage
            const paymentProcessor = new PaymentProcessor(new CreditCardPayment());
            console.log(paymentProcessor.pay(1000));  // Processing credit card payment of 1000


## Fascade Pattern
### 1. **What is the concept?**
The Facade Pattern is a structural design pattern that provides a simplified interface to a complex system of classes, libraries, or frameworks. It "hides" the complexity of the system behind a single unified interface that is easier to understand and use.
        
### 2. **Why is it important?**
- **Simplifies complex systems**: When a system becomes too complex or has too many classes, a Facade can simplify interaction with it by hiding unnecessary details.
- **Encapsulation**: It keeps the implementation details hidden from the client, promoting encapsulation.
- **Ease of use**: Users interact with a cleaner, more intuitive interface without needing to understand the inner workings of the system.

### 3. **How does it work?**
The Facade acts as a wrapper class that calls multiple underlying systems or APIs, hiding their complexity. The client only interacts with the Facade, which delegates the required functionality to appropriate classes.
        
### 4. **Problem statement**:
Suppose you are building a **trading application** (like Zerodha). You have various subsystems such as **order placement**, **portfolio management**, and **market data retrieval**. Instead of exposing the complexity of interacting with each of these systems, you provide a simple Facade for users, allowing them to place orders or view their portfolio with a single call.
        
### 5. **When should we use it?**
- When you need to **simplify** the interaction with a complex system.
- When you want to provide a clean, unified interface for a set of APIs or libraries.
- When you want to decouple a client from complex subsystems.

- Code Examples        
    - **Django (Python)**:
            
            
            # Complex subsystems
            class OrderPlacement:
                def place_order(self, stock_symbol, quantity):
                    return f"Order placed for {quantity} shares of {stock_symbol}"
            
            class PortfolioManagement:
                def view_portfolio(self):
                    return "Viewing portfolio details"
            
            class MarketDataRetrieval:
                def get_market_data(self):
                    return "Retrieving market data"
            
            # Facade
            class TradingFacade:
                def __init__(self):
                    self.order_placement = OrderPlacement()
                    self.portfolio_management = PortfolioManagement()
                    self.market_data = MarketDataRetrieval()
            
                def place_order(self, stock_symbol, quantity):
                    return self.order_placement.place_order(stock_symbol, quantity)
            
                def view_portfolio(self):
                    return self.portfolio_management.view_portfolio()
            
                def get_market_data(self):
                    return self.market_data.get_market_data()
            
            # Usage
            trading_facade = TradingFacade()
            print(trading_facade.place_order("AAPL", 100))
            print(trading_facade.view_portfolio())
            print(trading_facade.get_market_data())
            
            
            
    - **Flutter (Dart)**:                        
                
            // Complex subsystems
            class OrderPlacement {
              String placeOrder(String stockSymbol, int quantity) {
                return "Order placed for $quantity shares of $stockSymbol";
              }
            }
            
            class PortfolioManagement {
              String viewPortfolio() {
                return "Viewing portfolio details";
              }
            }
            
            class MarketDataRetrieval {
              String getMarketData() {
                return "Retrieving market data";
              }
            }
            
            // Facade
            class TradingFacade {
              final OrderPlacement _orderPlacement = OrderPlacement();
              final PortfolioManagement _portfolioManagement = PortfolioManagement();
              final MarketDataRetrieval _marketData = MarketDataRetrieval();
            
              String placeOrder(String stockSymbol, int quantity) {
                return _orderPlacement.placeOrder(stockSymbol, quantity);
              }
            
              String viewPortfolio() {
                return _portfolioManagement.viewPortfolio();
              }
            
              String getMarketData() {
                return _marketData.getMarketData();
              }
            }
            
            // Usage
            final tradingFacade = TradingFacade();
            print(tradingFacade.placeOrder("AAPL", 100));
            print(tradingFacade.viewPortfolio());
            print(tradingFacade.getMarketData());
            
            
            
    - **Nextjs**        
            
            
            // Complex subsystems
            class OrderPlacement {
              placeOrder(stockSymbol: string, quantity: number): string {
                return `Order placed for ${quantity} shares of ${stockSymbol}`;
              }
            }
            
            class PortfolioManagement {
              viewPortfolio(): string {
                return "Viewing portfolio details";
              }
            }
            
            class MarketDataRetrieval {
              getMarketData(): string {
                return "Retrieving market data";
              }
            }
            
            // Facade
            class TradingFacade {
              private orderPlacement = new OrderPlacement();
              private portfolioManagement = new PortfolioManagement();
              private marketData = new MarketDataRetrieval();
            
              placeOrder(stockSymbol: string, quantity: number): string {
                return this.orderPlacement.placeOrder(stockSymbol, quantity);
              }
            
              viewPortfolio(): string {
                return this.portfolioManagement.viewPortfolio();
              }
            
              getMarketData(): string {
                return this.marketData.getMarketData();
              }
            }
            
            // Usage
            const tradingFacade = new TradingFacade();
            console.log(tradingFacade.placeOrder("AAPL", 100));
            console.log(tradingFacade.viewPortfolio());
            console.log(tradingFacade.getMarketData());

    ### 
    
## Iterator and chain of reponsibility
    
    
    ### Prompts
        
        Act as   GOF Author Expert in Design  patterns
        
        Go through this reference refactoring guru :
        Search  web on below link  take concepts
        [https://refactoring.guru/design-patterns](https://refactoring.guru/design-patterns)
        
        Task:
        
        and then do below tasks
        
        can you structures this one with this  below structure
        -Agenda :
        -what is concept
        
        - why the name has given to that pattern
        - what problems solves to common problem
        - in what common problems we can apply this usecase
        -why
        - how
        - what makes it unique
        what problem statement that Iterator Pattern
        Chain of Responsibility solves in which scenerio we have to use
        - Problem statement of usecase
        Discuss each topic in detail what is and why we have to take decission to use this pattern single patterns and builder pattern only
        what concept is all about and then talk problem in usecse what isIterator Pattern
        Chain of Responsibility hoow can we utilize this :Iterator Pattern
        Chain of Responsibility and what problems solves with usecase one by one with what is Iterator Pattern
        Chain of Responsibility how can we use Iterator Pattern
        Chain of Responsibility to utilize this pattern
        
        can you  discuss Zerodha usecase  for this pattern
        with code examples  in python
        
        make it  very and laymann terms so that everyone can understand about this in 20 minutes wee discuss about this pattern

### 1. Agenda:
    
1. **What is the Concept?**
2. **Why the Name?**
3. **What Common Problems Do These Patterns Solve?**
4. **Common Scenarios Where We Apply Them**
5. **Why These Patterns Work**
6. **How They Are Implemented**
7. **What Makes Them Unique?**
8. **Problem Statements in Use Cases**
9. **Using These Patterns in Zerodha with Code Examples**
    
### Iterator Pattern
    
### 1. **What is the Concept?**
    
The **Iterator Pattern** is a design pattern that provides a way to access elements of a collection (like a list, set, or array) sequentially without exposing its underlying structure. Think of it like a playlist of songs where you can "play next" or "rewind" to previous songs without needing to know the inner details of the playlist's structure.
    
### 2. **Why the Name?**
    
The name "Iterator" signifies its purpose: it "iterates" or goes through a collection step by step. It’s like a guide that leads you through the collection one item at a time.
    
### 3. **What Problems Does it Solve?**
    
In programming, different collections (like lists, stacks, or trees) store items differently. Without the Iterator pattern, you would need to know each collection's structure to navigate it. Iterator solves this by providing a standard way to traverse any collection.
    
### 4. **Common Scenarios to Apply the Iterator Pattern**
    
1. Navigating through complex collections without knowing their underlying structures.
2. Performing sequential operations on items in a collection (e.g., summing numbers, finding matches).
3. Simplifying code by removing direct references to collection structures.
    
### 5. **Why Use the Iterator Pattern?**
    
This pattern makes it easier to add new types of collections because it provides a consistent interface for accessing elements, regardless of the collection type.
    
### 6. **How Is It Implemented?**
    
The Iterator pattern typically involves:
    
- **Iterator**: Defines methods to traverse a collection (e.g., `next`, `has_next`).
- **ConcreteIterator**: Implements the traversal.
- **Aggregate**: Collection interface.
- **ConcreteAggregate**: The specific collection (e.g., list, array) being iterated.
    
### 7. **What Makes It Unique?**
    
Its ability to abstract the traversal process, allowing you to work with collections interchangeably without modifying the traversal code.
    
### 8. **Problem Statement of Use Case: Zerodha Example**
    
In Zerodha’s platform, let’s say we need to track stock prices from multiple lists (like watchlists or portfolios) and access them one by one to check conditions (e.g., price limit alerts). We can use the Iterator pattern to abstract the access.
    
- Code Examples        
    - **Django (Python)**:
        
    python
    
        class StockIterator:        
            def __init__(self, stocks):
                self.stocks = stocks
                self.index = 0
        
            def has_next(self):
                return self.index < len(self.stocks)
        
            def next(self):
                if self.has_next():
                    stock = self.stocks[self.index]
                    self.index += 1
                    return stock
                else:
                    raise StopIteration
        
        class StockCollection:
            def __init__(self):
                self.stocks = []
        
            def add_stock(self, stock):
                self.stocks.append(stock)
        
            def __iter__(self):
                return StockIterator(self.stocks)
        
        # Zerodha Use Case
        portfolio = StockCollection()
        portfolio.add_stock("Tata Motors")
        portfolio.add_stock("Reliance")
        portfolio.add_stock("Infosys")
        
        for stock in portfolio:
            print(f"Tracking stock: {stock}")

    This example iterates over a portfolio of stocks, printing each one. The Iterator pattern ensures that Zerodha’s system can work with any collection of stocks seamlessly.
    
    ---

    
   