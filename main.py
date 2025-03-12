import customtkinter as ctk


class MainWindow(ctk.CTk):
    def __init__(self, file=None):
        super().__init__()
        self.title = "Excel Planet Converter"


if __name__ == '__main__':
    MainWindow()
