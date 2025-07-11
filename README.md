# Car Management and Shopping System

[cite_start]This application is a GUI-based car management and shopping system where users can log in to view cars, add them to their cart, and make purchases. [cite: 2] [cite_start]Admins have the ability to manage the database of cars and users. [cite: 3]

## Features

### For Users:
* [cite_start]Login or create a new account. [cite: 6]
* [cite_start]Browse the collection of available cars. [cite: 7]
* [cite_start]Add desired cars to a personal shopping cart and view the total cost. [cite: 8]
* [cite_start]Finalize purchases if their account balance is sufficient. [cite: 9]

### For Admins:
* [cite_start]Login using predefined administrator credentials. [cite: 11]
* [cite_start]Manage the car inventory by adding, updating, or deleting car entries. [cite: 12]
* [cite_start]Manage user accounts, including adding, updating, or deleting users. [cite: 13]

### Data Persistence:
* [cite_start]All user, car, and cart data are saved to files, ensuring data is retained between sessions. [cite: 15]

## How to Use

### For Users:

1.  **Login or Create a New Account:**
    * [cite_start]On the start screen, click the “User” button. [cite: 19]
    * [cite_start]Enter your username and password to log in. [cite: 20]
    * [cite_start]If you are a new user, enter your desired details and click “Create Account”. [cite: 21]

2.  **Browse Available Cars:**
    * [cite_start]Once logged in, you will be presented with a list of available cars, showing their brand, model, price, and a brief description. [cite: 23]
    * [cite_start]Click on any car to view its full description. [cite: 24]

3.  **Add Cars to Cart and View Total Cost:**
    * [cite_start]When viewing a car's details, click the “Add to Cart” button. [cite: 26]
    * [cite_start]The selected car will be added to your shopping cart, where you can also see the updated total cost. [cite: 27]

4.  **Finalize the Purchase:**
    * [cite_start]Click “Check Out” to review all the cars in your cart along with the final cost. [cite: 29]
    * [cite_start]If you have a sufficient balance, click “Purchase” to complete the transaction. [cite: 30]

5.  **Logout:**
    * [cite_start]Click the “Back” button to return to the main menu. [cite: 32]

### For Admins:

1.  **Login with Predefined Credentials:**
    * [cite_start]From the start screen, select “Admin”. [cite: 35]
    * [cite_start]Use the following credentials to log in: [cite: 36]
        * [cite_start]**Username:** admin [cite: 37]
        * [cite_start]**Password:** admin123 [cite: 38]

2.  **Manage Cars (Add, Update, or Delete):**
    * [cite_start]Navigate to the “Cars” section from the admin panel. [cite: 40]
    * **Add a new car:**
        1.  [cite_start]Click on “Add a new car”. [cite: 42]
        2.  [cite_start]Complete the form with the car's brand, model, price, description, and select an image. [cite: 43]
    * **Update a car:**
        1.  [cite_start]Click the “Update” button next to the car you wish to edit. [cite: 45]
        2.  [cite_start]Modify the necessary details and save your changes. [cite: 46]
    * **Delete a car:**
        1.  [cite_start]Click the “Delete” button next to the car you want to remove. [cite: 48]

3.  **Manage Users (Add, Update, or Delete):**
    * [cite_start]From the admin panel, go to the “Users” section. [cite: 50]
    * **Add a new user:**
        1.  [cite_start]Click “Add a new user”. [cite: 52]
        2.  [cite_start]Enter the new user's username, password, and initial balance. [cite: 53]
    * **Update a user:**
        1.  [cite_start]Click “Update” next to the user account you need to modify. [cite: 55]
        2.  [cite_start]Change the details as required and save. [cite: 56]
    * **Delete a user:**
        1.  [cite_start]Click “Delete” next to the user you wish to remove. [cite: 58]

4.  **Logout:**
    * [cite_start]Click “Log Out” to go back to the main menu. [cite: 60]

## Files

### Data Files:
* [cite_start]`user_database.pickle`: Stores all user details. [cite: 63]
* [cite_start]`car_database.pickle`: Contains the details of all cars. [cite: 64]
* [cite_start]`cart.pickle`: Holds the contents of the shopping cart. [cite: 65]

### Images:
* [cite_start]Ensure that all car images (e.g., `bmw.png`, `audi.png`) are located in the same directory as the script for them to be displayed correctly in the GUI. [cite: 67]

## Tips
* [cite_start]Passwords are case-sensitive. [cite: 69]
* [cite_start]Admins are not able to purchase cars or access user-specific functionalities. [cite: 70]
* [cite_start]To prevent missing images in the application, make sure all required image files are present. [cite: 71]

## Common Issues

* **No Cars or Users Found:**
    * If the Pickle files (`user_database.pickle`, `car_database.pickle`) are missing or have been corrupted, default data will be loaded for the cars. [cite_start]However, users will need to create new accounts. [cite: 74]
* **Insufficient Balance:**
    * [cite_start]Users are only able to purchase cars if their account balance is greater than or equal to the total cost of the items in their cart. [cite: 76]
* **File Not Found Errors:**
    * [cite_start]These errors typically occur if required files, such as images or Pickle files, are not in the correct directory. [cite: 78]