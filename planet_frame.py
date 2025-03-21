from functools import partial

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

attr_prop = {
    "name": {
        "display_name": "Name",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, },
    },
    "government": {
        "display_name": "Government",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, },
    },
    "type": {
        "display_name": "Type",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkOptionMenu,
        "field_kwargs": {"values": ["Rock", "Ice", "Gas_Giant", "Volcanic", "Water", "Terrestrial"]},
    },
    "surface": {
        "display_name": "Surface",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, },
    },
    "color": {
        "display_name": "Color",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, },
    },
    "orbitaldistance": {
        "display_name": "Orbital Distance",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, },
    },
    "eccentricity": {
        "display_name": "Eccentricity",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, },
    },
    "argumentofperiapsis": {
        "display_name": "Argument of Periapsis",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, },
    },
    "orbitalposition": {
        "display_name": "Orbital Position",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, },
    },
    "orbitalperiod": {
        "display_name": "Orbital Period",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, "state": "readonly"},
    },
    "rotationalperiod": {
        "display_name": "Rotational Period",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, },
    },
    "mass": {
        "display_name": "Mass",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, },
    },
    "radius": {
        "display_name": "Radius",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, },
    },
    "density": {
        "display_name": "Density",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, "state": "readonly"},
    },
    "inclination": {
        "display_name": "Inclination",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, },
    },
    "temperature": {
        "display_name": "Temperature",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {"border_width": 0, },
    },
}


class PlanetWindow(ctk.CTkToplevel):
    systems = {}
    
    def __init__(self, master, planet_obj: Planet, system):
        super().__init__(master)
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.expanded = False
        self.planet = planet_obj
        self.title(self.planet.name)
        self.system = system
        if system in PlanetWindow.systems.keys():
            PlanetWindow.systems[system].append(self)
        else:
            PlanetWindow.systems[system] = [self]
        
        for attr, attr_attrs in attr_prop.items():
            try:
                __value = planet_obj.__getattribute__(attr)
            except AttributeError:
                __value = ""
            self.__setattr__(f"planet.{attr}", __value)
            self.__setattr__(f"planet.{attr}.label", ctk.CTkLabel(self, text=f"{attr_attrs['display_name']}:"))
            self.__setattr__(f"planet.{attr}.label_after", ctk.CTkLabel(self, text=f"{attr_attrs['display_after'] or ' '}"))
            self.__setattr__(f"planet.{attr}.field", (attr_attrs["field_type"] or ctk.CTkEntry)(self, **attr_attrs["field_kwargs"]))
            self.__getattribute__(f"planet.{attr}.label").grid(sticky="E", padx=4, pady=1)
            field = self.__getattribute__(f"planet.{attr}.field")
            if isinstance(field, ctk.CTkEntry):
                if field.cget("state") == "readonly":
                    field.configure(state="normal")
                    field.insert(0, str(__value))
                    field.configure(state="readonly")
                field.insert(0, str(__value))
            else:
                field.set(__value)
            field.grid(row=self.__getattribute__(f"planet.{attr}.label").grid_info()["row"], column=1, padx=(4, 0), sticky="W")
            self.__getattribute__(f"planet.{attr}.label_after").grid(row=self.__getattribute__(f"planet.{attr}.label").grid_info()["row"], column=2, sticky="W", padx=(0, 4))
            self.__setattr__(f"planet.{attr}.validator", attr_attrs["validator"])
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        for attr, attr_attrs in attr_prop.items():
            self.planet.__setattr__(attr, self.__getattribute__(f"planet.{attr}.field").get())
            self.planet.__getattribute__(f"{attr}_var").set(self.__getattribute__(f"planet.{attr}.field").get())
        # for planet_button in self.master.children.values():
        #     if isinstance(planet_button, ctk.CTkButton) and planet_button.cget("text") == self.title():
        #         planet_button.configure(text=self.__getattribute__("planet.name.field").get())
        
        self.destroy()
            


if __name__ == '__main__':
    root = ctk.CTk()
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
    root.title("Planet Display Test")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    container = ctk.CTkScrollableFrame(root, width=350, height=400)
    container.grid(sticky="NESW")
    for planet in planets:
        button = ctk.CTkButton(container, textvariable=planet.name_var, command=partial(lambda p: PlanetWindow(container, p, "33 sextantis"), planet))
        button.grid()
        # planet_window =
    root.mainloop()
