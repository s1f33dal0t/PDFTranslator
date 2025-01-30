"""
PDF Translator using DeepL API

This script provides a graphical user interface (GUI) for translating PDF files 
using the DeepL API. It allows users to select a PDF file, choose a target language, 
and translate the file while monitoring internet connection status. The translated 
file is saved in the same directory as the original file with a modified filename.

Features:
- Internet connection check with dynamic status updates.
- File selection through a GUI.
- Support for multiple target languages.

Dependencies:
- deepl (DeepL Python API)
- tkinter
"""

import os
import time
import socket
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import deepl
from config import api_key as key

def check_internet_connection():

    """
    Continuously checks for an active internet connection by attempting to connect 
    to Google's public DNS server. Updates the GUI based on the connection status.
    """

    while True:
        try:
            # attempt connection every 5 sec
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            update_connection_status(True)
        except OSError:
            update_connection_status(False)
        time.sleep(5)

def update_connection_status(is_connected):

    """
    Updates the GUI to reflect the current internet connection status.

    Args:
        is_connected: True if connected, False otherwise.
    """

    if is_connected:
        result_label.config(text="Connected", fg="green")
        translate_button.config(state="normal")  # Enable translation button
    else:
        result_label.config(text="Connection failed, please connect to the internet", fg="red")
        translate_button.config(state="disabled")  # Disable translation button

def translate_pdf(input_pdf_path, output_pdf_path, target_lang, api_key):

    """
    Translates a PDF file using the DeepL API.

    Args:
        input_pdf_path (str): Path to the input PDF file.
        output_pdf_path (str): Path to save the translated PDF file.
        target_lang (str): Target language code (e.g., "FR" for French).
        api_key (str): DeepL API key for authentication.
    """

    translator = deepl.Translator(api_key)
    try:
        with open(input_pdf_path, "rb") as input_file, \
             open(output_pdf_path, "wb") as output_file:
            
            # Translate the document
            translator.translate_document(
                input_file,
                output_file,
                target_lang=target_lang
            )
        print("Translation completed and saved to:", output_pdf_path)
    except deepl.exceptions.QuotaExceededException as exc:
        raise Exception(f"Quota Exceeded: {str(exc)}") from exc
    except deepl.exceptions.DeepLException as exc:
        raise Exception(f"DeepL API error: {str(exc)}") from exc
    except Exception as exc:
        raise Exception(f"An error occurred: {str(exc)}") from exc

def select_file():

    """
    Opens a file dialog for selecting a PDF file and updates the input entry field 
    with the selected file's path.
    """

    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def check_usage(api_key):

    """
    Checks the current usage of the DeepL API and prints usage statistics.

    Args:
        api_key (str): DeepL API key for authentication.

    Raises:
        Exception: If character limit is exceeded.
    """

    translator = deepl.Translator(api_key)
    usage = translator.get_usage()
    if usage.character.limit_exceeded:
        raise Exception(f"Character limit exceeded. Used {usage.character.count} "
                        f"out of {usage.character.limit}")
    print(f"Characters used: {usage.character.count} out of {usage.character.limit}")

def translate():

    """
    Main translation function that orchestrates the PDF translation process.
    Handles file selection, API usage check, and translation with error handling.
    """
    
    input_pdf_path = input_entry.get()
    target_lang = lang_var.get()
    api_key = key

    # Validate input file and API key
    if not input_pdf_path or not api_key:
        messagebox.showerror("Error", "Please select an input file.")
        return

    # check API usage before translation
    try:
        check_usage(api_key)
    except Exception as exc:
        messagebox.showerror("API Usage Error", str(exc))
        return

    # output file path
    input_dir = os.path.dirname(input_pdf_path)
    input_filename = os.path.basename(input_pdf_path)
    output_filename = f"translated_{target_lang}_{input_filename}"
    output_pdf_path = os.path.join(input_dir, output_filename)

    # Translate
    try:
        translate_pdf(input_pdf_path, output_pdf_path, target_lang, api_key)
        messagebox.showinfo("Success!", f"Translation completed and saved to:\n{output_pdf_path}")
    except Exception as exc:
        messagebox.showerror("Error", str(exc))

# GUI Setup
root = tk.Tk()
root.title("PDF Translator")

# Connection status label
result_label = tk.Label(root, text="Checking connection...", font=("Arial", 12))
result_label.pack(pady=10)

# frame
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Select PDF File: ").pack(side="left")
input_entry = tk.Entry(frame, width=50)
input_entry.pack(side="left", padx=5)
browse_button = tk.Button(frame, text="Browse", command=select_file)
browse_button.pack(side="left")

# Language selection
available_languages = ["", "EN-US", "PL", "SK", "SL",  "ET", "LT", "DE", "FI", "LV", "RO", "RU", "TR", "UK"]
tk.Label(root, text="Target Language:").pack()
lang_var = tk.StringVar(value="EN-US")  # Default Language
lang_menu = ttk.OptionMenu(root, lang_var, *available_languages)
lang_menu.pack(pady=5)

# translate button
translate_button = tk.Button(root, text="Translate", command=translate, width=50)
translate_button.pack(pady=20)

# Start internet connection monitoring
threading.Thread(target=check_internet_connection, daemon=True).start()

root.mainloop()
