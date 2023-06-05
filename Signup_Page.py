import tkinter as tk
import customtkinter
from User_Page import UserPage
import psycopg2
from tkinter import messagebox


def check_signup_details(username):
    condition = True
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="TripPlannerDB",
            user="postgres",
            password="ROOT123123"
        )
        cursor = connection.cursor()

        # Execute a query to check if the username and password exist in the database
        query = f"SELECT EXISTS(SELECT 1 FROM useraccounts WHERE useraccounts.username = '{username}') AS username_exists;"
        cursor.execute(query)
        result = cursor.fetchone()
        result2 = result[0]

        if result2:
            condition = False

        connection.close()
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")
        print("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")
    return condition


def get_next_id():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="TripPlannerDB",
            user="postgres",
            password="ROOT123123"
        )
        cursor = connection.cursor()

        # Execute a query to check if the username and password exist in the database
        query = f"SELECT useraccounts.id FROM useraccounts ORDER BY useraccounts.id DESC LIMIT 1;"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        result += 1
        connection.close()
        return result

    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")
        print("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")


def update_database(name, surname, username, password, idd):
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="TripPlannerDB",
            user="postgres",
            password="ROOT123123"
        )
        cursor = connection.cursor()
        id = idd  # Get NEXT ID using last row of table useraccounts

        # Execute a query to INSERT info into database
        query2 = f"INSERT INTO useraccounts (id, name, surname, username, password) VALUES ({id}, '{name}', '{surname}', '{username}', '{password}');"
        cursor.execute(query2)
        connection.commit()
        connection.close()

    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")
        print("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")


class SignUpPage:
    def __init__(self):
        customtkinter.set_appearance_mode("dark")

        self.window = customtkinter.CTk()
        self.window.title("Sign Up")
        self.window.geometry("500x400")

        self.label = customtkinter.CTkLabel(self.window, text="Sign Up", font=("Arial", 25, "bold"))
        self.label.pack(padx=(10, 10), pady=(20, 0))

        self.frame = customtkinter.CTkFrame(self.window)
        self.frame.pack(pady=20, padx=90, fill="both", expand=True)

        self.name_entry = customtkinter.CTkEntry(self.frame, placeholder_text="              Name", width=140)
        self.name_entry.pack(padx=(10, 10), pady=(20, 0))

        self.surname_entry = customtkinter.CTkEntry(self.frame, placeholder_text="           Surname", width=140)
        self.surname_entry.pack(padx=(10, 10), pady=(20, 0))

        self.username_entry = customtkinter.CTkEntry(self.frame, placeholder_text="          Username", width=140)
        self.username_entry.pack(padx=(10, 10), pady=(20, 0))

        self.password_entry = customtkinter.CTkEntry(self.frame, placeholder_text="           Password", width=140,
                                                     show="*")
        self.password_entry.pack(padx=(10, 10), pady=(20, 0))

        self.confirm_password_entry = customtkinter.CTkEntry(self.frame, placeholder_text="    Confirm Password",
                                                             width=140, show="*")
        self.confirm_password_entry.pack(padx=(10, 10), pady=(20, 0))

        self.signup_button = customtkinter.CTkButton(self.frame, text="Sign Up", command=self.sign_up)
        self.signup_button.pack(padx=(10, 10), pady=(20, 0))

        self.window.protocol("WM_DELETE_WINDOW", self.window.quit())
        self.window.eval('tk::PlaceWindow . center')
        self.window.mainloop()

    def sign_up(self):
        # Get the entered values from the entry fields
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Perform validation and sign-up logic here
        if len(name) != 0 and len(surname) != 0 and len(username) != 0:
            if len(password) >= 6:
                if password == confirm_password:
                    condition = check_signup_details(username)
                    if condition:
                        messagebox.showinfo("Sign Up successful!", "Your account has been created successfully")
                        id = get_next_id()
                        update_database(name, surname, username, password, id)
                        self.window.destroy()
                        UserPage(id, name, surname)
                    else:
                        messagebox.showerror("Sign Up failed!", f"Username {username} already exists")
                        self.delete_entries()
                else:
                    messagebox.showerror("Sign Up failed!", "Password and Confirm password do not match")
                    self.delete_entries()
            else:
                messagebox.showerror("Password ERROR!", "Password must consist of at least 6 characters")
        else:
            messagebox.showerror("Sign up failed!", "Please enter all the information")

    def delete_entries(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)
        self.username_entry.focus_set()
