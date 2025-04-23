from functools import partial

import customtkinter as ctk
import tkinter as tk
import colour

import openpyxl
from lxml import etree

from planet import Planet
from types_ import Attribute

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

attr_to_widget = {
    "name": Attribute.name,
    "government": Attribute.government,
    "type": Attribute.type,
    "description": Attribute.description,
    "surface": Attribute.surface,
    "specular": Attribute.specular,
    "normal": Attribute.normal,
    "atmosphere_texture": Attribute.atmosphere_texture,
    "color": Attribute.color,
    "orbitaldistance": Attribute.orbitaldistance,
    "eccentricity": Attribute.eccentricity,
    "argumentofperiapsis": Attribute.argumentofperiapsis,
    "orbitalposition": Attribute.orbitalposition,
    "orbitalperiod": Attribute.orbitalperiod,
    "rotationalperiod": Attribute.rotationalperiod,
    "mass": Attribute.mass,
    "radius": Attribute.radius,
    "density": Attribute.density,
    "inclination": Attribute.inclination,
    "temperature": Attribute.temperature,
    "surface_minerals": Attribute.surface_minerals,
    "atmosphere_materials": Attribute.atmosphere_materials,
}


class PlanetWindow(ctk.CTkToplevel):
    systems = {}
    
    def __init__(self, master, planet_obj: Planet, system):
        super().__init__(master)
        self.geometry("500x700")
        self.attributes("-topmost", True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.expanded = False
        self.planet = planet_obj
        self.title(self.planet.name)
        self.system = system.get()
        self.sframe = ctk.CTkScrollableFrame(self)
        self.sframe.grid(row=0, column=0, sticky="NESW")
        if self.system in PlanetWindow.systems.keys():
            PlanetWindow.systems[self.system].append(self)
        else:
            PlanetWindow.systems[self.system] = [self]
        
        for attr, widget in attr_to_widget.items():
            try:
                __value = planet_obj.__getattribute__(attr)
            except AttributeError:
                __value = ""
            self.__setattr__(f"planet.{attr}", widget(self.sframe, __value))
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        for attr, widget in attr_to_widget.items():
            try:
                self.planet.__setattr__(attr, self.__getattribute__(f"planet.{attr}").get())
                self.planet.__getattribute__(f"{attr}_var").set(self.__getattribute__(f"planet.{attr}").get())
            except AttributeError:
                pass
        for system_frame in self.master.system_frames:
            for button in system_frame.children.values():
                if isinstance(button, ctk.CTkButton):
                    try:
                        button.__getattribute__("color_callback")()
                        button.update_idletasks()
                    except AttributeError:
                        pass
        
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
        Planet("i"),
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
        button = ctk.CTkButton(container,
                               fg_color=colour.rgb2hex((int(c) / 256 for c in planet.color.split(" ")[0:3])),
                               hover_color=colour.rgb2hex((int(c) / (256 + 128) for c in planet.color.split(" ")[0:3])),
                               text_color=colour.rgb2hex((int(c) / 512 for c in planet.color.split(" ")[0:3])),
                               textvariable=planet.name_var,
                               command=partial(lambda p: PlanetWindow(container, p, "33 sextantis"), planet))
        button.grid()
        # planet_window =
    root.mainloop()
