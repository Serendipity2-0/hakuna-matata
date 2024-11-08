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

    can you structures this one with this  below structure
    Agenda :
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

