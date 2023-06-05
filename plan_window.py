import tkinter as tk
import customtkinter as c
from TripName import TripName


class TripPlanWindow:
    def __init__(self, reply, close_callback, idd, destinationn, condition_for_saveButton, name, surname):
        self.reply = reply
        self.close_callback = close_callback
        self.user_id = idd
        self.destination = destinationn

        self.name = name
        self.surname = surname

        # Create the prompt window
        self.window = c.CTkToplevel()
        self.window.title("Travel Plan")
        self.window.geometry("860x600")
        c.set_appearance_mode("dark")

        self.scroll_area = c.CTkScrollableFrame(self.window)
        self.scroll_area.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.label_reply = c.CTkLabel(self.scroll_area, text=self.reply, wraplength=800)
        self.label_reply.grid(row=0, column=0, padx=15, pady=10)

        # Button to SAVE the TRIP
        if condition_for_saveButton:
            self.save_button = c.CTkButton(self.window, text="Save Trip", command=self.save_trip)
            self.save_button.pack()

        # Add a button to close the prompt window and stop the program
        self.close_button = c.CTkButton(self.window, text="Close", command=self.close)
        self.close_button.pack(pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.window.quit())
        self.window.mainloop()

    def close(self):
        # Destroy the prompt window
        self.window.destroy()
        from User_Page import UserPage
        UserPage(self.user_id, self.name, self.surname).window.deiconify()

    def save_trip(self):
        self.window.destroy()
        TripName(self.destination, self.reply, self.user_id, self.name, self.surname)
