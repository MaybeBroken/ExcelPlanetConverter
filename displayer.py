from functools import partial
from tkinter import filedialog

import colour
import customtkinter as ctk
import tkinter as tk

import openpyxl

from planet_toplevel import PlanetWindow
from system import System
from system_toplevel import SystemWindow

class SystemFrame(ctk.CTkFrame):
    def __init__(self, master, system):
        super().__init__(master)
        self.system = system
        self.bind("<Button-1>", lambda _: self.toggle())
        self.expanded = False
        self.collapse()
    
    def collapse(self):
        self.grid_propagate(False)
        self.configure(True, height=28)

    def expand(self):
        self.grid_propagate(True)

    def toggle(self):
        if self.expanded:
            self.collapse()
            self.expanded = not self.expanded
        else:
            self.expand()
            self.expanded = not self.expanded


class MainWindow(ctk.CTk):
    def __init__(self, *spreadsheet_files):
        super().__init__()
        self.title("System Display Test")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.container = ctk.CTkScrollableFrame(self, width=350, height=400, fg_color="transparent")
        self.container.grid(sticky="NESW")
        self.container.columnconfigure(0, weight=1)
        
        self.system_frames = []
        for spread_file in spreadsheet_files:
            spreadsheet = openpyxl.open(spread_file, data_only=True)
            
            system = System()
            system.fill_attr(spreadsheet)
            
            system_frame = SystemFrame(self.container, system)
            system_frame.grid(sticky="EW")
            system_frame.columnconfigure(0, weight=1)
            
            self.system_frames.append(system_frame)
            
            button = ctk.CTkButton(system_frame,
                                   fg_color=colour.rgb2hex((int(c) / 256 for c in system.color.split(" ")[0:3])),
                                   hover_color=colour.rgb2hex((int(c) / (256 + 128) for c in system.color.split(" ")[0:3])),
                                   text_color=colour.rgb2hex((int(c) / 512 for c in system.color.split(" ")[0:3])),
                                   textvariable=system.name_var,
                                   command=partial(lambda p: SystemWindow(self, p), system)
                                   )
            button.grid(row=1, sticky="W")
            for planet in system.planets:
                button = ctk.CTkButton(system_frame,
                                       fg_color=colour.rgb2hex((int(c) / 256 for c in planet.color.split(" ")[0:3])),
                                       hover_color=colour.rgb2hex((int(c) / (256 + 128) for c in planet.color.split(" ")[0:3])),
                                       text_color=colour.rgb2hex((int(c) / 512 for c in planet.color.split(" ")[0:3])),
                                       textvariable=planet.name_var,
                                       command=partial(lambda p: PlanetWindow(self, p, "33 sextantis"), planet))
                button.grid(sticky="W", padx=(16, 0))
        
        
if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    spreads = filedialog.askopenfilenames(defaultextension=".xlsx")
    if not spreads:
        exit(-1)
    main_window = MainWindow(*spreads)
    main_window.mainloop()
