import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import random
import sqlite3

def create_table():
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS books
                         (id INTEGER PRIMARY KEY,
                          title TEXT,
                          initials TEXT,
                          contact TEXT,
                          borrowal_date TEXT,
                          due_date TEXT,
                          renewed_date TEXT)''')

def add_book():
    book_id = random.randint(1, 1000)
    book_title = book_title_entry.get()
    borrower_initials = borrower_initials_entry.get()
    contact_no = contact_no_entry.get()
    borrowal_date = borrowal_date_entry.get()

    try:
        borrowal_date_obj = datetime.strptime(borrowal_date, "%Y-%m-%d")
        due_date_obj = borrowal_date_obj + timedelta(days=7)
        due_date = due_date_obj.strftime("%Y-%m-%d")
        renewed_date = ""
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid borrowal date in YYYY-MM-DD format.")
        return

    if book_title and borrower_initials and contact_no and borrowal_date:
        book = {
            "id": book_id,
            "title": book_title,
            "initials": borrower_initials,
            "contact": contact_no,
            "borrowal_date": borrowal_date,
            "due_date": due_date,
            "renewed_date": renewed_date
        }
        books.append(book)
        save_book_to_db(book)
        update_book_listbox()
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Please fill in all required fields.")

def update_book():
    selected_book_index = book_listbox.curselection()
    if selected_book_index:
        book_title = book_title_entry.get()
        borrower_initials = borrower_initials_entry.get()
        contact_no = contact_no_entry.get()
        borrowal_date = borrowal_date_entry.get()

        try:
            borrowal_date_obj = datetime.strptime(borrowal_date, "%Y-%m-%d")
            due_date_obj = borrowal_date_obj + timedelta(days=7)
            due_date = due_date_obj.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid borrowal date in YYYY-MM-DD format.")
            return

        if book_title and borrower_initials and contact_no and borrowal_date:
            book = books[selected_book_index[0]]
            book.update({
                "title": book_title,
                "initials": borrower_initials,
                "contact": contact_no,
                "borrowal_date": borrowal_date,
                "due_date": due_date
            })
            update_book_in_db(book)
            update_book_listbox()
            clear_entries()
        else:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
    else:
        messagebox.showwarning("Selection Error", "Please select a book to update.")

def delete_book():
    selected_book_index = book_listbox.curselection()
    if selected_book_index:
        book = books[selected_book_index[0]]
        delete_book_from_db(book['id'])
        del books[selected_book_index[0]]
        update_book_listbox()
    else:
        messagebox.showwarning("Selection Error", "Please select a book to delete.")

def renew_book():
    selected_book_index = book_listbox.curselection()
    if selected_book_index:
        book = books[selected_book_index[0]]
        try:
            due_date_obj = datetime.strptime(book['due_date'], "%Y-%m-%d")
            new_due_date_obj = due_date_obj + timedelta(days=7)
            new_due_date = new_due_date_obj.strftime("%Y-%m-%d")
            book.update({
                "renewed_date": datetime.now().strftime("%Y-%m-%d"),
                "due_date": new_due_date
            })
            update_book_in_db(book)
            update_book_listbox()
            messagebox.showinfo("Renewal Successful", f"Book renewed! New due date: {new_due_date}")
        except ValueError:
            messagebox.showwarning("Date Error", "The due date format is incorrect.")
    else:
        messagebox.showwarning("Selection Error", "Please select a book to renew.")

def update_book_listbox():
    book_listbox.delete(0, tk.END)
    for book in books:
        display_text = (f"ID: {book['id']} | Title: {book['title']} | Initials: {book['initials']} | "
                        f"Contact: {book['contact']} | Borrow Date: {book['borrowal_date']} | Due: {book['due_date']}")
        book_listbox.insert(tk.END, display_text)

def clear_entries():
    book_title_entry.delete(0, tk.END)
    borrower_initials_entry.delete(0, tk.END)
    contact_no_entry.delete(0, tk.END)
    borrowal_date_entry.delete(0, tk.END)

def populate_entries(any):
    selected_book_index = book_listbox.curselection()
    if selected_book_index:
        book = books[selected_book_index[0]]
        book_title_entry.delete(0, tk.END)
        book_title_entry.insert(0, book['title'])
        borrower_initials_entry.delete(0, tk.END)
        borrower_initials_entry.insert(0, book['initials'])
        contact_no_entry.delete(0, tk.END)
        contact_no_entry.insert(0, book['contact'])
        borrowal_date_entry.delete(0, tk.END)
        borrowal_date_entry.insert(0, book['borrowal_date'])

def save_book_to_db(book):
    with conn:
        conn.execute('''INSERT INTO books (id, title, initials, contact, borrowal_date, due_date, renewed_date)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (book['id'], book['title'], book['initials'], book['contact'], book['borrowal_date'], book['due_date'], book['renewed_date']))

def update_book_in_db(book):
    with conn:
        conn.execute('''UPDATE books SET title = ?, initials = ?, contact = ?, borrowal_date = ?, due_date = ?, renewed_date = ?
                         WHERE id = ?''',
                      (book['title'], book['initials'], book['contact'], book['borrowal_date'], book['due_date'], book['renewed_date'], book['id']))

def delete_book_from_db(book_id):
    with conn:
        conn.execute('''DELETE FROM books WHERE id = ?''', (book_id,))

def load_books_from_db():
    with conn:
        cursor = conn.execute('SELECT * FROM books')
        for row in cursor:
            book = {
                "id": row[0],
                "title": row[1],
                "initials": row[2],
                "contact": row[3],
                "borrowal_date": row[4],
                "due_date": row[5],
                "renewed_date": row[6]
            }
            books.append(book)

# Main program
root = tk.Tk()
root.title("Library Book Renewal System")
root.geometry("1000x700")

# Load background image
try:
    bg_image = Image.open("C:/Users/ASUS/Downloads/Designer (4).png")
    bg_image = bg_image.resize((1000, 700), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
except FileNotFoundError:
    messagebox.showerror("File Not Found", "The background image file was not found. Please check the file path.")

# Create a canvas to place the background image
canvas = tk.Canvas(root, width=750, height=500)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Database connection
conn = sqlite3.connect('library.db')

# Book list
books = []

# Book list display
book_listbox = tk.Listbox(root, width=150, height=17)
book_listbox_window = canvas.create_window(500, 480, window=book_listbox)  # Adjusted y-coordinate
def on_listbox_select(any):
    populate_entries(any)

book_listbox.bind("<<ListboxSelect>>", on_listbox_select)

# Create table if not exists
create_table()

# Load books from the database
load_books_from_db()
update_book_listbox()


# GUI elements
title_label = tk.Label(root, text="💠Diamond Library Renewal System💠", font=("Lobster", 24), bg="#ffffff", fg="black")
title_label_window = canvas.create_window(500, 30, window=title_label)

subtitle_label = tk.Label(root, text="Diamonds in the Rough~", font=("Brush Script MT", 16), bg="#ffffff", fg="black")
subtitle_label_window = canvas.create_window(500, 70, window=subtitle_label)

book_title_label = tk.Label(root, text="~💠💠💠~ Book Title:", font=("Arial", 12), bg="#ffffff", fg="black")
book_title_label_window = canvas.create_window(250, 120, window=book_title_label)
book_title_entry = tk.Entry(root, width=30, bg="#ffffff", bd=10, highlightthickness=0)
book_title_entry_window = canvas.create_window(450, 120, window=book_title_entry, anchor="w")

borrower_initials_label = tk.Label(root, text="~💠💠💠~ Borrower's Initials:", font=("Arial", 12), bg="#ffffff", fg="black")
borrower_initials_label_window = canvas.create_window(250, 160, window=borrower_initials_label)
borrower_initials_entry = tk.Entry(root, width=30, bg="#ffffff", bd=10, highlightthickness=0)
borrower_initials_entry_window = canvas.create_window(450, 160, window=borrower_initials_entry, anchor="w")

contact_no_label = tk.Label(root, text="~💠💠💠~ Contact No:", font=("Arial", 12), bg="#ffffff", fg="black")
contact_no_label_window = canvas.create_window(250, 200, window=contact_no_label)
contact_no_entry = tk.Entry(root, width=30, bg="#ffffff", bd=10, highlightthickness=0)
contact_no_entry_window = canvas.create_window(450, 200, window=contact_no_entry, anchor="w")

borrowal_date_label = tk.Label(root, text="~💠💠💠~ Borrowed Date (YYYY-MM-DD):", font=("Arial", 12), bg="#ffffff", fg="black")
borrowal_date_label_window = canvas.create_window(250, 240, window=borrowal_date_label)
borrowal_date_entry = tk.Entry(root, width=30, bg="#ffffff", bd=10, highlightthickness=0)
borrowal_date_entry_window = canvas.create_window(450, 240, window=borrowal_date_entry, anchor="w")

# Button styles
button_style = {
    "font": ("Bradley Hand ITC", 10, "bold"),
    "bg": "#006704",
    "fg": "white",
    "activebackground": "#006704",
    "width": 15,
    "height": 1,
    "bd": 17,
    "relief": "raised"
}

# Buttons
add_button = tk.Button(root, text="Add Book", command=add_book, **button_style)
add_button_window = canvas.create_window(850, 100, window=add_button)

update_button = tk.Button(root, text="Update Book", command=update_book, **button_style)
update_button_window = canvas.create_window(850, 150, window=update_button)

delete_button = tk.Button(root, text="Delete Book", command=delete_book, **button_style)
delete_button_window = canvas.create_window(850, 200, window=delete_button)

renew_button = tk.Button(root, text="Renew Book", command=renew_book, **button_style)
renew_button_window = canvas.create_window(850, 250, window=renew_button)

root.mainloop()
