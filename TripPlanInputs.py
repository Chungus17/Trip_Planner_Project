import tkinter as tk
import customtkinter as c
from plan_window import TripPlanWindow
import openai
from tkinter import messagebox

openai.api_key = "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"


def chatGPT_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response["choices"][0]["message"]["content"]
    return reply


class TripPlanInputs:
    def __init__(self, idd, name, surname):
        self.interests_array = []
        self.cuisines_array = []
        self.prompt = ""
        self.user_id = idd

        self.name = name
        self.surname = surname

        # Create the main window
        self.window = c.CTk()
        self.window.title("Travel Planner")
        self.window.geometry("500x700")

        # Create the destination label and entry
        self.dest_label = c.CTkLabel(self.window, text="Destination:")
        self.dest_label.grid(row=0, column=0, padx=10, pady=10)
        self.dest_entry = c.CTkEntry(self.window)
        self.dest_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create the budget label and entry
        self.budget_label = c.CTkLabel(self.window, text="Budget($):")
        self.budget_label.grid(row=1, column=0, padx=10, pady=10)
        self.budget_entry = c.CTkEntry(self.window)
        self.budget_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create the duration label and entry
        self.duration_label = c.CTkLabel(self.window, text="Duration:")
        self.duration_label.grid(row=2, column=0, padx=10, pady=10)
        self.duration_entry = c.CTkEntry(self.window)
        self.duration_entry.grid(row=2, column=1, padx=10, pady=10)

        # Create the interest label and checkboxes
        self.interest_label = c.CTkLabel(self.window, text="Interests:")
        self.interest_label.grid(row=3, column=0, padx=10, pady=10)

        # History
        self.history_var = tk.IntVar()
        self.history_checkbox = c.CTkCheckBox(self.window, text="History", variable=self.history_var)
        self.history_checkbox.grid(row=4, column=0, padx=10, pady=2)

        # Art
        self.art_var = tk.IntVar()
        self.art_checkbox = c.CTkCheckBox(self.window, text="Art", variable=self.art_var)
        self.art_checkbox.grid(row=4, column=1, padx=10, pady=2)

        # Architecture
        self.architecture_var = tk.IntVar()
        self.architecture_checkbox = c.CTkCheckBox(self.window, text="Architecture", variable=self.architecture_var)
        self.architecture_checkbox.grid(row=4, column=2, padx=10, pady=2)

        # Sports
        self.sports_var = tk.IntVar()
        self.sports_checkbox = c.CTkCheckBox(self.window, text="Sports", variable=self.sports_var)
        self.sports_checkbox.grid(row=5, column=0, padx=10, pady=2)

        # Nature
        self.nature_var = tk.IntVar()
        self.nature_checkbox = c.CTkCheckBox(self.window, text="Nature", variable=self.nature_var)
        self.nature_checkbox.grid(row=5, column=1, padx=10, pady=2)

        # Literature
        self.literature_var = tk.IntVar()
        self.literature_checkbox = c.CTkCheckBox(self.window, text="Literature", variable=self.literature_var)
        self.literature_checkbox.grid(row=5, column=2, padx=10, pady=2)

        # Music
        self.music_var = tk.IntVar()
        self.music_checkbox = c.CTkCheckBox(self.window, text="Music", variable=self.music_var)
        self.music_checkbox.grid(row=6, column=0, padx=10, pady=2)

        # Food
        self.food_var = tk.IntVar()
        self.food_checkbox = c.CTkCheckBox(self.window, text="Food", variable=self.food_var)
        self.food_checkbox.grid(row=6, column=1, padx=10, pady=2)

        # Photography
        self.photography_var = tk.IntVar()
        self.photography_checkbox = c.CTkCheckBox(self.window, text="Photography", variable=self.photography_var)
        self.photography_checkbox.grid(row=6, column=2, padx=10, pady=2)

        # Create the accommodation label and combobox
        self.accommodation_label = c.CTkLabel(self.window, text="Accommodation:")
        self.accommodation_label.grid(row=7, column=0, padx=10, pady=10)
        self.accommodation_combobox = c.CTkComboBox(self.window,
                                                    values=["Hotel", "Hostel", "Airbnb", "Camping", "Daily rentals"])
        self.accommodation_combobox.grid(row=7, column=1, padx=10, pady=10)

        # Create the travel style label and combobox
        self.travel_style_label = c.CTkLabel(self.window, text="Travel Style:")
        self.travel_style_label.grid(row=8, column=0, padx=10, pady=10)
        self.travel_style_combobox = c.CTkComboBox(self.window,
                                                   values=["Backpacking", "Luxury", "Adventure", "City Break", "Beach",
                                                           "Cultural"])
        self.travel_style_combobox.grid(row=8, column=1, padx=10, pady=10)

        # Create the transportation type label and combobox
        self.transportation_label = c.CTkLabel(self.window, text="Transportation:")
        self.transportation_label.grid(row=9, column=0, padx=10, pady=10)
        self.transportation_combobox = c.CTkComboBox(self.window, values=["Car", "Train", "Bus"])
        self.transportation_combobox.grid(row=9, column=1, padx=10, pady=10)

        # Create the activity type label and combobox
        self.activity_label = c.CTkLabel(self.window, text="Activity Type:")
        self.activity_label.grid(row=10, column=0, padx=10, pady=10)
        self.activity_combobox = c.CTkComboBox(self.window,
                                               values=["Outdoor", "Indoor", "Water Sports", "Sightseeing", "Shopping",
                                                       "Nightlife"])
        self.activity_combobox.grid(row=10, column=1, padx=10, pady=10)

        # Create the cuisine type label and checkboxes
        self.cuisine_label = c.CTkLabel(self.window, text="Cuisine Type:")
        self.cuisine_label.grid(row=11, column=0, padx=10, pady=10)

        self.italian_var = tk.IntVar()
        self.italian_checkbox = c.CTkCheckBox(self.window, text="Italian", variable=self.italian_var)
        self.italian_checkbox.grid(row=12, column=0, padx=10, pady=2)

        self.chinese_var = tk.IntVar()
        self.chinese_checkbox = c.CTkCheckBox(self.window, text="Chinese", variable=self.chinese_var)
        self.chinese_checkbox.grid(row=12, column=1, padx=10, pady=2)

        self.indian_var = tk.IntVar()
        self.indian_checkbox = c.CTkCheckBox(self.window, text="Indian", variable=self.indian_var)
        self.indian_checkbox.grid(row=12, column=2, padx=10, pady=2)

        self.japanese_var = tk.IntVar()
        self.japanese_checkbox = c.CTkCheckBox(self.window, text="Japanese", variable=self.japanese_var)
        self.japanese_checkbox.grid(row=13, column=0, padx=10, pady=2)

        self.mexican_var = tk.IntVar()
        self.mexican_checkbox = c.CTkCheckBox(self.window, text="Mexican", variable=self.mexican_var)
        self.mexican_checkbox.grid(row=13, column=1, padx=10, pady=2)

        self.french_var = tk.IntVar()
        self.french_checkbox = c.CTkCheckBox(self.window, text="French", variable=self.french_var)
        self.french_checkbox.grid(row=13, column=2, padx=10, pady=2)

        self.american_var = tk.IntVar()
        self.american_checkbox = c.CTkCheckBox(self.window, text="American", variable=self.american_var)
        self.american_checkbox.grid(row=14, column=0, padx=10, pady=2)

        self.greek_var = tk.IntVar()
        self.greek_checkbox = c.CTkCheckBox(self.window, text="Greek", variable=self.greek_var)
        self.greek_checkbox.grid(row=14, column=1, padx=10, pady=2)

        self.spanish_var = tk.IntVar()
        self.spanish_checkbox = c.CTkCheckBox(self.window, text="Spanish", variable=self.spanish_var)
        self.spanish_checkbox.grid(row=14, column=2, padx=10, pady=2)

        self.thai_var = tk.IntVar()
        self.thai_checkbox = c.CTkCheckBox(self.window, text="Thai", variable=self.thai_var)
        self.thai_checkbox.grid(row=15, column=0, padx=10, pady=2)

        # Create the Generate button
        self.generate_button = c.CTkButton(self.window, text="Generate", command=self.generate)
        self.generate_button.grid(row=16, column=1, padx=10, pady=20, columnspan=2, sticky="nsew")

        self.interestsCheckBoxes_Checked()
        self.cuisineCheckBoxes_Checked()

        self.window.eval('tk::PlaceWindow . center')
        self.window.protocol("WM_DELETE_WINDOW", self.window.quit())
        self.window.mainloop()

    def interestsCheckBoxes_Checked(self):
        if self.history_var.get() == 1:
            self.interests_array.append("history")
        if self.art_var.get() == 1:
            self.interests_array.append("art")
        if self.architecture_var.get() == 1:
            self.interests_array.append("architecture")
        if self.sports_var.get() == 1:
            self.interests_array.append("sports")
        if self.nature_var.get() == 1:
            self.interests_array.append("nature")
        if self.literature_var.get() == 1:
            self.interests_array.append("literature")
        if self.music_var.get() == 1:
            self.interests_array.append("music")
        if self.food_var.get() == 1:
            self.interests_array.append("food")
        if self.photography_var.get() == 1:
            self.interests_array.append("photography")

    def cuisineCheckBoxes_Checked(self):
        if self.italian_var.get() == 1:
            self.cuisines_array.append("italian")
        if self.chinese_var.get() == 1:
            self.cuisines_array.append("chinese")
        if self.indian_var.get() == 1:
            self.cuisines_array.append("indian")
        if self.japanese_var.get() == 1:
            self.cuisines_array.append("japanese")
        if self.mexican_var.get() == 1:
            self.cuisines_array.append("mexican")
        if self.french_var.get() == 1:
            self.cuisines_array.append("french")
        if self.american_var.get() == 1:
            self.cuisines_array.append("american")
        if self.greek_var.get() == 1:
            self.cuisines_array.append("greek")
        if self.spanish_var.get() == 1:
            self.cuisines_array.append("spanish")
        if self.thai_var.get() == 1:
            self.cuisines_array.append("thai")

    def generate(self):
        destination = self.dest_entry.get()
        budget = self.budget_entry.get()
        duration = self.duration_entry.get()
        accommodation = self.accommodation_combobox.get()
        travel_style = self.travel_style_combobox.get()
        transportation = self.transportation_combobox.get()
        activity = self.activity_combobox.get()

        # Create an instance of the Plan_window class
        if len(destination) != 0:
            if budget.isdigit():
                if duration.isdigit():
                    self.interestsCheckBoxes_Checked()
                    interests = ""
                    for i in range(len(self.interests_array)):
                        interests += f"{self.interests_array[i]}, "

                    self.cuisineCheckBoxes_Checked()
                    cuisines = ""
                    for i in range(len(self.cuisines_array)):
                        cuisines += f"{self.cuisines_array[i]}, "

                    self.prompt = f"Generate a personalized travel itinerary for a trip to {destination} with a budget of {budget} USD. The traveler is interested in a {interests} related vacation and enjoys {travel_style} travel style. They are looking for {accommodation} accommodations and prefer {transportation} transportation. The itinerary should include {activity} activities and {cuisines} dining options. Please provide a detailed itinerary with daily recommendations for {duration} days, including suggested destinations, activities, and dining options."
                    reply = chatGPT_response(self.prompt)
                    self.window.withdraw()
                    TripPlanWindow(reply, self.stop_program, self.user_id, destination, True, self.name, self.surname)
                else:
                    messagebox.showerror("ERROR!", "Please enter the duration as days (3 or 5 or 8 etc)")
            else:
                messagebox.showerror("ERROR!", "Please enter the budget as a number of $ (600 or 1000 etc...)")
        else:
            messagebox.showerror("ERROR!", "Please enter the destination")

    def stop_program(self):
        # Stop the running of the program
        self.window.quit()

    def get_prompt(self):
        return self.prompt
