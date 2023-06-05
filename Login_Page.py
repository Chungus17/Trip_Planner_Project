from tkinter import messagebox
import psycopg2
from Signup_Page import SignUpPage
from User_Page import UserPage
import customtkinter as c


class LoginPage:
    def __init__(self):
        c.set_appearance_mode("dark")
        self.window = c.CTk()
        self.window.geometry("500x400")
        self.window.title("Login Page")

        self.label = c.CTkLabel(self.window, text="Welcome to TripPlanner!", font=("arial", 25, "bold"))
        self.label.pack(pady=20)

        self.frame = c.CTkFrame(self.window)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.login_label = c.CTkLabel(self.frame, text="Login to your account", font=("Robota", 20))
        self.login_label.pack(pady=12, padx=10)

        self.username_entry = c.CTkEntry(self.frame, placeholder_text="Username", width=175, height=30)
        self.username_entry.pack(pady=(12, 0), padx=10)

        self.password_entry = c.CTkEntry(self.frame, placeholder_text="Password", show="*", width=175, height=30)
        self.password_entry.pack(pady=12, padx=10)

        self.login_button = c.CTkButton(self.frame, text="Login", width=175, height=30, command=self.login)
        self.login_button.pack(pady=(12, 0), padx=10)

        self.label2 = c.CTkLabel(self.frame, text="Don't have an account?")
        self.signup_button = c.CTkButton(self.frame, text="Sign Up", width=70, command=self.signup)

        self.label2.pack(padx=(85, 5), side='left')
        self.signup_button.pack(padx=(5, 0), side='left')

        self.window.eval('tk::PlaceWindow . center')
        self.window.protocol("WM_DELETE_WINDOW", self.window.quit())
        self.window.mainloop()

    def login(self):
        # Get the values entered in the textboxes
        username = self.username_entry.get()
        password = self.password_entry.get()

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
            query = f"SELECT * FROM useraccounts WHERE useraccounts.username = '{username}' AND useraccounts.password = '{password}'"
            cursor.execute(query)
            result = cursor.fetchall()

            if result:
                messagebox.showinfo("Login Successful", "Logged in successfully!")
                name = result[0][3]
                surname = result[0][4]
                self.window.withdraw()
                UserPage(result[0][0], name, surname)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

            connection.close()
        except psycopg2.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")
            print("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")

    def signup(self):
        self.window.destroy()
        SignUpPage()
