from tkinter import filedialog

import colour
import customtkinter as ctk
import tkinter as tk

import openpyxl

from system import System


class MainWindow(ctk.CTk):
    def __init__(self, spreadsheet):
        super().__init__()
        self.system = System()
        self.system.fill_attr(spreadsheet)
        
        
if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    spread = filedialog.askopenfilename(defaultextension=".xlsx")
    if not spread:
        exit(-1)
    main_window = MainWindow(openpyxl.open(spread, data_only=True))
    main_window.mainloop()
