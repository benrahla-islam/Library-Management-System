# import tkinter as tk
import time 
import ttkbootstrap as tkb
from ttkbootstrap.dialogs import Messagebox
from dbConnection import getConnection , verify_and_create_tables
import sqlite3 as db
# Create the main window with a Ttkbootstrap theme
root = tkb.Window(title='Library Management System')
root.geometry("1100x600+30+30")

verify_and_create_tables()

def ErrorMessage (ErrorText):
    Messagebox.show_error(
        title='ERROR',
        message= ErrorText
    )

def changeTheme(x):
    root.style.theme_use(x)

def changeLib():
    pass


# System Actions Section
def logout():
    """Handle logout functionality"""
    if Messagebox.show_question("Logout", "Are you sure you want to logout?"):
        root.quit()  # Or implement your specific logout logic



def update_time():
    """Update the time display"""
    current_time = time.strftime('%H:%M:%S')
    current_date = time.strftime('%Y-%m-%d')
    time_label.config(text=f"Date: {current_date}\nTime: {current_time}")
    root.after(1000, update_time)  # Update every second




def verify_reader(card_id_entry, reader_name_label):
    """Verify reader details by card ID and display the reader's name."""
    card_id = card_id_entry.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM readers WHERE reader_id=?", (card_id,))
        result = cursor.fetchone()
        if result:
            reader_name_label.config(text=result[0])
        else:
            reader_name_label.config(text="Reader not found")
    except db.Error as e:
        ErrorMessage(f"Error verifying reader: {e}")
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
        cursor.execute("SELECT title FROM books WHERE book_id=? AND available_copies > 0", (book_id,))
        result = cursor.fetchone()
        if result:
            book_title_label.config(text=result[0])
        else:
            book_title_label.config(text="Book not available")
    except db.Error as e:
        ErrorMessage(f"Error verifying book: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def confirm_loan(card_id_entry, book_id_entry):
    """Confirm the loan and update the database."""
    reader_id = card_id_entry.get().strip()
    book_id = book_id_entry.get().strip()

    try:
        conn = getConnection()
        cursor = conn.cursor()

        # Check if the reader exists
        cursor.execute("SELECT reader_id FROM readers WHERE reader_id = ?", (reader_id,))
        reader = cursor.fetchone()
        if not reader:
            ErrorMessage("Reader not found. Please check the Card ID.")
            return

        # Check if the book exists
        cursor.execute("SELECT title  FROM books WHERE book_id = ? AND status = 'Available'", (book_id,))
        book = cursor.fetchone()
        if not book:
            ErrorMessage("Book not found or not available. Please check the Book ID.")
            return

        # Proceed to add a borrowing record
        cursor.execute("""
            INSERT INTO borrowings (reader_id, book_id, borrow_date, due_date, status)
            VALUES (?, ?, DATE('now'), DATE('now', '+14 days'), 'Borrowed')
        """, (reader[0], book_id))

        # Update book's available copies
        cursor.execute("UPDATE books SET status = 'unavailable' WHERE book_id = ?", (book_id,))
        conn.commit()

        Messagebox.show_info(f"Loan successfully added for the book '{book[0]}'.")
    
    except Exception as e:
        ErrorMessage(f"Error confirming loan: {e}")
    
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
    except db.Error as e:
        ErrorMessage(f"Error confirming reservation: {e}")
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
    tkb.Label(top, text="Reader ID (Reader):").place(x=20, y=20)
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
    except db.Error as e:
        ErrorMessage(f"Error returning book: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()



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

    except db.Error as e:
        ErrorMessage(f"Error searching readers: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def edit_reader():
    """Function to update the reader's details in the database."""
    reader_id = root.reader_id_entry.get()
    name = root.name_entry.get()
    email = root.email_entry.get()
    phone = root.phone_entry.get()
    max_books = root.max_books_entry.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE readers SET name=%s, email=%s, phone=%s, max_books_to_borrow=%s WHERE reader_id=%s
        """, (name, email, phone, max_books, reader_id))
        conn.commit()
        print("Reader updated successfully.")
    except db.Error as e:
        ErrorMessage(f"Error updating reader: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

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
    tkb.Button(top, text="Save", style="outline-primary", command=edit_reader).place(x=50, y=300)
    tkb.Button(top, text="Cancel", style="outline-secondary", command=top.destroy).place(x=200, y=300)




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
    tkb.Button(top, text="Add", style="outline-primary", command=add_reader).place(x=50, y=300)
    tkb.Button(top, text="Cancel", style="outline-secondary", command=top.destroy).place(x=200, y=300)

def add_reader():
    """Function to insert the reader into the database."""
    name = root.name_entry.get()
    email = root.email_entry.get()
    phone = root.phone_entry.get()
    max_books = root.max_books_entry.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO readers (name, email, phone, max_books_to_borrow) VALUES (%s, %s, %s, %s)", 
                       (name, email, phone, max_books))
        conn.commit()
        print("Reader added successfully.")
    except db.Error as e:
        ErrorMessage(f"Error adding reader: {e}")
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
    tkb.Button(top, text="Delete", style="outline-primary", command=delete_reader).place(x=50, y=120)
    tkb.Button(top, text="Cancel", style="outline-secondary", command=top.destroy).place(x=150, y=120)

def delete_reader():
    """Function to delete a reader from the database."""
    reader_id = root.reader_id_entry.get()
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM readers WHERE reader_id=%s", (reader_id,))
        conn.commit()
        print("Reader deleted successfully.")
    except db.Error as e:
        ErrorMessage(f"Error deleting reader: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


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
themes=root.style.theme_names()
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
    command=changeLib()
)
librarianButton.place(relx=0.2, rely=0.25)

# Add a separator
separator = tkb.Separator(frame_left, bootstyle="info")
separator.place(relx=0.05, rely=0.35, relwidth=0.9)

# Quick Actions Section
quick_actions_label = tkb.Label(
    frame_left,
    text="Quick Actions",
    font=("TkDefaultFont", 12, "bold"),
    padding=3
)
quick_actions_label.place(relx=0.1, rely=0.4)

# Quick Action Buttons
quick_loan = tkb.Button(
    frame_left,
    text="Quick Loan",
    bootstyle="success-outline",
    padding=5,
    command=loan
)
quick_loan.place(relx=0.1, rely=0.47, relwidth=0.8)

quick_return = tkb.Button(
    frame_left,
    text="Quick Return",
    bootstyle="warning-outline",
    padding=5,
    command=book_return
)
quick_return.place(relx=0.1, rely=0.55, relwidth=0.8)

quick_reserve = tkb.Button(
    frame_left,
    text="Quick Reserve",
    bootstyle="info-outline",
    padding=5,
    command=reservation
)
quick_reserve.place(relx=0.1, rely=0.63, relwidth=0.8)

# Add another separator
separator2 = tkb.Separator(frame_left, bootstyle="info")
separator2.place(relx=0.05, rely=0.75, relwidth=0.9)



# Time and Date Display
time_label = tkb.Label(
    frame_left,
    text="",
    font=("TkDefaultFont", 10),
    padding=3
)
time_label.place(relx=0.1, rely=0.8)



# Start the time update
update_time()

# Logout Button
logout_btn = tkb.Button(
    frame_left,
    text="Logout",
    bootstyle="danger-outline",
    padding=5,
    command=logout
)
logout_btn.place(relx=0.1, rely=0.9, relwidth=0.8)




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

    except db.Error as e:
        ErrorMessage(f"Error searching books: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

searchbar.bind("<Return>", lambda event: search_books())


#creating the treeview for the books
tree = tkb.Treeview(tab_books, columns=("ID", "title", "Cote" ,"status" , "Borrow count"  ), show="headings", bootstyle="info")
tree.place(x=20 , y= 80 , relwidth= 0.95,relheight=0.68)

v_scroll = tkb.Scrollbar(tab_books, orient="vertical", command=tree.yview)
v_scroll.place(relx=0.965, y=80, relheight=0.68)  # Adjust relx and y to align with the treeview
tree.configure(yscrollcommand=v_scroll.set)

tree.heading("ID", text="ID",)
tree.heading("title", text="Title")
tree.heading("Cote", text="Cote")
tree.heading("status", text="status")
tree.heading("Borrow count", text="Borrow Count")
tree.column("ID", width=70, anchor="center")
tree.column("title", width=200, anchor="w")
tree.column("Cote", width=70,)
tree.column("status", width=100)
tree.column("Borrow count", width=70)


def populate_books_treeview():
    """Populates the books Treeview with data from the books table."""
    try:
        conn = getConnection()  # Assuming getConnection() returns a sqlite3 connection
        cursor = conn.cursor()

        cursor.execute("SELECT book_id, title, cote, status, borrow_count FROM books")
        rows = cursor.fetchall()

        # Clear existing data in the Treeview
        tree.delete(*tree.get_children())

        # Insert new data into the Treeview
        for row in rows:
            tree.insert("", "end", values=row)

    except db.Error as e:
        ErrorMessage(f"Error populating books Treeview: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

populate_books_treeview()


# Creating the search bar for the Readers tab
reader_searchbar = tkb.Entry(tab_readers, width=73, bootstyle="info")
reader_searchbar.place(x=20, y=20, relwidth=0.9)



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

def populate_readers_treeview():
    """Populates the readers Treeview with data from the readers table."""
    try:
        conn = getConnection()
        cursor = conn.cursor()

        cursor.execute("SELECT reader_id, name, email, phone, max_books_to_borrow FROM readers")
        rows = cursor.fetchall()

        # Clear existing data in the Treeview
        reader_tree.delete(*reader_tree.get_children())

        # Insert new data into the Treeview
        for row in rows:
            reader_tree.insert("", "end", values=row)

    except db.Error as e:
        ErrorMessage(f"Error populating readers Treeview: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

populate_readers_treeview()


# Adding necessary buttons for the Readers tab
add_reader = tkb.Button(tab_readers, text='Add Reader', style='outline-primary', command=add_reader_window)
add_reader.place(x=30, y=330)

edit_reader = tkb.Button(tab_readers, text='Edit Reader', style='outline-primary', command=edit_reader_window)
edit_reader.place(x=150, y=330)

delete_reader = tkb.Button(
    tab_readers,
    text='Delete Reader',
    style='outline-primary',
    command=delete_reader_window)
delete_reader.place(x=285, y=330)

#adding necessary buttons
add_loan = tkb.Button(tab_books,text='Add Loan',command=loan,style='outline-primary')
add_loan.place(x=30,y=-50,rely=1.0)
return_book = tkb.Button(tab_books,text='Return Book',command=book_return,style='outline-primary')
return_book.place(rely= 1.0,x=150,y=-50)



root.mainloop()
