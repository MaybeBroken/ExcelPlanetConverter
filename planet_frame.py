import customtkinter as ctk
import tkinter as tk

import openpyxl
from lxml import etree

from planet import Planet

limit_none = lambda v: True
limit_integer = lambda v: isinstance(v, int)
limit_float = lambda v: isinstance(v, float) or isinstance(v, int)
def limit_color(color_str):
    for val in color_str.split(" "):
        if not (val.isdigit() and 0 <= int(val) < 256):
            return False
    return True




ctk.set_appearance_mode("dark")

attr_to_display = {
    "name": "Name",
    "government": "Government",
    "type": "Type",
    "surface": "Surface",
    "color": "Color",
    "orbitaldistance": "Orbital Distance",
    "eccentricity": "Eccentricity",
    "argumentofperiapsis": "Argument of Periapsis",
    "orbitalposition": "Orbital Position",
    "orbitalperiod": "Orbital Period",
    "rotationalperiod": "Rotational Period",
    "mass": "Mass",
    "radius": "Radius",
    "density": "Density",
    "inclination": "Inclination",
    "temperature": "Temperature",
}

value_limits = {
    "name": (limit_none, None),
    "government": (limit_none, None),
    "type": (limit_none, lambda m, **kwargs: ctk.CTkOptionMenu(m, values=["Rock", "Ice", "Gas_Giant", "Volcanic", "Water", "Terrestrial", ])),
    "surface": (limit_none, None),
    "color": (limit_color, None, "RGBA"),
    "orbitaldistance": (limit_float, None, "°"),
    "eccentricity": (limit_float, None),
    "argumentofperiapsis": (limit_float, None, "°"),
    "orbitalposition": (limit_float, None, "°"),
    "orbitalperiod": (limit_float, None),
    "rotationalperiod": (limit_float, None),
    "mass": (limit_float, None, "und"),
    "radius": (limit_float, None),
    "density": (limit_float, None, "(g/cm³)"),
    "inclination": (limit_float, None, "°"),
    "temperature": (limit_float, None, "K"),
}


class PlanetFrame(ctk.CTkFrame):
    systems = {}
    
    def __init__(self, master, planet_obj: Planet, system):
        super().__init__(master, fg_color=("gray92", "gray14"), corner_radius=8, border_width=4, border_color=("gray92", "gray14"))
        self.columnconfigure(0, weight=1)
        self.title = ctk.CTkButton(self, text=planet_obj.__getattribute__("name") or " ", command=self.toggle_expansion)
        self.title.grid(sticky="EW", columnspan=3)
        self.expanded = False
        self.grid_propagate(False)
        self.update_idletasks()
        self.configure(height=self.title.winfo_height(), width=258)
        self.target_height = self.title.winfo_height()
        self.planet = planet_obj
        self.system = system
        if system in PlanetFrame.systems.keys():
            PlanetFrame.systems[system].append(self)
        else:
            PlanetFrame.systems[system] = [self]
        
        for attr, attr_attr in value_limits.items():
            try:
                __value = planet_obj.__getattribute__(attr)
            except AttributeError:
                __value = ""
            self.__setattr__(f"planet.{attr}", __value)
            self.__setattr__(f"planet.{attr}.label", ctk.CTkLabel(self, text=f"{attr_to_display[attr]}:"))
            try:
                self.__setattr__(f"planet.{attr}.label_after", ctk.CTkLabel(self, text=f"{attr_attr[2] or ' '}"))
            except IndexError:
                self.__setattr__(f"planet.{attr}.label_after", ctk.CTkLabel(self, text=f""))
            self.__setattr__(f"planet.{attr}.field", (attr_attr[1] or ctk.CTkEntry)(self, border_color=("gray92", "gray14")))
            self.__getattribute__(f"planet.{attr}.label").grid(sticky="E", padx=4, pady=1)
            field = self.__getattribute__(f"planet.{attr}.field")
            if isinstance(field, ctk.CTkEntry):
                field.insert(0, str(__value))
            else:
                field.set(__value)
            field.grid(row=self.__getattribute__(f"planet.{attr}.label").grid_info()["row"], column=1, padx=(4, 0), sticky="W")
            self.__getattribute__(f"planet.{attr}.label_after").grid(row=self.__getattribute__(f"planet.{attr}.label").grid_info()["row"], column=2, sticky="W", padx=(0, 4))
            self.__setattr__(f"planet.{attr}.limit", attr_attr[0])
        self.grid_propagate(False)
    
    def toggle_expansion(self):
        if not self.expanded:
            for p in PlanetFrame.systems[self.system]:
                p.de_expand()
            self.grid_propagate(True)
        else:
            self.grid_propagate(False)
            self.configure(height=self.title.winfo_height(), width=258, require_redraw=True)
        self.expanded = not self.expanded
    
    def de_expand(self):
        self.grid_propagate(False)
        self.configure(height=self.title.winfo_height(), width=258, require_redraw=True)
        self.expanded = False


if __name__ == '__main__':
    
    planets = [
        Planet("b"),
        Planet("c"),
        Planet("d"),
        Planet("e"),
        Planet("f"),
        Planet("g"),
        Planet("h"),
        # Planet("i"),
        # Planet("j"),
    ]
    print("building")
    spreadsheet = openpyxl.open("worldbuilding spreadsheet 33 sextantis.xlsx", data_only=True)
    for planet in planets:
        planet.fill_attr(spreadsheet)
    print("done")
    root = ctk.CTk()
    root.title("Planet Display Test")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    container = ctk.CTkScrollableFrame(root, width=350, height=400)
    container.grid(sticky="NESW")
    for planet in planets:
        # print(planet.get_xml_repr())
        # print(etree.tostring(etree.fromstring(planet.get_xml_repr()), pretty_print=True, encoding=str))
        frame = PlanetFrame(container, planet, "33 sextantis")
        frame.grid()
        # frame.grid_propagate(False)
    root.mainloop()
