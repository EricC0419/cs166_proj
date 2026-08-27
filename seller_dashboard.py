import tkinter as tk

from auction_dashboard import open_auction_search
from edit_profile import open_edit_profile
from item_dashboard import open_item_search
from sell_item import open_sell_item
from status_list import open_auction_statuses
from close_auction import open_close_auction


def open_seller_dashboard(root, connection, login):
    root.withdraw()

    dashboard = tk.Toplevel(root)
    dashboard.title("Seller Dashboard")
    dashboard.geometry("500x620")

    tk.Label(
        dashboard,
        text="Seller Dashboard",
        font=("Arial", 22, "bold")
    ).pack(pady=25)

    tk.Label(
        dashboard,
        text=f"Welcome, {login}"
    ).pack(pady=5)

    tk.Button(
        dashboard,
        text="Auction Statuses",
        width=25,
        height=2,
        command=lambda: open_auction_statuses(
            dashboard,
            connection,
            login
        )
    ).pack(pady=7)

    tk.Button(
        dashboard,
        text="Search Auction",
        width=25,
        height=2,
        command=lambda: open_auction_search(
            dashboard,
            connection,
            login
        )
    ).pack(pady=7)

    tk.Button(
        dashboard,
        text="Search Items",
        width=25,
        height=2,
        command=lambda: open_item_search(
            dashboard,
            connection
        )
    ).pack(pady=7)

    tk.Button(
        dashboard,
        text="Sell or Update Item",
        width=25,
        height=2,
        command=lambda: open_sell_item(
            dashboard,
            connection,
            login
        )
    ).pack(pady=7)

    # Close Auction
    close_auction_button = tk.Button(
        dashboard,
        text="Close Auction",
        width=25,
        height=2,
        command=lambda: open_close_auction(
            dashboard,
            connection,
            login
        )
    )
    
    close_auction_button.pack(pady=7)

    tk.Button(
        dashboard,
        text="Edit Profile",
        width=25,
        height=2,
        command=lambda: open_edit_profile(
            dashboard,
            connection,
            login
        )
    ).pack(pady=7)

    def logout():
        dashboard.destroy()
        root.deiconify()

    tk.Button(
        dashboard,
        text="Log Out",
        width=25,
        command=logout
    ).pack(pady=15)

    dashboard.protocol(
        "WM_DELETE_WINDOW",
        logout
    )