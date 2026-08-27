from decimal import Decimal, InvalidOperation
import tkinter as tk
from tkinter import ttk


def open_sell_item(parent, connection, seller_login):
    window = tk.Toplevel(parent)
    window.title("Sell or Update Items")
    window.geometry("900x650")

    tk.Label(
        window,
        text="Sell or Update Items",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    table = ttk.Treeview(
        window,
        columns=(
            "item_id",
            "auction_id",
            "name",
            "category",
            "price",
            "condition",
            "status"
        ),
        show="headings",
        height=8
    )

    headings = (
        ("item_id", "Item ID"),
        ("auction_id", "Auction ID"),
        ("name", "Name"),
        ("category", "Category"),
        ("price", "Starting Price"),
        ("condition", "Condition"),
        ("status", "Auction Status")
    )

    for column, heading in headings:
        table.heading(column, text=heading)

    table.pack(padx=15, pady=10, fill="x")

    form = tk.Frame(window)
    form.pack(pady=10)

    fields = [
        ("Item ID:", "item_id"),
        ("Auction ID:", "auction_id"),
        ("Item Name:", "item_name"),
        ("Category:", "category"),
        ("Starting Price:", "starting_price"),
        ("Condition:", "item_condition"),
        ("Image URL:", "image_url"),
        ("Description:", "description")
    ]

    entries = {}

    for index, (label, key) in enumerate(fields):
        row = index // 2
        pair = index % 2

        tk.Label(form, text=label).grid(
            row=row,
            column=pair * 2,
            padx=6,
            pady=6,
            sticky="e"
        )

        entry = tk.Entry(form, width=27)
        entry.grid(
            row=row,
            column=pair * 2 + 1,
            padx=6,
            pady=6
        )

        entries[key] = entry

    status_label = tk.Label(
        window,
        text="",
        fg="red",
        wraplength=850
    )
    status_label.pack(pady=8)

    def refresh_items():
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        i.item_id,
                        a.auction_id,
                        i.item_name,
                        i.category,
                        i.starting_price,
                        i.item_condition,
                        a.auction_status
                    FROM item AS i
                    LEFT JOIN auction AS a
                        ON i.item_id = a.item_id
                    WHERE i.seller_login = %s
                    ORDER BY i.item_id;
                    """,
                    (seller_login,)
                )

                items = cursor.fetchall()

        except Exception as error:
            connection.rollback()
            status_label.config(
                text=f"Unable to load items: {error}",
                fg="red"
            )
            return

        for row in table.get_children():
            table.delete(row)

        for item in items:
            table.insert("", tk.END, values=item)

    def parse_required_values():
        try:
            item_id = int(entries["item_id"].get().strip())
            auction_id = int(entries["auction_id"].get().strip())
            price = Decimal(
                entries["starting_price"].get().strip()
            )

        except (ValueError, InvalidOperation):
            raise ValueError(
                "IDs must be whole numbers and price must be numeric"
            )

        name = entries["item_name"].get().strip()
        category = entries["category"].get().strip()

        if not name or not category:
            raise ValueError(
                "Item name and category are required"
            )

        if price < 0:
            raise ValueError(
                "Starting price cannot be negative"
            )

        return item_id, auction_id, price, name, category

    def create_listing():
        try:
            item_id, auction_id, price, name, category = (
                parse_required_values()
            )

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO item (
                        item_id,
                        item_name,
                        category,
                        starting_price,
                        image_url,
                        item_condition,
                        description,
                        seller_login,
                        seller_role
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, 'Seller'
                    );
                    """,
                    (
                        item_id,
                        name,
                        category,
                        price,
                        entries["image_url"].get().strip() or None,
                        entries["item_condition"].get().strip() or None,
                        entries["description"].get().strip() or None,
                        seller_login
                    )
                )

                cursor.execute(
                    """
                    INSERT INTO auction (
                        auction_id,
                        item_id,
                        seller_login,
                        seller_role,
                        current_highest_bid,
                        auction_status
                    )
                    VALUES (
                        %s, %s, %s, 'Seller', %s, 'Active'
                    );
                    """,
                    (
                        auction_id,
                        item_id,
                        seller_login,
                        price
                    )
                )

            connection.commit()

        except ValueError as error:
            connection.rollback()
            status_label.config(
                text=str(error),
                fg="red"
            )
            return

        except Exception as error:
            connection.rollback()
            status_label.config(
                text=f"Unable to create listing: {error}",
                fg="red"
            )
            return

        status_label.config(
            text="Item and auction created successfully",
            fg="green"
        )

        refresh_items()

    def load_selected(_event):
        selected = table.selection()

        if not selected:
            return

        item_id = table.item(
            selected[0],
            "values"
        )[0]

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        i.item_id,
                        a.auction_id,
                        i.item_name,
                        i.category,
                        i.starting_price,
                        i.item_condition,
                        i.image_url,
                        i.description
                    FROM item AS i
                    LEFT JOIN auction AS a
                        ON i.item_id = a.item_id
                    WHERE i.item_id = %s
                      AND i.seller_login = %s;
                    """,
                    (item_id, seller_login)
                )

                values = cursor.fetchone()

        except Exception as error:
            connection.rollback()
            status_label.config(
                text=f"Unable to load item: {error}",
                fg="red"
            )
            return

        if values:
            for key, value in zip(entries, values):
                entries[key].delete(0, tk.END)
                entries[key].insert(0, value or "")

    def update_item():
        try:
            item_id = int(
                entries["item_id"].get().strip()
            )

            price = Decimal(
                entries["starting_price"].get().strip()
            )

        except (ValueError, InvalidOperation):
            status_label.config(
                text="Item ID and price must be numeric",
                fg="red"
            )
            return

        name = entries["item_name"].get().strip()
        category = entries["category"].get().strip()

        if not name or not category or price < 0:
            status_label.config(
                text=(
                    "Enter a name, category, "
                    "and nonnegative price"
                ),
                fg="red"
            )
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE item
                    SET item_name = %s,
                        category = %s,
                        starting_price = %s,
                        item_condition = %s,
                        image_url = %s,
                        description = %s
                    WHERE item_id = %s
                      AND seller_login = %s;
                    """,
                    (
                        name,
                        category,
                        price,
                        entries["item_condition"].get().strip() or None,
                        entries["image_url"].get().strip() or None,
                        entries["description"].get().strip() or None,
                        item_id,
                        seller_login
                    )
                )

                if cursor.rowcount == 0:
                    raise ValueError(
                        "Item not found or you do not own it"
                    )

            connection.commit()

        except ValueError as error:
            connection.rollback()
            status_label.config(
                text=str(error),
                fg="red"
            )
            return

        except Exception as error:
            connection.rollback()
            status_label.config(
                text=f"Unable to update item: {error}",
                fg="red"
            )
            return

        status_label.config(
            text="Item updated successfully",
            fg="green"
        )

        refresh_items()

    table.bind(
        "<<TreeviewSelect>>",
        load_selected
    )

    button_frame = tk.Frame(window)
    button_frame.pack(pady=8)

    tk.Button(
        button_frame,
        text="Create Listing",
        command=create_listing
    ).pack(side="left", padx=8)

    tk.Button(
        button_frame,
        text="Update Item",
        command=update_item
    ).pack(side="left", padx=8)

    tk.Button(
        button_frame,
        text="Refresh",
        command=refresh_items
    ).pack(side="left", padx=8)

    refresh_items()