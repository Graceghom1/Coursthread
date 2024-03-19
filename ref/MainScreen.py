# main_ui.py
import customtkinter as ctk
import tkinter as tk
import threading
import webview  # Make sure you have this installed via pip
from CTkTable import *
from analysis import get_html_content, analyze_html_content  # Adjust this import based on your file names and paths


def log_message(message):
    """Function to log messages to the UI."""
    if log_text:
        log_text.configure(state='normal')
        log_text.insert('end', message + '\n')
        log_text.configure(state='disabled')
        log_text.yview('end')


# main_ui.py
# Update UI function to call update_word_freq_table
def update_ui(analysis_results):
    """Function to update the UI with the analysis results."""

    def update_task():
        # Handle structured analysis results:
        for key, value in analysis_results.items():
            modified_key = f"{key}:"  # Your UI labels seem to expect a colon and space
            if modified_key in stats_vars:
                # Update UI directly with value, assuming value is already a string or convertible to string
                stats_vars[modified_key].set(str(value))
            else:
                log_message(f"Unknown key in results: {key}")

        # Display word frequency analysis result in the custom table
        word_freq_data = analysis_results.get("Word Frequency", {})
        update_word_freq_table(word_freq_data, word_freq_table)

        log_message("UI updated with analysis results.")

    app.after(0, update_task)


# main_ui.py
def perform_analysis(url):
    """Performs analysis on the specified URL."""
    if not url:
        log_message("No URL provided.")
        return
    log_message(f"Starting analysis for {url}...")
    html_content, loading_time, error = get_html_content(url)
    if error:
        log_message(error)
        return  # Early return on error
    analysis_results, error = analyze_html_content(html_content)
    if error:
        log_message(error)
        return  # Early return on error
    # Add loading time to analysis results
    analysis_results['Loading Time'] = f"{loading_time:.2f} seconds"
    app.after(0, lambda: update_ui(analysis_results))
    log_message(f"Analysis for {url} completed.")


def display_website():
    """Function to display the website in a separate window using webview."""
    url = url_entry.get()
    if url:
        log_message(f"Displaying website: {url}")
        webview.create_window('Website Display', url, confirm_close=True)
        webview.start(gui='qt')


def get_item_indices(word_freq_data: list, item):
    indices = []
    for index, (word, frequency) in enumerate(word_freq_data):
        if word == item:  # Check if the word matches the item
            indices.append(index)
    return indices


# Update function to populate CTkTable with word frequency data
def update_word_freq_table(word_freq_data: list, ):
    # Delete all existing rows from the table
    word_freq_table.delete_rows()

    # Add new rows to the table
    for word, frequency in word_freq_data:
        word_freq_table.add_row([word, frequency])

# Setup for the main window
app = ctk.CTk()
app.title("Website Analyzer")

# URL input
url_label = ctk.CTkLabel(app, text="Website URL:")
url_label.pack(pady=(20, 10))
url_var = tk.StringVar(value="https://www.lemonde.fr/")
url_entry = ctk.CTkEntry(app, width=400, textvariable=url_var)
url_entry.pack()

# Analyze button
analyze_button = ctk.CTkButton(app, text="Analyze Website", command=lambda: threading.Thread(target=perform_analysis,
                                                                                             args=(
                                                                                                 url_entry.get(),)).start())
analyze_button.pack(pady=10)

# View Website button
view_button = ctk.CTkButton(app, text="View Website", command=display_website)
view_button.pack(pady=10)

# Stats area setup
stats_frame = ctk.CTkFrame(app)
stats_frame.pack(pady=(10, 0), padx=20, fill='both', expand=True)
stats_labels = [
    "Loading Time:", "Word Frequency:", "Copy Paste Enabled:", "Outbound/Inbound Links:",
    "Image Sizes:", "Number of H1 in Source Code:", "Keywords Pertinence:",
    "Is the Website Mobile Friendly:", "Is the Website Accessible:"
]
stats_vars = {}
for label in stats_labels:
    row_frame = ctk.CTkFrame(stats_frame)
    row_frame.pack(fill='x', pady=2)
    ctk.CTkLabel(row_frame, text=label, width=200, anchor='w').pack(side='left')
    var = tk.StringVar(value="N/A")
    stats_vars[label] = var
    ctk.CTkLabel(row_frame, textvariable=var, width=200, anchor='w').pack(side='right')

# Word Frequency table setup
word_freq_frame = ctk.CTkFrame(app)
word_freq_frame.pack(pady=(10, 0), padx=20, fill='both', expand=True)
word_freq_label = ctk.CTkLabel(word_freq_frame, text="Word Frequency:")
word_freq_label.pack(anchor='w', padx=(0, 10), pady=(0, 5))

word_freq_table = CTkTable(master=word_freq_frame, row=0, column=2)
word_freq_table.pack(fill='both', expand=True)

# Log area setup
log_label = ctk.CTkLabel(app, text="Log:")
log_label.pack(pady=(10, 0))
log_frame = ctk.CTkFrame(app)
log_frame.pack(padx=20, fill='both', expand=True)
log_text = tk.Text(log_frame, state='disabled', height=8, wrap='word')
log_text.pack(expand=True, fill='both')

# Start the application loop
app.mainloop()
