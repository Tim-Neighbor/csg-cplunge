import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor


class ColorsPopup(tk.Toplevel):
    def __init__(self, parent, back_color, point_color, icon_color, grid_color):
        tk.Toplevel.__init__(self, parent)

        btn_width = 15

        lbl_y_pad = (2, 2)

        canv_x_pad = (5, 5)
        canv_y_pad = (5, 5)

        btn_y_pad = (10, 0)

        frm_x_margin = (10, 10)
        frm_y_margin = (10, 10)

        # region create widgets
        self.frame = ttk.Frame(self)

        self.lblInstruct = ttk.Label(self.frame)
        self.lblGridColor = ttk.Label(self.frame)
        self.lblPointColor = ttk.Label(self.frame)
        self.lblIconColor = ttk.Label(self.frame)
        self.lblBackColor = ttk.Label(self.frame)

        self.pbGrid = tk.Canvas(self.frame)
        self.pbPoint = tk.Canvas(self.frame)
        self.pbIcon = tk.Canvas(self.frame)
        self.pbBack = tk.Canvas(self.frame)

        self.btnCancel = ttk.Button(self.frame)
        self.btnOk = ttk.Button(self.frame)
        # endregion create widgets

        # region config widgets
        self.frame.grid(row=0, column=0, rowspan=4, columnspan=4,
                        padx=frm_x_margin, pady=frm_y_margin)

        self.lblInstruct.grid(row=0, column=0, columnspan=4,
                              pady=(lbl_y_pad[0], lbl_y_pad[1] + 5))
        self.lblInstruct.config(
            text='Click to change plotted colors.', anchor='w')

        self.lblGridColor.grid(row=1, column=0, pady=lbl_y_pad)
        self.lblGridColor.config(text='Grid Color:')

        self.lblPointColor.grid(row=1, column=2, pady=lbl_y_pad)
        self.lblPointColor.config(text='Point Color:')

        self.lblIconColor.grid(row=2, column=2, pady=lbl_y_pad)
        self.lblIconColor.config(text='Icon Color:')

        self.lblBackColor.grid(row=2, column=0, pady=lbl_y_pad)
        self.lblBackColor.config(text='Back Color:')

        self.pbGrid.grid(row=1, column=1, padx=canv_x_pad, pady=canv_y_pad)
        self.pbGrid.config(takefocus=0, width=30, height=30)
        self.pbGrid.bind('<Button-1>', self.pbGrid_Click)

        self.pbPoint.grid(row=1, column=3, padx=canv_x_pad, pady=canv_y_pad)
        self.pbPoint.config(takefocus=0, width=30, height=30)
        self.pbPoint.bind('<Button-1>', self.pbPoint_Click)

        self.pbBack.grid(row=2, column=1, padx=canv_x_pad, pady=canv_y_pad)
        self.pbBack.config(takefocus=0, width=30, height=30)
        self.pbBack.bind('<Button-1>', self.pbBack_Click)

        self.pbIcon.grid(row=2, column=3, padx=canv_x_pad, pady=canv_y_pad)
        self.pbIcon.config(takefocus=0, width=30, height=30)
        self.pbIcon.bind('<Button-1>', self.pbIcon_Click)

        self.btnCancel.grid(row=3, column=2, columnspan=2, pady=btn_y_pad)
        self.btnCancel.config(
            text="Cancel",
            command=self.btnCancel_Click, width=btn_width
        )

        self.btnOk.grid(row=3, column=0, columnspan=2, pady=btn_y_pad)
        self.btnOk.config(
            text="Ok",
            command=self.btnOk_Click, width=btn_width
        )

        self.geometry('255x170')
        self.title('Plot Colors')
        self.focus()
        # endregion config widgets

        # region constructor
        self.originalBack = back_color
        self.originalPoint = point_color
        self.originalIcon = icon_color
        self.originalGrid = grid_color

        self.pbBack.config(bg=back_color)
        self.pbPoint.config(bg=point_color)
        self.pbIcon.config(bg=icon_color)
        self.pbGrid.config(bg=grid_color)

        self.finalBack = ''
        self.finalPoint = ''
        self.finalIcon = ''
        self.finalGrid = ''

        self.pbGrid.focus_set()
        self.grab_set()
        self.resizable(False, False)
        # endregion constructor

    def pbGrid_Click(self, event):
        colors = askcolor(title="Color", parent=self)
        self.pbGrid.configure(bg=colors[1])

    def pbPoint_Click(self, event):
        colors = askcolor(title="Color", parent=self)
        self.pbPoint.configure(bg=colors[1])

    def pbBack_Click(self, event):
        colors = askcolor(title="Color", parent=self)
        self.pbBack.configure(bg=colors[1])

    def pbIcon_Click(self, event):
        colors = askcolor(title="Color", parent=self)
        self.pbIcon.configure(bg=colors[1])

    def getBack(self):
        return self.pbBack['background']

    def getGrid(self):
        return self.pbGrid['background']

    def getPoint(self):
        return self.pbPoint['background']

    def getIcon(self):
        return self.pbIcon['background']

    def btnCancel_Click(self):
        self.pbIcon.configure(bg=self.originalIcon)
        self.pbBack.configure(bg=self.originalBack)
        self.pbPoint.configure(bg=self.originalPoint)
        self.pbGrid.configure(bg=self.originalGrid)
        self.saveFinalColors()
        self.destroy()

    def btnOk_Click(self):
        self.saveFinalColors()
        self.destroy()

    def saveFinalColors(self):
        self.finalBack = self.getBack()
        self.finalPoint = self.getPoint()
        self.finalIcon = self.getIcon()
        self.finalGrid = self.getGrid()
