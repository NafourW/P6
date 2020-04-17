import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.text_box = tk.Text(self)
        self.text_box.pack()

        self.quit = tk.Button(self, text="Quit", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def text_insert(self, line):
        self.text_box.insert(tk.INSERT, line + "\n")
