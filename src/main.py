'''
Entry point for CSG + CPLUNGE application.
'''
import tkinter as tk

from Frames.AppFrame import AppFrame

root = tk.Tk()
root.title('CPLUNGE + CSG')

x_pad = (2, 2)
y_pad = (2, 2)

program_frame = AppFrame(root)
program_frame.grid(row=0, column=0, padx=x_pad, pady=y_pad)

root.mainloop()
