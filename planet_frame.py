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
        "field_kwargs": {},
    },
    "government": {
        "display_name": "Government",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {},
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
        "field_kwargs": {},
    },
    "color": {
        "display_name": "Color",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {},
    },
    "orbitaldistance": {
        "display_name": "Orbital Distance",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {},
    },
    "eccentricity": {
        "display_name": "Eccentricity",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {},
    },
    "argumentofperiapsis": {
        "display_name": "Argument of Periapsis",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {},
    },
    "orbitalposition": {
        "display_name": "Orbital Position",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {},
    },
    "orbitalperiod": {
        "display_name": "Orbital Period",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {},
    },
    "rotationalperiod": {
        "display_name": "Rotational Period",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {},
    },
    "mass": {
        "display_name": "Mass",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {},
    },
    "radius": {
        "display_name": "Radius",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {},
    },
    "density": {
        "display_name": "Density",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {},
    },
    "inclination": {
        "display_name": "Inclination",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {},
    },
    "temperature": {
        "display_name": "Temperature",
        "display_after": "",
        "validator": None,
        "editable": True,
        "field_type": ctk.CTkEntry,
        "field_kwargs": {},
    },
}


class PlanetFrame(ctk.CTkToplevel):
    systems = {}
    
    def __init__(self, master, planet_obj: Planet, system):
        super().__init__(master)
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.expanded = False
        self.planet = planet_obj
        self.title(self.planet.name)
        self.system = system
        if system in PlanetFrame.systems.keys():
            PlanetFrame.systems[system].append(self)
        else:
            PlanetFrame.systems[system] = [self]
        
        for attribute, attribute_attributes in attr_prop.items():
            try:
                __value = planet_obj.__getattribute__(attribute)
            except AttributeError:
                __value = ""
            self.__setattr__(f"planet.{attribute}", __value)
            self.__setattr__(f"planet.{attribute}.label", ctk.CTkLabel(self, text=f"{attribute_attributes['display_name']}:"))
            try:
                self.__setattr__(f"planet.{attribute}.label_after", ctk.CTkLabel(self, text=f"{attribute_attributes['display_after'] or ' '}"))
            except IndexError:
                self.__setattr__(f"planet.{attribute}.label_after", ctk.CTkLabel(self, text=f""))
            self.__setattr__(f"planet.{attribute}.field", (attribute_attributes["field_type"] or ctk.CTkEntry)(self, **attribute_attributes["field_kwargs"]))
            self.__getattribute__(f"planet.{attribute}.label").grid(sticky="E", padx=4, pady=1)
            field = self.__getattribute__(f"planet.{attribute}.field")
            if isinstance(field, ctk.CTkEntry):
                field.insert(0, str(__value))
            else:
                field.set(__value)
            field.grid(row=self.__getattribute__(f"planet.{attribute}.label").grid_info()["row"], column=1, padx=(4, 0), sticky="W")
            self.__getattribute__(f"planet.{attribute}.label_after").grid(row=self.__getattribute__(f"planet.{attribute}.label").grid_info()["row"], column=2, sticky="W", padx=(0, 4))
            self.__setattr__(f"planet.{attribute}.validator", attribute_attributes["validator"])


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
