
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import random

class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Book Renewal System")
        self.root.geometry("1000x700")

        # Load background image
        try:
            self.bg_image = Image.open("C:/Users/ASUS/Downloads/Designer (4).png")
            self.bg_image = self.bg_image.resize((1000, 700), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "The background image file was not found. Please check the file path.")

        # Create a canvas to place the background image
        self.canvas = tk.Canvas(self.root, width=750, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Book list
        self.books = []

        # GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(self.root, text="💠Diamond Library Renewal System💠", font=("Lobster", 24), bg="#ffffff", fg="black")
        self.title_label_window = self.canvas.create_window(500, 30, window=self.title_label)

        # Subtitle label
        self.subtitle_label = tk.Label(self.root, text="Diamonds in the Rough~", font=("Brush Script MT", 16), bg="#ffffff", fg="black")
        self.subtitle_label_window = self.canvas.create_window(500, 70, window=self.subtitle_label)

        # Book title entry
        self.book_title_label = tk.Label(self.root, text="~💠💠💠~ Book Title:", font=("Arial", 12), bg="#ffffff", fg="black")
        self.book_title_label_window = self.canvas.create_window(250, 120, window=self.book_title_label)
        self.book_title_entry = tk.Entry(self.root, width=30, bg="#ffffff", bd=10, highlightthickness=0)
        self.book_title_entry_window = self.canvas.create_window(450, 120, window=self.book_title_entry, anchor="w")

        # Borrower's initials entry
        self.borrower_initials_label = tk.Label(self.root, text="~💠💠💠~ Borrower's Initials:", font=("Arial", 12), bg="#ffffff", fg="black")
        self.borrower_initials_label_window = self.canvas.create_window(250, 160, window=self.borrower_initials_label)
        self.borrower_initials_entry = tk.Entry(self.root, width=30, bg="#ffffff", bd=10, highlightthickness=0)
        self.borrower_initials_entry_window = self.canvas.create_window(450, 160, window=self.borrower_initials_entry, anchor="w")

        # Borrower's contact number entry
        self.contact_no_label = tk.Label(self.root, text="~💠💠💠~ Contact No:", font=("Arial", 12), bg="#ffffff", fg="black")
        self.contact_no_label_window = self.canvas.create_window(250, 200, window=self.contact_no_label)
        self.contact_no_entry = tk.Entry(self.root, width=30, bg="#ffffff", bd=10, highlightthickness=0)
        self.contact_no_entry_window = self.canvas.create_window(450, 200, window=self.contact_no_entry, anchor="w")

        # Borrowal date entry
        self.borrowal_date_label = tk.Label(self.root, text="~💠💠💠~ Borrowed Date (YYYY-MM-DD):", font=("Arial", 12), bg="#ffffff", fg="black")
        self.borrowal_date_label_window = self.canvas.create_window(250, 240, window=self.borrowal_date_label)
        self.borrowal_date_entry = tk.Entry(self.root, width=30, bg="#ffffff", bd=10, highlightthickness=0)
        self.borrowal_date_entry_window = self.canvas.create_window(450, 240, window=self.borrowal_date_entry, anchor="w")

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
        self.add_button = tk.Button(self.root, text="Add Book", command=self.add_book, **button_style)
        self.add_button_window = self.canvas.create_window(850, 100, window=self.add_button)

        self.update_button = tk.Button(self.root, text="Update Book", command=self.update_book, **button_style)
        self.update_button_window = self.canvas.create_window(850, 150, window=self.update_button)

        self.delete_button = tk.Button(self.root, text="Delete Book", command=self.delete_book, **button_style)
        self.delete_button_window = self.canvas.create_window(850, 200, window=self.delete_button)

        self.renew_button = tk.Button(self.root, text="Renew Book", command=self.renew_book, **button_style)
        self.renew_button_window = self.canvas.create_window(850, 250, window=self.renew_button)

        # Book list display
        self.book_listbox = tk.Listbox(self.root, width=150, height=17)
        self.book_listbox_window = self.canvas.create_window(500, 480, window=self.book_listbox)  # Adjusted y-coordinate
        self.book_listbox.bind("<<ListboxSelect>>", self.populate_entries)

    def add_book(self):
        book_id = random.randint(1, 1000)
        book_title = self.book_title_entry.get()
        borrower_initials = self.borrower_initials_entry.get()
        contact_no = self.contact_no_entry.get()
        borrowal_date = self.borrowal_date_entry.get()

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
            self.books.append(book)
            self.update_book_listbox()
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")

    def update_book(self):
        selected_book_index = self.book_listbox.curselection()
        if selected_book_index:
            book_title = self.book_title_entry.get()
            borrower_initials = self.borrower_initials_entry.get()
            contact_no = self.contact_no_entry.get()
            borrowal_date = self.borrowal_date_entry.get()

            try:
                borrowal_date_obj = datetime.strptime(borrowal_date, "%Y-%m-%d")
                due_date_obj = borrowal_date_obj + timedelta(days=7)
                due_date = due_date_obj.strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid borrowal date in YYYY-MM-DD format.")
                return

            if book_title and borrower_initials and contact_no and borrowal_date:
                book = self.books[selected_book_index[0]]
                book.update({
                    "title": book_title,
                    "initials": borrower_initials,
                    "contact": contact_no,
                    "borrowal_date": borrowal_date,
                    "due_date": due_date
                })
                self.update_book_listbox()
                self.clear_entries()
            else:
                messagebox.showwarning("Input Error", "Please fill in all required fields.")
        else:
            messagebox.showwarning("Selection Error", "Please select a book to update.")

    def delete_book(self):
        selected_book_index = self.book_listbox.curselection()
        if selected_book_index:
            del self.books[selected_book_index[0]]
            self.update_book_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a book to delete.")

    def renew_book(self):
        selected_book_index = self.book_listbox.curselection()
        if selected_book_index:
            book = self.books[selected_book_index[0]]
            try:
                due_date_obj = datetime.strptime(book['due_date'], "%Y-%m-%d")
                new_due_date_obj = due_date_obj + timedelta(days=7)
                new_due_date = new_due_date_obj.strftime("%Y-%m-%d")
                book.update({
                    "renewed_date": datetime.now().strftime("%Y-%m-%d"),
                    "due_date": new_due_date
                })
                self.update_book_listbox()
                messagebox.showinfo("Renewal Successful", f"Book renewed! New due date: {new_due_date}")
            except ValueError:
                messagebox.showwarning("Date Error", "The due date format is incorrect.")
        else:
            messagebox.showwarning("Selection Error", "Please select a book to renew.")

    def update_book_listbox(self):
        self.book_listbox.delete(0, tk.END)
        for book in self.books:
            display_text = (f"ID: {book['id']} | Title: {book['title']} | Initials: {book['initials']} | "
                            f"Contact: {book['contact']} | Borrow Date: {book['borrowal_date']} | Due: {book['due_date']}")
            self.book_listbox.insert(tk.END, display_text)

    def clear_entries(self):
        self.book_title_entry.delete(0, tk.END)
        self.borrower_initials_entry.delete(0, tk.END)
        self.contact_no_entry.delete(0, tk.END)
        self.borrowal_date_entry.delete(0, tk.END)

    def populate_entries(self, event):
        selected_book_index = self.book_listbox.curselection()
        if selected_book_index:
            book = self.books[selected_book_index[0]]
            self.book_title_entry.delete(0, tk.END)
            self.book_title_entry.insert(0, book['title'])
            self.borrower_initials_entry.delete(0, tk.END)
            self.borrower_initials_entry.insert(0, book['initials'])
            self.contact_no_entry.delete(0, tk.END)
            self.contact_no_entry.insert(0, book['contact'])
            self.borrowal_date_entry.delete(0, tk.END)
            self.borrowal_date_entry.insert(0, book['borrowal_date'])

if __name__ == "__main__":
    root = tk.Tk()
    app = LibrarySystem(root)
    root.mainloop()