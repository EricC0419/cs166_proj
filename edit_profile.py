import tkinter as tk


def open_edit_profile(parent, connection, login):
    window = tk.Toplevel(parent)
    window.title("Edit Profile")
    window.geometry("520x400")

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT phone_num, address, favorite_category
                FROM users
                WHERE login = %s;
                """,
                (login,)
            )
            profile = cursor.fetchone()

    except Exception as error:
        connection.rollback()
        tk.Label(
            window,
            text=f"Unable to load profile: {error}",
            fg="red"
        ).pack(pady=20)
        return

    if not profile:
        tk.Label(
            window,
            text="Profile not found",
            fg="red"
        ).pack(pady=20)
        return

    tk.Label(
        window,
        text="Edit Profile",
        font=("Arial", 20, "bold")
    ).grid(row=0, column=0, columnspan=2, pady=20)

    tk.Label(
        window,
        text=f"Login: {login}"
    ).grid(row=1, column=0, columnspan=2, pady=5)

    labels = [
        "Phone Number:",
        "Address:",
        "Favorite Category:"
    ]

    entries = []

    for row, label in enumerate(labels, start=2):
        tk.Label(window, text=label).grid(
            row=row,
            column=0,
            padx=10,
            pady=10,
            sticky="e"
        )

        entry = tk.Entry(window, width=35)
        entry.grid(
            row=row,
            column=1,
            padx=10,
            pady=10
        )

        entries.append(entry)

    for entry, value in zip(entries, profile):
        entry.insert(0, value or "")

    status_label = tk.Label(
        window,
        text="",
        fg="red",
        wraplength=470
    )
    status_label.grid(
        row=6,
        column=0,
        columnspan=2,
        pady=10
    )

    def save_profile():
        phone = entries[0].get().strip()
        address = entries[1].get().strip()
        favorite = entries[2].get().strip() or None

        if not phone or not address:
            status_label.config(
                text="Phone number and address are required",
                fg="red"
            )
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users
                    SET phone_num = %s,
                        address = %s,
                        favorite_category = %s
                    WHERE login = %s;
                    """,
                    (phone, address, favorite, login)
                )

            connection.commit()

        except Exception as error:
            connection.rollback()
            status_label.config(
                text=f"Update failed: {error}",
                fg="red"
            )
            return

        status_label.config(
            text="Profile updated successfully",
            fg="green"
        )

    tk.Button(
        window,
        text="Save Changes",
        command=save_profile
    ).grid(
        row=5,
        column=0,
        columnspan=2,
        pady=15
    )