# Car Management and Shopping System

This application is a GUI-based car management and shopping system where users can log in to view cars, add them to their cart, and make purchases. Admins can manage the database of cars and users.

---

## Features

### 1. Users
- Login or create a new account.
- Browse available cars.
- Add cars to the cart and view the total cost.
- Finalize the purchase (if sufficient balance is available).

### 2. Admins
- Login using predefined credentials.
- Manage cars: add, update, or delete.
- Manage users: add, update, or delete.

### 3. Data Persistence
- User, car, and cart data are saved between sessions using files.

---

## How to Use

### For Users

#### 1. Login or Create a New Account
- Click **“User”** on the start screen.
- Enter your username and password.
- If you don’t have an account, enter details and click **“Create Account”**.

#### 2. Browse Available Cars
- After logging in, you will see a list of available cars with details (brand, model, price, and description).
- Click on a car to view its full description.

#### 3. Add Cars to the Cart and View Total Cost
- While viewing a car, click **“Add to Cart.”**
- The car will be added to your shopping cart, and the total cost will be shown.

#### 4. Finalize the Purchase
- Click **“Check Out”** to view all cars in your cart and the total cost.
- Click **“Purchase”** to finalize your order (only if you have enough balance).

#### 5. Logout
- Click **“Back”** to return to the main menu.

---

### For Admins

#### 1. Login
- Click **“Admin”** on the start screen.
- Use the credentials:
  - **Username:** `admin`
  - **Password:** `admin123`

#### 2. Manage Cars
- Click **“Cars”** in the admin panel.

##### Add a New Car
1. Click **“Add a new car”**
2. Fill in brand, model, price, description, and select an image.

##### Update a Car
1. Click **“Update”** next to the car you want to edit.
2. Modify the details and save.

##### Delete a Car
- Click **“Delete”** next to the car you want to remove.

#### 3. Manage Users
- Click **“Users”** in the admin panel.

##### Add a New User
1. Click **“Add a new user”**
2. Fill in the username, password, and initial balance.

##### Update a User
1. Click **“Update”** next to the user you want to edit.
2. Modify the details and save.

##### Delete a User
- Click **“Delete”** next to the user you want to remove.

#### 4. Logout
- Click **“Log Out”** to return to the main menu.

---

## Files

### 1. Data Files
- `user_database.pickle` — stores user details
- `car_database.pickle` — stores car details
- `cart.pickle` — stores the shopping cart

### 2. Images
- Ensure car images (e.g., `bmw.png`, `audi.png`) are in the same directory as the script.

---

## Tips

- Passwords are **case-sensitive**.
- Admins **cannot** purchase cars or use user functionalities.
- Ensure all required **image files exist** to avoid missing images in the GUI.

---

## Common Issues

### 1. No Cars or Users Found
- If the Pickle files are missing or corrupted, default data will be used for cars.
- Users will need to create accounts again.

### 2. Insufficient Balance
- Users can only purchase cars if their balance covers the total cost.

### 3. File Not Found Errors
- Make sure all required files (images and `.pickle` files) are in the correct location.
