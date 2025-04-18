import tkinter
from typing import Callable, Iterable

import customtkinter as ctk
from tkinter.filedialog import askopenfilename

from PIL import Image


class Attribute:
    def __init__(self, label: ctk.CTkLabel, value, ctk_vars: list[ctk.Variable], var_get: Callable):
        self.label = label
        self.value = value
        self.vars = ctk_vars
        self.get = var_get
    
    @classmethod
    def _short_text(cls, master, value: str, label_text: str, after_text="", editable=True, justify="left", width=100):
        """
        Short Text Input Creator
        :param master:
        :param value:
        :param label_text:
        :param after_text:
        :param editable:
        :return:
        """
        ctk_vars = [ctk.StringVar(master, value)]
        
        label = ctk.CTkLabel(master, text=label_text)
        label.grid(sticky="E")
        
        entry_frame = ctk.CTkFrame(master, fg_color="transparent")
        
        entry = ctk.CTkEntry(entry_frame, textvariable=ctk_vars[0], state="normal" if editable else "disabled", border_width=2 if editable else 0, justify=justify, width=width)
        entry.grid(row=0, column=0, sticky="EW")
        
        after = ctk.CTkLabel(entry_frame, text=after_text)
        after.grid(row=0, column=1, sticky="W", padx=2, pady=2)
        
        entry_frame.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="W")
        
        return cls(label, value, ctk_vars, ctk_vars[0].get)
    
    @classmethod
    def _multi_short(cls, master, value, label_text: str, after_text="", editable=True):
        """
        Multiple Short Text (separated by ' ') Input Creator
        :param master: parent container
        :param value: value
        :param label_text: text of label
        :param after_text: text after input
        :param editable: whether this input is editable
        :return:
        """
        ctk_vars = [ctk.StringVar(master, v) for v in value.strip().split(" ")]
        
        label = ctk.CTkLabel(master, text=label_text)
        label.grid(sticky="E")
        
        entry_frame = ctk.CTkFrame(master, fg_color="transparent")
        for i, var in enumerate(ctk_vars):
            entry = ctk.CTkEntry(entry_frame, textvariable=var, width=36, state="normal" if editable else "disabled", border_width=2 if editable else 0, justify="center")
            entry.grid(row=0, column=i, padx=2, pady=2)
        
        after = ctk.CTkLabel(entry_frame, text=after_text)
        after.grid(row=entry.grid_info()["row"], column=entry.grid_info()["column"] + 2, sticky="W", padx=2, pady=2)  # NOQA
        
        entry_frame.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="W")
        
        return cls(label, value, ctk_vars, lambda: " ".join([_.get().strip() for _ in ctk_vars]))
    
    @classmethod
    def _long_text(cls, master, value: str, label_text: str, after_text="", editable=True):
        """
        Long Text Input Creator
        :param master:
        :param value:
        :param label_text:
        :param after_text:
        :param editable:
        :return:
        """
        ctk_vars = [ctk.StringVar(master, value)]
        
        label = ctk.CTkLabel(master, text=label_text)
        label.grid(sticky="NE")
        
        entry = ctk.CTkTextbox(master, height=50)
        entry.insert(1.0, value)
        entry.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="W", padx=2, pady=2)
        
        return cls(label, value, ctk_vars, lambda: entry.get(1.0, ctk.END))
    
    @classmethod
    def _file_input(cls, master, value, label_text: str, filetypes: Iterable[tuple[str, str | list[str] | tuple[str, ...]]] | None, after_text="", editable=True, show_image=True):
        """
        :param master:
        :param value:
        :param label_text:
        :param filetypes:
        :param after_text: Not used
        :param editable:
        :param show_image:
        :return:
        """
        def pick_file():
            return askopenfilename(filetypes=filetypes)
        
        def update_short(*_):
            ctk_vars[1].set(ctk_vars[0].get().split("/")[-1] or "No File Specified")
        
        def update_image(*_):
            try:
                display.configure(image=ctk.CTkImage(Image.open((ctk_vars[0].get())), size=(28, 28)))
            except AttributeError:
                pass
        
        ctk_vars = [ctk.StringVar(master, value), ctk.StringVar(master, value or "No File Specified")]
        ctk_vars[0].trace_add("write", update_short)
        
        label = ctk.CTkLabel(master, text=label_text)
        label.grid(sticky="E")
        
        entry_frame = ctk.CTkFrame(master, fg_color="transparent")
        
        entry = ctk.CTkButton(entry_frame, textvariable=ctk_vars[1], command=lambda: ctk_vars[0].set(pick_file()), width=0, state="normal" if editable else "disabled")
        entry.grid(row=0, column=0, sticky="W", padx=2, pady=2)
        
        if show_image:
            try:
                display = ctk.CTkLabel(entry_frame, image=ctk.CTkImage(Image.open(open(ctk_vars[0].get()))))
                display.grid(row=0, column=1, sticky="W", padx=2, pady=2)
            except (FileNotFoundError, UnicodeDecodeError):
                display = ctk.CTkLabel(entry_frame, text="")
                display.grid(row=0, column=1, sticky="W", padx=2, pady=2)
        
            ctk_vars[0].trace_add("write", update_image)
        
        entry_frame.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="W")
        
        return cls(label, value, ctk_vars, ctk_vars[0].get)
    
    @classmethod
    def _dropdown(cls, master, value, label_text: str, options: list, after_text="", editable=True):
        """
        Dropdown Creator
        :param master:
        :param value:
        :param label_text:
        :param options:
        :param after_text:
        :param editable:
        :return:
        """
        ctk_vars = [ctk.StringVar(master, value)]
        
        label = ctk.CTkLabel(master, text=label_text)
        label.grid(sticky="E")
        
        entry_frame = ctk.CTkFrame(master, fg_color="transparent")
        
        entry = ctk.CTkOptionMenu(entry_frame, values=options, variable=ctk_vars[0], state="normal" if editable else "disabled")
        entry.grid(row=0, column=0, sticky="EW")
        
        after = ctk.CTkLabel(entry_frame, text=after_text)
        after.grid(row=0, column=1, sticky="W", padx=2, pady=2)
        
        entry_frame.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="W")
        
        return cls(label, value, ctk_vars, ctk_vars[0].get)
    
    @classmethod
    def _mineral_values(cls, master, value, label_text: str, options: list[str], editable=True):
        """
        Mineral Input Creator
        :param master: parent container
        :param value: value
        :param label_text: text of label
        :param editable: whether this input is editable
        :return:
        """
        ctk_vars = [ctk.StringVar(master, v) for v in value.strip().split(" ")]
        
        label = ctk.CTkLabel(master, text=label_text)
        label.grid(sticky="E")
        
        entry_frame = ctk.CTkFrame(master, fg_color="transparent")
        
        
        
        entry_frame.grid(row=label.grid_info()["row"], column=label.grid_info()["column"] + 1, sticky="W")
        
        return cls(label, value, ctk_vars, lambda: " ".join([_.get().strip() for _ in ctk_vars]))
    
    @classmethod
    def name(cls, master, value="Unnamed"):
        return cls._short_text(master, value, "Name: ", width=200)
    
    @classmethod
    def government(cls, master, value=""):
        return cls._dropdown(master, value or "Unknown", "Government: ", ["Anarchical", "Dictatorship", "Democracy", "Fascism", "Feudalism", "Republic", "Socialism", "Unknown"])
    
    @classmethod
    def description(cls, master, value=""):
        cls._long_text(master, value, "Description: ")
    
    @classmethod
    def type(cls, master, value=None):
        return cls._dropdown(master, value or "Rock", "Type: ", ["Rock", "Ice", "Gas_Giant", "Volcanic", "Water", "Terrestrial"])
    
    @classmethod
    def surface(cls, master, value: str = None):
        return cls._file_input(master, value, "Surface Map: ", [("Image", [".png", ".jpg"])])
    
    @classmethod
    def specular(cls, master, value: str = None):
        return cls._file_input(master, value, "Specular Map: ", [("Image", [".png", ".jpg"])])
    
    @classmethod
    def normal(cls, master, value: str = None):
        return cls._file_input(master, value, "Normal Map: ", [("Image", [".png", ".jpg"])])
    
    @classmethod
    def atmosphere_texture(cls, master, value=""):
        return cls._file_input(master, value, "Atmosphere Map: ", [("Image", [".png", ".jpg"])])
    
    @classmethod
    def color(cls, master, value: str = "0 176 80"):
        value = value.strip()
        while len(value.strip().split(" ")) <= 3:
            value += " 255"
        return cls._multi_short(master, value, "Color: ", editable=False)
    
    @classmethod
    def orbitaldistance(cls, master, value=None, moon=False):
        return cls._short_text(master, value, "Orbital Distance: ", "km" if moon else "AU")
    
    @classmethod
    def eccentricity(cls, master, value=None):
        return cls._short_text(master, value, "Eccentricity: ")
    
    @classmethod
    def argumentofperiapsis(cls, master, value=None):
        return cls._short_text(master, value, "Argument of Periapsis: ", "°")
    
    @classmethod
    def orbitalposition(cls, master, value=None):
        return cls._short_text(master, value, "Orbital Position: ", "°")
    
    @classmethod
    def orbitalperiod(cls, master, value=None):
        return cls._short_text(master, value, "Orbital Period: ", "Earth days", False)
    
    @classmethod
    def rotationalperiod(cls, master, value=None):
        return cls._short_text(master, value, "Rotational Period: ", "h")
    
    @classmethod
    def mass(cls, master, value=None):
        return cls._short_text(master, value, "Mass: ", "kg")
    
    @classmethod
    def radius(cls, master, value=None, system=False, moon=False):
        return cls._short_text(master, value, "Radius: ", "Solar Radii" if system else "Lunar Radii" if moon else "Earth Radii")
    
    @classmethod
    def density(cls, master, value=None):
        return cls._short_text(master, value, "Density: ", "kg/m^3", False)
    
    @classmethod
    def inclination(cls, master, value=None):
        return cls._short_text(master, value, "Inclination: ", "°")
    
    @classmethod
    def temperature(cls, master, value=None):
        return cls._short_text(master, value, "Temperature: ", "K")
    
    @classmethod
    def faction(cls, master, value=""):
        return cls._dropdown(master, value or "Independent", "Faction: ", ["House Anoway", "House Cardilir", "House Dezadi", "House Meylek", "House Piddlewee", "House Terra", "House Tinarrah", "Independent"])
    
    @classmethod
    def class_(cls, master, value=""):
        return cls._dropdown(master, value or "M", "Star Class: ", ["O", "B", "A", "F", "G", "K", "M"])
    
    @classmethod
    def luminosity(cls, master, value=""):
        return cls._short_text(master, value, "Luminosity: ", "Solar Luminosities")
    
    @classmethod
    def position(cls, master, value: str = "0 0 0"):
        value = value.strip()
        while len(value.strip().split(" ")) <= 2:
            value += " 0"
        return cls._multi_short(master, value, "Position: ", "LY")
    
    @classmethod
    def ambient(cls, master, value: str = "255 255 255"):
        value = value.strip()
        while len(value.strip().split(" ")) <= 3:
            value += " 255"
        return cls._multi_short(master, value, "Ambient: ", editable=False)
    
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
    ctk.set_default_color_theme("./blue.json")
    root = ctk.CTk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    sf = ctk.CTkScrollableFrame(root, width=400, height=900)
    sf.grid(sticky="NESW")
    l = []
    for attr in vars(Attribute).keys():
        if attr.startswith("_"):
            continue
        l.append(getattr(Attribute, attr)(sf))
    root.mainloop()
