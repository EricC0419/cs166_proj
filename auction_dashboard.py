# changed the auction search so it passes the logged-in user’s identity when they place a bid.
# removed the duplicate bidding code and made it use the existing bid_dashboard.py instead.
import tkinter as tk

# Use the separate bid dashboard to validate and record bids.
from bid_dashboard import open_bid


# Opens a window where the user can search for an auction by its ID.
def open_auction_search(dashboard, connection, login):
    search_window = tk.Toplevel(dashboard)
    search_window.title("Search Auction")
    search_window.geometry("500x520")

    # Searches the database for the entered auction ID.
    def search_auction():
        raw_id = auction_entry.get().strip()

        # Auction IDs must be whole numbers.
        try:
            auction_id = int(raw_id)

        except ValueError:
            result_label.config(
                text="Auction ID must be a whole number"
            )
            bid_button.config(state="disabled")
            return

        try:
            with connection.cursor() as cursor:
                # Join auction and item to display the auction's item details.
                cursor.execute(
                    """
                    SELECT
                        a.auction_id,
                        i.item_name,
                        i.category,
                        i.starting_price,
                        a.current_highest_bid,
                        a.auction_status,
                        a.seller_login
                    FROM auction AS a
                    JOIN item AS i
                        ON a.item_id = i.item_id
                    WHERE a.auction_id = %s;
                    """,
                    (auction_id,)
                )

                auction = cursor.fetchone()
                    # Check whether the logged-in user is a Buyer.
                cursor.execute(
                    """
                    SELECT role
                    FROM users
                    WHERE login = %s;
                    """,
                    (login,)
                )

                role_result = cursor.fetchone()
                user_role = role_result[0] if role_result else None

        except Exception as error:
            connection.rollback()
            result_label.config(
                text=f"Database error: {error}"
            )
            bid_button.config(state="disabled")
            return

        # Display an error if the entered auction does not exist.
        if not auction:
            result_label.config(
                text="Auction not found"
            )
            bid_button.config(state="disabled")
            return

        # Display the information for the matching auction.
        result_label.config(
            text=(
                f"Auction ID: {auction[0]}\n"
                f"Item Name: {auction[1]}\n"
                f"Category: {auction[2]}\n"
                f"Starting Price: ${auction[3]}\n"
                f"Current Highest Bid: ${auction[4]}\n"
                f"Auction Status: {auction[5]}\n"
                f"Seller: {auction[6]}"
            )
        )

        # Bids can only be placed on active auctions.
        if auction[5] == "Active" and user_role == "Buyer":
            bid_button.config(
                state="normal",
                command=lambda: open_bid(
                    search_window,
                    connection,
                    auction[0],
                    login
                )
            )

        else:
            bid_button.config(state="disabled")

            if auction[5] == "Active" and user_role != "Buyer":
                result_label.config(
                    text=result_label.cget("text")
                    + "\n\nOnly Buyer accounts can place bids."
                )
    # Search interface

    tk.Label(
        search_window,
        text="Search Auction",
        font=("Arial", 20)
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        pady=20
    )

    tk.Label(
        search_window,
        text="Auction ID:"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )

    auction_entry = tk.Entry(
        search_window,
        width=20
    )
    auction_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )

    tk.Button(
        search_window,
        text="Search",
        command=search_auction
    ).grid(
        row=2,
        column=0,
        columnspan=2,
        pady=10
    )

    # Displays either the auction details or an error message.
    result_label = tk.Label(
        search_window,
        text="",
        justify="left",
        wraplength=450
    )
    result_label.grid(
        row=3,
        column=0,
        columnspan=2,
        padx=20,
        pady=20
    )

    # This button stays disabled until an active auction is found.
    bid_button = tk.Button(
        search_window,
        text="Place Bid",
        state="disabled"
    )
    bid_button.grid(
        row=4,
        column=0,
        columnspan=2,
        pady=10
    )

    # Pressing Enter also starts the search.
    auction_entry.bind(
        "<Return>",
        lambda _event: search_auction()
    )