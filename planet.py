name_to_location = {
    
}


class Planet:
    def __init__(self, name=None, government=None, description=None, type_=None, surface=None, color=None,
                 orbital_distance=None, eccentricity=None, argument_of_periapsis=None, orbital_position=None,
                 orbital_period=None, rotational_period=None, mass=None, radius=None, density=None, inclination=None,
                 temperature=None):
        self.name = name
        self.government = government
        self.description = description
        self.type_ = type_
        self.surface = surface
        self.color = color
        self.orbital_distance = orbital_distance
        self.eccentricity = eccentricity
        self.argument_of_periapsis = argument_of_periapsis
        self.orbital_position = orbital_position
        self.orbital_period = orbital_period
        self.rotational_period = rotational_period
        self.mass = mass
        self.radius = radius
        self.density = density
        self.inclination = inclination
        self.temperature = temperature
