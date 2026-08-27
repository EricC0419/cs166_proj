import tkinter as tk


# Allows a Seller to close one of their active auctions.
def open_close_auction(parent, connection, seller_login):

    window = tk.Toplevel(parent)
    window.title("Close Auction")
    window.geometry("480x300")

    tk.Label(
        window,
        text="Close Auction",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text="Auction ID:"
    ).pack(pady=5)

    auction_entry = tk.Entry(
        window,
        width=20
    )
    auction_entry.pack(pady=5)

    status_label = tk.Label(
        window,
        text="",
        fg="red",
        wraplength=440
    )
    status_label.pack(pady=12)

    def close_auction():

        # Auction IDs must be whole numbers.
        try:
            auction_id = int(
                auction_entry.get().strip()
            )

        except ValueError:
            status_label.config(
                text="Auction ID must be a whole number",
                fg="red"
            )
            return

        try:
            with connection.cursor() as cursor:
                # Lock the auction while checking and closing it.
                cursor.execute(
                    """
                    SELECT
                        seller_login,
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
                        "Auction not found"
                    )

                # Sellers can only close auctions they own.
                if auction[0] != seller_login:
                    raise ValueError(
                        "You can only close your own auction"
                    )

                if auction[1] == "Closed":
                    raise ValueError(
                        "Auction is already closed"
                    )

                # Find the buyer with the highest bid.
                cursor.execute(
                    """
                    SELECT buyer_login
                    FROM bid
                    WHERE auction_id = %s
                    ORDER BY
                        bid_amount DESC,
                        bid_timestamp ASC
                    LIMIT 1;
                    """,
                    (auction_id,)
                )

                winner_row = cursor.fetchone()

                if winner_row:
                    winner = winner_row[0]

                else:
                    winner = None

                # Close the auction and store the winner.
                cursor.execute(
                    """
                    UPDATE auction
                    SET auction_status = 'Closed',
                        winner_login = %s,
                        winner_role =
                            CASE
                                WHEN %s IS NULL THEN NULL
                                ELSE 'Buyer'
                            END
                    WHERE auction_id = %s;
                    """,
                    (
                        winner,
                        winner,
                        auction_id
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
                text=f"Unable to close auction: {error}",
                fg="red"
            )
            return

        if winner:
            status_label.config(
                text=f"Auction closed. Winner: {winner}",
                fg="green"
            )

        else:
            status_label.config(
                text="Auction closed with no bids",
                fg="green"
            )

    tk.Button(
        window,
        text="Close Auction",
        command=close_auction
    ).pack(pady=8)

    auction_entry.bind(
        "<Return>",
        lambda _event: close_auction()
    )