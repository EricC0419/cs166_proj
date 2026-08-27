#Fixed the undefined bid_amount variable.
#Added checks for invalid, negative, equal, or lower bids.
#Blocked bidding on closed auctions and your own auction.
#Recorded the logged-in buyer and updated current_highest_bid.
#Added commit(), rollback(), and row locking so the database stays consistent.
from decimal import Decimal, InvalidOperation
import tkinter as tk


# Opens the bidding window for a selected auction.
def open_bid(parent, connection, auction_id, buyer_login):
    bid_window = tk.Toplevel(parent)
    bid_window.title("Place Bid")
    bid_window.geometry("500x400")

    # Load the current bid when the window first opens.
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT current_highest_bid
                FROM auction
                WHERE auction_id = %s;
                """,
                (auction_id,)
            )

            result = cursor.fetchone()

    except Exception as error:
        connection.rollback()

        tk.Label(
            bid_window,
            text=f"Database error: {error}",
            fg="red"
        ).pack(pady=20)

        return

    if not result:
        tk.Label(
            bid_window,
            text="Auction not found",
            fg="red"
        ).pack(pady=20)

        return

    # Validates and records the user's bid.
    def place_bid():
        try:
            bid_amount = Decimal(
                bid_entry.get().strip()
            )

        except (InvalidOperation, ValueError):
            status_label.config(
                text="Enter a valid dollar amount",
                fg="red"
            )
            return

        if bid_amount <= 0:
            status_label.config(
                text="Bid must be greater than $0",
                fg="red"
            )
            return

        try:
            with connection.cursor() as cursor:
                # Lock the auction row while checking and updating the bid.
                # This prevents two users from changing it simultaneously.
                cursor.execute(
                    """
                    SELECT
                        seller_login,
                        current_highest_bid,
                        auction_status
                    FROM auction
                    WHERE auction_id = %s
                    FOR UPDATE;
                    """,
                    (auction_id,)
                )

                auction = cursor.fetchone()

                if not auction:
                    raise ValueError(
                        "Auction no longer exists"
                    )

                seller_login = auction[0]
                current_bid = auction[1]
                auction_status = auction[2]

                # Only active auctions accept bids.
                if auction_status != "Active":
                    raise ValueError(
                        "This auction is closed"
                    )

                # Sellers cannot bid on their own auctions.
                if buyer_login == seller_login:
                    raise ValueError(
                        "You cannot bid on your own auction"
                    )

                # A new bid must be greater than the current highest bid.
                if bid_amount <= current_bid:
                    raise ValueError(
                        f"Bid must be higher than ${current_bid}"
                    )

                # Generate the next bid ID.
                cursor.execute(
                    """
                    SELECT COALESCE(MAX(bid_id), 0) + 1
                    FROM bid;
                    """
                )

                bid_id = cursor.fetchone()[0]

                # Store the new bid.
                cursor.execute(
                    """
                    INSERT INTO bid (
                        bid_id,
                        auction_id,
                        buyer_login,
                        buyer_role,
                        bid_amount
                    )
                    VALUES (%s, %s, %s, 'Buyer', %s);
                    """,
                    (
                        bid_id,
                        auction_id,
                        buyer_login,
                        bid_amount
                    )
                )

                # Update the auction's current highest bid.
                cursor.execute(
                    """
                    UPDATE auction
                    SET current_highest_bid = %s
                    WHERE auction_id = %s;
                    """,
                    (bid_amount, auction_id)
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
                text=f"Bid failed: {error}",
                fg="red"
            )
            return

        current_bid_value.config(
            text=f"${bid_amount:.2f}"
        )

        status_label.config(
            text="Bid placed successfully",
            fg="green"
        )

        bid_entry.delete(0, tk.END)

    # --------------------------------------------------
    # Bid interface
    # --------------------------------------------------

    tk.Label(
        bid_window,
        text="Place Bid",
        font=("Arial", 20)
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        pady=20
    )

    tk.Label(
        bid_window,
        text="Auction ID:"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=8
    )

    tk.Label(
        bid_window,
        text=str(auction_id)
    ).grid(
        row=1,
        column=1,
        padx=10,
        pady=8
    )

    tk.Label(
        bid_window,
        text="Buyer:"
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=8
    )

    tk.Label(
        bid_window,
        text=buyer_login
    ).grid(
        row=2,
        column=1,
        padx=10,
        pady=8
    )

    tk.Label(
        bid_window,
        text="Current Highest Bid:"
    ).grid(
        row=3,
        column=0,
        padx=10,
        pady=8
    )

    current_bid_value = tk.Label(
        bid_window,
        text=f"${result[0]}"
    )
    current_bid_value.grid(
        row=3,
        column=1,
        padx=10,
        pady=8
    )

    tk.Label(
        bid_window,
        text="Your Bid:"
    ).grid(
        row=4,
        column=0,
        padx=10,
        pady=8
    )

    bid_entry = tk.Entry(
        bid_window,
        width=20
    )
    bid_entry.grid(
        row=4,
        column=1,
        padx=10,
        pady=8
    )

    tk.Button(
        bid_window,
        text="Place Bid",
        command=place_bid
    ).grid(
        row=5,
        column=0,
        columnspan=2,
        pady=15
    )

    status_label = tk.Label(
        bid_window,
        text="",
        fg="red",
        wraplength=450
    )
    status_label.grid(
        row=6,
        column=0,
        columnspan=2,
        pady=10
    )

    # Pressing Enter also submits the bid.
    bid_entry.bind(
        "<Return>",
        lambda _event: place_bid()
    )