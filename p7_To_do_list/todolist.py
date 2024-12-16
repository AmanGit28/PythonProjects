import tkinter as tk

# Task storage list
task_storage = []

# Create main window
window = tk.Tk()
window.geometry("1080x640")
window.title("To Do List")
window.configure(bg="#EAF6FF")
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

# Define functions
def addtask():
    task = input_label.get()
    if task.strip():  # Add task only if it is not empty
        task_storage.append(task)
        task_listbox.insert(tk.END, task)
        input_label.delete(0, tk.END)

def removetask():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:  # Remove only if a task is selected
        task_storage.pop(selected_task_index[0])
        task_listbox.delete(selected_task_index)

def closewindow():
    window.title("***Closing***")
    window.destroy()

# Create input field
input_label = tk.Entry(window, font=("Helvetica", 14), width=40)
input_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Create task selection section
task_listbox = tk.Listbox(window, font=("Helvetica", 14), width=40, height=10)
task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create buttons
button_frame = tk.Frame(window, bg="#EAF6FF")
button_frame.grid(row=3, column=0, columnspan=2, pady=10)

button1 = tk.Button(
    button_frame,
    text="Add",
    command=addtask,
    bg="#B3DAF1",
    fg="#1F3A93",
    activebackground="#0F3057",
    font=("Helvetica", 14),
    width=15
)
button1.grid(row=0, column=0, padx=10)

button2 = tk.Button(
    button_frame,
    text="Remove",
    command=removetask,
    bg="#B3DAF1",
    fg="#1F3A93",
    activebackground="#0F3057",
    font=("Helvetica", 14),
    width=15
)
button2.grid(row=0, column=1, padx=10)

button3 = tk.Button(
    text="Close",
    command=closewindow,
    bg="#B3DAF1",
    fg="#1F3A93",
    activebackground="#0F3057",
    font=("Helvetica", 14),
    width=40
)
button3.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Run the application
if __name__ == "__main__":
    window.mainloop()
