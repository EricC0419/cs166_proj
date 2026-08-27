import tkinter as tk


# Opens a window where a new user can create a Buyer account.
def open_register(parent, connection):

    register_window = tk.Toplevel(parent)
    register_window.title("Create Account")
    register_window.geometry("500x470")

    tk.Label(
        register_window,
        text="Create Account",
        font=("Arial", 20, "bold")
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        pady=20
    )

    fields = [
        ("Login:", "login"),
        ("Password:", "password"),
        ("Confirm Password:", "confirm_password"),
        ("Phone Number:", "phone_num"),
        ("Address:", "address"),
        ("Favorite Category:", "favorite_category")
    ]

    entries = {}

    for row, (label_text, field_name) in enumerate(
        fields,
        start=1
    ):
        tk.Label(
            register_window,
            text=label_text
        ).grid(
            row=row,
            column=0,
            padx=10,
            pady=8,
            sticky="e"
        )

        # Hide both password fields.
        if field_name in (
            "password",
            "confirm_password"
        ):
            entry = tk.Entry(
                register_window,
                width=30,
                show="*"
            )

        else:
            entry = tk.Entry(
                register_window,
                width=30
            )

        entry.grid(
            row=row,
            column=1,
            padx=10,
            pady=8
        )

        entries[field_name] = entry

    status_label = tk.Label(
        register_window,
        text="",
        fg="red",
        wraplength=450
    )
    status_label.grid(
        row=8,
        column=0,
        columnspan=2,
        pady=10
    )

    def create_account():
        login = entries["login"].get().strip()
        password = entries["password"].get()
        confirm_password = entries[
            "confirm_password"
        ].get()
        phone_num = entries["phone_num"].get().strip()
        address = entries["address"].get().strip()
        favorite_category = (
            entries["favorite_category"].get().strip()
            or None
        )

        # Required fields cannot be blank.
        if not login or not password or not phone_num or not address:
            status_label.config(
                text=(
                    "Login, password, phone number, "
                    "and address are required"
                ),
                fg="red"
            )
            return

        if password != confirm_password:
            status_label.config(
                text="Passwords do not match",
                fg="red"
            )
            return

        try:
            with connection.cursor() as cursor:
                # Role is omitted so PostgreSQL assigns the default Buyer role.
                cursor.execute(
                    """
                    INSERT INTO users (
                        login,
                        password,
                        phone_num,
                        address,
                        favorite_category
                    )
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (
                        login,
                        password,
                        phone_num,
                        address,
                        favorite_category
                    )
                )

            connection.commit()

        except Exception as error:
            connection.rollback()
            status_label.config(
                text=f"Unable to create account: {error}",
                fg="red"
            )
            return

        status_label.config(
            text="Buyer account created successfully",
            fg="green"
        )

        # Clear the form after successful registration.
        for entry in entries.values():
            entry.delete(0, tk.END)

    create_button = tk.Button(
        register_window,
        text="Create Buyer Account",
        command=create_account
    )
    create_button.grid(
        row=7,
        column=0,
        columnspan=2,
        pady=15
    )