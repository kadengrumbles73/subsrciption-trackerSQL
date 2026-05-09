# Overview

I did this project to practice applying my SQL relational database skills to real life programs.

I made a subscription tracker app that stores the subscriptions and payments in a SQLite database. I made made functions that takes user input and stores clean data in a database

{Provide a link to your YouTube demonstration. It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of how created the Relational Database.}

[Software Demo Video](https://youtu.be/M9JB7YnLsao)

# Relational Database

I used the SQLite library in python

I created two tables, the subscriptions and payment history tables. The subscription table holds the names, categories, price, and monthly bill date and the payment history.

# Development Environment

The tools I used was VScode with a SQLite viewer extension to view the SQLite database and interacted with the program using the terminal.

The language I used was python with the SQLite3 library.

# Useful Websites

- [W3 Schools](https://www.w3schools.com/sql/default.asp)
- [SQLite Tutorials](https://www.sqlitetutorial.net/)

# Future Work

- I need to make the data more consistent by adding more constraints to prevent crashing from user input. 
- I need to add a feature that actually shows you if your up to speed with payments.
- In the pay subscription function I need to put text that says how much is due.