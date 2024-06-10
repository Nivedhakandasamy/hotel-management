import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Connect to SQLite database
conn = sqlite3.connect('hotel_management.db')
c = conn.cursor()

# Create the tables
def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS guests (
                    guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
                    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guest_id INTEGER,
                    room_number INTEGER,
                    check_in_date TEXT,
                    check_out_date TEXT,
                    FOREIGN KEY (guest_id) REFERENCES guests(guest_id))''')
    conn.commit()

create_tables()

# GUI Functions
def add_guest():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    if name and phone and email:
        c.execute("INSERT INTO guests (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        conn.commit()
        messagebox.showinfo("Success", "Guest added successfully")
        clear_guest_entries()
        view_guests()
    else:
        messagebox.showwarning("Input Error", "All fields are required")

def update_guest():
    selected_item = guest_tree.focus()  # Get the selected item from the Treeview
    if selected_item:
        # Retrieve the values from the Entry widgets
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        new_guest_id = guest_id_entry.get()  # Retrieve the updated guest ID

        # Retrieve the guest_id from the selected item
        values = guest_tree.item(selected_item, 'values')
        old_guest_id = values[0]  # The first value is the old guest_id

        # Check if all fields are filled
        if name and phone and email and new_guest_id:
            # Update the guest in the database
            c.execute("UPDATE guests SET guest_id = ?, name = ?, phone = ?, email = ? WHERE guest_id = ?", 
                      (new_guest_id, name, phone, email, old_guest_id))
            conn.commit()
            messagebox.showinfo("Success", "Guest updated successfully")
            clear_guest_entries()
            view_guests()  # Call view_guests() after updating
        else:
            messagebox.showwarning("Input Error", "All fields are required")
    else:
        messagebox.showwarning("Selection Error", "Please select a guest to update")



def delete_guest():
    guest_id = guest_id_entry.get()
    if guest_id:
        c.execute("DELETE FROM guests WHERE guest_id = ?", (guest_id,))
        conn.commit()
        messagebox.showinfo("Success", "Guest deleted successfully")
        clear_guest_entries()
        view_guests()
    else:
        messagebox.showwarning("Input Error", "Guest ID is required")

def view_guests():
    for row in guest_tree.get_children():
        guest_tree.delete(row)
    c.execute("SELECT * FROM guests")
    rows = c.fetchall()
    for i, row in enumerate(rows):
        color = 'lightgrey' if i % 2 == 0 else 'white'
        guest_tree.insert("", tk.END, values=row, tags=('oddrow' if i % 2 == 0 else 'evenrow'), iid=i)

def clear_guest_entries():
    guest_id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Hotel Management System")

# Guest Management Frame
guest_frame = tk.Frame(root)
guest_frame.pack(pady=10)

# Guest Form
tk.Label(guest_frame, text="Guest ID", padx=10, pady=5, fg="blue").grid(row=0, column=0)
guest_id_entry = tk.Entry(guest_frame)
guest_id_entry.grid(row=0, column=1)

tk.Label(guest_frame, text="Name", padx=10, pady=5, fg="blue").grid(row=1, column=0)
name_entry = tk.Entry(guest_frame)
name_entry.grid(row=1, column=1)

tk.Label(guest_frame, text="Phone", padx=10, pady=5, fg="blue").grid(row=2, column=0)
phone_entry = tk.Entry(guest_frame)
phone_entry.grid(row=2, column=1)

tk.Label(guest_frame, text="Email", padx=10, pady=5, fg="blue").grid(row=3, column=0)
email_entry = tk.Entry(guest_frame)
email_entry.grid(row=3, column=1)

# Guest Buttons
tk.Button(guest_frame, text="Add Guest", command=add_guest, bg="green").grid(row=4, column=0, pady=5, padx=5)
tk.Button(guest_frame, text="Update Guest", command=update_guest, bg="blue").grid(row=4, column=1, pady=5, padx=5)
tk.Button(guest_frame, text="Delete Guest", command=delete_guest, bg="red").grid(row=4, column=2, pady=5, padx=5)

# Guest Treeview
guest_tree = ttk.Treeview(root, columns=("ID", "Name", "Phone", "Email"), show="headings")
guest_tree.heading("ID", text="ID", anchor=tk.W)
guest_tree.heading("Name", text="Name", anchor=tk.W)
guest_tree.heading("Phone", text="Phone", anchor=tk.W)
guest_tree.heading("Email", text="Email", anchor=tk.W)
guest_tree.tag_configure('oddrow', foreground='green', background='white')  # Set the text color for odd rows
guest_tree.tag_configure('evenrow', foreground='blue', background='lightgrey')  # Set the text color for even rows
guest_tree.pack(pady=10, padx=10, fill="both")

# Load guest data initially
view_guests()

# Run the application
root.mainloop()

# Close the database connection
conn.close()
