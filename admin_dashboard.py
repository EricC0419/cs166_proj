#Corrected the window title from Buyer Dashboard to Admin Dashboard.
#Replaced undefined current_user_id with login.
#Corrected the search function names.
#Connected manager.py using open_manager().
#Removed the Sell button because Admin is not a Seller in the Phase 2 schema.
#Added logout behavior.
import tkinter as tk

from status_list import open_auction_statuses
from auction_dashboard import open_auction_search
from item_dashboard import open_item_search
from edit_profile import open_edit_profile
from manager import open_manager


def open_admin_dashboard(root, connection, login):

    # Hide the login window.
    root.withdraw()

    dashboard = tk.Toplevel(root)
    dashboard.title("Admin Dashboard")
    dashboard.geometry("500x540")

    title_label = tk.Label(
        dashboard,
        text="Admin Dashboard",
        font=("Arial", 22, "bold")
    )
    title_label.pack(pady=25)

    welcome_label = tk.Label(
        dashboard,
        text=f"Welcome, {login}"
    )
    welcome_label.pack(pady=5)

    # Auction Statuses
    auction_status_button = tk.Button(
        dashboard,
        text="All Auction Statuses",
        width=25,
        height=2,
        command=lambda: open_auction_statuses(
            dashboard,
            connection,
            login
        )
    )
    auction_status_button.pack(pady=8)

    # Search Auction
    search_auction_button = tk.Button(
        dashboard,
        text="Search Auction",
        width=25,
        height=2,
        command=lambda: open_auction_search(
            dashboard,
            connection,
            login
        )
    )
    search_auction_button.pack(pady=8)

    # Search Item
    search_item_button = tk.Button(
        dashboard,
        text="Search Item",
        width=25,
        height=2,
        command=lambda: open_item_search(
            dashboard,
            connection
        )
    )
    search_item_button.pack(pady=8)

    # Manage Roles and Auctions
    manager_button = tk.Button(
        dashboard,
        text="Manage Roles/Auctions",
        width=25,
        height=2,
        command=lambda: open_manager(
            dashboard,
            connection
        )
    )
    manager_button.pack(pady=8)

    # Edit Profile
    edit_profile_button = tk.Button(
        dashboard,
        text="Edit Profile",
        width=25,
        height=2,
        command=lambda: open_edit_profile(
            dashboard,
            connection,
            login
        )
    )
    edit_profile_button.pack(pady=8)

    # Return to the login screen.
    def logout():
        dashboard.destroy()
        root.deiconify()

    logout_button = tk.Button(
        dashboard,
        text="Log Out",
        width=25,
        command=logout
    )
    logout_button.pack(pady=15)

    # Closing the dashboard also returns to the login screen.
    dashboard.protocol(
        "WM_DELETE_WINDOW",
        logout
    )