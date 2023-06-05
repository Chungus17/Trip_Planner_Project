from tkinter import messagebox

import customtkinter as c
import psycopg2


def get_trip_id():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="TripPlannerDB",
            user="postgres",
            password="ROOT"
        )
        cursor = connection.cursor()

        # Execute a query to check if the username and password exist in the database
        query = "SELECT trip_id FROM trips ORDER BY trip_id DESC LIMIT 1;"

        cursor.execute(query)
        cursor.execute(query)
        result = cursor.fetchone()

        if result is not None:
            trip_id = result[0] + 1
        else:
            # If no rows are returned, set the trip_id to 1
            trip_id = 1

        connection.close()

        return trip_id

    except psycopg2.Error:
        print("Database ERROR!")


class TripName:
    def __init__(self, destinationn, replyy, idd, name, surname):
        self.destination = destinationn
        self.reply = replyy
        self.user_id = idd
        self.name = name
        self.surname = surname

        c.set_appearance_mode("dark")

        self.window = c.CTk()
        self.window.title("Trip Name")
        self.window.geometry("230x120")

        # TRIP NAME Label
        self.trip_name_label = c.CTkLabel(self.window, text="Trip name: ")
        self.trip_name_label.grid(row=0, column=0, padx=(10, 0), pady=(15, 0))

        # TRIP NAME Entry
        self.trip_name_entry = c.CTkEntry(self.window)
        self.trip_name_entry.grid(row=0, column=1, padx=(5, 0), pady=(15, 0))
        # SAVE Button
        self.save_button = c.CTkButton(self.window, text="Save", command=self.save_trip)
        self.save_button.grid(row=1, column=0, columnspan=2, pady=(20, 0))

        self.window.eval('tk::PlaceWindow . center')
        self.window.protocol("WM_DELETE_WINDOW", self.window.quit())
        self.window.mainloop()

    def save_trip(self):
        filename = self.trip_name_entry.get()
        condition = self.trip_name_check(filename.split(".")[0])

        if condition:
            file_name = self.save_trip_intoFile()

            with open(file_name, 'rb') as file:
                file_data = file.read()

            try:
                connection = psycopg2.connect(
                    host="localhost",
                    port=5432,
                    database="TripPlannerDB",
                    user="postgres",
                    password="ROOT"
                )
                cursor = connection.cursor()
                trip_id = get_trip_id()

                # Execute a query to check if the username and password exist in the database
                query = f"INSERT INTO trips (destination, trip_id, trip_name, trip_text, user_id) VALUES (%s, %s, %s, %s, %s);"

                cursor.execute(query, (self.destination, trip_id, file_name.split(".")[0], psycopg2.Binary(file_data), self.user_id))
                connection.commit()
                connection.close()

            except psycopg2.Error as e:
                messagebox.showerror("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")
                print("Database Error", f"An error occurred while connecting to the database:\n{str(e)}")

            self.window.destroy()
            from User_Page import UserPage
            UserPage(self.user_id, self.name, self.surname)
        else:
            messagebox.showerror("ERROR!", f"Trip name {filename} already exists! Please use a different trip name")

    def save_trip_intoFile(self):
        trip_name = self.trip_name_entry.get()  # Get the trip name from the entry widget

        # Generate a new file name
        file_name = f"{trip_name}.txt"

        # Write the trip name to the file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(self.reply)

        print("Trip name saved to file.")

        return file_name

    # Check if the trip name already exists
    def trip_name_check(self, tripName):
        trip_name = tripName
        user_id = self.user_id
        try:
            connection = psycopg2.connect(
                host="localhost",
                port=5432,
                database="TripPlannerDB",
                user="postgres",
                password="ROOT"
            )
            cursor = connection.cursor()

            # Execute a query to check if the username and password exist in the database
            query = f"SELECT trip_name FROM trips WHERE user_id = {user_id}"

            cursor.execute(query)
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)

            for item in result:
                if trip_name == item[0]:
                    return False

            return True

        except psycopg2.Error:
            print("Database ERROR!")

