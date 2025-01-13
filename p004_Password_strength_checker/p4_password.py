import tkinter as tk

# Create the main window for the application
window = tk.Tk()
window.geometry("1080x720")  # Set the size of the window
window.title("Password Strength Checker")  # Set the title of the window
window.configure(bg="#EAF6FF")  # Set the background color of the window

# Function to check the strength of the entered password
def checking_string():
    # Retrieve the password entered by the user
    password = input_label.get()

    # Initialize flags to check password conditions
    has_uppercase = False
    has_lowercase = False
    has_numbers = False
    has_special_chars = False

    # Check each character in the password for specific conditions
    for char in password:
        if char.isupper():  # Check for uppercase letters
            has_uppercase = True
        elif char.islower():  # Check for lowercase letters
            has_lowercase = True
        elif char.isdigit():  # Check for numeric digits
            has_numbers = True
        elif not char.isalnum():  # Check for special characters
            has_special_chars = True

    # Determine if the password meets all criteria for strength
    if (
        has_uppercase
        and has_lowercase
        and has_numbers
        and has_special_chars
        and len(password) >= 8
    ):
        # If all conditions are met, the password is strong
        output_label.config(text="Password is strong", fg="green")
    else:
        # Otherwise, provide feedback on why the password is not strong
        output_label.config(
            text="Password is not strong.\n"
                 "Make sure it has:\n"
                 "- At least 8 characters\n"
                 "- Uppercase and lowercase letters\n"
                 "- Numbers\n"
                 "- Special characters",
            fg="red",
        )

# Function to close the application
def closing_tab():
    window.title("***Closing***")  # Update the title during closing
    window.configure(bg="black")  # Change the background to black for effect
    window.destroy()  # Close the application

# ----------------------------------
# UI COMPONENTS
# ----------------------------------

# Input Section: Create an entry box for the user to input their password
input_label = tk.Entry(
    window,
    font=("Helvetica", 14),  # Set font style and size
)
input_label.grid(row=0, column=0, sticky="WE", padx=20, pady=10)  # Position the entry box

# Output Section: Create a label to display feedback or results
output_label = tk.Label(
    window,
    text="Display for Password Status",  # Default text for the output label
    width=50,
    height=6,
    pady=10,
    wraplength=800,  # Wrap text within the specified width
    font=("Helvetica", 14),
)
output_label.grid(row=1, column=0, sticky="WE", padx=20, pady=10)

# Buttons Section: Add buttons for user actions

# Button 1: Check Password Strength
button1 = tk.Button(
    text="Check",
    command=checking_string,  # Link to the function to check password strength
    bg="#B3DAF1",  # Background color
    fg="#1F3A93",  # Text color
    activebackground="#0F3057",  # Color when clicked
    font=("Helvetica", 14),
)
button1.grid(row=2, column=0, sticky="WE", padx=20, pady=10)  # Position the button

# Button 2: Close the Application
button2 = tk.Button(
    text="Close",
    command=closing_tab,  # Link to the function to close the application
    bg="#B3DAF1",
    fg="#1F3A93",
    activebackground="#0F3057",
    font=("Helvetica", 14),
)
button2.grid(row=3, column=0, sticky="WE", padx=20, pady=10)

# ----------------------------------
# MAINLOOP: Start the application
# ----------------------------------
if __name__ == "__main__":
    window.mainloop()
