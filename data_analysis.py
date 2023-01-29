import json
import tkinter as tk
from tkinter import filedialog


class DataAnalysis:
    def __init__(self):
        self.data_analysis = tk.Toplevel()
        self.data_analysis.title = "FBI Most Wanted - Data Analysis Panel"
        self.data_analysis.geometry("720x420")

        # Data
        self.sus_data = None
        self.amount = 0
        self.missing = 0
        self.appr = 0
        self.dead = 0
        self.found = 0
        self.conceded = 0
        self.recovered = 0

        # TODO !WAŻNE! pozmieniać w kodzie wszystkie te skróty gdzie zamiast analysis jest anal bo to źle wygląda xD
        # Frame management - big-frames
        self.framebig_load = tk.Frame(self.data_analysis)
        self.framebig_load.configure(padx=24, pady=12, relief=tk.GROOVE, border=2)
        self.framebig_load.grid(row=1, column=1)

        self.framebig_anal = tk.Frame(self.data_analysis)
        self.framebig_anal.configure(padx=24, pady=12, relief=tk.GROOVE, border=2)
        self.framebig_anal.grid(row=1, column=2)

        # Frame management - sub-frames
        # Loading
        self.frame_load = tk.Frame(self.framebig_load)
        self.frame_load.configure(padx=12, pady=12)
        self.frame_load.grid(row=1, column=1)

        self.frame_filter = tk.Frame(self.framebig_load)
        self.frame_filter.configure(padx=12, pady=12)
        self.frame_filter.grid(row=2, column=1)

        self.frame_analysis = tk.Frame(self.framebig_load)
        self.frame_analysis.configure(padx=12, pady=12)
        self.frame_analysis.grid(row=3, column=1)

        # Results
        self.frame_results = tk.Frame(self.framebig_anal)
        self.frame_results.configure(padx=12, pady=12)
        self.frame_results.grid(row=1, column=1)

        # Data loading - 1
        self.load_dialog = tk.Button(self.frame_load, text="Load Data", command=self.open_file)
        self.load_text = tk.Label(self.frame_load, text="1. Select .JSON file to be used as data:")
        self.load_text.pack()
        self.load_dialog.pack()

        # Data filtering - 2
        self.filter_text = tk.Label(self.frame_filter, text="2. Apply a filter if desired - category equal to phrase:")
        self.filter_text.pack()
        # Filter by:
        self.filter_by = tk.StringVar()
        self.filter_options = ["title", "sex", "nationality", "eyes_raw", "hair", "race_raw"]
        self.filter_dropdown = tk.OptionMenu(self.frame_filter, self.filter_by, *self.filter_options)
        self.filter_phrase = tk.Entry(self.frame_filter)
        self.filter_label = tk.Label(self.frame_filter, text=" must be: ")
        self.filter_button = tk.Button(self.frame_filter, text="Save new .JSON", command=self.save_filtered)
        self.filter_button.pack(side=tk.TOP)
        self.filter_dropdown.pack(side=tk.LEFT)
        self.filter_label.pack(side=tk.LEFT)
        self.filter_phrase.pack(side=tk.RIGHT)

        # Data analysis choices - 3
        self.anal_text = tk.Label(self.frame_analysis, text="3. Select desired analysis:")
        self.anal_quick_button = tk.Button(self.frame_analysis, text="Update Preview", command=self.quick_results)
        self.anal_text.grid(row=0, column=2)
        self.anal_quick_button.grid(row=1, column=1)

        self.anal_graphfreq_button = tk.Button(self.frame_analysis, text="Graph", command=self.quick_results)
        self.anal_graphfreq_entry = tk.Entry(self.frame_analysis)
        self.anal_graphfreq_text = tk.Label(self.frame_analysis, text="where length is: ")
        self.anal_graphfreq_button.grid(row=2, column=1)
        self.anal_graphfreq_entry.grid(row=2, column=3)
        self.anal_graphfreq_text.grid(row=2, column=2)

        self.anal_piechart_button = tk.Button(self.frame_analysis, text="Pie-chart", command=self.quick_results)
        self.anal_piechart_entry = tk.Entry(self.frame_analysis)
        self.anal_piechart_text = tk.Label(self.frame_analysis, text="where area is: ")
        self.anal_piechart_button.grid(row=3, column=1)
        self.anal_piechart_entry.grid(row=3, column=3)
        self.anal_piechart_text.grid(row=3, column=2)

        # OTHER FRAME

        # Results - 1
        self.results_text = tk.Label(self.frame_results, text=f"Quick preview of loaded data: \n Update to see overview of current file")
        self.results_text.pack()



    def open_file(self):
        filepath = filedialog.askopenfilename(defaultextension=".json", initialdir="./", initialfile="suspects_mega.json", title="Select a file",
                                              filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        with open(filepath, 'r') as f:
            self.sus_data = json.load(f)
        self.load_text.configure(text="1. File successfully loaded!", fg='green')

    def save_filtered(self):
        value = self.filter_phrase.get()
        key = self.filter_by.get()

        filtered_data = [entry for entry in self.sus_data if entry[key] == value]
        with open("filtered_mega.json", 'w') as f:
            json.dump(filtered_data, f)

        self.filter_text.configure(text="2. Filtered file saved successfully!", fg='green')
        print(f"{key} must be: {value}")


    def quick_results(self):
        self.amount = len(self.sus_data)
        self.missing = len([entry for entry in self.sus_data if entry["status"] == "na"])
        self.appr = len([entry for entry in self.sus_data if entry["status"] == "captured"])
        self.dead = len([entry for entry in self.sus_data if entry["status"] == "deceased"])
        self.found = len([entry for entry in self.sus_data if entry["status"] == "located"])
        self.conceded = len([entry for entry in self.sus_data if entry["status"] == "surrendered"])
        self.recovered = len([entry for entry in self.sus_data if entry["status"] == "recovered"])

        print("Quick results")
        self.results_text.configure(text=f"Quick preview of loaded data: \nTotal: {self.amount} \n Not Apprehended / Missing: {self.missing} \n Captured / Found: {self.appr} \n Dead: {self.dead} \n Surrendered: {self.conceded} \n Recovered: {self.recovered}")


    def show(self):
        self.data_analysis.mainloop()

