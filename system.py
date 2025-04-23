import colour
import customtkinter as ctk
import lxml.etree
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from planet import Planet

props = [
    "name",
    "faction",
    "class",
    "radius",
    "luminosity",
    "position",
    "color",
    "ambient",
    "pedia",
]

color_vals = []


def linear_gradient(start_color, end_color, steps):
    """
    Generates a linear color gradient between two colors.

    Parameters:
        start_color (str): Hexadecimal representation of the starting color (e.g., "#FFFFFF" for white).
        end_color (str): Hexadecimal representation of the ending color.
        steps (int): Number of color steps in the gradient.

    Returns:
        list: A list of hexadecimal color values representing the gradient.
    """
    
    start_rgb = mcolors.hex2color(start_color)
    end_rgb = mcolors.hex2color(end_color)
    
    gradient_rgb = [
        (
            start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / (steps - 1),
            start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / (steps - 1),
            start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / (steps - 1)
        )
        for i in range(steps)
    ]
    
    gradient_hex = [mcolors.rgb2hex(rgb) for rgb in gradient_rgb]
    return gradient_hex


def create_color_range():
    minimum = "#9BBCFF"
    middle = "#FEF9FF"
    maximum = "#FF3800"
    color_vals.extend(linear_gradient(minimum, minimum, 72 + 1))
    color_vals.extend(linear_gradient(minimum, middle, 439 - 72))
    color_vals.extend(linear_gradient(middle, maximum, 2898 - 439))
    # print(*[f"{v}" for i, v in enumerate(color_vals)], sep="\n")


create_color_range()

prop_locations = {
    "name": "B5",
    "faction": "",
    "class": "",
    "radius": ("F12", "E12"),
    "luminosity": ("F11", "E11"),
    "position": "",
    # "color": "E14",
    # "ambient": "",
    "pedia": "",
}

default_vals = {
    "name": "Unnamed Star System",
    "faction": "",
    "class": "",
    "radius": 1.0,
    "luminosity": 1.0,
    "position": "",
    "color": "255 255 255 255",
    "ambient": "255 255 255 255",
    "pedia": "",
}

PLANET_MASS_COL = "L"
PLANET_MASS_ROW = 6


class System:
    """
    @DynamicAttrs
    """
    
    def __init__(self, **kwargs):
        self.planets = []
        for attr, val, in kwargs.items():
            self.__setattr__(attr, val)
        for attr in props:
            try:
                self.__getattribute__(attr)
            except AttributeError:
                try:
                    self.__setattr__(attr, default_vals[attr])
                except KeyError:
                    self.__setattr__(attr, "")
            
            try:
                self.__setattr__(f"{attr}_var", ctk.StringVar(value=self.__getattribute__(attr)))
            except (RuntimeError, AttributeError):
                pass
        self.system_info_var = ctk.StringVar(value=f"{self.name}: {len(self.planets)} planets")
        self.name_var.trace_add("write", self.update_info)
        
    def update_info(self, *_):
        self.system_info_var.set(f"{self.name_var.get()}: {len(self.planets)} planets")
    
    def fill_attr(self, spreadsheet) -> None:
        try:
            self.__setattr__("color", " ".join((*[str(int(_ * 256)) for _ in colour.hex2rgb(color_vals[int(spreadsheet["System Builder"]["E14"].value)])], "255")))
            self.__setattr__("color_var", ctk.StringVar(value=" ".join((*[str(int(_ * 256)) for _ in colour.hex2rgb(color_vals[int(spreadsheet["System Builder"]["E14"].value)])], "255"))))
            self.__setattr__("ambient", " ".join((*[str(int(_ * 256)) for _ in colour.hex2rgb(color_vals[int(spreadsheet["System Builder"]["E14"].value)])], "255")))
            self.__setattr__("ambient_var", ctk.StringVar(value=" ".join((*[str(int(_ * 256)) for _ in colour.hex2rgb(color_vals[int(spreadsheet["System Builder"]["E14"].value)])], "255"))))
        except KeyError:
            pass
        except ValueError:
            pass
        for prop, location in prop_locations.items():
            try:
                if isinstance(location, tuple):
                    value = spreadsheet["System Builder"][location[0]].value
                    i = 1
                    while not value:
                        value = spreadsheet["System Builder"][location[i]].value
                        i += 1
                else:
                    value = spreadsheet["System Builder"][location].value
                if isinstance(value, float):
                    self.__setattr__(prop, (round(float(value), 2)))
                    try:
                        self.__getattribute__(f"{prop}_var").set((round(float(value), 2)))
                    except (RuntimeError, AttributeError):
                        pass
                else:
                    self.__setattr__(prop, value if value not in [None, "#NUM!", "#DIV/0!"] else default_vals[prop])
                    try:
                        self.__getattribute__(f"{prop}_var").set(value if value not in [None, "#NUM!", "#DIV/0!"] else default_vals[prop])
                    except (RuntimeError, AttributeError):
                        pass
            except IndexError:
                self.__setattr__(prop, default_vals[prop])
        col = PLANET_MASS_COL
        row = PLANET_MASS_ROW
        while spreadsheet["System Builder"][f"{col}{row}"].value:
            planet = Planet(spreadsheet["System Builder"][f"K{row}"].value)
            self.planets.append(planet)
            planet.fill_attr(spreadsheet)
            row += 1
        self.update_info()
    
    def get_xml_repr(self) -> str:
        """
        <location type="StarSystem" name="Sol" faction="Alliance" pedia="" class="G" radius="1" luminosity="1" position="0 0 0" color="255 255 130 255" ambient="255 255 255 255">
        :return:
        """
        s = '<location type="StarSystem" '
        for prop in props:
            try:
                s += f'{prop}="{self.__getattribute__(prop)}" '
            except AttributeError:
                pass
        s += '>\n'
        for planet in self.planets:
            s += planet.get_xml_repr()
            s += '\n'
        s += '</location>'
        return lxml.etree.tostring(lxml.etree.fromstring(s.replace("\n", "")), pretty_print=True, encoding=str)


if __name__ == '__main__':
    create_color_range()
    system = System()
    system.fill_attr(openpyxl.open("worldbuilding spreadsheet 33 sextantis.xlsx", data_only=True))
    print(vars(system))
