from tkinter import *
from tkinter import ttk

class Scroll:
    def __init__(self, frame, canvascolor="#D1D1D1", scrollSide=RIGHT):
        self.frame = frame
        self.canvascolor = canvascolor
        self.scrollSide = scrollSide

        self.canvas = Canvas(self.frame)
        self.canvasFrame = Frame(self.canvas)
        self.yscroll = ttk.Scrollbar(
            self.frame, orient="vertical", command=self.canvas.yview
        )

        self.yscroll.pack(side=self.scrollSide, fill="y")
        self.canvas.pack(side=self.scrollSide, fill="both", expand="yes")
        self.canvas.config(bg=self.canvascolor)
        self.canvasFrame.config(bg=self.canvascolor)
        self.canvas.configure(yscrollcommand=self.yscroll.set)
        self.canvas.create_window((0, 0), window=self.canvasFrame, anchor="nw")

    def removeScroll(self):
        self.yscroll.pack_forget()

    def bindScrollAction(self):
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

    def returnFrame(self):
        return self.canvasFrame