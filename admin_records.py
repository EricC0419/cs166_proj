import tkinter as tk
from tkinter import ttk, messagebox


# Allows Admins to manage items, payments, and shipments.
def open_admin_records(parent, connection):

    window = tk.Toplevel(parent)
    window.title("Manage Project Records")
    window.geometry("950x600")

    notebook = ttk.Notebook(window)
    notebook.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    item_tab = tk.Frame(notebook)
    payment_tab = tk.Frame(notebook)
    shipment_tab = tk.Frame(notebook)

    notebook.add(
        item_tab,
        text="Items"
    )
    notebook.add(
        payment_tab,
        text="Payments"
    )
    notebook.add(
        shipment_tab,
        text="Shipments"
    )

    # --------------------------------------------------
    # Item Management
    # --------------------------------------------------

    item_table = ttk.Treeview(
        item_tab,
        columns=(
            "item_id",
            "item_name",
            "category",
            "seller",
            "auction_id"
        ),
        show="headings",
        height=17
    )

    item_table.heading(
        "item_id",
        text="Item ID"
    )
    item_table.heading(
        "item_name",
        text="Item Name"
    )
    item_table.heading(
        "category",
        text="Category"
    )
    item_table.heading(
        "seller",
        text="Seller"
    )
    item_table.heading(
        "auction_id",
        text="Auction ID"
    )

    item_table.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    def load_items():
        for row in item_table.get_children():
            item_table.delete(row)

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        i.item_id,
                        i.item_name,
                        i.category,
                        i.seller_login,
                        a.auction_id
                    FROM item AS i
                    LEFT JOIN auction AS a
                        ON i.item_id = a.item_id
                    ORDER BY i.item_id;
                    """
                )

                for item in cursor.fetchall():
                    item_table.insert(
                        "",
                        tk.END,
                        values=item
                    )

        except Exception as error:
            connection.rollback()
            messagebox.showerror(
                "Database Error",
                f"Unable to load items:\n{error}",
                parent=window
            )

    def remove_item():
        selected = item_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Item Selected",
                "Select an item first.",
                parent=window
            )
            return

        values = item_table.item(
            selected[0],
            "values"
        )

        item_id = values[0]
        item_name = values[1]
        auction_id = values[4]

        confirmed = messagebox.askyesno(
            "Remove Item",
            (
                f"Remove {item_name} and its related "
                f"auction records?"
            ),
            parent=window
        )

        if not confirmed:
            return

        try:
            with connection.cursor() as cursor:
                # Payment and shipment prevent an auction from being deleted,
                # so remove those records first when they exist.
                if auction_id:
                    cursor.execute(
                        """
                        DELETE FROM shipment
                        WHERE auction_id = %s;
                        """,
                        (auction_id,)
                    )

                    cursor.execute(
                        """
                        DELETE FROM payment
                        WHERE auction_id = %s;
                        """,
                        (auction_id,)
                    )

                    # Deleting the auction also deletes its bids.
                    cursor.execute(
                        """
                        DELETE FROM auction
                        WHERE auction_id = %s;
                        """,
                        (auction_id,)
                    )

                cursor.execute(
                    """
                    DELETE FROM item
                    WHERE item_id = %s;
                    """,
                    (item_id,)
                )

                if cursor.rowcount == 0:
                    raise ValueError(
                        "Item no longer exists"
                    )

            connection.commit()

        except ValueError as error:
            connection.rollback()
            messagebox.showerror(
                "Removal Failed",
                str(error),
                parent=window
            )
            return

        except Exception as error:
            connection.rollback()
            messagebox.showerror(
                "Removal Failed",
                f"Unable to remove item:\n{error}",
                parent=window
            )
            return

        messagebox.showinfo(
            "Success",
            f"Item {item_id} was removed.",
            parent=window
        )

        load_items()
        load_payments()
        load_shipments()

    tk.Button(
        item_tab,
        text="Remove Selected Item",
        command=remove_item
    ).pack(pady=10)

    # --------------------------------------------------
    # Payment Management
    # --------------------------------------------------

    payment_table = ttk.Treeview(
        payment_tab,
        columns=(
            "payment_id",
            "auction_id",
            "buyer",
            "amount",
            "status"
        ),
        show="headings",
        height=15
    )

    payment_table.heading(
        "payment_id",
        text="Payment ID"
    )
    payment_table.heading(
        "auction_id",
        text="Auction ID"
    )
    payment_table.heading(
        "buyer",
        text="Buyer"
    )
    payment_table.heading(
        "amount",
        text="Amount"
    )
    payment_table.heading(
        "status",
        text="Status"
    )

    payment_table.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    payment_status = ttk.Combobox(
        payment_tab,
        values=(
            "Pending",
            "Completed",
            "Failed"
        ),
        state="readonly"
    )
    payment_status.set("Pending")
    payment_status.pack(pady=5)

    def load_payments():
        for row in payment_table.get_children():
            payment_table.delete(row)

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        payment_id,
                        auction_id,
                        buyer_login,
                        amount,
                        payment_status
                    FROM payment
                    ORDER BY payment_id;
                    """
                )

                for payment in cursor.fetchall():
                    payment_table.insert(
                        "",
                        tk.END,
                        values=payment
                    )

        except Exception as error:
            connection.rollback()
            messagebox.showerror(
                "Database Error",
                f"Unable to load payments:\n{error}",
                parent=window
            )

    def update_payment():
        selected = payment_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Payment Selected",
                "Select a payment first.",
                parent=window
            )
            return

        payment_id = payment_table.item(
            selected[0],
            "values"
        )[0]

        new_status = payment_status.get()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE payment
                    SET payment_status = %s
                    WHERE payment_id = %s;
                    """,
                    (
                        new_status,
                        payment_id
                    )
                )

            connection.commit()

        except Exception as error:
            connection.rollback()
            messagebox.showerror(
                "Update Failed",
                f"Unable to update payment:\n{error}",
                parent=window
            )
            return

        messagebox.showinfo(
            "Success",
            f"Payment {payment_id} updated.",
            parent=window
        )

        load_payments()

    tk.Button(
        payment_tab,
        text="Update Payment Status",
        command=update_payment
    ).pack(pady=10)

    # --------------------------------------------------
    # Shipment Management
    # --------------------------------------------------

    shipment_table = ttk.Treeview(
        shipment_tab,
        columns=(
            "shipment_id",
            "auction_id",
            "address",
            "status",
            "tracking"
        ),
        show="headings",
        height=14
    )

    shipment_table.heading(
        "shipment_id",
        text="Shipment ID"
    )
    shipment_table.heading(
        "auction_id",
        text="Auction ID"
    )
    shipment_table.heading(
        "address",
        text="Address"
    )
    shipment_table.heading(
        "status",
        text="Status"
    )
    shipment_table.heading(
        "tracking",
        text="Tracking Number"
    )

    shipment_table.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    shipment_status = ttk.Combobox(
        shipment_tab,
        values=(
            "Pending",
            "Shipped",
            "Delivered"
        ),
        state="readonly"
    )
    shipment_status.set("Pending")
    shipment_status.pack(pady=5)

    tk.Label(
        shipment_tab,
        text="Tracking Number:"
    ).pack()

    tracking_entry = tk.Entry(
        shipment_tab,
        width=35
    )
    tracking_entry.pack(pady=5)

    def load_shipments():
        for row in shipment_table.get_children():
            shipment_table.delete(row)

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        shipment_id,
                        auction_id,
                        address,
                        shipment_status,
                        tracking_number
                    FROM shipment
                    ORDER BY shipment_id;
                    """
                )

                for shipment in cursor.fetchall():
                    shipment_table.insert(
                        "",
                        tk.END,
                        values=shipment
                    )

        except Exception as error:
            connection.rollback()
            messagebox.showerror(
                "Database Error",
                f"Unable to load shipments:\n{error}",
                parent=window
            )

    def update_shipment():
        selected = shipment_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Shipment Selected",
                "Select a shipment first.",
                parent=window
            )
            return

        shipment_id = shipment_table.item(
            selected[0],
            "values"
        )[0]

        new_status = shipment_status.get()
        tracking_number = (
            tracking_entry.get().strip()
            or None
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE shipment
                    SET shipment_status = %s,
                        tracking_number = %s
                    WHERE shipment_id = %s;
                    """,
                    (
                        new_status,
                        tracking_number,
                        shipment_id
                    )
                )

            connection.commit()

        except Exception as error:
            connection.rollback()
            messagebox.showerror(
                "Update Failed",
                f"Unable to update shipment:\n{error}",
                parent=window
            )
            return

        messagebox.showinfo(
            "Success",
            f"Shipment {shipment_id} updated.",
            parent=window
        )

        load_shipments()

    tk.Button(
        shipment_tab,
        text="Update Shipment",
        command=update_shipment
    ).pack(pady=10)

    load_items()
    load_payments()
    load_shipments()