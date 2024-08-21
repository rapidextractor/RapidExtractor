import tkinter as tk                        # Provides a standard Python interface to create GUIs
from tkinter import simpledialog, messagebox 
import sys
import os
import logging
from datetime import datetime

def generate_batch_file(selected_modules, case_name, device_name, batch_dir):
    """
    Generates a batch file to run the main Python script with selected modules.

    Args:
        selected_modules (str): A space-separated string of selected module names.
        case_name (str): The name of the case or operation.
        device_name (str): The name of the target device.
        batch_dir (str): The directory where the batch file will be saved.
    """
    batch_file_content = f"""@echo off
REM Dynamically determine the drive letter of the USB stick
set USB_DRIVE=%~d0

REM Set the path to the portable Python interpreter
set "PYTHON_PATH=%USB_DRIVE%\\WPy64-31241\\python-3.12.4.amd64\\python.exe"

REM Set the path to the main Python script
set "SCRIPT_PATH=%USB_DRIVE%\\RapidExtractor\\scripts\\main.py"

REM Debug output
echo Python Path: %PYTHON_PATH%
echo Script Path: %SCRIPT_PATH%

REM Check if the Python interpreter exists
if not exist "%PYTHON_PATH%" (
    echo The specified Python interpreter does not exist: %PYTHON_PATH%
    pause
    exit /b
)

REM Check if the main script exists
if not exist "%SCRIPT_PATH%" (
    echo The specified Python script does not exist: %SCRIPT_PATH%
    pause
    exit /b
)

REM Run the main script with selected modules
"%PYTHON_PATH%" "%SCRIPT_PATH%" "{selected_modules}" "{case_name}" "{device_name}"

pause
"""

    batch_file_name = os.path.join(batch_dir, f"{case_name}_{device_name}.bat")
    try:
        with open(batch_file_name, "w") as batch_file:
            batch_file.write(batch_file_content)
        logging.info(f"Batch file '{batch_file_name}' created successfully.")
        messagebox.showinfo("Success", f"Batch file '{batch_file_name}' has been created successfully.")
    except Exception as e:
        logging.error(f"Failed to create batch file '{batch_file_name}': {e}")
        messagebox.showerror("Error", f"Failed to create batch file '{batch_file_name}': {e}")

def prompt_retry_abort(message):
    """
    Prompts the user with a Retry or Abort dialog.

    Args:
    message (str): The message to display in the dialog.

    Returns:
    str: "retry" if the user chooses to retry, "abort" if the user chooses to abort.
    """
    result = messagebox.askretrycancel("Input Error", message)
    if result:
        return "retry"
    else:
        sys.exit()

def on_closing():
    """
    Handles the event when the user tries to close the window.
    """
    if messagebox.askyesno("Quit", "Do you really want to quit?"):
        root.destroy()
        sys.exit()

def create_gui():
    """
    Creates a GUI for selecting modules and generating a batch file.
    """
    global root
    root = tk.Tk()
    root.title("RapidExtractor")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Prompt the user to enter the case name
    while True:
        case_name = simpledialog.askstring("Input", "Enter the case or operation name:", parent=root)
        if not case_name:
            if prompt_retry_abort("Case or operation name is required.") == "retry":
                continue
        else:
            break

    # Prompt the user to enter the target device name
    while True:
        device_name = simpledialog.askstring("Input", "Enter the target device name:", parent=root)
        if not device_name:
            if prompt_retry_abort("Target device name is required.") == "retry":
                continue
        else:
            break

    # Create the main extraction directory based on the case name, device name, and current date
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    current_date = datetime.now().strftime("%Y-%m-%d")
    extraction_dir = os.path.join(base_dir, 'cases', f"{case_name}_{current_date}", device_name, 'extraction_results')

    if not os.path.exists(extraction_dir):
        os.makedirs(extraction_dir)

    # Create the batch file directory within the case directory
    batch_dir = os.path.join(base_dir, 'cases', f"{case_name}_{current_date}", device_name)
    if not os.path.exists(batch_dir):
        os.makedirs(batch_dir)

    # Create a subdirectory for logs within the device-specific directory
    logs_dir = os.path.join(base_dir, 'cases', f"{case_name}_{current_date}", device_name, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Configure logging to save the log file in the logs directory
    log_file_name = f"gui_{current_date}_{case_name}_{device_name}.log"
    log_file_path = os.path.join(logs_dir, log_file_name)
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    logging.info(f"Started GUI for case: {case_name}, device: {device_name}")

    root.withdraw()  # Hide the main window

    selected_modules = []
    select_all_state = tk.BooleanVar(value=True)

    # Define the modules available for selection
    modules = [
        ("DirTree", tk.BooleanVar(name="dir_tree")),
        ("Prefetch", tk.BooleanVar(name="prefetch")),
        ("Processes", tk.BooleanVar(name="processes")),
        ("Installed Programs", tk.BooleanVar(name="installed_programs")),
        ("TeamViewer", tk.BooleanVar(name="teamviewer")),
        ("BET", tk.BooleanVar(name="bet")),
        ("Browser History", tk.BooleanVar(name="browser_history"))
    ]

    def on_select():
        """
        Handles the selection of modules and generates the batch file.
        """
        nonlocal selected_modules
        selected_modules.clear()
        for module_name, module_var in modules:
            if module_var.get():
                selected_modules.append(module_var._name)
        if selected_modules:
            selected_modules_str = " ".join(selected_modules)
            generate_batch_file(selected_modules_str, case_name, device_name, batch_dir)
            logging.info(f"Selected modules: {selected_modules_str}")
            root.quit()

    def toggle_select_all():
        """
        Toggles the selection of all modules.
        """
        state = select_all_state.get()
        for _, module_var in modules:
            module_var.set(state)
        select_all_state.set(not state)
        toggle_button.config(text="Deselect All" if state else "Select All")

    # Create the main window
    main_window = tk.Toplevel(root)
    main_window.title("Module Selector")
    main_window.protocol("WM_DELETE_WINDOW", on_closing)

    # Create a header
    header = tk.Label(main_window, text="RapidExtractor", font=("Helvetica", 16, "bold"))
    header.pack(pady=10)

    # Create a table with headers
    table_frame = tk.Frame(main_window)
    table_frame.pack(pady=10)

    tk.Label(table_frame, text="Modules", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(table_frame, text="Description", font=("Helvetica", 12, "bold")).grid(row=0, column=1, padx=10, pady=5)

    descriptions = {
        "DirTree": "Shows the directory tree structure of the target device in a simple .txt format.",
        "Prefetch": "Extracts all prefetch files from target device from the following path: %SystemRoot%\\Windows\\Prefetch.",
        "Processes": "Lists the currently running processes on the target device.",
        "Installed Programs": "Shows the list of installed programs on target device.",
        "TeamViewer": "Extracts data from TeamViewer logs on target device.",
        "BET": "Extracts logfiles from BET betting software for proving betting activities on target device.",
        "Browser History": "Extracts browsing history from target device for Chrome, Edge and Firefox (if installed)."
    }

    for idx, (module_name, module_var) in enumerate(modules, start=1):
        tk.Checkbutton(table_frame, text=module_name, variable=module_var).grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)
        tk.Label(table_frame, text=descriptions[module_name], anchor="w").grid(row=idx, column=1, padx=10, pady=5, sticky=tk.W)

    # Create buttons for select/deselect all and generate batch file
    button_frame = tk.Frame(main_window)
    button_frame.pack(pady=10)

    toggle_button = tk.Button(button_frame, text="Select All", command=toggle_select_all)
    toggle_button.pack(side=tk.LEFT, padx=5)

    generate_button = tk.Button(button_frame, text="Generate Batch File", command=on_select, width=20)
    generate_button.pack(side=tk.LEFT, padx=5)

    root.deiconify()  # Show the main window
    root.mainloop()

if __name__ == "__main__":
    create_gui()
