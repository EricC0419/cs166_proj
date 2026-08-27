import tkinter as tk
from admin_dashboard import open_admin_dashboard
from seller_dashboard import open_seller_dashboard
from buyer_dashboard import open_buyer_dashboard


def open_login(root, conn):

    def login():
        # .get() pulls the current value from each input box.
        username = username_entry.get().strip()
        password = password_entry.get()

        if not username or not password:
            status_label.config(text="Enter both login and password")
            return

        try:
            # The cursor sends SQL commands to the database.
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT login, password, role
                FROM users
                WHERE login = %s
                  AND password = %s;
                """,
                (username, password)
            )

            # fetchone() gets one matching row.
            user = cursor.fetchone()
            cursor.close()

        except Exception as error:
            conn.rollback()
            status_label.config(
                text=f"Database error: {error}"
            )
            return

        if user:
            login_name = user[0]
            role = user[2]

            status_label.config(text="")

            if role == "Buyer":
                open_buyer_dashboard(
                    root,
                    conn,
                    login_name
                )

            elif role == "Seller":
                open_seller_dashboard(
                    root,
                    conn,
                    login_name
                )

            elif role == "Admin":
                open_admin_dashboard(
                    root,
                    conn,
                    login_name
                )

            else:
                status_label.config(
                    text="This account has an invalid role"
                )

        else:
            status_label.config(
                text="Invalid login"
            )

    # Shows the text boxes.
    username_label = tk.Label(
        root,
        text="Username:"
    )
    username_label.grid(
        row=0,
        column=0
    )

    # Entry lets the user enter text.
    username_entry = tk.Entry(root)
    username_entry.grid(
        row=0,
        column=1
    )

    password_label = tk.Label(
        root,
        text="Password:"
    )
    password_label.grid(
        row=1,
        column=0
    )

    password_entry = tk.Entry(
        root,
        show="*"
    )
    password_entry.grid(
        row=1,
        column=1
    )

    status_label = tk.Label(
        root,
        text="",
        fg="red"
    )
    status_label.grid(
        row=3,
        column=0,
        columnspan=2
    )

    login_button = tk.Button(
        root,
        text="Login",
        command=login
    )

    login_button.grid(
        row=2,
        column=0,
        columnspan=2
    )

    password_entry.bind(
        "<Return>",
        lambda _event: login()
    )