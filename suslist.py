import tkinter as tk

import requests
from PIL import Image, ImageTk

from susdetails import SuspectDetails


def suspect_details(suspect):
    SuspectDetails(suspect).show()


class SuspectsList:
    def __init__(self, suspects):
        self.back_button = None
        self.next_button = None
        self.suspects_list = tk.Toplevel()
        self.suspects_list.title("Suspects List")
        self.suspects = suspects

        # Pages
        self.index = 0  # add a variable to keep track of the current index


        self.display_suspects(self.index)
        # self.next_button = tk.Button(self.suspects_list, text="Next", command=self.next_suspects)
        # self.next_button.grid(row=6, column=1)

        # def display_suspects(self, index):
        #     for suspect in self.suspects[index:index+10]:
        #         number = tk.Label(self.suspects_list, text=str(self.suspects.index(suspect) + 1) + ".")
        #         number.grid(row=self.suspects.index(suspect), column=0)
        #         name_label = tk.Label(self.suspects_list, text=suspect["title"], cursor="hand2")
        #         name_label.grid(row=self.suspects.index(suspect), column=1)
        #         name_label.bind("<Button-1>", lambda event, arg=suspect: suspect_details(arg))
        #         try:
        #             image_url = suspect["images"][0]["thumb"]
        #             image_data = requests.get(image_url).content
        #             with open("temp.png", "wb") as handler:
        #                 handler.write(image_data)
        #             image = Image.open("temp.png")
        #             image = image.resize((50, 50), Image.ANTIALIAS)
        #             image = ImageTk.PhotoImage(image)
        #             image_label = tk.Label(self.suspects_list, image=image)
        #             image_label.image = image
        #             image_label.grid(row=self.suspects.index(suspect), column=2)
        #         except:
        #             pass

    def show(self):
        self.suspects_list.mainloop()

    def display_suspects(self, index):
        for widget in self.suspects_list.grid_slaves():
            widget.destroy()


        for suspect in self.suspects[index:index + 5]:
            number = tk.Label(self.suspects_list, text=str(self.suspects.index(suspect) + 1) + ".")
            number.grid(row=self.suspects.index(suspect)+1, column=0)
            name_label = tk.Label(self.suspects_list, text=suspect["title"], cursor="hand2")
            name_label.grid(row=self.suspects.index(suspect)+1, column=1)
            name_label.bind("<Button-1>", lambda event, arg=suspect: suspect_details(arg))
            try:
                image_url = suspect["images"][0]["thumb"]
                image_data = requests.get(image_url).content
                with open("temp.png", "wb") as handler:
                    handler.write(image_data)
                image = Image.open("temp.png")
                image = image.resize((50, 50), Image.ANTIALIAS)
                image = ImageTk.PhotoImage(image)
                image_label = tk.Label(self.suspects_list, image=image)
                image_label.image = image
                image_label.grid(row=self.suspects.index(suspect)+1, column=2)
            except:
                pass

        # NEXT
        self.next_button = tk.Button(self.suspects_list, text="Next", command=self.next_suspects)
        self.next_button.grid(row=0, column=1)
        # PREVIOUS
        self.back_button = tk.Button(self.suspects_list, text="Back", command=self.back_suspects)
        if self.index == 0:
            self.back_button.configure(state=tk.DISABLED)
        self.back_button.grid(row=0, column=0)

    def next_suspects(self):
        self.index += 5
        self.display_suspects(self.index)

    def back_suspects(self):
        self.index -= 5
        self.display_suspects(self.index)