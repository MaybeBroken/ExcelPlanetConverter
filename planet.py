import random

import openpyxl
from lxml import etree

import customtkinter as ctk

props = [
    "name",
    "government",
    "description",
    "type",
    "surface",
    "color",
    "orbitaldistance",
    "eccentricity",
    "argumentofperiapsis",
    "orbitalposition",
    "orbitalperiod",
    "rotationalperiod",
    "mass",
    "radius",
    "density",
    "inclination",
    "temperature",
]
prop_locations = {
    "name": "BK",
    "government": "BZ",
    "description": "BZ",
    "type": "BL",
    "surface": "BM",
    # "color": "",  # location coded elsewhere
    "orbitaldistance": "T",
    "eccentricity": "Z",
    "argumentofperiapsis": ("BO", "BN"),
    "orbitalposition": ("BS", "BR"),
    "orbitalperiod": "V",
    "rotationalperiod": "U",
    "mass": "L",
    "radius": ("Q", "P"),
    "density": "S",
    "inclination": ("BQ", "BP"),
    "temperature": "AI",
}
hab_to_color = {
    "Roche": "#808080FF",
    "Melting": "#FF0000FF",
    "Hot": "#FF6600FF",
    "Low-hum": "#FFC000FF",
    "Slow-rot": "#FFFF00FF",
    "Opt in": "#92D050FF",
    "Ideal": "#00B050FF",
    "Opt out": "#00FFCCFF",
    "Dry/H2": "#00B0F0FF",
    "High-H2": "#2F75B5FF",
    "Frozen": "#9BC2E6FF",
}

default_vals = {
    "name": "Unnamed Planet",
    "government": "",
    "description": "",
    "type": "Rock",
    "surface": "",
    "color": "",
    "orbitaldistance": "",
    "eccentricity": "",
    "argumentofperiapsis": "",
    "orbitalposition": "",
    "orbitalperiod": "",
    "rotationalperiod": "",
    "mass": "",
    "radius": "",
    "density": "",
    "inclination": "",
    "temperature": "",
}

suffixes = "bcdefghijklmnopqrstuvwxyz"


def hex_to_rgb(hex_color) -> tuple[str, ...]:
    hex_color = hex_color.lstrip("#")
    return tuple(str(int(hex_color[i:i + 2], 16)) for i in (0, 2, 4, 6))


class Planet:
    """
    @DynamicAttrs
    """
    
    def __init__(self, suffix, **kwargs):
        self.moons = []
        if suffix not in suffixes:
            raise ValueError("Invalid suffix: suffix must be within b-z")
        self.row_index = suffixes.index(suffix) + 6  # Where the row of info in the spreadsheet is
        for attr, val, in kwargs.items():
            self.__setattr__(attr, val)
        for attr in props:
            try:
                self.__getattribute__(attr)
            except AttributeError:
                self.__setattr__(attr, default_vals[attr])
            try:
                self.__setattr__(f"{attr}_var", ctk.StringVar(value=self.__getattribute__(attr)))
            except (RuntimeError, AttributeError):
                pass
    
    def fill_attr(self, spreadsheet) -> None:
        try:
            self.__setattr__("color", " ".join(list(hex_to_rgb(hab_to_color[spreadsheet["System Builder"]["AJ" + str(self.row_index)].value]))))
            self.__setattr__("color_var", ctk.StringVar(value=" ".join(list(hex_to_rgb(hab_to_color[spreadsheet["System Builder"]["AJ" + str(self.row_index)].value])))))
        except KeyError:
            pass
        except ValueError:
            pass
        for prop, location in prop_locations.items():
            try:
                if isinstance(location, tuple):
                    value = spreadsheet["System Builder"][location[0] + str(self.row_index)].value
                    i = 1
                    while not value:
                        value = spreadsheet["System Builder"][location[i] + str(self.row_index)].value
                        i += 1
                else:
                    value = spreadsheet["System Builder"][location + str(self.row_index)].value
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
            except AttributeError as e:
                print(e)
                self.__setattr__(prop, "")
    
    def get_xml_repr(self) -> str:
        s = "<planet model='Planet' "
        for prop in props:
            try:
                value = self.__getattribute__(prop)
            except AttributeError:
                continue
            if value is not None and value not in ("#NUM!", "#DIV/0!"):
                if str(value).replace(".", "").isnumeric():
                    if int(float(value)) != float(value):
                        value = round(float(value), 2)
                s += f"{prop}={str(value).__repr__()} "
        s += ">\n<description>"
        if (description := self.__getattribute__("description")) is not None:
            s += description
        s += "</description>\n"
        s += "<atmosphere />\n"  # to be implemented
        s += "</planet>"
        return s


if __name__ == '__main__':
    planets = [
        Planet("b"),
        Planet("c"),
        Planet("d"),
        Planet("e"),
        Planet("f"),
        Planet("g"),
        Planet("h"),
        Planet("i"),
        Planet("j"),
    ]
    print("building")
    spreadsheet = openpyxl.open("worldbuilding spreadsheet 33 sextantis.xlsx", data_only=True, rich_text=True)
    for planet in planets:
        planet.fill_attr(spreadsheet)
    print("done")
    for planet in planets:
        # print(planet.get_xml_repr())
        print(etree.tostring(etree.fromstring(planet.get_xml_repr()), pretty_print=True, encoding=str))
