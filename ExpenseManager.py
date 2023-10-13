from tkinter import *
from customtkinter import CTk, CTkButton, CTkFrame, CTkCanvas, CTkLabel, CTkFont, CTkCheckBox, CTkScrollbar, CTkComboBox, CTkTextbox, CTkScrollableFrame
from Account import *
class ExpenseManager:
    def __init__(self):
        self.window = CTk()
        self.window.title("Bulldog Auto & Turf")
        self.window.resizable(True, True)
        self.window.attributes("-fullscreen", True)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        background = PhotoImage(file="Pictures/background.png")
        background = background.zoom(2,2)
        self.bg = Label(self.window, image=background)
        self.bg.grid(column=0, row=0, columnspan=4, rowspan=4)


        self.window.mainloop()