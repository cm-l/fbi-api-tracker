import tkinter as tk
import requests
import json
from tkinter import messagebox
import tkinter.ttk as ttk

from data_analysis import DataAnalysis
from suslist import SuspectsList

from PIL import Image, ImageTk


class App:
    def __init__(self):
        self.open_analysis = None
        self.loading_label = None
        self.progress = None
        self.root = tk.Tk()
        self.root.geometry("680x260")
        self.root.title("FBI Most Wanted - Search or Analyze")

        # Frame management
        self.frame_search = tk.Frame(self.root)
        self.frame_search.configure(padx=32, pady=32, relief=tk.GROOVE, border=2)
        self.frame_search.grid(column=1, row=1)

        self.frame_branding = tk.Frame(self.root)
        self.frame_branding.configure(padx=16, pady=16, relief=tk.FLAT, border=5)
        self.frame_branding.grid(column=2, row=1)

        self.frame_analyze = tk.Frame(self.root)
        self.frame_analyze.configure(padx=16, pady=16, relief=tk.GROOVE, border=2)
        self.frame_analyze.grid(column=3, row=1)

        # Create a variable to store the selected search parameter
        self.parameter = tk.StringVar()
        self.parameter.set("title")

        # Create a dropdown menu to allow the user to select the search parameter
        self.parameter_title = tk.Label(self.frame_search, text="1. Data Inspection", font=("Helvetica", 16), pady=8)
        self.parameter_text = tk.Label(self.frame_search, text="Search person by:")
        self.parameter_dropdown = tk.OptionMenu(self.frame_search, self.parameter, "title", "status",
                                                "person_classification")
        self.parameter_title.pack()
        self.parameter_text.pack()
        self.parameter_dropdown.pack()

        # Create an entry widget for the user to enter the search term
        self.search_term = tk.Entry(self.frame_search)
        self.search_term.pack()

        # Create a button to initiate the search
        self.search_button = tk.Button(self.frame_search, text="Search", command=self.search)
        self.search_button.pack()

        # Button to create mega json and title
        self.loading_title = tk.Label(self.frame_analyze, text="2. Data Analysis", font=("Helvetica", 16), pady=8)
        self.load_button = tk.Button(self.frame_analyze, text="Load Data", command=self.load_data)
        self.loading_title.pack()
        self.load_button.pack()

        # Open analysis button
        self.open_analysis = tk.Button(self.frame_analyze, text="Open Analysis Panel", command=open_analysis)
        self.open_analysis.pack()

        # Logo and names
        self.entitle = tk.Label(self.frame_branding, text="C. Leszczyński, J. Głowaczewska\nUEP P4.0 2023", font=("Trebuchet", 9), fg='gray', pady=9)
        self.entitle.pack(side=tk.BOTTOM)

        self.logo_img = Image.open("small_fbi.png")
        self.logo = ImageTk.PhotoImage(self.logo_img)
        self.logo_label = tk.Label(self.frame_branding, image=self.logo)
        self.logo_label.pack()

        # Create a listbox to display the search results
        self.results = tk.Listbox(self.frame_analyze)
        # self.results.pack()

    def search(self):
        # Clear the previous search results
        self.results.delete(0, tk.END)

        # Get the selected search parameter and the search term
        parameter = self.parameter.get()
        term = self.search_term.get()

        # Make the API request using the requests package
        url = "https://api.fbi.gov/wanted/v1/list"
        params = {parameter: term}
        response = requests.get(url, params=params)
        data = json.loads(response.text)

        # Display the search results in the listbox
        for index, suspect in enumerate(data["items"]):
            susentry = suspect["title"]
            SuspectsList(data["items"]).show()

    def load_data(self):
        # Progress bar
        self.progress = ttk.Progressbar(self.frame_analyze, orient='horizontal', length=100, mode='determinate')
        self.loading_label = tk.Label(self.frame_analyze, text="Loading wanted persons...")
        self.progress.start()
        self.progress.pack()
        self.loading_label.pack()

        # Open analysis button
        # self.open_analysis = tk.Button(self.root, text="Open Analysis Panel", command=open_analysis)
        # self.open_analysis.pack()

        # Show buttons
        self.root.update()

        # Make the API request using the requests package
        # MEGA-JSON:
        mega_suspects_list = []

        for i in range(20):
            url_load = "https://api.fbi.gov/wanted/v1/list"
            params = {'page': i + 1, 'pageSize': 50}
            response = requests.get(url_load, params)
            suspects_data = json.loads(response.text)["items"]

            mega_suspects_list.extend(suspects_data)

            # poprogressuj sobie bar
            self.progress['value'] += 4
            self.progress.update()

            print(len(mega_suspects_list))
            self.loading_label.configure(text="Saved {0} wanted persons!".format(
                str(len(mega_suspects_list))))

        self.progress.stop()
        self.progress['value'] = 100
        self.open_analysis.configure(state=tk.NORMAL)
        with open("suspects_mega.json", "w") as f:
            json.dump(mega_suspects_list, f)


def open_analysis():
    print("Opening module...")
    DataAnalysis().show()


app = App()
app.root.mainloop()
