#!/usr/bin/env python
# coding: utf-8

import tkinter as tk



def display(file_name):
    """
    This function pops up
    a window and displays
    the chef's scorecard
    text file.
    """

    def open_file(file_name):
        """
        This function opens
        the chef's scorecard
        text file.
        """

        with open(file_name, "r") as file:
            content = file.read()
            text_widget.delete("1.0", tk.END)  # Clear the existing content.
            text_widget.insert(tk.END, content)  # Insert the content into the Text widget.

    root = tk.Tk("Recipes.")
    
    text_widget = tk.Text(root)
    text_widget.pack()
    
    open_file(file_name)  # Call the function to open the file and display its content.
    root.mainloop()