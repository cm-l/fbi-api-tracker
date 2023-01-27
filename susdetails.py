import tkinter as tk

import requests
from PIL import Image, ImageTk


# noinspection PyBroadException
class SuspectDetails:
    def __init__(self, suspect):
        self.suspect_details = tk.Toplevel()
        self.suspect_details.title("FBI Most Wanted - Suspect Details")
        self.suspect = suspect
        name_label = tk.Label(self.suspect_details, text=self.suspect["title"])
        name_label.grid(row=0, column=0)
        try:
            image_url = self.suspect["images"][0]["large"]
            image_data = requests.get(image_url).content
            with open("temp.png", "wb") as handler:
                handler.write(image_data)
            image = Image.open("temp.png")
            image = image.resize((256, 256), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            image_label = tk.Label(self.suspect_details, image=image)
            image_label.image = image
            image_label.grid(row=1, column=0)
        except:
            pass

        # STATUS (missing, dead, captured, etc.)
        try:

            # Translate status into something more readable
            if self.suspect["status"] == "na":
                full_status = "Not Apprehended / Missing"
            else:
                full_status = self.suspect["status"]

            states_label = tk.Label(self.suspect_details, text="Status: " + full_status)
            states_label.grid(row=2, column=0)
        except:
            pass

        # SUBJECT (organized crime, cybercrime, missing person, kidnapped, etc.)
        try:
            charges_label = tk.Label(self.suspect_details, text="Subject: " + self.suspect["subjects"][0])
            charges_label.grid(row=3, column=0)
        except:
            pass

        # DESCRIPTION (lengthy-ish block of text)
        try:
            description_label = tk.Label(self.suspect_details, text="Description: " + self.suspect["description"])
            description_label.grid(row=4, column=0)
        except:
            pass

        # DETAILS (lengthy-ish block of text)
        # try:
        #     description_label = tk.Label(self.suspect_details, text="Details: " + self.suspect["details"])
        #     description_label.grid(row=5, column=0)
        # except:
        #     pass

        # DATE OF PUBLICATION (when was this wanted entry posted)
        try:
            date_label = tk.Label(self.suspect_details, text="Wanted since: " + self.suspect["publication"])
            date_label.grid(row=6, column=0)
        except:
            pass

        # KNOWN ALIASES
        try:
            aliases = []
            for alias in self.suspect["aliases"]:
                aliases.append(alias)

            aliases_label = tk.Label(self.suspect_details, text="AKA: " + ', '.join(aliases))
            aliases_label.grid(row=7, column=0)
        except:
            pass

        # KNOWN NATIONALITY
        try:
            nationality_label = tk.Label(self.suspect_details, text="Nationality: " + self.suspect["nationality"])
            nationality_label.grid(row=8, column=0)
        except:
            pass

    # w zależnosci od daty dodania na liste most wanted

    # metoda load all data (Dla każej strony która jest) -> mam dane na dysku w jednym megajsonie ->
    # -> liczenie danych jakościowych
    # rozmieszczeni w czasie (np narodowość - czas)
    def show(self):
        self.suspect_details.mainloop()
