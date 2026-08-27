import tkinter as tk
from tkinter import ttk, messagebox


def open_manager(parent, connection):
    window = tk.Toplevel(parent)
    window.title("Admin Manager")
    window.geometry("850x600")

    notebook = ttk.Notebook(window)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    users_tab = tk.Frame(notebook)
    auctions_tab = tk.Frame(notebook)

    notebook.add(users_tab, text="Manage User Roles")
    notebook.add(auctions_tab, text="Manage Auctions")

    # Manage user roles

    user_tree = ttk.Treeview(
        users_tab,
        columns=("login", "role"),
        show="headings",
        height=15
    )

    user_tree.heading("login", text="Login")
    user_tree.heading("role", text="Role")
    user_tree.column("login", width=250)
    user_tree.column("role", width=150)
    user_tree.pack(fill="both", expand=True, padx=10, pady=10)

    role_choice = ttk.Combobox(
        users_tab,
        values=("Buyer", "Seller", "Admin"),
        state="readonly"
    )
    role_choice.set("Buyer")
    role_choice.pack(pady=5)

    def load_users():
        for row in user_tree.get_children():
            user_tree.delete(row)

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT login, role
                    FROM users
                    ORDER BY login;
                    """
                )

                for user in cursor.fetchall():
                    user_tree.insert("", "end", values=user)

        except Exception as error:
            connection.rollback()
            messagebox.showerror(
                "Database Error",
                f"Unable to load users:\n{error}",
                parent=window
            )

    def update_role():
        selected = user_tree.selection()

        if not selected:
            messagebox.showwarning(
                "No User Selected",
                "Select a user first.",
                parent=window
            )
            return

        login = user_tree.item(selected[0], "values")[0]
        new_role = role_choice.get()

        if not new_role:
            messagebox.showwarning(
                "Missing Role",
                "Select a role.",
                parent=window
            )
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users
                    SET role = %s
                    WHERE login = %s;
                    """,
                    (new_role, login)
                )

            connection.commit()

            messagebox.showinfo(
                "Success",
                f"{login}'s role changed to {new_role}.",
                parent=window
            )

            load_users()

        except Exception as error:
            connection.rollback()
            messagebox.showerror(
                "Update Failed",
                f"Unable to update the role:\n{error}",
                parent=window
            )

    tk.Button(
        users_tab,
        text="Update Selected User's Role",
        command=update_role
    ).pack(pady=10)

    # Manage auctions

    auction_tree = ttk.Treeview(
        auctions_tab,
        columns=(
            "auction_id",
            "item_name",
            "seller",
            "highest_bid",
            "status"
        ),
        show="headings",
        height=15
    )

    auction_tree.heading("auction_id", text="Auction ID")
    auction_tree.heading("item_name", text="Item")
    auction_tree.heading("seller", text="Seller")
    auction_tree.heading("highest_bid", text="Highest Bid")
    auction_tree.heading("status", text="Status")

    auction_tree.column("auction_id", width=90)
    auction_tree.column("item_name", width=200)
    auction_tree.column("seller", width=150)
    auction_tree.column("highest_bid", width=110)
    auction_tree.column("status", width=100)

    auction_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_auctions():
        for row in auction_tree.get_children():
            auction_tree.delete(row)

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        a.auction_id,
                        i.item_name,
                        a.seller_login,
                        a.current_highest_bid,
                        a.auction_status
                    FROM auction AS a
                    JOIN item AS i
                        ON a.item_id = i.item_id
                    ORDER BY a.auction_id;
                    """
                )

                for auction in cursor.fetchall():
                    auction_tree.insert("", "end", values=auction)

        except Exception as error:
            connection.rollback()
            messagebox.showerror(
                "Database Error",
                f"Unable to load auctions:\n{error}",
                parent=window
            )

    def terminate_auction():
        selected = auction_tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Auction Selected",
                "Select an auction first.",
                parent=window
            )
            return

        values = auction_tree.item(selected[0], "values")
        auction_id = values[0]
        current_status = values[4]

        if current_status != "Active":
            messagebox.showwarning(
                "Auction Not Active",
                "Only an active auction can be terminated.",
                parent=window
            )
            return

        confirmed = messagebox.askyesno(
            "Terminate Auction",
            f"Terminate auction {auction_id}?",
            parent=window
        )

        if not confirmed:
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE auction
                    SET auction_status = 'Closed'
                    WHERE auction_id = %s
                      AND auction_status = 'Active';
                    """,
                    (auction_id,)
                )

                if cursor.rowcount == 0:
                    connection.rollback()
                    messagebox.showwarning(
                        "No Change",
                        "The auction is no longer active.",
                        parent=window
                    )
                    load_auctions()
                    return

            connection.commit()

            messagebox.showinfo(
                "Success",
                f"Auction {auction_id} was terminated.",
                parent=window
            )

            load_auctions()

        except Exception as error:
            connection.rollback()
            messagebox.showerror(
                "Termination Failed",
                f"Unable to terminate the auction:\n{error}",
                parent=window
            )

    tk.Button(
        auctions_tab,
        text="Terminate Selected Auction",
        command=terminate_auction
    ).pack(pady=10)

    load_users()
    load_auctions()