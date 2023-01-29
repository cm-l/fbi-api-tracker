import tkinter as tk
import requests
import json
from tkinter import messagebox
import tkinter.ttk as ttk

from data_analysis import DataAnalysis
from suslist import SuspectsList


class App:
    def __init__(self):
        self.open_analysis = None
        self.loading_label = None
        self.progress = None
        self.root = tk.Tk()
        self.root.geometry("640x360")
        self.root.title("FBI Most Wanted - Search")

        # Frame management
        self.frame_search = tk.Frame(self.root)
        self.frame_search.configure(padx=32, pady=32, relief=tk.RAISED, border=2)
        self.frame_search.pack(side=tk.TOP)

        # Create a variable to store the selected search parameter
        self.parameter = tk.StringVar()
        self.parameter.set("title")

        # Create a dropdown menu to allow the user to select the search parameter
        self.parameter_dropdown = tk.OptionMenu(self.frame_search, self.parameter, "title", "status", "person_classification")
        self.parameter_dropdown.pack()

        # Create an entry widget for the user to enter the search term
        self.search_term = tk.Entry(self.frame_search)
        self.search_term.pack()

        # Create a button to initiate the search
        self.search_button = tk.Button(self.frame_search, text="Search", command=self.search)
        self.search_button.pack()

        # Button to create mega json
        self.load_button = tk.Button(self.root, text="Load Data", command=self.load_data)
        self.load_button.pack()

        # Open analysis button
        self.open_analysis = tk.Button(self.root, text="Open Analysis Panel", command=open_analysis)
        self.open_analysis.pack()

        # Create a listbox to display the search results
        self.results = tk.Listbox(self.root)
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
        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=100, mode='determinate')
        self.loading_label = tk.Label(self.root, text="Loading wanted persons...")
        self.progress.start()
        self.progress.pack()
        self.loading_label.pack()

        # Open analysis button
        self.open_analysis = tk.Button(self.root, text="Open Analysis Panel", command=open_analysis)
        self.open_analysis.pack()

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
            self.loading_label.configure(text="Successfully saved {0} wanted persons locally!".format(
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
