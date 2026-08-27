import tkinter as tk
from admin_dashboard import open_admin_dashboard
from seller_dashboard import open_seller_dashboard
from buyer_dashboard import open_buyer_dashboard

def open_login(root, conn):

    def login():
        #.get() current value stored into the input box pull from the box 
        username = username_entry.get()
        password = password_entry.get()
        #cursor controls mouse
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT login, password, role
            FROM users
            WHERE username = %s
            AND password = %s
            """,
            (username, password)
        )
        #fetch gets a row one is row one all is all rows and etc
        user = cursor.fetchone()

        cursor.close()

        if user:
            print("Login successful")
            role = user[2]
            root.withdraw()
            if role == "Buyer":
                open_buyer_dashboard(root,conn)
            if role == "Seller":
                open_seller_dashboard(root, conn)
            if role == "Admin":
                open_admin_dashboard(root, conn)
        else:
            status_label.config(text= "Invalid login")

    #shows the text boxes
    username_label = tk.Label(root, text="Username:")
    username_label.grid(row=0, column=0)
    #entry lets you put text into it 
    username_entry = tk.Entry(root)
    username_entry.grid(row=0, column=1)

    password_label = tk.Label(root, text="Password:")
    password_label.grid(row=1, column=0)

    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=1, column=1)

    status_label = tk.Label(root, text="")
    status_label.grid(row=3, column=0, columnspan=2)

    login_button = tk.Button(
        root,
        text="Login",
        command=login
    )

    login_button.grid(row=2, column=0, columnspan=2)