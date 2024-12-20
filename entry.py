import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime

# File to store the data
FILE_NAME = "visitors.csv"

# Create the CSV file if it doesn't exist
def initialize_csv():
    try:
        with open(FILE_NAME, mode="x", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone", "Address", "Entry Date & Time"])
    except FileExistsError:
        pass

# Function to add entry
def add_entry():
    name = name_var.get()
    phone = phone_var.get()
    address = address_var.get()
    if not name or not phone or not address:
        messagebox.showerror("Input Error", "All fields are required!")
        return

    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILE_NAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name, phone, address, entry_time])
    messagebox.showinfo("Success", "Entry added successfully!")

    # Clear the input fields
    name_var.set("")
    phone_var.set("")
    address_var.set("")

    # Automatically retrieve and display updated entries
    view_entries()

# Function to delete selected entry
def delete_entry():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "No entry selected!")
        return

    data = tree.item(selected_item, "values")
    all_entries = []

    # Read existing entries
    with open(FILE_NAME, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        all_entries = list(reader)

    # Remove the selected entry
    with open(FILE_NAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for entry in all_entries:
            if entry != list(data):
                writer.writerow(entry)

    messagebox.showinfo("Success", "Entry deleted successfully!")

    # Automatically refresh the table
    view_entries()

# Function to view all entries
def view_entries(search_term=""):
    for row in tree.get_children():
        tree.delete(row)

    try:
        with open(FILE_NAME, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                if search_term.lower() in row[0].lower() or search_term in row[1]:
                    tree.insert("", "end", values=row)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")

# Function for the search feature
def search_entries():
    search_term = search_var.get()
    view_entries(search_term)

# Initialize the CSV file
initialize_csv()

# GUI setup
root = tk.Tk()
root.title("Visitor Entry System")
root.geometry("800x500")
root.configure(bg="#f2f2f2")  # Set background color

# Title Label
title_label = tk.Label(root, text="Visitor Entry System", font=("Helvetica", 18, "bold"), bg="#f2f2f2", fg="#333")
title_label.pack(pady=10)

# Variables
name_var = tk.StringVar()
phone_var = tk.StringVar()
address_var = tk.StringVar()
search_var = tk.StringVar()

# Input fields
frame = tk.Frame(root, bg="#f2f2f2")
frame.pack(pady=10)

tk.Label(frame, text="Name:", font=("Helvetica", 12), bg="#f2f2f2").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(frame, textvariable=name_var, font=("Helvetica", 12), width=25).grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Phone:", font=("Helvetica", 12), bg="#f2f2f2").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(frame, textvariable=phone_var, font=("Helvetica", 12), width=25).grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Address:", font=("Helvetica", 12), bg="#f2f2f2").grid(row=2, column=0, padx=5, pady=5)
tk.Entry(frame, textvariable=address_var, font=("Helvetica", 12), width=25).grid(row=2, column=1, padx=5, pady=5)

# Buttons
button_frame = tk.Frame(root, bg="#f2f2f2")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Entry", font=("Helvetica", 12), command=add_entry, bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=10, pady=10)
tk.Button(button_frame, text="Delete Entry", font=("Helvetica", 12), command=delete_entry, bg="#F44336", fg="white", width=15).grid(row=0, column=1, padx=10, pady=10)

# Search bar
tk.Label(root, text="Search:", font=("Helvetica", 12), bg="#f2f2f2").pack(pady=5)
tk.Entry(root, textvariable=search_var, font=("Helvetica", 12), width=30).pack(pady=5)
tk.Button(root, text="Search", font=("Helvetica", 12), command=search_entries, bg="#2196F3", fg="white").pack(pady=10)

# Treeview for displaying entries with scrollbars
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True)

tree_scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
tree_scroll_y.pack(side="right", fill="y")

tree_scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")
tree_scroll_x.pack(side="bottom", fill="x")

tree = ttk.Treeview(tree_frame, columns=("Name", "Phone", "Address", "Entry Date & Time"), show="headings", yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Address", text="Address")
tree.heading("Entry Date & Time", text="Entry Date & Time")

tree.pack(fill=tk.BOTH, expand=True)

tree_scroll_y.config(command=tree.yview)
tree_scroll_x.config(command=tree.xview)

# View Entries initially
view_entries()

root.mainloop()
