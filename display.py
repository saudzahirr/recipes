#!/usr/bin/env python
# coding: utf-8

from tkinter import *
from tkinter import filedialog



def display():
    def open_file():
        tf = filedialog.askopenfilename(
            initialdir="", title="Open Recipe", 
            filetypes=(("Text Files", "*.txt"),)
        )
        path.insert(END, tf)
        tf = open(tf)
        data = tf.read()
        text_area.insert(END, data)
        tf.close()
        
    window = Tk()
    window.title("Recipes")
    window.geometry("1080x980")
    window['bg'] = '#000000'
        
    text_area = Text(window, width = window.winfo_screenwidth(), height = 35)
    text_area.pack(pady = 20)
        
    path = Entry(window)
    path.pack(side = LEFT, expand = True, fill = X, padx = 20)

    Button(window, text = "Open Recipe", command = open_file).pack(side = RIGHT, expand = True, fill = X, padx = 20)
        
    window.mainloop()