from functools import partial

import colour
import customtkinter as ctk
import tkinter as tk

import openpyxl

from planet_toplevel import PlanetWindow
from system import System
from types_ import Attribute

attr_to_display = {
    "name": "Name",
    "faction": "Faction",
    "class": "Class",
    "radius": "Radius",
    "luminosity": "Luminosity",
    "position": "Position",
    "color": "Color",
    "ambient": "Ambient",
    "pedia": "Pedia",
}

attr_to_widget = {
    "name": Attribute.name,
    "faction": Attribute.faction,
    "class": Attribute.class_,
    "radius": Attribute.radius,
    "luminosity": Attribute.luminosity,
    "position": Attribute.position,
    "color": Attribute.color,
    "ambient": Attribute.ambient,
    "pedia": Attribute.pedia,
}


class SystemWindow(ctk.CTkToplevel):
    systems = {}
    
    def __init__(self, master, system_obj: System):
        super().__init__(master)
        self.attributes("-topmost", True)
        self.geometry(f"500x700")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.system = system_obj
        self.title(self.system.name)
        self.sframe = ctk.CTkScrollableFrame(self)
        self.sframe.grid(row=0, column=0, sticky="NESW")
        
        for attr, widget in attr_to_widget.items():
            try:
                __value = system_obj.__getattribute__(attr)
            except AttributeError:
                __value = ""
            self.__setattr__(f"system.{attr}", widget(self.sframe, __value))
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        for attr, widget in attr_to_widget.items():
            self.system.__setattr__(attr, self.__getattribute__(f"system.{attr}").get())
            self.system.__getattribute__(f"{attr}_var").set(self.__getattribute__(f"system.{attr}").get())
        for system_frame in self.master.system_frames:
            for button in system_frame.children.values():
                if isinstance(button, ctk.CTkButton):
                    try:
                        button.__getattribute__("color_callback")()
                        button.update_idletasks()
                    except AttributeError:
                        pass
        
        self.destroy()


# def collapse():
#     system_container.grid_propagate(False)
#     system_container.configure(True, height=28)
#
# def expand():
#     system_container.grid_propagate(True)
#
# def toggle():
#     global expanded
#     if expanded:
#         collapse()
#         expanded = not expanded
#     else:
#         expand()
#         expanded = not expanded
            
    


if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    spreadsheet = openpyxl.open("worldbuilding spreadsheet 33 sextantis.xlsx", data_only=True)
    system = System()
    system.fill_attr(spreadsheet)
    root.title("System Display Test")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    container = ctk.CTkScrollableFrame(root, width=350, height=400, fg_color="transparent")
    container.grid(sticky="NESW")
    container.columnconfigure(0, weight=1)
    expanded = True
    system_container = ctk.CTkFrame(container)
    # system_container.bind("<Button-1>", lambda _: toggle())
    system_container.grid(sticky="EW")
    system_container.columnconfigure(0, weight=1)
    button = ctk.CTkButton(system_container,
                           fg_color=colour.rgb2hex((int(c) / 256 for c in system.color.split(" ")[0:3])),
                           hover_color=colour.rgb2hex((int(c) / (256 + 128) for c in system.color.split(" ")[0:3])),
                           text_color=colour.rgb2hex((int(c) / 512 for c in system.color.split(" ")[0:3])),
                           textvariable=system.name_var,
                           command=partial(lambda p: SystemWindow(container, p), system)
                           )
    button.grid(sticky="W")
    for planet in system.planets:
        button = ctk.CTkButton(system_container,
                               fg_color=colour.rgb2hex((int(c) / 256 for c in planet.color.split(" ")[0:3])),
                               hover_color=colour.rgb2hex((int(c) / (256 + 128) for c in planet.color.split(" ")[0:3])),
                               text_color=colour.rgb2hex((int(c) / 512 for c in planet.color.split(" ")[0:3])),
                               textvariable=planet.name_var,
                               command=partial(lambda p: PlanetWindow(container, p, "33 sextantis"), planet))
        button.grid(sticky="W", padx=(16, 0))
        # planet_window =
    root.mainloop()
