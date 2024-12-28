# Library Management System

## Overview

The **Library Management System** is a Python-based application designed to simplify the management of libraries by automating tasks such as managing readers, books, and borrowing activities. It features a modern graphical user interface (GUI) built using **Tkinter** and styled with **ttkbootstrap**, providing a user-friendly and visually appealing experience. The system uses a relational database for efficient data storage and retrieval.

---

## Features

### **1. Readers Management**

- **Table Structure**:
  - `id`: Unique identifier for each reader.
  - `name`: Full name of the reader.
  - `email`: Email address of the reader.
  - `phone`: Contact number.
  - `card_id`: Unique card number for identification.
  - `max_books`: Maximum number of books a reader can borrow.
- **Functionality**:
  - Add random readers using the `Faker` library for testing purposes.
  - View, search, and update reader information.

### **2. Books Management**

- **Table Structure**:
  - `ID`: Unique identifier for each book.
  - `title`: Title of the book.
  - `Cote`: Book code for easy identification.
  - `status`: Availability status (e.g., Available, Borrowed).
  - `Borrow Count`: Tracks how often the book has been borrowed.
- **Functionality**:
  - Display books using a Treeview widget.
  - Dynamic scrollbars for navigation.
  - Search and filter options to quickly locate books.

### **3. Borrowing Management**

- Tracks borrowing activities using a dedicated `borrowings` table:
  - `reader_id`: ID of the reader borrowing the book.
  - `book_id`: ID of the borrowed book.
  - `borrow_date`: Date the book was borrowed.
  - `due_date`: Due date for returning the book.
  - `status`: Borrowing status (e.g., Borrowed, Returned).
- Ensures data consistency by:
  - Validating reader ID.
  - Checking book availability before confirming a loan.

### **4. GUI Features**

- **Modern Design**: Styled with **ttkbootstrap** for an intuitive user interface.
- **Dynamic Resizing**: Adapts to window size while maintaining layout integrity.
- **Error Handling**: User-friendly error messages for database and input issues.

---

## Technologies Used

- **Programming Language**: Python 3.11+
- **GUI Framework**: Tkinter with ttkbootstrap for styling.
- **Database**: can be adapted to SQLite.
- **Libraries**:
  - `ttkbootstrap`: Enhanced styling for the GUI.
  - `faker`: Generating realistic random data for testing.
  - `sqlite3`: Database connectivity.

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```

2. **Set Up the Environment**:

   - Install Python 3.11+.
   - Install required dependencies:
     ```bash
     pip install ttkbootstrap faker mysql-connector-python
     ```

3. **Run the Application**:

   ```bash
   python main.py
   ```

---

## Usage

1. Launch the application using `main.py`.
2. Navigate through the tabs:
   - **Readers**: Add, view, or manage reader data.
   - **Books**: Browse and manage book inventory.
   - **Borrowings**: Confirm and track borrowing activities.
3. Use the search and filter options for quick data access.

---



## Future Improvements

- Add user authentication for enhanced security.
- Include report generation for borrowing history.
- Implement notifications for overdue books.
- Enhance the search feature with advanced filters.
- fill the statistics tab with useful data analysis.

---

## Contribution

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Commit your changes with descriptive messages.
4. Submit a pull request.


