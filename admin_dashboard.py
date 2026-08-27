import tkinter as tk

from status_list import open_auction_statuses
from auction_dashboard import open_auction_search
from item_dashboard import open_item_search
from sell_item import open_sell_item
from edit_profile import open_edit_profile
from manager import manager 

def open_admin_dashboard(root, connection, login):

    # Hide the login window
    root.withdraw()

    dashboard = tk.Toplevel(root)
    dashboard.title("Buyer Dashboard")
    dashboard.geometry("500x500")

    title_label = tk.Label(
        dashboard,
        text="Buyer Dashboard",
        font=("Arial", 22, "bold")
    )
    title_label.pack(pady=30)

    # Auction Statuses
    auction_status_button = tk.Button(
        dashboard,
        text="Auction Statuses",
        width=25,
        height=2,
        command=lambda: open_auction_statuses(
            dashboard,
            connection,
            current_user_id
        )
    )
    auction_status_button.pack(pady=10)

    # Search Auction
    search_auction_button = tk.Button(
        dashboard,
        text="Search Auction",
        width=25,
        height=2,
        command=lambda: open_search_auction(
            dashboard,
            connection,
            current_user_id
        )
    )
    search_auction_button.pack(pady=10)

    # Search Item
    search_item_button = tk.Button(
        dashboard,
        text="Search Item",
        width=25,
        height=2,
        command=lambda: open_search_item(
            dashboard,
            connection,
            current_user_id
        )
    )
    search_item_button.pack(pady=10)

    # Sell
    sell_button = tk.Button(
        dashboard,
        text="Sell",
        width=25,
        height=2,
        command=lambda: open_sell_item(
            dashboard,
            connection,
            current_user_id
        )
    )
    sell_button.pack(pady=10)

    # Edit Profile
    edit_profile_button = tk.Button(
        dashboard,
        text="Edit Profile",
        width=25,
        height=2,
        command=lambda: open_edit_profile(
            dashboard,
            connection,
            current_user_id
        )
    )
    edit_profile_button.pack(pady=10)

    manager_button = tk.Button(
        dashboard,
        text="Manage Roles/Auctions",
        width=25,
        height=2,
        command=lambda: manager(
            dashboard,
            connection,
            current_user_id
        )
    )
    manager_button.pack(pady=10)