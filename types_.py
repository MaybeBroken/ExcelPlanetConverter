from typing import Callable

import customtkinter as ctk


class Attribute:
    def __init__(self, frame: ctk.CTkFrame, value, ctk_vars: ctk.Variable, var_get: Callable):
        self.frame = frame
        self.value = value
        self.vars = ctk_vars
    
    @classmethod
    def name(cls, master, value):
        frame = ctk.CTkFrame(master)
        
        return cls(frame, value)
    
    @classmethod
    def government(cls, master, value):
        pass
    
    @classmethod
    def description(cls, master, value):
        pass
    
    @classmethod
    def type(cls, master, value):
        pass
    
    @classmethod
    def surface(cls, master, value):
        pass
    
    @classmethod
    def color(cls, master, value):
        pass
    
    @classmethod
    def orbitaldistance(cls, master, value):
        pass
    
    @classmethod
    def eccentricity(cls, master, value):
        pass
    
    @classmethod
    def argumentofperiapsis(cls, master, value):
        pass
    
    @classmethod
    def orbitalposition(cls, master, value):
        pass
    
    @classmethod
    def orbitalperiod(cls, master, value):
        pass
    
    @classmethod
    def rotationalperiod(cls, master, value):
        pass
    
    @classmethod
    def mass(cls, master, value):
        pass
    
    @classmethod
    def radius(cls, master, value):
        pass
    
    @classmethod
    def density(cls, master, value):
        pass
    
    @classmethod
    def inclination(cls, master, value):
        pass
    
    @classmethod
    def temperature(cls, master, value):
        pass
    
    @classmethod
    def new(cls, master, value):
        pass