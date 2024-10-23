import customtkinter as ctk
import threading
import time

# Function to generate a text-based progress bar
def create_text_progress_bar(percentage, total_length=70):
    # Determine the number of filled positions
    filled_length = int(percentage / 100 * total_length)
    # Create the bar with '#' for filled and '-' for unfilled
    bar = '|' * filled_length + '' * (total_length - filled_length)
    return f"[{bar}] {percentage:.0f}%"

# Function to automatically update progress over 10 seconds (1% every 0.1 seconds)
def auto_fill_progress(textbox, progress_callback):
    for i in range(101):  # 0% to 100%
        percentage = i  # Calculate percentage
        progress_callback(percentage)  # Update progress bar
        
        # Create the text-based progress bar
        progress_text = create_text_progress_bar(percentage)
        
        textbox.delete("1.0", ctk.END)  # Delete previous content in the textbox
        textbox.insert(ctk.END, progress_text)  # Insert new progress bar with percentage
        textbox.see(ctk.END)  # Scroll to the end (optional, for larger textboxes)
        
        time.sleep(0.01)  # Wait for 0.1 seconds between updates (total 10 seconds)

# Function to start the auto-fill in a separate thread
def start_auto_fill(textbox):
    thread = threading.Thread(target=auto_fill_progress, args=(textbox, update_progress))
    thread.start()

# Update the progress bar (visual progress bar below the text box)
def update_progress(percentage):
    progress_bar.set(percentage / 100)  # Update the visual progress bar

# GUI setup
def create_gui():
    app = ctk.CTk()
    app.geometry("400x300")

    global progress_bar
    progress_bar = ctk.CTkProgressBar(app, width=300)
    progress_bar.pack(pady=20)

    # Create the textbox for the text-based progress bar
    textbox = ctk.CTkTextbox(app, height=50, width=300)
    textbox.pack(pady=10)

    # Button to start the auto-fill progress
    button = ctk.CTkButton(app, text="Start Auto-Fill", command=lambda: start_auto_fill(textbox))
    button.pack(pady=10)

    app.mainloop()

# Run the GUI
create_gui()
