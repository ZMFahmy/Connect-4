import tkinter as tk


def print_list_of_strings(strings):
    root = tk.Tk()
    root.title("List of Strings")

    text_widget = tk.Text(root, height=10, width=40)
    text_widget.pack()

    # Insert each string from the list into the Text widget
    for string in strings:
        text_widget.insert(tk.END, string + '\n')  # Add newline after each string

    root.mainloop()
