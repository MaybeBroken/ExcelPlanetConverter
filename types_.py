import tkinter
from typing import Callable

import customtkinter as ctk
from tkinter.filedialog import askopenfilename


class Attribute:
    def __init__(self, label: ctk.CTkLabel, value, ctk_vars: list[ctk.Variable], var_get: Callable):
        self.label = label
        self.value = value
        self.vars = ctk_vars
        self.get = var_get
    
    @classmethod
    def _short_text(cls, master, value: str, label_text: str, after_text="", editable=True):
        ctk_vars = [ctk.StringVar(master, value)]
        label = ctk.CTkLabel(master, text=label_text)
        label.grid(sticky="E")
        entry = ctk.CTkEntry(master, textvariable=ctk_vars[0], state=tkinter.NORMAL if editable else tkinter.DISABLED)
        entry.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="EW")
        after = ctk.CTkLabel(master, text=after_text)
        after.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 2, sticky="W", padx=(2, 4))
        
        return cls(label, value, ctk_vars, ctk_vars[0].get)
    
    @classmethod
    def _dropdown(cls, master, value, label_text: str, options: list, after_text="", editable=True):
        ctk_vars = [ctk.StringVar(master, value)]
        label = ctk.CTkLabel(master, text=label_text)
        label.grid(sticky="E")
        entry = ctk.CTkOptionMenu(master, values=options, variable=ctk_vars[0])
        entry.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="EW")
        after = ctk.CTkLabel(master, text=after_text)
        after.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 2, sticky="W", padx=(2, 4))
        
        return cls(label, value, ctk_vars, ctk_vars[0].get)
    
    @classmethod
    def name(cls, master, value="Unnamed"):
        return cls._short_text(master, value, "Name: ")
    
    @classmethod
    def government(cls, master, value=""):
        return cls._dropdown(master, value or "Unknown", "Government: ", ["Anarchical", "Dictatorship", "Democracy", "Fascism", "Feudalism", "Republic", "Socialism", "Unknown"])
    
    @classmethod
    def description(cls, master, value=""):
        ctk_vars = [ctk.StringVar(master, value)]
        label = ctk.CTkLabel(master, text="Description: ")
        label.grid(sticky="E")
        entry = ctk.CTkTextbox(master, height=50)
        entry.insert(1.0, value)
        entry.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="W")
        
        return cls(label, value, ctk_vars, lambda: entry.get(1.0, ctk.END))
    
    @classmethod
    def type(cls, master, value=None):
        return cls._dropdown(master, value or "Rock", "Type: ", ["Rock", "Ice", "Gas_Giant", "Volcanic", "Water", "Terrestrial"])
    
    @classmethod
    def surface(cls, master, value: str = None):
        
        def pick_file():
            return askopenfilename(filetypes=[("Image", [".png", ".jpg"])])
        
        def update_short(*_):
            ctk_vars[1].set(ctk_vars[0].get().split("/")[-1] or "No File Specified")
        
        ctk_vars = [ctk.StringVar(master, value), ctk.StringVar(master, value or "No File Specified")]
        ctk_vars[0].trace_add("write", update_short)
        label = ctk.CTkLabel(master, text="Surface: ")
        label.grid(sticky="E")
        entry = ctk.CTkButton(master, textvariable=ctk_vars[1], command=lambda: ctk_vars[0].set(pick_file()))
        entry.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="W")
        
        return cls(label, value, ctk_vars, ctk_vars[0].get)
    
    @classmethod
    def color(cls, master, value: str = "0 176 80"):
        if len(value.strip().split(" ")) == 3:
            value += " 255"
        ctk_vars = [ctk.StringVar(master, v) for v in value.strip().split(" ")]
        label = ctk.CTkLabel(master, text="Color: ")
        label.grid(sticky="E")
        entry_frame = ctk.CTkFrame(master)
        entry = ctk.CTkEntry(entry_frame, textvariable=ctk_vars[0], width=40)
        entry.grid(row=0, column=0)
        entry = ctk.CTkEntry(entry_frame, textvariable=ctk_vars[1], width=40)
        entry.grid(row=0, column=1)
        entry = ctk.CTkEntry(entry_frame, textvariable=ctk_vars[2], width=40)
        entry.grid(row=0, column=2)
        entry = ctk.CTkEntry(entry_frame, textvariable=ctk_vars[3], width=40)
        entry.grid(row=0, column=3)
        entry_frame.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="W")
        
        return cls(label, value, ctk_vars, lambda: " ".join([_.get().strip() for _ in ctk_vars]))
    
    @classmethod
    def orbitaldistance(cls, master, value=None, moon=False):
        return cls._short_text(master, value, "Orbital Distance: ", "km" if moon else "AU")
    
    @classmethod
    def eccentricity(cls, master, value=None):
        return cls._short_text(master, value, "Eccentricity: ")
    
    @classmethod
    def argumentofperiapsis(cls, master, value=None):
        return cls._short_text(master, value, "Argument of Periapsis: ")
    
    @classmethod
    def orbitalposition(cls, master, value=None):
        return cls._short_text(master, value, "Orbital Position: ")
    
    @classmethod
    def orbitalperiod(cls, master, value=None):
        return cls._short_text(master, value, "Orbital Period: ", "Earth days", False)
    
    @classmethod
    def rotationalperiod(cls, master, value=None):
        return cls._short_text(master, value, "Rotational Period: ", "h")
    
    @classmethod
    def mass(cls, master, value=None):
        return cls._short_text(master, value, "Mass: ")
    
    @classmethod
    def radius(cls, master, value=None, system=False, moon=False):
        return cls._short_text(master, value, "Radius: ", "Solar Radii" if system else "Lunar Radii" if moon else "Earth Radii")
    
    @classmethod
    def density(cls, master, value=None):
        return cls._short_text(master, value, "Density: ", "kg/m^3", False)
    
    @classmethod
    def inclination(cls, master, value=None):
        return cls._short_text(master, value, "Inclination: ")
    
    @classmethod
    def temperature(cls, master, value=None):
        return cls._short_text(master, value, "Temperature: ", "K")
    
    @classmethod
    def faction(cls, master, value=""):
        return cls._dropdown(master, value, "Faction: ", ["House Anoway", "House Cardilir", "House Dezadi", "House Meylek", "House Piddlewee", "House Terra", "House Tinarrah", "Independent"])
    
    @classmethod
    def class_(cls, master, value=""):
        return cls._short_text(master, value, "Star Class: ")
    
    @classmethod
    def luminosity(cls, master, value=""):
        return cls._short_text(master, value, "Luminosity: ")
    
    @classmethod
    def position(cls, master, value: str = "0 0 0"):
        ctk_vars = [ctk.StringVar(master, v) for v in value.strip().split(" ")]
        label = ctk.CTkLabel(master, text="Position: ")
        label.grid(sticky="E")
        entry_frame = ctk.CTkFrame(master)
        entry = ctk.CTkEntry(entry_frame, textvariable=ctk_vars[0], width=40)
        entry.grid(row=0, column=0)
        entry = ctk.CTkEntry(entry_frame, textvariable=ctk_vars[1], width=40)
        entry.grid(row=0, column=1)
        entry = ctk.CTkEntry(entry_frame, textvariable=ctk_vars[2], width=40)
        entry.grid(row=0, column=2)
        entry_frame.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="W")
        
        return cls(label, value, ctk_vars, lambda: " ".join([_.get().strip() for _ in ctk_vars]))
    
    @classmethod
    def ambient(cls, master, value: str = "255 255 255"):
        if len(value.strip().split(" ")) == 3:
            value += " 255"
        ctk_vars = [ctk.StringVar(master, v) for v in value.strip().split(" ")]
        label = ctk.CTkLabel(master, text="Ambient: ")
        label.grid(sticky="E")
        entry_frame = ctk.CTkFrame(master)
        entry = ctk.CTkEntry(entry_frame, textvariable=ctk_vars[0], width=40)
        entry.grid(row=0, column=0)
        entry = ctk.CTkEntry(entry_frame, textvariable=ctk_vars[1], width=40)
        entry.grid(row=0, column=1)
        entry = ctk.CTkEntry(entry_frame, textvariable=ctk_vars[2], width=40)
        entry.grid(row=0, column=2)
        entry = ctk.CTkEntry(entry_frame, textvariable=ctk_vars[3], width=40)
        entry.grid(row=0, column=3)
        entry_frame.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="W")
        
        return cls(label, value, ctk_vars, lambda: " ".join([_.get().strip() for _ in ctk_vars]))
    
    @classmethod
    def pedia(cls, master, value=""):
        return cls._short_text(master, value, "Pedia: ")
    
    # @classmethod
    # def new(cls, master, value):
    #     ctk_vars = [ctk.StringVar(master, value)]
    #     label = ctk.CTkLabel(master, text="New: ")
    #     label.grid(sticky="E")
    #     entry = ctk.CTkEntry(master, textvariable=ctk_vars[0])
    #     entry.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="W")
    #
    #     return cls(label, value, ctk_vars, ctk_vars[0].get)


if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    l = []
    for attr in vars(Attribute).keys():
        if attr.startswith("_"):
            continue
        l.append(getattr(Attribute, attr)(root, "test t t "))
    root.mainloop()
