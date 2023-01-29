import json
import tkinter as tk
from tkinter import filedialog

import matplotlib.pyplot as plt
from collections import Counter

import numpy as np



class DataAnalysis:
    def __init__(self):
        self.data_analysis = tk.Toplevel()
        self.data_analysis.title = "FBI Most Wanted - Data Analysis Dashboard"
        self.data_analysis.geometry("790x420")

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

        self.frame_time = tk.Frame(self.framebig_anal)
        self.frame_time.configure(padx=12, pady=12)
        self.frame_time.grid(row=2, column=1)

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
        self.anal_time_button = tk.Button(self.frame_analysis, text="Time Analysis", command=self.time_analysis)
        self.anal_time_button.grid(row=1,column=2)
        self.anal_timeline_button = tk.Button(self.frame_analysis, text="Line-Graph Time", command=self.time_line)
        self.anal_timeline_button.grid(row=1,column=3)

        self.anal_graphfreq_button = tk.Button(self.frame_analysis, text="Graph", command=self.create_bar_graph)
        self.anal_graphfreq_entry = tk.Entry(self.frame_analysis)
        self.anal_graphfreq_text = tk.Label(self.frame_analysis, text="where length is: ")
        self.anal_graphfreq_button.grid(row=2, column=1)
        self.anal_graphfreq_entry.grid(row=2, column=3)
        self.anal_graphfreq_text.grid(row=2, column=2)

        self.anal_piechart_button = tk.Button(self.frame_analysis, text="Pie-chart", command=self.create_pie_graph)
        self.anal_piechart_entry = tk.Entry(self.frame_analysis)
        self.anal_piechart_text = tk.Label(self.frame_analysis, text="where area is: ")
        self.anal_piechart_button.grid(row=3, column=1)
        self.anal_piechart_entry.grid(row=3, column=3)
        self.anal_piechart_text.grid(row=3, column=2)

        # OTHER FRAME

        # Results - 1
        self.results_text = tk.Label(self.frame_results, text=f"Quick preview of loaded data: \n Update to see overview of current file")
        self.results_text.pack()

        self.time_text = tk.Label(self.frame_time, text=f"Time analysis: \n Launch time analysis to see results")
        self.time_text.pack()



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

    def create_bar_graph(self):

        print(self.anal_graphfreq_entry.get())
        values = [entry[self.anal_graphfreq_entry.get()] for entry in self.sus_data]
        value_counts = dict(Counter(values))

        # No None
        value_counts = {k if k is not None else 'Unknown': v for k, v in value_counts.items()}

        keys = list(value_counts.keys())
        values = list(value_counts.values())

        plt.rcParams["figure.figsize"] = [8, 9]
        plt.rcParams["figure.autolayout"] = True

        plt.barh(keys, values)


        plt.xlabel('Frequency')
        plt.xticks(rotation=90)
        plt.ylabel(self.anal_graphfreq_entry.get())
        plt.show()

    def create_pie_graph(self):
        values = [entry[self.anal_piechart_entry.get()] for entry in self.sus_data]
        value_counts = dict(Counter(values))

        # No None
        value_counts = {k if k is not None else 'Unknown': v for k, v in value_counts.items()}

        keys = list(value_counts.keys())
        values = list(value_counts.values())

        plt.rcParams["figure.figsize"] = [8, 9]
        plt.rcParams["figure.autolayout"] = True

        plt.pie(value_counts.values(), labels=value_counts.keys())

        plt.show()

    def time_analysis(self):
        date_list = []
        for entry in self.sus_data:
            if entry["publication"] is None:
                print("Missing!")
            else:
                date_list.append(int((entry["publication"].split("-")[0])))
        print(date_list)
        self.time_text.configure(text=f"Time Analysis: \nMedian time of publication: {np.median(date_list)} \n Average time of publication {np.average(date_list)} \n Std. deviation of publication: {np.std(date_list)} \n Variance of publication: {np.var(date_list)}")

    def time_line(self):
        years = [str(year) for year in range(2010, 2024)]
        year_count = {year: 0 for year in years}
        for entry in self.sus_data:
            if entry["publication"] is None:
                year = "1900"
            else:
                year = entry["publication"].split("-")[0]
            if year in years:
                year_count[year] += 1

        plt.rcParams["figure.figsize"] = [9, 6]
        plt.rcParams["figure.autolayout"] = True

        plt.plot(years, list(year_count.values()))
        plt.xlabel("Year")
        plt.ylabel("Number of Entries")
        plt.title("Number of Entries per Year")
        plt.show()

    def show(self):
        self.data_analysis.mainloop()

