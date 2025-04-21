from functools import partial
from tkinter import filedialog

import colour
import customtkinter as ctk
import tkinter as tk

import openpyxl
from typing_extensions import override

from planet_toplevel import PlanetWindow
from system import System
from system_toplevel import SystemWindow
import lxml.etree


def set_color(widget, color):
    widget.configure(fg_color=colour.rgb2hex((int(c) / 256 for c in color.split(" ")[0:3])),
                     hover_color=colour.rgb2hex((int(c) / (256 + 128) for c in color.split(" ")[0:3])),
                     text_color=colour.rgb2hex((int(c) / 512 for c in color.split(" ")[0:3])),
                     )
    
class ExpandableFrame(ctk.CTkFrame):
    def __init__(self, master, obj, **kwargs):
        super().__init__(master, **kwargs)
        self.obj = obj
        self.expanded = False
        self.button = None
    
    def collapse(self):
        self.grid_propagate(False)
        self.configure(True, height=28)
        self.button.grid(sticky="W")
        self.expanded = False
    
    def expand(self):
        self.grid_propagate(True)
        self.button.grid_remove()
        self.expanded = True
    
    def toggle(self):
        pass


class SystemFrame(ExpandableFrame):
    def __init__(self, master, obj):
        super().__init__(master, obj, border_width=2)
        self.system = obj
        self.bind("<Button-1>", lambda _: self.toggle())
        self.button = ctk.CTkButton(self,
                                    width=0,
                                    textvariable=obj.system_info_var,
                                    fg_color=colour.rgb2hex((int(c) / 256 for c in obj.color.split(" ")[0:3])),
                                    hover_color=colour.rgb2hex((int(c) / (256 + 128) for c in obj.color.split(" ")[0:3])),
                                    text_color=colour.rgb2hex((int(c) / 512 for c in obj.color.split(" ")[0:3])),
                                    command=self.expand)
        if len(self.obj.planets):
            self.expanded = False
            self.collapse()
        else:
            self.expanded = True
            self.expand()
    
    @override
    def toggle(self):
        if len(self.obj.planets) == 0:
            return
        if self.expanded:
            self.collapse()
        else:
            self.expand()


class PlanetFrame(ExpandableFrame):
    def __init__(self, master, obj):
        super().__init__(master, obj, border_width=2)
        self.system = obj
        self.bind("<Button-1>", lambda _: self.toggle())
        self.button = ctk.CTkButton(self,
                                    width=0,
                                    textvariable=obj.system_info_var,
                                    fg_color=colour.rgb2hex((int(c) / 256 for c in obj.color.split(" ")[0:3])),
                                    hover_color=colour.rgb2hex((int(c) / (256 + 128) for c in obj.color.split(" ")[0:3])),
                                    text_color=colour.rgb2hex((int(c) / 512 for c in obj.color.split(" ")[0:3])),
                                    command=self.expand)
        if len(self.obj.moons):
            self.expanded = False
            self.collapse()
        else:
            self.expanded = True
            self.expand()
    
    @override
    def toggle(self):
        if len(self.obj.moons) == 0:
            return
        if self.expanded:
            self.collapse()
        else:
            self.expand()


class MainWindow(ctk.CTk):
    def __init__(self, *spreadsheet_files):
        super().__init__()
        self.title("System Display Test")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(10, weight=0)
        
        self.container = ctk.CTkScrollableFrame(self, width=350, height=400, fg_color="transparent")
        self.container.grid(sticky="NESW")
        self.container.columnconfigure(0, weight=1)
        
        self.system_frames = []
        for spread_file in spreadsheet_files:
            spreadsheet = openpyxl.open(spread_file, data_only=True)
            
            system = System()
            system.fill_attr(spreadsheet)
            
            system_frame = SystemFrame(self.container, system)  # NOQA
            system_frame.grid(sticky="EW", pady=2)
            system_frame.columnconfigure(0, weight=1)
            
            self.system_frames.append(system_frame)
            
            button = ctk.CTkButton(system_frame,
                                   fg_color=colour.rgb2hex((int(c) / 256 for c in system.color.split(" ")[0:3])),
                                   hover_color=colour.rgb2hex((int(c) / (256 + 128) for c in system.color.split(" ")[0:3])),
                                   text_color=colour.rgb2hex((int(c) / 512 for c in system.color.split(" ")[0:3])),
                                   textvariable=system.name_var,
                                   width=0,
                                   command=partial(lambda p: SystemWindow(self, p), system)
                                   )
            button.grid(row=1, sticky="W")
            for planet in system.planets:
                button = ctk.CTkButton(system_frame,
                                       fg_color=colour.rgb2hex((int(c) / 256 for c in planet.color.split(" ")[0:3])),
                                       hover_color=colour.rgb2hex((int(c) / (256 + 128) for c in planet.color.split(" ")[0:3])),
                                       text_color=colour.rgb2hex((int(c) / 512 for c in planet.color.split(" ")[0:3])),
                                       textvariable=planet.name_var,
                                       width=0,
                                       command=partial(lambda p: PlanetWindow(self, p, system.name_var), planet))
                button.__setattr__("color_callback", partial(lambda b=button, p=planet: set_color(b, p.color_var.get())))
                # button.__setattr__("planet_color_callback", partial(lambda b=button, p=planet: print(p.color_var.get())))
                button.grid(sticky="W", padx=(16, 0))
                
        self.export_button = ctk.CTkButton(self, text="Export", command=lambda : print(*[sysframe.system.get_xml_repr() for sysframe in self.system_frames], sep="\n"))
        self.export_button.grid(row=10, column=0, sticky="SEW")


if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("./blue.json")
    spreads = filedialog.askopenfilenames(defaultextension=".xlsx", filetypes=[("Excel Sheet", ".xlsx")])
    if not spreads:
        exit(-1)
    main_window = MainWindow(*spreads)
    main_window.mainloop()
