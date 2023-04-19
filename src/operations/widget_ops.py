import tkinter as tk
from tkinter import ttk


def put_tagged_tuples_in_text_box(tagged_tuples: list, text_box: tk.Text):
    text_box.delete(0.0, tk.END)
    for tagged_tuple in tagged_tuples:
        text_box.insert(tk.END, tagged_tuple[0], tagged_tuple[1])


def get_selected_tab_index(tab_control: ttk.Notebook):
    return tab_control.index(tab_control.select())

# disables all widge ts in a given list (including children of frames)


def disable(children: list[tk.Widget], exclude: list[tk.Widget] = []):

    for child in children:
        if child.winfo_class() == 'Frame':
            if not child in exclude:
                disable(child.winfo_children(), exclude)
        else:
            if not child in exclude:
                child['state'] = 'disabled'

# enables all widgets in a given list (including children of frames)


def enable(children: list[tk.Widget]):
    for child in children:
        if child.winfo_class() == 'Frame':
            enable(child.winfo_children())
        else:
            child['state'] = 'normal'


def set_text_widget_to_list(text_widget, content_list):
    set_text(text_widget, '')
    for string in content_list:
        text_widget.insert(tk.END, string + '\n')


def set_text(entry_or_text_widget, text):

    if isinstance(entry_or_text_widget, tk.Entry):
        entry_or_text_widget.delete(0, tk.END)
    else:
        entry_or_text_widget.delete(0.0, tk.END)

    entry_or_text_widget.insert(tk.END, text)
