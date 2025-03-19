import random

import openpyxl
from lxml import etree

props = [
    "name",
    "government",
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
    "argumentofperiapsis": "BN",
    #     "orbitalposition": "",  # location coded elsewhere
    "orbitalperiod": "V",
    "rotationalperiod": "U",
    "mass": "L",
    "radius": "P",
    "density": "S",
    "inclination": "BO",
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

suffixes = "bcdefghijklmnopqrstuvwxyz"


def hex_to_rgb(hex_color) -> tuple[str, ...]:
    hex_color = hex_color.lstrip("#")
    return tuple(str(int(hex_color[i:i + 2], 16)) for i in (0, 2, 4, 6))


class Moon:
    def __init__(self, suffix, **kwargs):
        self.row_index = suffixes.index(suffix) + 6  # Where the row of info in the spreadsheet is
        for attr, val, in kwargs.items():
            self.__setattr__(attr, val)
    
    def fill_attr(self, spreadsheet) -> None:
        try:
            self.__setattr__("color", " ".join(list(hex_to_rgb(hab_to_color[spreadsheet["System Builder"]["AJ" + str(self.row_index)].value]))))
        except KeyError:
            pass
        self.__setattr__("orbitalposition", random.randint(0, 3590) / 10)
        for prop, location in prop_locations.items():
            try:
                value = spreadsheet["System Builder"][location + str(self.row_index)].value
                if isinstance(value, float):
                    self.__setattr__(prop, (round(float(value), 2)))
                else:
                    self.__setattr__(prop, value if value not in [None, "#NUM!", "#DIV/0!"] else "")
            except AttributeError as e:
                print(e)
                self.__setattr__(prop, "")
    
    def get_xml_repr(self) -> str:
        """
            <moon
                name= "Mercury"
                model= "Moon"
                type= "Rock"
                surface= "mercury.jpg"
                color= "255 160 0 255"
                orbitaldistance= "0.38"
                orbitalposition= "190"
                orbitalperiod= "0.24"
                rotationperiod= "58.666"
                mass= "455.8115"
                radius= "2439"
                density= "5.43"
                axistilt= "0"
            />
        """
        s = "<moon model='Moon' "
        for prop in props:
            try:
                value = self.__getattribute__(prop)
            except AttributeError:
                continue
            if value is not None and value not in ("#NUM!", "#DIV/0!"):
                if str(value).replace(".", "").isnumeric():
                    if int(value) != float(value):
                        value = round(float(value), 2)
                s += f"{prop}={str(value).__repr__()} "
        s += ">\n<description>"
        if (description := self.__getattribute__("description")) is not None:
            s += description
        s += "</description>\n"
        s += "<atmosphere />\n"  # to be implemented
        s += "</moon>\n"
        return s


if __name__ == '__main__':
    moons = [
        Moon("b"),
        Moon("c"),
        Moon("d"),
        Moon("e"),
        Moon("f"),
        Moon("g"),
        Moon("h"),
        Moon("i"),
        Moon("j"),
    ]
    print("building")
    spreadsheet = openpyxl.open("worldbuilding spreadsheet 33 sextantis.xlsx", data_only=True)
    for moon in moons:
        moon.fill_attr(spreadsheet)
    print("done")
    for moon in moons:
        # print(moon.get_xml_repr())
        print(etree.tostring(etree.fromstring(moon.get_xml_repr()), pretty_print=True, encoding=str))
