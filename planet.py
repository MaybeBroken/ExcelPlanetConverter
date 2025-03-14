import openpyxl

attr_to_prop = {
    "name": "name",
    "government": "government",
    "description": "description",
    "type": "type",
    "surface": "surface",
    "color": "color",
    "orbital_distance": "orbitaldistance",
    "eccentricity": "eccentricity",
    "argument_of_periapsis": "argumentofperiapsis",
    "orbital_position": "orbitalposition",
    "orbital_period": "orbitalperiod",
    "rotational_period": "rotationalperiod",
    "mass": "mass",
    "radius": "radius",
    "density": "density",
    "inclination": "inclination",
    "temperature": "temperature",
}
prop_locations = {
    "name": "BK",
    "government": "BZ",
    "description": "BZ",
    "type": "BL",
    "surface": "BM",
    "color": "",  # needs coding
    "orbitaldistance": "T",
    "eccentricity": "Z",
    "argumentofperiapsis": "BN",
    "orbitalposition": "",  # needs coding
    "orbitalperiod": "V",
    "rotationalperiod": "U",
    "mass": "L",
    "radius": "P",
    "density": "S",
    "inclination": "BO",
    "temperature": "AI",
}

suffixes = "abcdefghijklmnopqrstuvwxyz"


class Planet:
    def __init__(self, suffix, **kwargs):
        self.row_index = suffixes.index(suffix) + 5  # Where the row of info in the spreadsheet is
        for attr, val, in kwargs.items():
            self.__setattr__(attr, val)
    
    def fill_attr(self, spreadsheet: openpyxl.Workbook):
        for prop, location in prop_locations.items():
            try:
                self.__setattr__(prop, spreadsheet["System Builder"][location + str(self.row_index)].value)
            except AttributeError:
                pass


if __name__ == '__main__':
    planets = [
        Planet("b"),
        Planet("c"),
        Planet("d"),
        Planet("e"),
        Planet("f"),
        Planet("g"),
        Planet("h"),
    ]
    for planet in planets:
        planet.fill_attr(openpyxl.open("worldbuilding spreadsheet 33 sextantis.xlsx", data_only=True))
        print("\n".join(f"{key}: {val}" for key, val in planet.__dict__.items()))
