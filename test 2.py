import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from dbConnection import *

# Create the main window with a Ttkbootstrap theme
root = tkb.Window(themename="superhero",title='Library Management System')  # Choose a theme like "darkly", "flatly", etc.
root.geometry("1100x600+30+30")

def changeTheme(x):
    root.style.theme_use(x)

# Create the Menu Bar
menubar = tkb.Menu(root)

# Create the File Menu
file_menu = tkb.Menu(menubar, tearoff=0)
file_menu.add_command(label="Open", command=lambda: print("Open clicked"))
file_menu.add_command(label="Save", command=lambda: print("Save clicked"))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create the Help Menu
help_menu = tkb.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=lambda: print("About clicked"))

theme_menu = tkb.Menu(menubar,tearoff=0)
themes=(root.style.theme_names())
for theme in themes :
    theme_menu.add_command(label=theme,command=lambda t=theme: changeTheme(t) )


# Add the File and Help Menus to the Menu Bar
menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label='Themes',menu=theme_menu)
menubar.add_cascade(label="Help", menu=help_menu)


root.config(menu=menubar)

# Left frame (Librarian section)
frame_left = tkb.LabelFrame(root, text="Librarian Info", bootstyle="primary")
frame_left.place(relheight=1, relwidth=0.3)

# Right frame 1 (Search bar section)
frame_right1 = tkb.LabelFrame(root, text="Search Section", bootstyle="success")
frame_right1.place(relx=0.3, relheight=0.8, relwidth=0.7)

# --- Tab Control (Notebook) ---
notebook = tkb.Notebook(frame_right1, bootstyle="success")  # Changed parent to frame_right1 and style to match
notebook.place(x=0, y=0, relwidth=1, relheight=1)  # Place at top of frame_right1, adjust height

# --- Tabs ---
tab_books = tkb.Frame(notebook)
tab_readers = tkb.Frame(notebook)
tab_statistics = tkb.Frame(notebook)

notebook.add(tab_books, text="Books")
notebook.add(tab_readers, text="Readers")
notebook.add(tab_statistics, text="Statistics")

# Right frame 2 (Footer or additional controls)
frame_right2 = tkb.LabelFrame(root, text="Footer Section", bootstyle="info")
frame_right2.place(rely=0.8, relx=0.3, relheight=0.2, relwidth=0.7)


# Function to change librarian (placeholder functionality)
def changeLib():
    tkb.Toplevel(frame_left).mainloop()

def verify_reader(card_id_entry, reader_name_label):
    """Verify reader details by card ID and display the reader's name."""
    card_id = card_id_entry.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM readers WHERE card_number=%s", (card_id,))
        result = cursor.fetchone()
        if result:
            reader_name_label.config(text=result[0])
        else:
            reader_name_label.config(text="Reader not found")
    except Exception as e:
        print(f"Error verifying reader: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def verify_book(book_id_entry, book_title_label):
    """Verify book details by book ID and display the book's title."""
    book_id = book_id_entry.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM books WHERE book_id=%s AND available_copies > 0", (book_id,))
        result = cursor.fetchone()
        if result:
            book_title_label.config(text=result[0])
        else:
            book_title_label.config(text="Book not available")
    except Exception as e:
        print(f"Error verifying book: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()



def confirm_loan(card_id_entry, book_id_entry):
    """Confirm the loan and update the database."""
    card_id = card_id_entry.get()
    book_id = book_id_entry.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO borrowings (reader_id, book_id, borrow_date, due_date, status) "
                       "VALUES ((SELECT reader_id FROM readers WHERE card_number=%s), %s, NOW(), DATE_ADD(NOW(), INTERVAL 14 DAY), 'Borrowed')",
                       (card_id, book_id))
        cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id=%s", (book_id,))
        conn.commit()
        print("Loan successfully added.")
    except Exception as e:
        print(f"Error confirming loan: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()



def reservation():
    """Toplevel window to handle book reservations."""
    top = tkb.Toplevel(title="Reserve Book")
    top.geometry("400x400")
    top.resizable(False, False)

    # Labels and Entries
    tkb.Label(top, text="Card ID (Reader):").place(x=20, y=20)
    card_id_entry = tkb.Entry(top)
    card_id_entry.place(x=150, y=20, width=200)

    tkb.Label(top, text="Reader Name:").place(x=20, y=70)
    reader_name_label = tkb.Label(top, text="", relief="solid", font=("arial", 14), borderwidth=5)
    reader_name_label.place(x=150, y=70, width=200)

    tkb.Label(top, text="Book ID:").place(x=20, y=140)
    book_id_entry = tkb.Entry(top)
    book_id_entry.place(x=150, y=140, width=200)

    tkb.Label(top, text="Book Title:").place(x=20, y=190)
    book_title_label = tkb.Label(top, text="", relief="solid", font=("arial", 14), borderwidth=5)
    book_title_label.place(x=150, y=190, width=200)

    # Verify buttons
    tkb.Button(top, text="Verify Reader", style="outline-secondary", 
               command=lambda: verify_reader(card_id_entry, reader_name_label)).place(x=20, y=100)
    tkb.Button(top, text="Verify Book", style="outline-secondary", 
               command=lambda: verify_book(book_id_entry, book_title_label)).place(x=20, y=220)

    # Confirm and Cancel Buttons
    tkb.Button(top, text="Confirm", style="outline-primary", 
               command=lambda: confirm_reservation(card_id_entry, book_id_entry)).place(x=50, y=300)
    tkb.Button(top, text="Cancel", style="outline-secondary", command=top.destroy).place(x=200, y=300)

def confirm_reservation(card_id_entry, book_id_entry):
    """Confirm the reservation and update the database."""
    card_id = card_id_entry.get()
    book_id = book_id_entry.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reservations (reader_id, book_id, reservation_date, status) "
                       "VALUES ((SELECT reader_id FROM readers WHERE card_number=%s), %s, NOW(), 'Active')",
                       (card_id, book_id))
        conn.commit()
        print("Reservation successfully added.")
    except Exception as e:
        print(f"Error confirming reservation: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def loan():
    """Toplevel window to handle book loans."""
    top = tkb.Toplevel(title="Add Loan")
    top.geometry("400x400")
    top.resizable(False, False)

    # Labels and Entries
    tkb.Label(top, text="Card ID (Reader):").place(x=20, y=20)
    card_id_entry = tkb.Entry(top)
    card_id_entry.place(x=150, y=20, width=200)

    tkb.Label(top, text="Reader Name:").place(x=20, y=70)
    reader_name_label = tkb.Label(top, text="", relief="solid", font=("arial", 14), borderwidth=5)
    reader_name_label.place(x=150, y=70, width=200)

    tkb.Label(top, text="Book ID:").place(x=20, y=140)
    book_id_entry = tkb.Entry(top)
    book_id_entry.place(x=150, y=140, width=200)

    tkb.Label(top, text="Book Title:").place(x=20, y=190)
    book_title_label = tkb.Label(top, text="", relief="solid", font=("arial", 14), borderwidth=5)
    book_title_label.place(x=150, y=190, width=200)

    # Verify buttons
    tkb.Button(top, text="Verify Reader", style="outline-secondary", 
               command=lambda: verify_reader(card_id_entry, reader_name_label)).place(x=20, y=100)
    tkb.Button(top, text="Verify Book", style="outline-secondary", 
               command=lambda: verify_book(book_id_entry, book_title_label)).place(x=20, y=220)

    # Confirm and Cancel Buttons
    tkb.Button(top, text="Confirm", style="outline-primary", 
               command=lambda: confirm_loan(card_id_entry, book_id_entry)).place(x=50, y=300)
    tkb.Button(top, text="Cancel", style="outline-secondary", command=top.destroy).place(x=200, y=300)

def book_return():
    """Toplevel window to handle book returns."""
    top = tkb.Toplevel(title="Return Book")
    top.geometry("400x300")
    top.resizable(False, False)

    # Labels and Entries
    tkb.Label(top, text="Borrowing ID:").place(x=20, y=20)
    borrowing_id_entry = tkb.Entry(top)
    borrowing_id_entry.place(x=150, y=20, width=200)

    # Action Buttons
    tkb.Button(top, text="Return", style="outline-primary", command=lambda: return_book_entry(borrowing_id_entry)).place(x=50, y=200)
    tkb.Button(top, text="Cancel", style="outline-secondary", command=top.destroy).place(x=200, y=200)

def return_book_entry(borrowing_id_entry):
    """Function to mark a book as returned."""
    borrowing_id = borrowing_id_entry.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE borrowings SET return_date=NOW(), status='Returned' WHERE borrowing_id=%s
        """, (borrowing_id,))
        conn.commit()
        print("Book return processed successfully.")
    except Exception as e:
        print(f"Error returning book: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


# Librarian Information Labels and Button
labelLibrarian = tkb.Label(
    frame_left,
    text="Librarian in Charge:",
    anchor="w",
    font=("TkDefaultFont", 12),
    padding=3
)
labelLibrarian.place(relx=0.1, rely=0.05)

labelLibrarianName = tkb.Label(
    frame_left,
    text="John Doe",  # Replace with the actual librarian name
    anchor="w",
    font=("Arial", 18),
    borderwidth=3,
    relief="groove",
    padding=15
)
labelLibrarianName.place(relx=0.1, rely=0.1)

# Change Librarian Button
librarianButton = tkb.Button(
    frame_left,
    text="Change Librarian",
    bootstyle="outline-primary",
    padding=5,
    command=changeLib
)
librarianButton.place(relx=0.2, y=140)

# Additional Feature: Statistics on Left Frame
stats_label = tkb.Label(
    frame_left,
    text="Statistics:",
    anchor="w",
    font=("TkDefaultFont", 12),
    padding=3
)
stats_label.place(relx=0.1, y=200)

most_borrowed_label = tkb.Label(
    frame_left,
    text="Most Borrowed Book: XYZ",
    anchor="w",
    font=("TkDefaultFont", 10),
    padding=3
)
most_borrowed_label = tkb.Label(
    frame_left,
    text="Most Borrowed Book: XYZ",  # Replace 'XYZ' dynamically with query results
    anchor="w",
    font=("TkDefaultFont", 10),
    padding=3
)
most_borrowed_label.place(relx=0.1, y=230)

penalized_readers_label = tkb.Label(
    frame_left,
    text="Penalized Readers: 5",  # Replace '5' dynamically with query results
    anchor="w",
    font=("TkDefaultFont", 10),
    padding=3
)
penalized_readers_label.place(relx=0.1, y=260)

# Additional Stats Queries
def update_stats():
    """Update statistics dynamically on the left frame."""
    try:
        conn = getConnection()
        cursor = conn.cursor()

        # Query for most borrowed book
        cursor.execute("""
            SELECT title FROM books 
            WHERE book_id = (SELECT book_id FROM borrowings GROUP BY book_id ORDER BY COUNT(*) DESC LIMIT 1)
        """)
        most_borrowed = cursor.fetchone()
        most_borrowed_label.config(text=f"Most Borrowed Book: {most_borrowed[0]}" if most_borrowed else "Most Borrowed Book: N/A")

        # Query for penalized readers count
        cursor.execute("SELECT COUNT(*) FROM penalties WHERE penalty_status = 'Unpaid'")
        penalized_count = cursor.fetchone()
        penalized_readers_label.config(text=f"Penalized Readers: {penalized_count[0]}")

    except Exception as e:
        print(f"Error updating stats: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Call the update_stats function to populate the statistics when the app starts
update_stats()







# Search Bar in Right Frame 1
searchbar = tkb.Entry(tab_books, width=73, bootstyle="info")
searchbar.place(x=20, y=20 , relwidth=0.9)


def search_books():
    """Searches for books based on the query in the search bar."""
    query = searchbar.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        # Example query (adjust to your needs):
        cursor.execute(f"""
            SELECT book_id, title, cote, status, borrow_count 
            FROM books 
            WHERE title LIKE '%{query}%' OR cote LIKE '%{query}%'
        """)
        rows = cursor.fetchall()

        # Clear existing data and insert filtered data
        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            tree.insert("", "end", values=row)

    except Exception as e:
        print(f"Error searching books: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

searchbar.bind("<Return>", lambda event: search_books())


#creating the treeview for the books
tree = tkb.Treeview(tab_books, columns=("ID", "title", "Cote" ,"status" , "Borrow count"  ), show="headings", bootstyle="info")
tree.place(x=20 , y= 80 , relwidth= 0.95)

tree.heading("ID", text="ID")
tree.heading("title", text="Title")
tree.heading("Cote", text="Cote")
tree.heading("status", text="status")
tree.heading("Borrow count", text="Borrow Count")
tree.column("ID", width=70, anchor="center")
tree.column("title", width=200, anchor="w")
tree.column("Cote", width=70,)
tree.column("status", width=100)
tree.column("Borrow count", width=70)



# Creating the search bar for the Readers tab
reader_searchbar = tkb.Entry(tab_readers, width=73, bootstyle="info")
reader_searchbar.place(x=20, y=20, relwidth=0.9)

def search_readers():
    """Searches for readers based on the query in the search bar."""
    query = reader_searchbar.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        # Example query (adjust to your needs):
        cursor.execute(f"""
            SELECT reader_id, name, email, phone, max_books_to_borrow 
            FROM readers 
            WHERE name LIKE '%{query}%' OR email LIKE '%{query}%'
        """)
        rows = cursor.fetchall()

        # Clear existing data and insert filtered data
        for item in reader_tree.get_children():
            reader_tree.delete(item)
        for row in rows:
            reader_tree.insert("", "end", values=row)

    except Exception as e:
        print(f"Error searching readers: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

reader_searchbar.bind("<Return>", lambda event: search_readers())

# Creating the treeview for the Readers tab
reader_tree = tkb.Treeview(tab_readers, columns=("ID", "Name", "Email", "Phone", "Max Books"), show="headings", bootstyle="info")
reader_tree.place(x=20, y=80, relwidth=0.95)

reader_tree.heading("ID", text="ID")
reader_tree.heading("Name", text="Name")
reader_tree.heading("Email", text="Email")
reader_tree.heading("Phone", text="Phone")
reader_tree.heading("Max Books", text="Max Books")
reader_tree.column("ID", width=70, anchor="center")
reader_tree.column("Name", width=150, anchor="w")
reader_tree.column("Email", width=200, anchor="w")
reader_tree.column("Phone", width=120, anchor="center")
reader_tree.column("Max Books", width=100, anchor="center")



def edit_reader_window():
    """Toplevel window to edit an existing reader."""
    top = tkb.Toplevel(title="Edit Reader")
    top.geometry("400x400")
    top.resizable(False, False)

    # Labels and Entries
    tkb.Label(top, text="Reader ID:").place(x=20, y=20)
    reader_id_entry = tkb.Entry(top)
    reader_id_entry.place(x=120, y=20, width=200)

    tkb.Label(top, text="Name:").place(x=20, y=70)
    name_entry = tkb.Entry(top)
    name_entry.place(x=120, y=70, width=200)

    tkb.Label(top, text="Email:").place(x=20, y=120)
    email_entry = tkb.Entry(top)
    email_entry.place(x=120, y=120, width=200)

    tkb.Label(top, text="Phone:").place(x=20, y=170)
    phone_entry = tkb.Entry(top)
    phone_entry.place(x=120, y=170, width=200)

    tkb.Label(top, text="Max Books:").place(x=20, y=220)
    max_books_entry = tkb.Entry(top)
    max_books_entry.place(x=120, y=220, width=200)

    # Action Buttons
    tkb.Button(top, text="Save", style="outline-primary", command=lambda: edit_reader(reader_id_entry, name_entry, email_entry, phone_entry, max_books_entry)).place(x=50, y=300)
    tkb.Button(top, text="Cancel", style="outline-secondary", command=top.destroy).place(x=200, y=300)

def edit_reader(reader_id_entry, name_entry, email_entry, phone_entry, max_books_entry):
    """Function to update the reader's details in the database."""
    reader_id = reader_id_entry.get()
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    max_books = max_books_entry.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE readers SET name=%s, email=%s, phone=%s, max_books_to_borrow=%s WHERE reader_id=%s
        """, (name, email, phone, max_books, reader_id))
        conn.commit()
        print("Reader updated successfully.")
    except Exception as e:
        print(f"Error updating reader: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()



def add_reader_window():
    """Toplevel window to add a new reader."""
    top = tkb.Toplevel(title="Add Reader")
    top.geometry("400x400")
    top.resizable(False, False)

    # Labels and Entries
    tkb.Label(top, text="Name:").place(x=20, y=20)
    name_entry = tkb.Entry(top)
    name_entry.place(x=120, y=20, width=200)

    tkb.Label(top, text="Email:").place(x=20, y=70)
    email_entry = tkb.Entry(top)
    email_entry.place(x=120, y=70, width=200)

    tkb.Label(top, text="Phone:").place(x=20, y=120)
    phone_entry = tkb.Entry(top)
    phone_entry.place(x=120, y=120, width=200)

    tkb.Label(top, text="Max Books:").place(x=20, y=170)
    max_books_entry = tkb.Entry(top)
    max_books_entry.place(x=120, y=170, width=200)

    # Action Buttons
    tkb.Button(top, text="Add", style="outline-primary", command=lambda: add_reader(name_entry, email_entry, phone_entry, max_books_entry)).place(x=50, y=300)
    tkb.Button(top, text="Cancel", style="outline-secondary", command=top.destroy).place(x=200, y=300)

def add_reader(name_entry, email_entry, phone_entry, max_books_entry):
    """Function to insert the reader into the database."""
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    max_books = max_books_entry.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO readers (name, email, phone, max_books_to_borrow) VALUES (%s, %s, %s, %s)", 
                       (name, email, phone, max_books))
        conn.commit()
        print("Reader added successfully.")
    except Exception as e:
        print(f"Error adding reader: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()



def delete_reader_window():
    """Toplevel window to delete a reader."""
    top = tkb.Toplevel(title="Delete Reader")
    top.geometry("300x200")
    top.resizable(False, False)

    # Labels and Entries
    tkb.Label(top, text="Reader ID:").place(x=20, y=50)
    reader_id_entry = tkb.Entry(top)
    reader_id_entry.place(x=120, y=50, width=150)

    # Action Buttons
    tkb.Button(top, text="Delete", style="outline-primary", command=lambda: delete_reader(reader_id_entry)).place(x=50, y=120)
    tkb.Button(top, text="Cancel", style="outline-secondary", command=top.destroy).place(x=150, y=120)

def delete_reader(reader_id_entry):
    """Function to delete a reader from the database."""
    reader_id = reader_id_entry.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM readers WHERE reader_id=%s", (reader_id,))
        conn.commit()
        print("Reader deleted successfully.")
    except Exception as e:
        print(f"Error deleting reader: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()



# Adding necessary buttons for the Readers tab
add_reader = tkb.Button(tab_readers, text='Add Reader', style='outline-primary', command=add_reader_window)
add_reader.place(x=30, y=330)

edit_reader = tkb.Button(tab_readers, text='Edit Reader', style='outline-primary', command=edit_reader_window)
edit_reader.place(x=150, y=330)

delete_reader = tkb.Button(tab_readers, text='Delete Reader', style='outline-primary', command=delete_reader_window)
delete_reader.place(x=285, y=330)

#adding necessary buttons
add_loan = tkb.Button(tab_books,text='Add Loan',command=loan,style='outline-primary')
add_loan.place(x=30,y=330)
return_book = tkb.Button(tab_books,text='Return Book',command=book_return,style='outline-primary')
return_book.place(x=150,y=330)
reservation_button = tkb.Button(tab_books,text='Reserve Book',command=reservation,style='outline-primary')
reservation_button.place(x=285,y=330)



root.mainloop()
