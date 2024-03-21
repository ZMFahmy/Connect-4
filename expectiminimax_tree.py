import tkinter as tk


def print_list_of_strings(strings):
    root = tk.Tk()
    root.title("List of Strings")

    # Create a Text widget with scroll bars
    text_widget = tk.Text(root, height=10, width=40)
    scroll_y = tk.Scrollbar(root, command=text_widget.yview)
    scroll_y.pack(side='right', fill='y')  # Vertical scrollbar
    scroll_x = tk.Scrollbar(root, command=text_widget.xview, orient='horizontal')
    scroll_x.pack(side='bottom', fill='x')  # Horizontal scrollbar
    text_widget.config(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    text_widget.pack(expand=True, fill='both')  # Expand to fill both horizontally and vertically

    # Insert each string from the list into the Text widget
    for string in strings:
        text_widget.insert(tk.END, string + '\n')  # Add newline after each string

    root.mainloop()