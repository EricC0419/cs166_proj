import tkinter as tk
from tkinter import ttk


def open_item_search(dashboard, conn):

    # Create new window
    search_window = tk.Toplevel(dashboard)

    search_window.title("Search Items")
    search_window.geometry("900x500")
    def search_items():
        #pulls from search box
        search = search_entry.get()
        #allows for characters to be between serached name
        search_value = "%" + search + "%"

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                auction.auction_id,
                item.item_id,
                item.item_name,
                item.category,
                item.starting_price,
                item.item_condition,
                item.seller_login
            FROM item
            LEFT JOIN auction
                ON item.item_id = auction.item_id
            WHERE item.item_name ILIKE %s
               OR item.category ILIKE %s;
            """,
            (search_value, search_value)
            #we are using ILIKE to accomodate upper case characters and lowercase
        )
        #gets all characters 
        items = cursor.fetchall()
        #previous tables in treeview will appear if not cleared
        cursor.close()
        # Clear previous results
        for row in table.get_children():
            table.delete(row)

        # Add new results
        for item in items:

            table.insert(
                "",
                tk.END,
                values=item
            )

    title = tk.Label(
        search_window,
        text="Search Items",
        font=("Arial", 20)
    )

    title.grid(
        row=0,
        column=0,
        columnspan=2,
        pady=20
    )
    #labels for text and display
    search_label = tk.Label(
        search_window,
        text="Search:"
    )

    search_label.grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )


    search_entry = tk.Entry(
        search_window,
        width=40
    )

    search_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )



    #buttons 
    search_button = tk.Button(
        search_window,
        text="Search",
        command=search_items
    )

    search_button.grid(
        row=1,
        column=2,
        padx=10,
        pady=10
    )


    # Results table

    table = ttk.Treeview(
        search_window,
        columns=(
            "auction_id",
            "item_id",
            "item_name",
            "category",
            "starting_price",
            "condition",
            "seller"
        ),
        show="headings"
    )


    table.heading(
        "auction_id",
        text="Auction ID"
    )

    table.heading(
        "item_id",
        text="Item ID"
    )

    table.heading(
        "item_name",
        text="Item Name"
    )

    table.heading(
        "category",
        text="Category"
    )

    table.heading(
        "starting_price",
        text="Starting Price"
    )

    table.heading(
        "condition",
        text="Condition"
    )

    table.heading(
        "seller",
        text="Seller"
    )


    table.grid(
        row=2,
        column=0,
        columnspan=3,
        padx=20,
        pady=20
    )