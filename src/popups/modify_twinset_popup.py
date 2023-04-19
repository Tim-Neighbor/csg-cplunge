import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from Frames import TwinSetFieldsPanel
from DataObjects import TwinSet


class ModifyTwinsetPopUp(tk.Toplevel):
    '''
    Popup that is created when a user wants to modify a twinset.
    '''

    def __init__(self, parent, passed_sets, entry_font):
        tk.Toplevel.__init__(self, parent)

        frm_x_margin = (10, 10)
        frm_y_margin = (10, 10)

        spn_box_x_pad = (2, 2)
        spn_box_y_pad = (2, 2)

        lbl_y_pad = (2, 2)

        btn_x_pad = (2, 2)
        btn_y_pad = (5, 5)

        spn_box_width = 5

        btn_width = 15

        self.original_color = 'white'
        self.twin_sets = passed_sets

        self.frame = ttk.Frame(self)

        # region create widgets
        self.num_cur_twin_set = tk.Spinbox(
            self.frame,
            name='num_cur_twin_set',
            command=self.num_cur_twin_set_value_changed
        )
        self.panel1 = TwinSetFieldsPanel.TwinSetFieldsPanel(
            self.frame, name='panel1', entry_font=entry_font)
        self.lbl_twin_set = ttk.Label(self.frame, name='lbl_twin_set')
        self.btn_cancel = ttk.Button(self.frame, name='btn_cancel')
        self.btn_apply = ttk.Button(self.frame, name='btn_apply')
        self.btn_ok = ttk.Button(self.frame, name='btn_OK')
        self.btn_delete_single_set = ttk.Button(
            self.frame, name='btn_delete_single_set')
        # endregion

        # region frame
        self.frame.grid(row=0, column=0, rowspan=3, columnspan=4,
                        padx=frm_x_margin, pady=frm_y_margin)
        self.frame.rowconfigure(1, weight=1)
        # endregion

        # region num_cur_twin_set
        self.spin_box_num = tk.IntVar()
        self.spin_box_num.set(1)
        self.num_cur_twin_set.grid(
            row=0, column=1, padx=spn_box_x_pad, pady=spn_box_y_pad, sticky=tk.NW)
        self.num_cur_twin_set.config(
            textvariable=self.spin_box_num,
            from_=1,
            to=len(self.twin_sets),
            wrap=True,
            width=spn_box_width
        )
        # self.spin_box_num.trace_add('write', lambda a,b,c:self.num_cur_twin_set_value_changed(a,b,c))

        # endregion

        # region lbl_twin_set
        self.lbl_twin_set.grid(row=0, column=0, pady=lbl_y_pad, sticky=tk.NE)
        self.lbl_twin_set.config(text='Twinset:')
        # endregion

        # region panel1
        self.panel1.grid(row=0, column=2, rowspan=2, columnspan=2)
        self.panel1.all_entries_valid.trace_add(
            'write', lambda a, b, c: self.change_made(a, b, c))
        # endregion

        # region btn_cancel
        self.btn_cancel.grid(row=2, column=3, padx=btn_x_pad, pady=btn_y_pad)
        self.btn_cancel.config(text='Cancel', width=btn_width)
        self.btn_cancel.config(command=lambda: self.btn_cancel_click())
        # endregion

        # region btn_apply
        self.btn_apply['state'] = 'disabled'
        self.btn_apply.grid(row=2, column=2, padx=btn_x_pad, pady=btn_y_pad)
        self.btn_apply.config(text='Apply', width=btn_width)
        self.btn_apply.config(command=lambda: self.btn_apply_click())
        # endregion

        # region btn_OK
        self.btn_ok['state'] = 'disabled'
        self.btn_ok.grid(row=2, column=0, columnspan=2,
                         padx=btn_x_pad, pady=btn_y_pad)
        self.btn_ok.config(text='OK', width=btn_width)
        self.btn_ok.config(command=lambda: self.btn_ok_click())
        # endregion

        # region btn_delete_single_set
        self.btn_delete_single_set.grid(
            row=1, column=0, columnspan=2, padx=btn_x_pad, pady=btn_y_pad, sticky=tk.N)
        self.btn_delete_single_set.config(text='Delete Set', width=btn_width)
        self.btn_delete_single_set.config(
            command=lambda: self.btn_delete_single_set_click())
        # endregion

        # region ModifyPopUp
        # self.geometry('284x368')
        self.title('Modify Twinset')

        self.grab_set()
        self.resizable(False, False)
        # endregion

        # region constructor

        lowest = self.twin_sets[0]
        self.last_twin_set = 1

        self.has_change = False

        self.set_entries_to_ts_values(lowest)

        self.in_valid_state = True
        self.btn_apply['state'] = 'disabled'
        # endregion

    def num_cur_twin_set_value_changed(self):
        if not self.has_change:
            # no change, good to go
            self.update_entries_to_next_ts()
        elif self.in_valid_state:
            # has change, but in a valid state, check to see if they want to save
            confirm = messagebox.askyesnocancel(
                'Confirm', 'Do you want to save the changes to the current Twinset?',
                parent=self)

            if confirm is None:
                self.spin_box_num.set(self.last_twin_set)
            elif confirm:
                self.twin_set_creator(self.last_twin_set)
                self.update_entries_to_next_ts()
                # self.set_entries_to_ts_values(next_ts)
                # self.twin_set_creator(self.last_twin_set)
                #self.last_twin_set = x
            else:
                self.update_entries_to_next_ts()
        elif not self.in_valid_state:
            messagebox.showerror(
                title='Invalid Data',
                message='The data entered for the current Twinset is invalid, please correct this before changing Twinsets.',
                parent=self
            )
            self.spin_box_num.set(self.last_twin_set)

    def update_entries_to_next_ts(self):
        next_ts_num = self.spin_box_num.get()
        next_ts = self.twin_sets[next_ts_num - 1]

        self.set_entries_to_ts_values(next_ts)
        self.btn_apply['state'] = 'disabled'
        self.last_twin_set = next_ts_num

        self.has_change = False

    def btn_apply_click(self):
        '''Handles click on the "apply" button.'''
        self.twin_set_creator(int(self.num_cur_twin_set.get()))
        self.has_change = False
        self.btn_apply['state'] = 'disabled'

    def twin_set_creator(self, ts_num):
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

        self.twin_sets[ts_num-1] = ts
        return

    def change_made(self, a, b, c):
        if self.panel1.all_entries_valid.get():
            self.btn_apply['state'] = 'normal'
            self.btn_ok['state'] = 'normal'
            self.has_change = True
            self.in_valid_state = True
        else:
            self.btn_apply['state'] = 'disabled'
            self.btn_ok['state'] = 'disabled'
            self.has_change = True
            self.in_valid_state = False

    def btn_cancel_click(self):
        self.destroy()

    def btn_ok_click(self):
        if self.has_change:
            self.twin_set_creator(self.spin_box_num.get())
        self.destroy()

    def btn_delete_single_set_click(self):

        next_ts_num = self.ts_num_after_deletion()

        confirm = messagebox.askyesno(
            'Confirm', 'Are you sure you wish to delete this Twinset? \n(This action cannot be undone.)',
            parent=self)

        if confirm:
            self.twin_sets.pop(int(self.spin_box_num.get()) - 1)
            self.has_change = False

            if len(self.twin_sets) == 0:
                self.destroy()
            else:
                self.spin_box_num.set(next_ts_num)
                self.update_entries_to_next_ts()

        self.reset_spin_box_bounds()

    def reset_spin_box_bounds(self):
        self.num_cur_twin_set.config(
            from_=1,
            to=len(self.twin_sets)
        )

    def ts_num_after_deletion(self):
        if self.spin_box_num.get() == len(self.twin_sets):
            return self.spin_box_num.get() - 1
        else:
            return self.spin_box_num.get()

    def set_entry_text(self, entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, text)

    def set_entries_to_ts_values(self, ts):
        has_change_store = self.has_change

        self.set_entry_text(self.panel1.txt_CVIV,
                            str(TwinSet.min_num(ts.cviv)))
        self.set_entry_text(self.panel1.txt_CVP, str(TwinSet.min_num(ts.cvp)))
        self.set_entry_text(self.panel1.txt_KODEC,
                            str(TwinSet.min_num(ts.kodec)))
        self.set_entry_text(self.panel1.txt_TWINIV,
                            str(TwinSet.min_num(ts.twiniv)))
        self.set_entry_text(self.panel1.txt_TWINP,
                            str(TwinSet.min_num(ts.twinp)))
        self.set_entry_text(self.panel1.txt_KODEE,
                            str(TwinSet.min_num(ts.kodee)))
        self.set_entry_text(self.panel1.txt_TOTALM,
                            str(TwinSet.min_num(ts.totalm)))
        self.set_entry_text(self.panel1.txt_THICKM,
                            str(TwinSet.min_num(ts.thickm)))
        self.set_entry_text(self.panel1.txt_TOTALT,
                            str(TwinSet.min_num(ts.totalt)))
        self.set_entry_text(self.panel1.txt_THICKO,
                            str(TwinSet.min_num(ts.thicko)))
        self.set_entry_text(self.panel1.txt_THICKI,
                            str(TwinSet.min_num(ts.thicki)))
        self.set_entry_text(self.panel1.txt_WIDTHN,
                            str(TwinSet.min_num(ts.widthn)))

        self.has_change = has_change_store
