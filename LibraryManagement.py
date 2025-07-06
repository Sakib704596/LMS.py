from tkinter import *
import mysql.connector
import tkinter.messagebox as sms
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="S@kib2005",
    database="Library_database"
)
curr=conn.cursor()
conn.commit()
root = Tk()
root.geometry("700x600")
root.title("Library Management System")
root.config(bg="#f4f4f4")
Label(root, text="📚 College Library Management System!!",
      font="TimesNewRoman 18 bold italic", fg="black", bg="#f4f4f4").pack(pady=20)
def Add():
    open_window=Toplevel(root)
    open_window.title("Add New Book")
    open_window.geometry("250x250")
    L1=Label(open_window,text="Book_Id:")
    L1.grid(row=0,column=0)
    id=Entry(open_window)
    id.grid(row=0,column=1)
    L2=Label(open_window,text="Book_Name:")
    L2.grid(row=1,column=0)
    book_name=Entry(open_window)
    book_name.grid(row=1,column=1)
    L3=Label(open_window,text="Author_Name:")
    L3.grid(row=2,column=0)
    author_name=Entry(open_window)
    author_name.grid(row=2,column=1)
    def save_book():
        b_id=id.get()
        b_name=book_name.get()
        a_name=author_name.get()
        if b_id and b_name and a_name:
            query="Insert into books(book_id,book_name,author_name) values (%s,%s,%s)"
            values=(b_id,b_name,a_name)
            curr.execute(query,values)
            conn.commit()
            open_window.destroy()       
    Exit=Button(open_window,text="Submit",fg="white",bg="Blue",font="TimesNewRoman 12 ",command=save_book)
    Exit.grid(row=3,column=1)
def Search_Book():
    def Alter():
        search_term = search_entry.get()

        if not search_term:
            sms.showwarning("Input Error", "Please enter a book title.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="S@kib2005",
                database="Library_database"
            )
            curr = conn.cursor()
            query = """
            SELECT book_id, book_name, author_name FROM books
            WHERE book_name LIKE %s OR book_id LIKE %s OR author_name LIKE %s
            """
            wildcard_term = f"%{search_term}%"
            curr.execute(query, (wildcard_term, wildcard_term, wildcard_term))
            results = curr.fetchall()

            listbox.delete(0, END)  

            if not results:
                listbox.insert(END, "No results found.")
            else:
                for row in results:
                    listbox.insert(END, f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]}")

            conn.close()
        except Exception as e:
            sms.showerror("Error", f"Search failed: {e}")

    open_window5 = Toplevel(root)
    open_window5.title("Search Book")
    open_window5.geometry("400x300")

    Label(open_window5, text="Enter Book Title / ID / Author:", fg="black", font="TimesNewRoman 10 bold").grid(row=0, column=0, padx=10, pady=10)
    search_entry = Entry(open_window5, width=30)
    search_entry.grid(row=0, column=1, padx=10)

    Button(open_window5, text="Search", bg="lightgreen", command=Alter).grid(row=1, column=0, columnspan=2, pady=10)
    listbox = Listbox(open_window5, width=50)
    listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)  
def Issue_Book():
    def confirm_issue():
        book_id = book_id_entry.get()
        if not book_id:
            sms.showwarning("Input Error", "Please enter a Book ID.")
            return
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="S@kib2005",
                database="Library_database"
            )
            curr = conn.cursor()
            curr.execute("SELECT book_id, book_name, author_name, is_issued FROM books WHERE book_id = %s", (book_id,))
            result = curr.fetchone()
            if not result:
                sms.showerror("Not Found", f"No book found with ID {book_id}")
            elif result[3] == 1:
                sms.showwarning("Already Issued", "This book is already issued.")
            else:
                curr.execute("UPDATE books SET is_issued = TRUE WHERE book_id = %s", (book_id,))
                conn.commit()
                issued_listbox.insert(END, f"{result[1]} | ID: {result[0]} | Author: {result[2]}")
                sms.showinfo("Success", f"Book '{result[1]}' issued successfully!")
                issue_window.destroy()
            conn.close()
        except Exception as e:
            sms.showerror("Database Error", f"Something went wrong: {e}")
    issue_window = Toplevel(root)
    issue_window.title("Issue Book")
    issue_window.geometry("300x120")
    Label(issue_window, text="Enter Book ID:", font="Arial 10").grid(row=0, column=0, padx=10, pady=10)
    book_id_entry = Entry(issue_window)
    book_id_entry.grid(row=0, column=1, padx=10)
    Button(issue_window, text="Issue", command=confirm_issue, bg="lightgreen").grid(row=1, column=0, columnspan=2, pady=10)
def Return_Book():
    def confirm_return():
        book_id = return_entry.get()
        if not book_id:
            sms.showwarning("Input Error", "Please enter a Book ID.")
            return
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="S@kib2005",
                database="Library_database"
            )
            curr = conn.cursor()
            curr.execute("SELECT book_id, book_name, author_name, is_issued FROM books WHERE book_id = %s", (book_id,))
            result = curr.fetchone()
            if not result:
                sms.showerror("Not Found", f"No book found with ID {book_id}")
            elif result[3] == 0:
                sms.showinfo("Not Issued", "This book is not currently issued.")
            else:
                curr.execute("UPDATE books SET is_issued = FALSE WHERE book_id = %s", (book_id,))
                conn.commit()
                for i in range(issued_listbox.size()):
                    if f"ID: {book_id}" in issued_listbox.get(i) or f"ID:{book_id}" in issued_listbox.get(i):
                        issued_listbox.delete(i)
                        break

                sms.showinfo("Success", f"Book '{result[1]}' returned successfully!")
                return_window.destroy()
            conn.close()
        except Exception as e:
            sms.showerror("Database Error", f"Something went wrong: {e}")
    return_window = Toplevel(root)
    return_window.title("Return Book")
    return_window.geometry("300x120")

    Label(return_window, text="Enter Book ID:", font="Arial 10").grid(row=0, column=0, padx=10, pady=10)
    return_entry = Entry(return_window)
    return_entry.grid(row=0, column=1, padx=10)
    Button(return_window, text="Return", command=confirm_return, bg="lightcoral").grid(row=1, column=0, columnspan=2, pady=10)
def Delete_Book():
    def Delete_Book2():
        def confirm_delete():
            book_id = a1.get()
            if not book_id:
                sms.showwarning("Input Error", "Please enter a Book ID.")
                return
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="S@kib2005",
                    database="Library_database"
                )
                curr = conn.cursor()
                curr.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
                conn.commit()
                conn.close()
                sms.showinfo("Success", "Book deleted successfully.")
                new_window4.destroy()
            except Exception as e:
                sms.showerror("Error", f"Could not delete book: {e}")

        new_window4 = Toplevel(root)
        new_window4.title("Delete a Book")
        new_window4.geometry("300x150")

        Label(new_window4, text="Book ID:", fg="black", font="TimesNewRoman 10 bold").grid(row=0, column=0, pady=10, padx=10)
        a1 = Entry(new_window4)
        a1.grid(row=0, column=1, padx=10)

        Button(new_window4, text="Delete", command=confirm_delete).grid(row=1, column=0, columnspan=2, pady=20)

    warn = sms.askyesno("Are You Sure??", "You will no longer be able to access it!!")
    if warn:
        Delete_Book2()
def View_Book():
    open_window3=Toplevel(root)
    open_window3.title("Books Available")
    open_window3.geometry("400x200")
    sb=Scrollbar(open_window3,orient=VERTICAL)
    sb.pack(side=RIGHT,fill=Y)
    sb1=Scrollbar(open_window3,orient=HORIZONTAL)
    sb1.pack(side="bottom",fill="x")
    lbx=Listbox(open_window3,yscrollcommand=sb.set,xscrollcommand=sb1.set)
    lbx.pack(fill=BOTH,expand=True)
    conn = mysql.connector.connect(host="localhost", user="root", password="S@kib2005", database="Library_database")
    curr = conn.cursor()
    curr.execute("SELECT * FROM books")
    rows = curr.fetchall()
    for row in rows:
            lbx.insert(END, f"ID: {row[0]} | Name: {row[1]} | Author: {row[2]}")

    conn.close()
    sb.config(command=lbx.yview)
    sb1.config(command=lbx.xview)
def Exit_Lib():
    root.destroy()
button_frame = Frame(root, bg="#f4f4f4")
button_frame.pack(pady=10)
button_style = {
    "font": "TimesNewRoman 11 bold",
    "fg": "white",
    "width": 20,
    "padx": 10,
    "pady": 5
}
Button(button_frame, text="➕ Add Book", bg="#007B5E", command=Add, **button_style).grid(row=0, column=0, padx=10, pady=5)
Button(button_frame, text="📚 View All Books", bg="#007B5E", command=View_Book, **button_style).grid(row=0, column=1, padx=10, pady=5)
Button(button_frame, text="📖 Issue Book", bg="#007B5E", command=Issue_Book, **button_style).grid(row=1, column=0, padx=10, pady=5)
Button(button_frame, text="↩️ Return Book", bg="#007B5E", command=Return_Book, **button_style).grid(row=1, column=1, padx=10, pady=5)
Button(button_frame, text="❌ Delete Book", bg="red", command=Delete_Book, **button_style).grid(row=2, column=0, padx=10, pady=5)
Button(button_frame, text="🔍 Search Book", bg="#007B5E", command=Search_Book, **button_style).grid(row=2, column=1, padx=10, pady=5)
Button(button_frame, text="🚪 Exit", bg="#444", command=root.destroy, **button_style).grid(row=3, column=0, columnspan=2, pady=10)
Label(root, text="📦 Books Issued", font="TimesNewRoman 12 bold", bg="#f4f4f4").pack(pady=10)
issued_listbox = Listbox(root, width=70, height=6, font="Arial 10")
issued_listbox.pack(pady=5)
root.mainloop()