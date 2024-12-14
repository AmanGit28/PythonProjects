# QUOTE GENERATOR
# Import necessary libraries
# pip install requests
import tkinter as tk
import requests
from threading import Thread

# API endpoint for random quotes
api = "http://api.quotable.io/random"
quotes = []  # List to store preloaded quotes
quote_number = 0  # Index of the current quote

# Initialize the Tkinter window
window = tk.Tk()
window.geometry("960x260")
window.title("Quote Generation")
window.grid_columnconfigure(0, weight=1)
window.resizable(False, False)
window.configure(bg="#EAF6FF")

# Function to preload 10 quotes in the background
def preload_quotes():
    global quotes
    print("***Loading more Quotes***")
    for x in range(10):
        random_quote = requests.get(api).json()
        content = random_quote["content"]
        author = random_quote["author"]
        quote = content + "\n\n" + "by " + author
        print(content)
        quotes.append(quote)
    print("Finished loading more quotes")

# Preload initial quotes
preload_quotes()

# Function to display a random quote
def get_random_quote():
    global quote_label, quotes, quote_number
    quote_label.configure(text=quotes[quote_number])  # Show current quote
    quote_number += 1  # Increment quote index
    print(quote_number)
    # Preload more quotes if reaching near the end of the list
    if quotes[quote_number] == quotes[-3]:
        thread = Thread(target=preload_quotes)  # Load quotes in a separate thread
        thread.start()
        
# ----------------------------------
# UI COMPONENTS
# ----------------------------------
quote_label = tk.Label(
    window, text="Generate new quote", height=6, pady=10, wraplength=800, font=("Helvetica", 14)
)
quote_label.grid(row=0, column=0, stick="WE", padx=20, pady=10)

button = tk.Button(
    text="Generate",
    command=get_random_quote,
    bg="#B3DAF1",
    fg="#1F3A93",
    activebackground="#0F3057",
    font=("Helvetica", 14),
)
button.grid(row=1, column=0, stick="WE", padx=20, pady=10)

# ----------------------------------
# MAINLOOP: Start the application
# ----------------------------------

# Run the application
if __name__ == "__main__":
    window.mainloop()
