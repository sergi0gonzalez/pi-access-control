import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()
    

class GUImain(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "IEETA Security UI")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        label = tk.Label(self, text="Welcome to IEETA, please choose a method of Authentication", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.icon = ImageTk.PhotoImage(Image.open("ieta.jpeg"))
        self.icon_size = tk.Label(self)
        self.icon_size.image = self.icon
        panel = tk.Label(self, image = self.icon)
        panel.pack()

        button1 = ttk.Button(self, text="NFC Authentication", command = lambda: popupmsg("Not supported just yet!"))
        button1.pack()

        button2 = ttk.Button(self, text="SmartCard Authentication", command = lambda: popupmsg("Not supported just yet!"))
        button2.pack()

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        


app = GUImain()
app.mainloop()