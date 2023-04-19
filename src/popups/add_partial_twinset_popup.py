import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from idlelib.tooltip import Hovertip

from Collections.Fonts import Fonts
from DataObjects.TwinSet import TwinSet
from operations.os_ops import is_mac
from operations.num_ops import num_to_str
from Logic import cplunge


class AddPartialTwinsetPopup(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        ent_x_pad = (2, 2)
        ent_y_pad = (2, 2)

        lbl_y_pad = (2, 2)

        sep_x_pad = (10, 10)

        btn_y_pad = (10, 0)

        btn_width = 15
        ent_width = 10

        self.new_ts = None
        self.created = False

        self.working_ts = None

        if is_mac():
            self.entry_font = Fonts.mac_default_entry_font
        else:
            self.entry_font = Fonts.win_default_entry_font

        self.frame = ttk.Frame(self)

        self.lbl_bc = ttk.Label(self.frame)
        self.lbl_be = ttk.Label(self.frame)
        self.lbl_pe = ttk.Label(self.frame)
        self.lbl_d = ttk.Label(self.frame)

        self.lbl_initial_instruction = ttk.Label(self.frame)
        self.lbl_check_these = ttk.Label(self.frame)

        self.lbl_op_1 = ttk.Label(self.frame)
        self.lbl_op_2 = ttk.Label(self.frame)
        self.lbl_dA = ttk.Label(self.frame)

        self.ent_bc = ttk.Entry(self.frame, font=self.entry_font)
        self.ent_be = ttk.Entry(self.frame, font=self.entry_font)
        self.ent_pe = ttk.Entry(self.frame, font=self.entry_font)
        self.ent_d = ttk.Entry(self.frame, font=self.entry_font)

        self.btn_calc = ttk.Button(self.frame)

        self.sep = ttk.Separator(self.frame)

        self.ent_op_1 = ttk.Entry(self.frame, font=self.entry_font)
        self.ent_op_2 = ttk.Entry(self.frame, font=self.entry_font)

        self.btn_OK = ttk.Button(self.frame)
        self.btn_cancel = ttk.Button(self.frame)

        self.rdo_op_1 = ttk.Radiobutton(self.frame)
        self.rdo_op_2 = ttk.Radiobutton(self.frame)

        # region frame
        self.frame.grid(row=0, column=0, rowspan=6,
                        columnspan=5, padx=10, pady=10)
        # endregion

        # region lbl_bc
        self.lbl_bc.grid(row=1, column=0, sticky=tk.E, pady=lbl_y_pad)
        self.lbl_bc.config(text='Bc:')
        # endregion

        # region lbl_be
        self.lbl_be.grid(row=2, column=0, sticky=tk.E, pady=lbl_y_pad)
        self.lbl_be.config(text='Be:')
        # endregion

        # region lbl_pe
        self.lbl_pe.grid(row=3, column=0, sticky=tk.E, pady=lbl_y_pad)
        self.lbl_pe.config(text='Pe:')
        # endregion

        # region lbl_d
        self.lbl_d.grid(row=4, column=0, sticky=tk.E, pady=lbl_y_pad)
        self.lbl_d.config(text='D:')
        # endregion

        # region lbl_initial_instruction
        self.lbl_initial_instruction.grid(
            row=0, column=0, columnspan=2, pady=lbl_y_pad)
        self.lbl_initial_instruction.config(
            text='Enter Bc, Be, Pe, D (+ up or - down):')
        # endregion

        # region lbl_dA
        self.var_dA = tk.StringVar(value='dA = ')
        self.lbl_dA.grid(row=4, column=3, columnspan=4, pady=lbl_y_pad)
        self.lbl_dA.config(textvariable=self.var_dA)
        Hovertip(self.lbl_dA, 'CALCULATED ANGLE BETWEEN C-AXIS AND E-POLE', 800)
        # endregion

        # region ent_bc
        self.var_bc = tk.StringVar()
        self.var_bc.trace_add('write', lambda a, b,
                              c: self.change_made(a, b, c))
        self.ent_bc.grid(row=1, column=1, sticky=tk.W,
                         padx=ent_x_pad, pady=ent_y_pad)
        self.ent_bc.config(textvariable=self.var_bc, width=ent_width)
        self.tip_ent_bc = Hovertip(self.ent_bc, 'C-AXIS BEARING', 800)
        self.ent_bc.bind('<Return>', lambda event: self.btn_calc_click(event))
        # endregion

        # region ent_be
        self.var_be = tk.StringVar()
        self.var_be.trace_add('write', lambda a, b,
                              c: self.change_made(a, b, c))
        self.ent_be.grid(row=2, column=1, sticky=tk.W,
                         padx=ent_x_pad, pady=ent_y_pad)
        self.ent_be.config(textvariable=self.var_be, width=ent_width)
        self.tip_ent_be = Hovertip(self.ent_be, 'E-POLE BEARING', 800)
        self.ent_be.bind('<Return>', lambda event: self.btn_calc_click(event))
        # endregion

        # region ent_pe
        self.var_pe = tk.StringVar()
        self.var_pe.trace_add('write', lambda a, b,
                              c: self.change_made(a, b, c))
        self.ent_pe.grid(row=3, column=1, sticky=tk.W,
                         padx=ent_x_pad, pady=ent_y_pad)
        self.ent_pe.config(textvariable=self.var_pe, width=ent_width)
        self.tip_ent_pe = Hovertip(self.ent_pe, 'E-POLE PLUNGE', 800)
        self.ent_pe.bind('<Return>', lambda event: self.btn_calc_click(event))
        # endregion

        # region ent_d
        self.var_d = tk.StringVar()
        self.var_d.trace_add('write', lambda a, b,
                             c: self.change_made(a, b, c))
        self.ent_d.grid(row=4, column=1, sticky=tk.W,
                        padx=ent_x_pad, pady=ent_y_pad)
        self.ent_d.config(textvariable=self.var_d, width=ent_width)
        self.tip_ent_d = Hovertip(
            self.ent_d, 'DIRECTION OF TILT OF E-W AXIS', 800)
        self.ent_d.bind('<Return>', lambda event: self.btn_calc_click(event))
        # endregion

        # region sep
        self.sep.config(orient=tk.VERTICAL)
        self.sep.grid(row=0, column=2, sticky=tk.NS, rowspan=6, padx=sep_x_pad)
        # endregion

        # region lbl_check_these
        self.var_check_these = tk.StringVar(
            value='Check these on your microscope \nand select the correct option:')
        self.lbl_check_these.grid(
            row=0, column=3, columnspan=4, pady=lbl_y_pad)
        self.lbl_check_these.config(
            textvariable=self.var_check_these,
            justify=tk.CENTER
        )
        # endregion

        # region ent_op_1
        self.var_op_1 = tk.StringVar()
        self.var_op_1.set('')
        self.ent_op_1.grid(row=1, column=4, sticky=tk.W,
                           columnspan=3, rowspan=2, padx=ent_x_pad, pady=ent_y_pad)
        self.ent_op_1.config(textvariable=self.var_op_1,
                             state='readonly', width=ent_width)
        self.ent_op_1.bind(
            '<Button-1>', lambda event: self.ent_op_1_click(event))
        self.ent_op_1.bind(
            '<Return>', lambda event: self.ent_op_1_click(event))
        self.ent_op_1.bind('<space>', lambda event: self.ent_op_1_click(event))
        # endregion

        # region ent_op_2
        self.var_op_2 = tk.StringVar()
        self.var_op_2.set('')
        self.ent_op_2.grid(row=2, column=4, sticky=tk.W,
                           columnspan=3, rowspan=2, padx=ent_x_pad, pady=ent_y_pad)
        self.ent_op_2.config(textvariable=self.var_op_2,
                             state='readonly', width=ent_width)
        self.ent_op_2.bind(
            '<Button-1>', lambda event: self.ent_op_2_click(event))
        self.ent_op_2.bind(
            '<Return>', lambda event: self.ent_op_2_click(event))
        self.ent_op_2.bind('<space>', lambda event: self.ent_op_2_click(event))
        # endregion

        # region rdo_op_1
        self.var_op_choice = tk.IntVar()
        self.var_op_choice.set(0)
        self.var_op_choice.trace_add(
            'write', lambda a, b, c: self.var_op_choice_change(a, b, c))
        self.rdo_op_1.grid(row=1, column=3, rowspan=2, sticky=tk.E)
        self.rdo_op_1.config(
            state=tk.DISABLED,
            variable=self.var_op_choice,
            value=1
        )
        # endregion

        # region rdo_op_2
        self.rdo_op_2.grid(row=2, column=3, rowspan=2, sticky=tk.E)
        self.rdo_op_2.config(
            state=tk.DISABLED,
            variable=self.var_op_choice,
            value=2
        )
        # endregion

        # region btn_calc
        self.btn_calc.grid(row=5, column=0, columnspan=2, pady=btn_y_pad)
        self.btn_calc.config(
            text='Calculate',
            command=lambda: self.btn_calc_click(), width=btn_width
        )
        self.btn_calc.bind(
            '<Return>', lambda event: self.btn_calc_click(event))
        # endregion

        # region btn_ok
        self.btn_OK['state'] = 'disabled'
        self.btn_OK.grid(row=5, column=3, columnspan=2, pady=btn_y_pad)
        self.btn_OK.config(text='Add', width=btn_width)
        self.btn_OK.config(command=lambda: self.btn_OK_click())
        # endregion

        # region btn_cancel
        self.btn_cancel.grid(row=5, column=5, columnspan=2, pady=btn_y_pad)
        self.btn_cancel.config(text='Cancel', width=btn_width)
        self.btn_cancel.config(command=lambda: self.btn_cancel_click())
        # endregion

        # region AddToplevel
        self.geometry('465x225')
        self.grab_set()
        self.ent_bc.focus_set()
        self.resizable(False, False)
        # endregion

    def var_op_choice_change(self, a, b, c):
        if self.var_op_choice.get() != 0:
            result = ''

            if self.var_op_choice.get() == 1:
                result = self.ent_op_1.get()
            elif self.var_op_choice.get() == 2:
                result = self.ent_op_2.get()

            split_result = result.split()

            opt_ax_plunge = float(split_result[0])
            opt_ax_arrow = split_result[1]

            self.working_ts.cvp = opt_ax_plunge
            self.working_ts.kodec = arrow_to_num(opt_ax_arrow)

            if num_to_arrow(self.working_ts.kodec) == '<':
                temp_pc = -1 * self.working_ts.cvp
            else:
                temp_pc = self.working_ts.cvp

            dA = cplunge.angle(
                self.working_ts.cviv,
                self.working_ts.twiniv,
                self.working_ts.twinp,
                num_to_sign(self.working_ts.kodee),
                temp_pc
            )
            self.working_ts.d_a = dA

            self.var_dA.set('dA = ' + num_to_str(dA, 2, True))

            self.btn_OK.config(state=tk.NORMAL)

    def btn_OK_click(self):

        self.new_ts = self.working_ts
        self.created = True

        self.destroy()

    def btn_cancel_click(self):
        self.destroy()

    def btn_calc_click(self, event=None):
        try:
            if self.var_d.get().strip() != '+' and self.var_d.get().strip() != '-':
                raise Exception()
            result = cplunge.one_twin_set(
                float(self.var_bc.get()),
                float(self.var_be.get()),
                float(self.var_pe.get()),
                self.var_d.get()
            )
        except Exception as e:
            messagebox.showerror(
                'Error', 'Error when calculating answer, please check inputs and try again.', parent=self)
            return

        option_1 = []
        option_2 = []
        needed_adjustment = result[0]
        if needed_adjustment:
            messagebox.showinfo('Bc Adjusted', 'No solution was found for a Bc of ' + str(
                self.var_bc.get()) + ', so it was adjusted to ' + str(result[1][0]), parent=self)
            self.var_bc.set(result[1][0])
            option_1.append(result[1][1])
            option_1.append(result[1][2])
            option_2.append(result[1][3])
            option_2.append(result[1][4])
        else:
            option_1.append(result[1][0])
            option_1.append(result[1][1])
            option_2.append(result[1][2])
            option_2.append(result[1][3])

        self.var_op_1.set(str(option_1[0]) + ' ' + str(option_1[1]))
        self.var_op_2.set(str(option_2[0]) + ' ' + str(option_2[1]))

        self.rdo_op_1.config(state=tk.NORMAL)
        self.rdo_op_2.config(state=tk.NORMAL)

        self.working_ts = TwinSet(
            cviv=float(self.var_bc.get()),
            twiniv=float(self.var_be.get()),
            twinp=float(self.var_pe.get()),
            kodee=float(sign_to_num(self.var_d.get())),
            is_complete=False
        )

    def change_made(self, a, b, c):
        self.var_op_1.set('')
        self.var_op_2.set('')
        self.var_op_choice.set(0)
        self.btn_OK.config(state=tk.DISABLED)
        self.rdo_op_1.config(state=tk.DISABLED)
        self.rdo_op_2.config(state=tk.DISABLED)

    def ent_op_1_click(self, event):
        state = str(self.rdo_op_1['state'])

        if state != 'disabled':
            self.var_op_choice.set(1)

    def ent_op_2_click(self, event):
        state = str(self.rdo_op_2['state'])

        if state != 'disabled':
            self.var_op_choice.set(2)


def arrow_to_num(string):
    if string == '>':
        return 2
    else:
        return 4


def num_to_arrow(num):
    if num == 2:
        return '>'
    else:
        return '<'


def sign_to_num(string):
    if string == '+':
        return 1
    else:
        return 3


def num_to_sign(num):
    if num == 1:
        return '+'
    else:
        return '-'
