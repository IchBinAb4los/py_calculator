import time
import random
import threading
from tkinter import *
from tkinter.font import *
from functools import partial

SMALL_DEFAULT = ("Helvetica", "15")
DEFAULT_BOLD = ("Helvetica", "20", "bold")
BUTTON_BOLD = ("Helvetica", "17", "bold")

buttonPos = {
    "%":[1, 1], "CE":[1, 2], "C":[1, 3], u"\u2190":[1, 4],
    "1/x":[2, 1], "x"+u"\u00b2":[2, 2], "√x":[2, 3], u"\u00f7":[2, 4],
    7:[3, 1], 8:[3, 2], 9:[3, 3], "x":[3, 4],
    4:[4, 1], 5:[4, 2], 6:[4, 3], "-":[4, 4],
    1:[5, 1], 2:[5, 2], 3:[5, 3], "+":[5, 4],
    u"\u00b1":[6, 1], 0:[6, 2], ".":[6, 3], "=":[6, 4]
}

def isInt(_):
    try:
        int(_)
        return True
    except ValueError:
        return False

class Calculator:
    def __init__(self):
        self.root = Tk()
        self.root.title("Calculadora")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        self.root.iconbitmap("./img/icon.ico")
        self.fDisplay = self.fDisplay_create()
        self.fButtons = self.fButtons_create()
        self.fDisplay_total_label, self.fDisplay_actual_label = self.fDisplay_labels_create(self.fDisplay)
        self.buttons = self.fButtons_buttons_create(self.fButtons)
        self.fButtons.rowconfigure(0, weight=1)
        self.colorLoop()
        self.firstClick = True

        self.actualResult = 0

        for i in range(1, 5):
            self.fButtons.rowconfigure(i, weight=1)
            self.fButtons.columnconfigure(i, weight=1)

    def do(self, _str):
        if isInt(_str):
            if self.firstClick:
                self.firstClick = False
            n = int(_str)
            if not self.fDisplay_actual_label.cget("text") == "0":
                self.fDisplay_actual_label.config(text=self.fDisplay_actual_label.cget("text")+str(n))
            else:
                self.fDisplay_actual_label.config(text=str(n))
        else:
            if not self.firstClick:
                self.firstClick = True
                op = _str
                if op == "+":
                    n = int(self.fDisplay_actual_label.cget("text"))
                    self.actualResult += n
                    self.fDisplay_total_label.config(text=self.actualResult)
                    self.fDisplay_actual_label.config(text="0")

    def changeColor(self, i, colors):
        try:
            i["bg"] = colors[random.randint(0, len(colors) - 1)]
            time.sleep(random.uniform(0.6, 1.7))
            self.changeColor(i, colors)
        except RuntimeError:
            pass

    def colorLoop(self):
        colors = ["#ffffff", "#e3e3e3", "#d9d8d9"]
        for i in self.buttons:
            threading.Thread(target=self.changeColor, args=(i, colors)).start()

    def fButtons_buttons_create(self, frame):
        bs = []
        for k,v in buttonPos.items():
            b = Button(frame, command=partial(self.do, str(k)), text=str(k), font=BUTTON_BOLD, borderwidth=4)
            b.grid(row=v[0], column=v[1], sticky=NSEW)
            bs.append(b)
        return bs

    def fDisplay_labels_create(self, frame):
        total_label = Label(frame, text="", anchor="e", bg="#050505", fg="#ffffff", padx=10, pady=5,
                            font=SMALL_DEFAULT)
        total_label.pack(expand=True, fill="both")

        actual_label = Label(frame, text="0", anchor="e", bg="#050505", fg="#ffffff", padx=10,
                             pady=5, font=DEFAULT_BOLD)
        actual_label.pack(expand=True, fill="both")
        return total_label, actual_label

    def fDisplay_create(self):
        frame = Frame(self.root, bg="#ebebeb", height="90", borderwidth=3, relief="ridge")
        frame.pack(fill="x")
        return frame

    def fButtons_create(self):
        frame = Frame(self.root, bg="#ebebeb")
        frame.pack(fill="both", expand="True")
        return frame

    def loop(self):
        self.root.mainloop()

if __name__ == "__main__":
    c = Calculator()
    c.loop()