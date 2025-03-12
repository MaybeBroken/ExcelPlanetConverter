from tkinter import filedialog
import customtkinter as ctk
from main import MainWindow


class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title = "Launcher"
        self.open_button = ctk.CTkButton(self,
                                         text="Open xml file...",
                                         command=self.launch)
        self.open_button.grid()

    def launch(self):
        MainWindow(filedialog.askopenfilename(filetypes=(("Galaxy Files", "*.xml"),)))


if __name__ == '__main__':
    Launcher().mainloop()
