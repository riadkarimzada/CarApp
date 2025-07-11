"""
The main idea of this code is to implement a GUI-based car management and shopping application.
It supports user login, shopping cart functionality, and admin management for users and cars.
The app uses Pickle library to persist data, Tkinter for the graphical interface, Glob to automatically
gather all PNG files in the current directory instead of hard-coding the filenames and Math to specifically
calculate the number of rows needed for the “Available Cars” panel (the main user panel where available cars are shown).
"""

import glob
import pickle
import math
from tkinter import *
from tkinter import messagebox, ttk

#Shows a car with basic attributes: brand, model, price, description, and image.
class Car:
    def __init__(self, brand, model, price, description, photo):
        self.brand = brand
        self.model = model
        self.price = price
        self.description = description
        self.photo = photo

# Represents a user with a username, password, and an account balance.
class User:
    def __init__(self, username, password, balance=0.0):
        self.username = username
        self.password = password
        self.balance = balance

# Shows an admin user, extending the User class with authentication logic.
class Admin(User):
    # Stores admin credentials
    admin_credentials = {"admin": "admin123"}

    #Validates if the given username and password match the admin credentials
    def authenticate(self, username, password):
        return Admin.admin_credentials.get(username) == password

#Handles shopping cart functionality, including adding, removing, clearing, and saving items.
class Cart:
    def __init__(self):
        self.items = []
        self.load_cart()  # Loads saved cart data

    def add(self, car):
        self.items.append(car)
        print(f"{car.model} added to the cart!")

    def remove(self, car):
        if car in self.items:
            self.items.remove(car)
            print(f"{car.model} removed from the cart!")

    def clear(self):
        self.items = []
        print("Cart cleared!")

    #Calculates the total cost of all items in the cart.
    def get_total_cost(self):
        return sum(car.price for car in self.items)

    # Saves cart items to a file.
    def save_cart(self):
        with open('cart.pickle', 'wb') as f:
            pickle.dump(self.items, f)

    # Loads cart items from a file, or initializes as empty if the file doesn't exist.
    def load_cart(self):
        try:
            with open('cart.pickle', 'rb') as f:
                self.items = pickle.load(f)
        except FileNotFoundError:
            self.items = []

#Manages the database of cars, including adding, updating, deleting, and saving cars.
class CarDatabase:
    def __init__(self):
        self.cars = []
        self.load_car_database()  # Loads saved car data

    def add(self, car):
        self.cars.append(car)
        self.save_car_database()  # Saves changes to the database

    def update(self, index, updated_car):
        if 0 <= index < len(self.cars):
            self.cars[index] = updated_car
            self.save_car_database()

    def delete(self, index):
        if 0 <= index < len(self.cars):
            del self.cars[index]
            self.save_car_database()

    #Saves the car database to a file.
    def save_car_database(self):
        with open('car_database.pickle', 'wb') as f:
            pickle.dump(self.cars, f)

    # Loads the car database from a file, or initializes with default cars if the file doesn't exist.
    def load_car_database(self):
        try:
            with open('car_database.pickle', 'rb') as f:
                car_data = pickle.load(f)
                self.cars = [Car(**car) if isinstance(car, dict) else car for car in car_data]
        except FileNotFoundError:
            #default car data if no database exists.
            self.cars = [
                Car("Mercedes-Benz", "S500", 60000, "Luxury Sedan", "mers_s500.png"),
                Car("Mercedes-Benz", "G 63 AMG", 63000, "Brutal", "mers_gwagon.png"),
                Car("Volkswagen", "ID.6", 3500, "Compact Car", "vw.png"),
                Car("Porsche", "Panamera 4S", 22000, "Luxury Sports Car", "pors.png")
            ]

# Manages the database of users, including adding, updating, deleting, and authenticating users.
class UserDatabase:
    def __init__(self):
        self.users = {}
        self.load_user_database()  #loads saved user data

    def add(self, user):
        self.users[user.username] = user
        self.save_user_database()

    def update(self, username, updated_user):
        self.users[username] = updated_user
        self.save_user_database()

    def delete(self, username):
        if username in self.users:
            del self.users[username]
        self.save_user_database()

    def authenticate(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return user
        return None

    #saves the user database to a file.
    def save_user_database(self):
        with open('user_database.pickle', 'wb') as f:
            pickle.dump(self.users, f)

    # loads the user database from a file, or initializes as empty if the file doesn't exist.
    def load_user_database(self):
        try:
            with open('user_database.pickle', 'rb') as f:
                self.users = pickle.load(f)
                for username, data in self.users.items():
                    if isinstance(data, str):
                        self.users[username] = User(username, data, 0.0)
        except FileNotFoundError:
            self.users = {}

#The main application class, responsible for managing GUI components and interactions.
class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x1000")
        self.root.resizable(True, True)
        self.root.configure(bg='black')
        self.root.bind("<F11>", self.toggle_fullscreen)  #enables fullscreen toggling with F11 key

        self.cart = Cart()            #runs the shopping cart
        self.car_db = CarDatabase()   # runs the car database
        self.user_db = UserDatabase() #Runs the user database
        self.current_user = None      # Keeps track of the logged-in user

        self.start_panel()  #launches the start panel

    def toggle_fullscreen(self, event=None):
        #toggles fullscreen mode for the app window
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def start_panel(self):
        #Displays the initial panel with options to log in as admin, user, or exit
        start_frame = Frame(self.root, bg="black")
        start_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Button for admin login, goes to the admin login panel
        admin_btn = Button(start_frame, text="Admin", font=("Comic Sans Ms", 30),
                           command=self.login_panel_admin)
        admin_btn.place(relx=0.3, rely=0.3, relwidth=0.3)

        #Button for user login, goes to the user login pane
        user_btn = Button(start_frame, text="User", font=("Comic Sans Ms", 30),
                          command=self.login_panel_user)
        user_btn.place(relx=0.3, rely=0.45, relwidth=0.3)

        # Button to exit the application
        exit_btn = Button(start_frame, text="Exit", font=("Comic Sans Ms", 30),
                          command=self.root.quit)
        exit_btn.place(relx=0.3, rely=0.6, relwidth=0.3)

    def login_panel_admin(self):
        #displays the login panel for admin users.
        login_frame = Frame(self.root, bg="black")
        login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        #Username label and entry field
        username_lbl = Label(login_frame, text="Username", font=("Comic Sans Ms", 25),
                             bg="black", fg="white")
        username_lbl.place(relx=0.1, rely=0.1, relwidth=0.2)
        username_entry = Entry(login_frame, font=("Comic Sans Ms", 25))
        username_entry.place(relx=0.3, rely=0.1, relwidth=0.3)

        # Password label and entry field
        password_lbl = Label(login_frame, text="Password", font=("Comic Sans Ms", 25),
                             bg="black", fg="white")
        password_lbl.place(relx=0.1, rely=0.2, relwidth=0.2)
        password_entry = Entry(login_frame, show="*", font=("Comic Sans Ms", 25))
        password_entry.place(relx=0.3, rely=0.2, relwidth=0.3)

        def check_admin(): # Authenticates the admin using the provided credentials and redirects to the admin panel on success and displays an error message on failure
            admin = Admin(username_entry.get(), password_entry.get())
            if admin.authenticate(username_entry.get(), password_entry.get()):
                messagebox.showinfo(title="Login Success",
                                    message=f"Welcome, {username_entry.get()}!")
                self.admin_panel()
            else:
                messagebox.showerror(title="Login Failed",
                                     message="Invalid username or password")

        # Button to initiate admin login authentication
        login_btn = Button(login_frame, text="Login", font=("Comic Sans Ms", 25), command=check_admin)
        login_btn.place(relx=0.2, rely=0.5, relwidth=0.3)

        #Back button to return to the start panel
        back_btn = Button(login_frame, text="Back", font=("Comic Sans Ms", 20), command=self.start_panel)
        back_btn.place(relx=0.9, rely=0, relwidth=0.1)

    def login_panel_user(self): # Displays the login panel for users (with login and create account options).
        login_frame = Frame(self.root, bg="black")
        login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        #Username label and entry field
        username_lbl = Label(login_frame, text="Username", font=("Comic Sans Ms", 25),
                             bg="black", fg="white")
        username_lbl.place(relx=0.1, rely=0.1, relwidth=0.2)
        username_entry = Entry(login_frame, font=("Comic Sans Ms", 25))
        username_entry.place(relx=0.3, rely=0.1, relwidth=0.3)

        # Password label and entry field
        password_lbl = Label(login_frame, text="Password", font=("Comic Sans Ms", 25),
                             bg="black", fg="white")
        password_lbl.place(relx=0.1, rely=0.2, relwidth=0.2)
        password_entry = Entry(login_frame, show="*", font=("Comic Sans Ms", 25))
        password_entry.place(relx=0.3, rely=0.2, relwidth=0.3)

        def check_user(): #authenticates the user using the provided credentials. If successful, logs the user in and redirects to the user panel. Otherwise, displays an error message
            user = self.user_db.authenticate(username_entry.get(), password_entry.get())
            if user:
                self.current_user = user
                messagebox.showinfo(title="Login Success",
                                    message=f"Welcome, {username_entry.get()}!")
                self.show_user_panel()
            else:
                messagebox.showerror(title="Login Failed",
                                     message="Invalid username or password")

        def create_account():# creates a new user account with the entered username and password and checks for duplicate usernames (or passwords) or empty fields and displays appropriate error messages
            username = username_entry.get()
            password = password_entry.get()
            if username in self.user_db.users:
                messagebox.showerror(title="Error", message="User already exists!")
            elif not username or not password:
                messagebox.showerror(title="Error",
                                     message="Username and Password must not be empty!")
            else:
                new_user = User(username, password)
                self.user_db.add(new_user)
                messagebox.showinfo(title="Success",
                                    message="Account created successfully!")

        # Button to log in the user
        login_btn = Button(login_frame, text="Login", font=("Comic Sans Ms", 25),
                           command=check_user)
        login_btn.place(relx=0.2, rely=0.5, relwidth=0.3)

        # Button to create a new user account
        create_account_btn = Button(login_frame, text="Create Account", font=("Comic Sans Ms", 25),
                                    command=create_account)
        create_account_btn.place(relx=0.55, rely=0.5, relwidth=0.3)

        #Back button to return to the start panel
        back_btn = Button(login_frame, text="Back", font=("Comic Sans Ms", 20),
                          command=self.start_panel)
        back_btn.place(relx=0.9, rely=0, relwidth=0.1)

    def checkout(self):#displays the checkout panel with a scrollable list of cart items
        checkout_frame = Frame(self.root, bg="black")
        checkout_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # title of the checkout page
        title_label = Label(checkout_frame, text="Your Cart", font=("Comic Sans Ms", 35),
                            bg="black", fg="white")
        title_label.place(relx=0.05, rely=0.05)

        # creates a canvas with a light gray background
        canvas = Canvas(checkout_frame, bg="lightgray", highlightthickness=0)
        canvas.place(relx=0.05, rely=0.15, relwidth=0.8, relheight=0.6)
        scrollbar = Scrollbar(checkout_frame, orient="vertical", command=canvas.yview)
        scrollbar.place(relx=0.85, rely=0.15, relwidth=0.05, relheight=0.6)
        canvas.configure(yscrollcommand=scrollbar.set)

        inner_frame = Frame(canvas, bg="lightgray")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        #fills the inner frame with each cart item with extra spacing
        for i, car in enumerate(self.cart.items):
            car_details = f"Brand: {car.brand} | Model: {car.model} | Price: ${car.price:.2f}"
            car_lbl = Label(inner_frame, text=car_details, font=("Comic Sans Ms", 18),
                            bg="lightgray", fg="black")
            car_lbl.grid(row=i, column=0, padx=30, pady=15, sticky="w")
            #Button to delete this item from the cart
            delete_btn = Button(inner_frame, text="Delete", font=("Comic Sans Ms", 15),
                                command=lambda i=i: self.remove_from_cart(i))
            delete_btn.grid(row=i, column=1, padx=30, pady=15)

        total_cost = self.cart.get_total_cost() # Calculates the total cost of items in the cart

        # Label to display the total cost
        total_label = Label(checkout_frame, text=f"Total Cost: ${total_cost:.2f}",
                            font=("Comic Sans Ms", 25), bg="black", fg="white")
        total_label.place(relx=0.1, rely=0.8)

        # Button to confirm the purchase
        purchase_btn = Button(checkout_frame, text="Purchase", font=("Comic Sans Ms", 20),
                              command=self.confirm_purchase)
        purchase_btn.place(relx=0.4, rely=0.85, relwidth=0.2)

        #Back button to return to the user panel
        back_btn = Button(checkout_frame, text="Back", font=("Comic Sans Ms", 20),
                          command=self.show_user_panel)
        back_btn.place(relx=0.9, rely=0, relwidth=0.1)

    def confirm_purchase(self):# confirms the purchase: checks balance, deducts cost, updates database, and clears the cart.
        total_cost = self.cart.get_total_cost()
        if total_cost > self.current_user.balance: #Notifies the user if they don't have enough funds
            messagebox.showerror("Insufficient Funds",
                                 "You do not have enough balance to complete the purchase.")
            return

        self.current_user.balance -= total_cost # Deducts total cost from user's balance
        self.user_db.update(self.current_user.username, self.current_user) #updates user data in the database

        #Clears the cart and saves it
        self.cart.clear()
        self.cart.save_cart()

        # Notifies the user of a successful purchase
        messagebox.showinfo("Success",
                            "Purchase completed successfully! Your order will arrive soon.")
        self.show_user_panel() #Redirects the user back to the user panel

    def remove_from_cart(self, index):# Removes a specific item from the user's cart by index and saves the updated cart data and refreshes the checkout panel.
        self.cart.items.pop(index)  #Removes the item from the cart
        self.cart.save_cart()       #Saves the updated cart to file
        self.checkout()             # Refreshes the checkout panel to reflect the change

    def show_user_panel(self):# Displays the main user panel where available cars are shown.
        user_frame = Frame(self.root, bg="black")
        user_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        #Title of the user panel
        title_label = Label(user_frame, text="Available Cars", font=("Comic Sans Ms", 35),
                            bg="black", fg="white")
        title_label.place(relx=0.05, rely=0.05)

        #creates a scrollable canvas
        cars_canvas = Canvas(user_frame, bg="black", highlightthickness=0)
        cars_canvas.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.7)
        scrollbar = Scrollbar(user_frame, orient="vertical", command=cars_canvas.yview)
        scrollbar.place(relx=0.95, rely=0.15, relwidth=0.03, relheight=0.7)
        cars_canvas.configure(yscrollcommand=scrollbar.set)

        user_frame.update_idletasks()
        canvas_width = int(cars_canvas.winfo_width())
        row_height = 260  #Fixed height per row
        num_rows = math.ceil(len(self.car_db.cars) / 3)
        inner_height = num_rows * row_height

        inner_frame = Frame(cars_canvas, bg="black", width=canvas_width, height=inner_height)
        cars_canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        inner_frame.bind("<Configure>", lambda e: cars_canvas.configure(scrollregion=cars_canvas.bbox("all")))

        inner_width = canvas_width

        # Displays all available cars
        for i, car in enumerate(self.car_db.cars):
            col = i % 3
            row = i // 3
            x = int(0.05 * inner_width + col * (0.3 * inner_width))
            y = row * row_height
            widget_width = int(0.25 * inner_width)

            #Displays car image
            try:
                car_image = PhotoImage(file=car.photo)
            except Exception:
                car_image = None
            if car_image:
                image_label = Label(inner_frame, image=car_image, bg="black")
                image_label.image = car_image #keeps a reference to avoid garbage collection
                image_label.place(x=x, y=y, width=widget_width, height=150)

            # Shows car details and button to view more information
            details = f"Brand: {car.brand}\nModel: {car.model}\nPrice: ${car.price:.2f}"
            car_btn = Button(inner_frame, text=details, font=("Comic Sans Ms", 18),
                             command=lambda c=car: self.show_car_info(c))
            car_btn.place(x=x, y=y+160, width=widget_width, height=100)

        #Displays user's current balance
        balance_label = Label(user_frame, text=f"Balance: ${self.current_user.balance:.2f}",
                              font=("Comic Sans Ms", 20), bg="black", fg="white")
        balance_label.place(relx=0.05, rely=0.9)

        # button to proceed to checkout
        checkout_btn = Button(user_frame, text="Check Out", font=("Comic Sans Ms", 20),
                              command=self.checkout)
        checkout_btn.place(relx=0.4, rely=0.9, relwidth=0.2)

        #Back button to log out and return to the start panel
        back_btn = Button(user_frame, text="Back", font=("Comic Sans Ms", 20),
                          command=self.start_panel)
        back_btn.place(relx=0.9, rely=0, relwidth=0.1)

    def show_car_info(self, car):#shows detailed information about a specific car, including its image, brand, model, price, and description. Users can add the car to their cart from this panel.
        car_info_frame = Frame(self.root, bg="black")
        car_info_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        #Displays car details (brand, model, price, description)
        info = f"Brand: {car.brand}\nModel: {car.model}\nPrice: ${car.price:.2f}\nDescription: {car.description}"
        info_label = Label(car_info_frame, text=info, font=("Comic Sans Ms", 25),
                           bg="black", fg="white", anchor="w", justify=LEFT)
        info_label.place(relx=0.1, rely=0.1, relwidth=0.6)

        # Shows car image
        try:
            car_image = PhotoImage(file=car.photo)
        except Exception:
            car_image = None
        if car_image:
            image_label = Label(car_info_frame, image=car_image, bg="black")
            image_label.image = car_image  #keeps a reference to avoid garbage collection
            image_label.place(relx=0.1, rely=0.4, relwidth=0.5, relheight=0.4)

        # Button to add this car to the cart
        add_to_cart_btn = Button(car_info_frame, text="Add to Cart", font=("Comic Sans Ms", 20),
                                 command=lambda: self.add_to_cart(car))
        add_to_cart_btn.place(relx=0.1, rely=0.85, relwidth=0.2)

        #Back button to return to the user panel
        back_btn = Button(car_info_frame, text="Back", font=("Comic Sans Ms", 20),
                          command=self.show_user_panel)
        back_btn.place(relx=0.9, rely=0, relwidth=0.1)

    def add_to_cart(self, car): # Adds the selected car to the user's cart, saves the updated cart data, and notifies the user of the addition.
        self.cart.add(car)  #Adds the car to the cart
        self.cart.save_cart()  # Saves the updated cart
        messagebox.showinfo("Cart", f"{car.model} added to your cart!")  # Notifies the user

    def admin_panel(self):#displays the admin panel with options to manage cars or users
        admin_frame = Frame(self.root, bg="black")
        admin_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Button to manage cars, redirects to the car management panel
        cars_btn = Button(admin_frame, text="Cars", font=("Comic Sans Ms", 30),
                          command=self.car_management_panel)
        cars_btn.place(relx=0.3, rely=0.3, relwidth=0.3)

        #button to manage users, redirects to the user management panel
        users_btn = Button(admin_frame, text="Users", font=("Comic Sans Ms", 30),
                           command=self.user_management_panel)
        users_btn.place(relx=0.3, rely=0.45, relwidth=0.3)

        # Button to log out and return to the start panel
        back_btn = Button(admin_frame, text="Log Out", font=("Comic Sans Ms", 20),
                          command=self.start_panel)
        back_btn.place(relx=0.9, rely=0, relwidth=0.1)

    def car_management_panel(self):# displays the admin car management panel with a scrollable list of cars.
        car_frame = Frame(self.root, bg="black")
        car_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        #Title for the car management panel
        title_label = Label(car_frame, text="Car Management", font=("Comic Sans Ms", 35),
                            bg="black", fg="white")
        title_label.place(relx=0.05, rely=0.05)

        # Column headers for the car list
        brand_label = Label(car_frame, text="Brand", font=("Comic Sans Ms", 20),
                            bg="black", fg="white")
        brand_label.place(relx=0.05, rely=0.2)
        model_label = Label(car_frame, text="Model", font=("Comic Sans Ms", 20),
                            bg="black", fg="white")
        model_label.place(relx=0.25, rely=0.2)
        price_label = Label(car_frame, text="Price", font=("Comic Sans Ms", 20),
                            bg="black", fg="white")
        price_label.place(relx=0.45, rely=0.2)
        action_label = Label(car_frame, text="Action", font=("Comic Sans Ms", 20),
                             bg="black", fg="white")
        action_label.place(relx=0.65, rely=0.2)

        #creates a canvas with a light gray background.
        canvas = Canvas(car_frame, bg="lightgray", highlightthickness=0)
        canvas.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.55)
        scrollbar = Scrollbar(car_frame, orient="vertical", command=canvas.yview)
        scrollbar.place(relx=0.95, rely=0.25, relwidth=0.05, relheight=0.55)
        canvas.configure(yscrollcommand=scrollbar.set)

        inner_frame = Frame(canvas, bg="lightgray")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        #Shows each car in the database with update and delete options
        for i, car in enumerate(self.car_db.cars):
            brand_lbl = Label(inner_frame, font=("Comic Sans Ms", 18), text=car.brand,
                              bg="lightgray", fg="black")
            brand_lbl.grid(row=i, column=0, padx=30, pady=15, sticky="w")
            model_lbl = Label(inner_frame, font=("Comic Sans Ms", 18), text=car.model,
                              bg="lightgray", fg="black")
            model_lbl.grid(row=i, column=1, padx=30, pady=15, sticky="w")
            price_lbl = Label(inner_frame, font=("Comic Sans Ms", 18),
                              text=f"${car.price:.2f}", bg="lightgray", fg="black")
            price_lbl.grid(row=i, column=2, padx=30, pady=15, sticky="w")

            # Button to update this car's details
            update_btn = Button(inner_frame, text="Update", font=("Comic Sans Ms", 15),
                                command=lambda i=i: self.open_car_form("Update", i))
            update_btn.grid(row=i, column=3, padx=30, pady=15)

            #Button to delete this car from the database
            delete_btn = Button(inner_frame, text="Delete", font=("Comic Sans Ms", 15),
                                command=lambda i=i: self.delete_car(i))
            delete_btn.grid(row=i, column=4, padx=30, pady=15)

        # Button to add a new car
        add_car_btn = Button(car_frame, text="Add a new car", font=("Comic Sans Ms", 20),
                             command=lambda: self.open_car_form("Add"))
        add_car_btn.place(relx=0.1, rely=0.85, relwidth=0.2)

        #Back button to return to the admin panel
        back_btn = Button(car_frame, text="Back", font=("Comic Sans Ms", 20),
                          command=self.admin_panel)
        back_btn.place(relx=0.8, rely=0.85, relwidth=0.1)

    def delete_car(self, index): #Deletes a car from the database by its index and refreshes the car management panel to reflect the updated list.
        self.car_db.delete(index)  # Removes the car from the database
        self.car_management_panel()  #Refreshes the panel

    def delete_user(self, username):# Deletes a user from the user database by username and refreshes the user management panel to reflect the updated list.
        self.user_db.delete(username)  #removes the user from the database
        self.user_management_panel()  # Refresh the panel

    def open_car_form(self, action, car_index=None):# Opens a form for adding/updating a car.
        form_frame = Frame(self.root, bg="black")
        form_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        #Title of the form, depending on whether the action is "Add" or "Update"
        title_label = Label(form_frame, text=f"{action} Car", font=("Comic Sans Ms", 35),
                            bg="black", fg="white")
        title_label.place(relx=0.3, rely=0.1)

        # Form fields for car attributes
        brand_label = Label(form_frame, text="Brand", font=("Comic Sans Ms", 20),
                            bg="black", fg="white")
        brand_label.place(relx=0.3, rely=0.3)
        brand_entry = Entry(form_frame, font=("Comic Sans Ms", 20))
        brand_entry.place(relx=0.4, rely=0.3, relwidth=0.3)

        model_label = Label(form_frame, text="Model", font=("Comic Sans Ms", 20),
                            bg="black", fg="white")
        model_label.place(relx=0.3, rely=0.4)
        model_entry = Entry(form_frame, font=("Comic Sans Ms", 20))
        model_entry.place(relx=0.4, rely=0.4, relwidth=0.3)

        price_label = Label(form_frame, text="Price", font=("Comic Sans Ms", 20),
                            bg="black", fg="white")
        price_label.place(relx=0.3, rely=0.5)
        price_entry = Entry(form_frame, font=("Comic Sans Ms", 20))
        price_entry.place(relx=0.4, rely=0.5, relwidth=0.3)

        description_label = Label(form_frame, text="Description", font=("Comic Sans Ms", 20),
                                  bg="black", fg="white")
        description_label.place(relx=0.3, rely=0.6)
        description_entry = Entry(form_frame, font=("Comic Sans Ms", 20))
        description_entry.place(relx=0.4, rely=0.6, relwidth=0.3)
        
        # Collects all png files in the current directory
        image_list = [f for f in glob.glob("*.png")]
        photo_combo = ttk.Combobox(form_frame, values=image_list, font=("Comic Sans Ms", 20))
        photo_combo.place(relx=0.4, rely=0.7, relwidth=0.3)

        #Optionally selects the first image by default if the directory is not empty
        if image_list:
            photo_combo.current(0)

        if action == "Update" and car_index is not None:
            # Pre-fill form fields with existing car data
            car = self.car_db.cars[car_index]
            brand_entry.insert(0, car.brand)
            model_entry.insert(0, car.model)
            price_entry.insert(0, str(car.price))
            description_entry.insert(0, car.description)
            photo_combo.set(car.photo)

        def save_car():
            brand = brand_entry.get()
            model = model_entry.get()
            price = price_entry.get()
            description = description_entry.get()
            photo = photo_combo.get()

            if not brand or not model or not price or not description:
                messagebox.showerror("Error", "All fields must be filled!")
                return
            try:
                price = float(price)
            except ValueError:
                messagebox.showerror("Error", "Price must be a number!")
                return

            if action == "Add":
                self.car_db.add(Car(brand, model, price, description, photo))
                messagebox.showinfo("Success", "Car added successfully!")
            elif action == "Update" and car_index is not None:
                self.car_db.update(car_index, Car(brand, model, price, description, photo))
                messagebox.showinfo("Success", "Car updated successfully!")

            self.car_management_panel()

        save_btn = Button(form_frame, text="Save", font=("Comic Sans Ms", 20),
                          command=save_car)
        save_btn.place(relx=0.4, rely=0.85)
        back_btn = Button(form_frame, text="Back", font=("Comic Sans Ms", 20),
                          command=self.car_management_panel)
        back_btn.place(relx=0.8, rely=0.85)

    def open_user_form(self, action, username=None):# opens a form for adding/updating a user.
        form_frame = Frame(self.root, bg="black")
        form_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        title_label = Label(form_frame, text=f"{action} User", font=("Comic Sans Ms", 35),
                            bg="black", fg="white")
        title_label.place(relx=0.3, rely=0.1)

        username_label = Label(form_frame, text="Username", font=("Comic Sans Ms", 20),
                               bg="black", fg="white")
        username_label.place(relx=0.3, rely=0.3)
        username_entry = Entry(form_frame, font=("Comic Sans Ms", 20))
        username_entry.place(relx=0.4, rely=0.3, relwidth=0.3)

        password_label = Label(form_frame, text="Password", font=("Comic Sans Ms", 20),
                               bg="black", fg="white")
        password_label.place(relx=0.3, rely=0.4)
        password_entry = Entry(form_frame, font=("Comic Sans Ms", 20), show="*")
        password_entry.place(relx=0.4, rely=0.4, relwidth=0.3)

        balance_label = Label(form_frame, text="Balance", font=("Comic Sans Ms", 20),
                              bg="black", fg="white")
        balance_label.place(relx=0.3, rely=0.5)
        balance_entry = Entry(form_frame, font=("Comic Sans Ms", 20))
        balance_entry.place(relx=0.4, rely=0.5, relwidth=0.3)

        if action == "Update" and username:
            user = self.user_db.users.get(username)
            username_entry.insert(0, user.username)
            password_entry.insert(0, user.password)
            balance_entry.insert(0, str(user.balance))

        def save_user():
            username_val = username_entry.get()
            password_val = password_entry.get()
            balance_val = balance_entry.get()
            if not username_val or not password_val or not balance_val:
                messagebox.showerror("Error", "All fields must be filled!")
                return
            try:
                balance_val = float(balance_val)
            except ValueError:
                messagebox.showerror("Error", "Balance must be a valid number!")
                return

            if action == "Add":
                if username_val in self.user_db.users:
                    messagebox.showerror("Error", "User already exists!")
                else:
                    new_user = User(username_val, password_val, balance_val)
                    self.user_db.add(new_user)
                    messagebox.showinfo("Success", "User added successfully!")
            elif action == "Update":
                user = User(username_val, password_val, balance_val)
                self.user_db.update(username_val, user)
                messagebox.showinfo("Success", "User updated successfully!")

            self.user_management_panel()

        save_btn = Button(form_frame, text="Save", font=("Comic Sans Ms", 20),
                          command=save_user)
        save_btn.place(relx=0.4, rely=0.7)
        back_btn = Button(form_frame, text="Back", font=("Comic Sans Ms", 20),
                          command=self.user_management_panel)
        back_btn.place(relx=0.8, rely=0.7)

    def user_management_panel(self):#displays the admin user management panel with a scrollable list of users.
        user_frame = Frame(self.root, bg="black")
        user_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        title_label = Label(user_frame, text="User Management", font=("Comic Sans Ms", 35),
                            bg="black", fg="white")
        title_label.place(relx=0.05, rely=0.05)

        username_label = Label(user_frame, text="Username", font=("Comic Sans Ms", 20),
                               bg="black", fg="white")
        username_label.place(relx=0.05, rely=0.2)
        password_label = Label(user_frame, text="Password", font=("Comic Sans Ms", 20),
                               bg="black", fg="white")
        password_label.place(relx=0.2, rely=0.2)
        balance_label = Label(user_frame, text="Balance", font=("Comic Sans Ms", 20),
                              bg="black", fg="white")
        balance_label.place(relx=0.35, rely=0.2)
        action_label = Label(user_frame, text="Action", font=("Comic Sans Ms", 20),
                             bg="black", fg="white")
        action_label.place(relx=0.6, rely=0.2)

        #creates a canvas with same light gray background as before
        canvas = Canvas(user_frame, bg="lightgray", highlightthickness=0)
        canvas.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.55)
        scrollbar = Scrollbar(user_frame, orient="vertical", command=canvas.yview)
        scrollbar.place(relx=0.95, rely=0.25, relwidth=0.05, relheight=0.55)
        canvas.configure(yscrollcommand=scrollbar.set)

        inner_frame = Frame(canvas, bg="lightgray")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        #Shows each user in the database with update and delete options
        for i, (username, user) in enumerate(self.user_db.users.items()):
            username_lbl = Label(inner_frame, font=("Comic Sans Ms", 18), text=username,
                                 bg="lightgray", fg="black")
            username_lbl.grid(row=i, column=0, padx=50, pady=25, sticky="w")
            password_lbl = Label(inner_frame, font=("Comic Sans Ms", 18),
                                 text="*" * len(user.password), bg="lightgray", fg="black")
            password_lbl.grid(row=i, column=1, padx=50, pady=25, sticky="w")
            balance_lbl = Label(inner_frame, font=("Comic Sans Ms", 18),
                                text=f"${user.balance:.2f}", bg="lightgray", fg="black")
            balance_lbl.grid(row=i, column=2, padx=50, pady=25, sticky="w")
            update_btn = Button(inner_frame, text="Update", font=("Comic Sans Ms", 15),
                                command=lambda u=username: self.open_user_form("Update", u))
            update_btn.grid(row=i, column=3, padx=50, pady=25)
            delete_btn = Button(inner_frame, text="Delete", font=("Comic Sans Ms", 15),
                                command=lambda u=username: self.delete_user(u))
            delete_btn.grid(row=i, column=4, padx=50, pady=25)

        add_user_btn = Button(user_frame, text="Add a new user", font=("Comic Sans Ms", 20),
                              command=lambda: self.open_user_form("Add"))
        add_user_btn.place(relx=0.1, rely=0.85, relwidth=0.2)
        back_btn = Button(user_frame, text="Back", font=("Comic Sans Ms", 20),
                          command=self.admin_panel)
        back_btn.place(relx=0.8, rely=0.85, relwidth=0.1)

#Main function to initialize and run the application.
root = Tk()
root.title("Car Management Panel")
app = App(root)
root.mainloop()