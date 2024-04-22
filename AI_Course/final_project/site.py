import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

import mediaPipe_project


def save_text_file(file_name, content):
    try:
        file_path = "/Users/slothsmba/Desktop/mediaPipe/"
        with open(file_path + file_name + ".txt", 'w') as file:
            file.write(content)
    except Exception as e:
        print("Exception" + str(e))


def on_submit():
    number = T_num.get()
    if number.isdigit():
        scrollable_label.insert(tk.END, "Entered number for judgement: " + number + "\n")
        T_num.delete(0, tk.END)

        result = mediaPipe_project.detection(int(number))
        scrollable_label.insert(tk.END, result)
        save_text_file("info", result)
        save_text_file("name", T_name.get())
        save_text_file("status", "1")
    else:
        messagebox.showerror("Error", "Please enter a valid number.")


def on_T_num_focus_in(event):
    if T_num.get() == num_hint_text:
        T_num.delete(0, tk.END)
        T_num.config(fg="black")  # Change text color to black


def on_T_num_focus_out(event):
    if T_num.get() == "":
        T_num.insert(0, num_hint_text)
        T_num.config(fg="gray")  # Change text color to gray


def on_T_name_focus_in(event):
    if T_name.get() == name_hint_text:
        T_name.delete(0, tk.END)
        T_name.config(fg="black")  # Change text color to black


def on_T_name_focus_out(event):
    if T_name.get() == "":
        T_name.insert(0, name_hint_text)
        T_name.config(fg="gray")  # Change text color to gray


# Create main window
window = tk.Tk()
window.title("Reaction Detection")

title = tk.Label(window, text="Reaction Detection", font=("Arial Bold", 50))
title.pack()

label = tk.Label(window, text=" ")
label.pack()

# Create text box and button on the first row
zero_row_frame = tk.Frame(window)
zero_row_frame.pack()

label = tk.Label(zero_row_frame, text="Please Enter Your Name: ")
label.pack(side="left")

T_name = tk.Entry(zero_row_frame, validate="key")
name_hint_text = "Name"
T_name.insert(0, name_hint_text)
T_name.config(fg="gray")
T_name.bind("<FocusIn>", on_T_name_focus_in)
T_name.bind("<FocusOut>", on_T_name_focus_out)
T_name.pack(side="left")

# Create text box and button on the first row
first_row_frame = tk.Frame(window)
first_row_frame.pack()

label = tk.Label(first_row_frame, text="Enter for reaction detection cycle: ")
label.pack(side="left")

T_num = tk.Entry(first_row_frame, validate="key")
num_hint_text = "Numbers ONLY"
T_num.insert(0, num_hint_text)
T_num.config(fg="gray")
T_num.bind("<FocusIn>", on_T_num_focus_in)
T_num.bind("<FocusOut>", on_T_num_focus_out)
T_num.pack(side="left")

B_submit = tk.Button(first_row_frame, text="Submit", command=on_submit)
B_submit.pack(side="left")

label = tk.Label(window, text=" ")
label.pack()

# Create scrollable label on the second row
scrollable_label = scrolledtext.ScrolledText(window, width=80, height=20)
# scrollable_label.configure(state='disabled')
scrollable_label.pack()

label = tk.Label(window, text=" ")
label.pack()

# Start the GUI event loop
window.mainloop()





































