from tkinter import messagebox
import customtkinter
from TripPlanInputs import TripPlanInputs
from plan_window import TripPlanWindow
import psycopg2
import os


class UserPage:
    def __init__(self, idd, name, surname):
        customtkinter.set_appearance_mode("dark")
        self.name = name
        self.surname = surname

        self.user_id = idd
        self.window = customtkinter.CTk()
        self.window.title("User Page")
        self.window.geometry("460x460")

        # HI, NAME SURNAME Label
        self.hi_label_text = f"Hi, {name} {surname}"
        self.hi_label = customtkinter.CTkLabel(self.window, text=self.hi_label_text, font=("Arial", 25, "bold"))
        self.hi_label.grid(row=0, column=0, pady=30, padx=10, sticky="w")

        # LOG OUT Button
        self.log_out_button = customtkinter.CTkButton(self.window, text="Log Out", fg_color="red2",
                                                      command=self.log_out, width=120)
        self.log_out_button.grid(row=0, column=1, pady=30, sticky="E")

        # NEW TRIP Button
        self.new_trip_button = customtkinter.CTkButton(self.window, text="Plan New Trip", command=self.new_trip)
        self.new_trip_button.place(x=165, y=380)

        # YOUR PLANS: Label
        self.your_plan_label = customtkinter.CTkLabel(self.window, text="Your Plans:", font=("Arial", 20))
        self.your_plan_label.grid(row=1, column=0, sticky="w", padx=10)

        self.scrollableFrame = customtkinter.CTkScrollableFrame(self.window, width=410)
        self.scrollableFrame.grid(row=2, column=0, columnspan=2, pady=5, padx=10)

        self.window.eval('tk::PlaceWindow . center')
        self.window.protocol("WM_DELETE_WINDOW", self.window.quit())

        self.your_plans()
        self.window.mainloop()

    def new_trip(self):
        self.window.destroy()
        TripPlanInputs(self.user_id, self.name, self.surname)

    def log_out(self):
        from Login_Page import LoginPage
        self.window.destroy()
        LoginPage().window.wm_deiconify()

    def your_plans(self):
        try:
            connection = psycopg2.connect(
                host="localhost",
                port=5432,
                database="TripPlannerDB",
                user="postgres",
                password="ROOT123123"
            )
            cursor = connection.cursor()

            query = f"SELECT * FROM trips where trips.user_id = {self.user_id}"

            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
            connection.close()
            self.place_trips(result)

        except psycopg2.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")
            print("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")
            pass

    def place_trips(self, result):
        if not result:
            label1 = customtkinter.CTkLabel(self.scrollableFrame, text="You don't have any previous trip plans!", font=("Vendetta", 16))
            label1.grid(row=0, column=0, padx=(10, 10), pady=(20, 0))
        else:
            for index, item in enumerate(result):
                trip_name = item[3]
                destination = item[2].capitalize()

                button = customtkinter.CTkButton(self.scrollableFrame, text=trip_name,
                                                 command=lambda trip=trip_name: self.view_old_plan(trip))
                button.grid(row=index, column=0, padx=(10, 0), pady=(10, 0))

                label = customtkinter.CTkLabel(self.scrollableFrame, text=destination)
                label.grid(row=index, column=1, padx=(50, 0), pady=(10, 0))

                delete_button = customtkinter.CTkButton(self.scrollableFrame, text="X", width=20, fg_color="red2",
                                                        command=lambda idx=index, tripName=trip_name: self.delete_trip(
                                                            idx,
                                                            tripName))
                delete_button.grid(row=index, column=2, padx=10, pady=(10, 0), sticky="E")

                self.scrollableFrame.columnconfigure(2, weight=1)

    def delete_trip(self, index, tripName):
        # Get the widgets at the specified index
        trip_button = self.scrollableFrame.grid_slaves(row=index, column=0)[0]
        delete_button = self.scrollableFrame.grid_slaves(row=index, column=1)[0]
        label = self.scrollableFrame.grid_slaves(row=index, column=2)[0]

        print(trip_button, label, delete_button)

        # Remove the widgets from the scrollable frame
        trip_button.grid_forget()
        delete_button.grid_forget()
        label.grid_forget()

        # Perform any additional delete logic for the corresponding trip
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
            query = "DELETE FROM trips WHERE trip_name = %s"
            cursor.execute(query, (tripName,))
            connection.commit()
            connection.close()
            if f"{tripName}.txt":
                os.remove(f"{tripName}.txt")

        except psycopg2.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")
            print("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")

        # Rearrange the remaining widgets in the scrollable frame
        self.your_plans()

    def view_old_plan(self, tripName):
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
            query = f"SELECT * FROM trips where trip_name = '{tripName}'"

            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
            connection.close()

        except psycopg2.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")
            print("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")

        binary_data = result[0][4]
        bytes_data = bytes(binary_data)
        reply = bytes_data.decode('utf-8')

        user_id = result[0][1]
        destination = result[0][2]

        self.window.withdraw()
        TripPlanWindow(reply, False, user_id, destination, False, self.name, self.surname)