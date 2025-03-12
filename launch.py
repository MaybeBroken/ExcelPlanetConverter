from tkinter import filedialog
import customtkinter as ctk
from main import MainWindow


class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title = "Launcher"
        self.open_button = ctk.CTkButton("Open xml file...",
                                         command=lambda: MainWindow(
                                             filedialog.askopenfilename(defaultextension="xml",
                                                                        filetypes=(("Galaxy Files", "*.xml"),))))
