import tkinter as tk


class DataAnalysis:
    def __init__(self):
        self.data_analysis = tk.Toplevel()
        self.data_analysis.title = "FBI Most Wanted - Data Analysis Panel"
        self.data_analysis.geometry("640x360")

    def show(self):
        self.data_analysis.mainloop()

