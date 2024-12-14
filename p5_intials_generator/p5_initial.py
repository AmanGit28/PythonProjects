import tkinter as tk

# Create the main window for the application
window = tk.Tk()
window.geometry("1080x720")  # Set the size of the window
window.title("Name Initials Generator")  # Set the title of the window
window.configure(bg="#EAF6FF")  # Set the background color of the window

# Function to generate initials
def generate_initials():
    # Retrieve the first and last name entered by the user
    first_name = first_name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    
    # Check if both inputs are valid
    if not first_name or not last_name:
        output_label.config(text="Please enter both first and last names.", fg="red")
        return

    # Generate initials (capitalize the first letter of each name)
    first_initial = first_name[0].upper() if first_name else ""
    last_initial = last_name[0].upper() if last_name else ""

    # Display the initials
    initials = f"{first_initial}.{last_initial}."
    output_label.config(text=f"Initials: {initials}", fg="green")

# Function to close the application
def closing_tab():
    window.title("***Closing***")  # Update the title during closing
    window.configure(bg="black")  # Change the background to black for effect
    window.destroy()  # Close the application

# ----------------------------------
# UI COMPONENTS
# ----------------------------------

# Input Section: Create two entry boxes for first name and last name
first_name_label = tk.Label(window, text="First Name:", font=("Helvetica", 14), bg="#EAF6FF")
first_name_label.grid(row=0, column=0, padx=20, pady=10, sticky="W")

first_name_entry = tk.Entry(window, font=("Helvetica", 14))
first_name_entry.grid(row=0, column=1, padx=20, pady=10, sticky="WE")

last_name_label = tk.Label(window, text="Last Name:", font=("Helvetica", 14), bg="#EAF6FF")
last_name_label.grid(row=1, column=0, padx=20, pady=10, sticky="W")

last_name_entry = tk.Entry(window, font=("Helvetica", 14))
last_name_entry.grid(row=1, column=1, padx=20, pady=10, sticky="WE")

# Output Section: Create a label to display feedback or results
output_label = tk.Label(
    window,
    text="Enter your first and last names and press 'Generate Initials'",  # Default text for the output label
    width=50,
    height=6,
    pady=10,
    wraplength=800,  # Wrap text within the specified width
    font=("Helvetica", 14),
    bg="#EAF6FF",
)
output_label.grid(row=2, column=0, columnspan=2, sticky="WE", padx=20, pady=10)

# Buttons Section: Add buttons for user actions

# Button 1: Generate Initials
button1 = tk.Button(
    text="Generate Initials",
    command=generate_initials,  # Link to the function to generate initials
    bg="#B3DAF1",  # Background color
    fg="#1F3A93",  # Text color
    activebackground="#0F3057",  # Color when clicked
    font=("Helvetica", 14),
)
button1.grid(row=3, column=0, columnspan=2, sticky="WE", padx=20, pady=10)

# Button 2: Close the Application
button2 = tk.Button(
    text="Close",
    command=closing_tab,  # Link to the function to close the application
    bg="#B3DAF1",
    fg="#1F3A93",
    activebackground="#0F3057",
    font=("Helvetica", 14),
)
button2.grid(row=4, column=0, columnspan=2, sticky="WE", padx=20, pady=10)

# ----------------------------------
# MAINLOOP: Start the application
# ----------------------------------
if __name__ == "__main__":
    window.mainloop()
