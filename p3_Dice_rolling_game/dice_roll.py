# Dice Rolling Game
import tkinter as tk
from PIL import Image, ImageTk
import random

# Initialize the main window
window = tk.Tk()
window.geometry("1080x720")  # Set the window size
window.title("Dice Game")  # Set the window title
window.configure(bg="#EAF6FF")  # Set the background color

# List of dice images
dice = [
    "D:/Project per DAY/a3 Dice Simulator/dice1.png",
    "D:/Project per DAY/a3 Dice Simulator/dice2.png",
    "D:/Project per DAY/a3 Dice Simulator/dice3.png",
    "D:/Project per DAY/a3 Dice Simulator/dice4.png",
    "D:/Project per DAY/a3 Dice Simulator/dice5.png",
    "D:/Project per DAY/a3 Dice Simulator/dice6.png"
]

# Load the initial dice image
image1 = ImageTk.PhotoImage(Image.open(random.choice(dice)))

# Display the initial dice image
label1 = tk.Label(window, image=image1)
label1.image = image1
label1.place(x=284, y=100)  # Position the dice image

# Function to roll the dice and update the image
def roll_dice():
    new_image = ImageTk.PhotoImage(Image.open(random.choice(dice)))  # Load a random dice image
    label1.configure(image=new_image)  # Update the label with the new image
    label1.image = new_image  # Keep a reference to avoid garbage collection

# Create the roll button and position it at the center bottom
button = tk.Button(
    window,
    text="Roll",
    command=roll_dice,
    bg="#B3DAF1",
    fg="#1F3A93",
    activebackground="#0F3057",
    font=("Helvetica", 14),
    width=20,  # Width in characters
    height=2   # Height in text lines
)

# Calculate button position to center it horizontally
button_width = 160  # Approximate width of the button in pixels
button_x = (1080 - button_width) // 2  # Center horizontally in a 1080px wide window
button.place(x=button_x, y=10)  # Place the button near the bottom

# Run the Tkinter event loop
window.mainloop()
