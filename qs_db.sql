CREATE DATABASE IF NOT EXISTS qs_db;
USE qs_db;

/*
This SQL is only for demonstrate and inspect db internal, query and transaction all performed by Django
*/

CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role ENUM('customer', 'admin') NOT NULL
);

CREATE TABLE Products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Category VARCHAR(255),
    Description TEXT,
    ImageName VARCHAR(255),
    Price DECIMAL(10, 2) NOT NULL,
    Discount DECIMAL(10, 2),
    StockQuantity INT NOT NULL,
    Sales INT DEFAULT 0
);

CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    OrderDate DATETIME NOT NULL,
    Status ENUM('Placed', 'Paid', 'Shipped', 'Completed', 'Cancelled') NOT NULL,
    TotalPrice DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE OrderDetails (
    OrderDetailsID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT NOT NULL,
    PriceAtPurchase DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE RatingsReviews (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    UserID INT,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Comment TEXT,
    ReviewDate DATETIME NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Transactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    TransactionDate DATETIME NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    PaymentMethod ENUM('Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer'),
    Status ENUM('Success', 'Pending', 'Failed', 'Refunded') NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

CREATE TABLE SupportTicket (
    TicketID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Subject VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    Status ENUM('Open', 'In Progress', 'Resolved', 'Closed') NOT NULL DEFAULT 'Open',
    CreationDate DATETIME NOT NULL,
    ResolutionDate DATETIME,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

SELECT * FROM shop_order;
SELECT * FROM shop_user;
SELECT * FROM shop_product;
