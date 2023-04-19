import tkinter as tk
from tkinter import ttk
from idlelib.tooltip import Hovertip
import DataObjects.TwinSet as TwinSet
import Frames.TwinSetFieldsPanel as TwinSetFieldsPanel


class AddCompleteTwinsetPopup(tk.Toplevel):

    def __init__(self, parent, entry_font, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        btn_width = 15

        btn_y_pad = (5, 5)

        self.new_ts = []
        self.original_color = 'white'
        self.created = False

        # region create widgets
        #self.frame = ttk.Frame(self)
        self.panel1 = TwinSetFieldsPanel.TwinSetFieldsPanel(
            self, name='panel1', entry_font=entry_font)
        self.btn_OK = ttk.Button(
            self, name='btn_OK', width=btn_width)
        self.btn_cancel = ttk.Button(
            self, name='btn_cancel', width=btn_width)
        # endregion

        self.panel1.all_entries_valid.trace_add(
            'write', lambda a, b, c: self.set_OK_btn_state(a, b, c))
        self.panel1.grid(row=0, column=0, columnspan=2)

        # region frame
        #self.frame.grid(row=0, column=0, rowspan=2, columnspan=2)
        # endregion

        # region btn_OK
        self.btn_OK['state'] = 'disabled'
        self.btn_OK.grid(row=1, column=0, pady=btn_y_pad)
        self.btn_OK.config(text='Ok')
        self.btn_OK.config(command=lambda: self.btn_OK_click())
        Hovertip(self.btn_OK, 'test')

        # endregion

        # region btn_cancel
        self.btn_cancel.grid(row=1, column=1, pady=btn_y_pad)
        self.btn_cancel.config(text='Cancel')
        self.btn_cancel.config(command=lambda: self.btn_cancel_click())
        # endregion

        # region AddPopUp
        self.geometry('191x373')
        self.title('Add Twinset')

        self.panel1.txt_CVIV.focus()
        self.grab_set()
        self.resizable(False, False)

        # endregion

    def set_OK_btn_state(self, var, index, mode):
        if self.panel1.all_entries_valid.get():
            self.btn_OK['state'] = 'normal'
        else:
            self.btn_OK['state'] = 'disabled'

    def btn_OK_click(self):
        ts = TwinSet.TwinSet()

        ts.cviv = float(self.panel1.txt_CVIV.get())
        ts.cvp = float(self.panel1.txt_CVP.get())
        ts.kodec = float(self.panel1.txt_KODEC.get())
        ts.kodee = float(self.panel1.txt_KODEE.get())
        ts.thicki = float(self.panel1.txt_THICKI.get())
        ts.thickm = float(self.panel1.txt_THICKM.get())
        ts.thicko = float(self.panel1.txt_THICKO.get())
        ts.totalm = float(self.panel1.txt_TOTALM.get())
        ts.totalt = float(self.panel1.txt_TOTALT.get())
        ts.twiniv = float(self.panel1.txt_TWINIV.get())
        ts.twinp = float(self.panel1.txt_TWINP.get())
        ts.widthn = float(self.panel1.txt_WIDTHN.get())

        self.new_ts = ts
        self.created = True
        self.destroy()

    def btn_cancel_click(self):
        self.created = False
        self.destroy()
