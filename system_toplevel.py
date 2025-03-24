import customtkinter as ctk
import tkinter as tk


class SystemWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    SystemWindow().mainloop()
