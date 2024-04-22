import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import mediaPipe_doctor_firebase


def on_Name_renew():
    comboName = mediaPipe_doctor_firebase.firebaseGET("user/allUser")
    combo1['values'] = comboName.split(",")


def on_Name_selected(a=None):
    name = combo1.get()
    if name == "":
        return
    comboDate = mediaPipe_doctor_firebase.firebaseGET("user/" + name + "/all")
    comboDate = comboDate.replace("_", "/")
    comboDate = comboDate.replace("=", ":")
    if "," not in comboDate:
        combo2['values'] = [comboDate]
    else:
        combo2['values'] = comboDate.split(",")


def on_Date_selected(a=None):
    name = combo1.get()
    date = combo2.get()
    date = date.replace("/", "_")
    date = date.replace(":", "=")
    info = mediaPipe_doctor_firebase.firebaseGET("user/" + name + "/" + date)
    scrollable_label.delete('1.0', tk.END)
    scrollable_label.insert(tk.END, info)


# Create the main window
window = tk.Tk()
window.title("Doctor's Site")

label = tk.Label(window, text=" ")
label.pack()

zero_row_frame = tk.Frame(window)
zero_row_frame.pack()
label1 = ttk.Label(zero_row_frame, text="Name: ")
label1.pack(side="left")
combo1 = ttk.Combobox(zero_row_frame)
combo1.bind("<<ComboboxSelected>>", on_Name_selected)
combo1['values'] = ('', '')
combo1.pack(side="left")
B_renew = tk.Button(zero_row_frame, text="Renew", command=on_Name_renew)
B_renew.pack(side="left")

label = tk.Label(window, text=" ")
label.pack()

# Second row
first_row_frame = tk.Frame(window)
first_row_frame.pack()
label2 = ttk.Label(first_row_frame, text="Date: ")
label2.pack(side="left")
combo2 = ttk.Combobox(first_row_frame)
combo2.bind("<<ComboboxSelected>>", on_Date_selected)
combo2['values'] = ('', '')
combo2.pack(side="left")

label = tk.Label(window, text=" ")
label.pack()

# Third row
scrollable_label = scrolledtext.ScrolledText(window, width=80, height=20)
# scrollable_label.configure(state='disabled')
scrollable_label.pack()
label = tk.Label(window, text=" ")
label.pack()

on_Name_renew()

# Start the main event loop
window.mainloop()
