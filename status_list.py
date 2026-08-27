import tkinter as tk


def open_auction_statuses(parent, connection, login):

    status_window = tk.Toplevel(parent)
    status_window.title("Auction Statuses")
    status_window.geometry("500x400")

    title_label = tk.Label(
        status_window,
        text="My Auction Statuses",
        font=("Arial", 18, "bold")
    )
    title_label.pack(pady=15)

    status_text = tk.Text(
        status_window,
        width=50,
        height=15
    )
    status_text.pack(pady=10)

    def show_auction_statuses():

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT DISTINCT
                a.auctionID,
                a.status
            FROM Auction a
            LEFT JOIN Bid b
                ON a.auctionID = b.auctionID
            WHERE a.sellerID = %s
               OR b.buyerID = %s
            ORDER BY a.auctionID;
            """,
            (current_user_id, current_user_id)
        )

        results = cursor.fetchall()

        cursor.close()

        # Clear previous results
        status_text.delete("1.0", tk.END)

        if len(results) == 0:
            status_text.insert(
                tk.END,
                "You are not associated with any auctions."
            )

        else:
            for auction_id, status in results:

                status_text.insert(
                    tk.END,
                    f"Auction {auction_id}: {status}\n"
                )

    refresh_button = tk.Button(
        status_window,
        text="Refresh",
        command=show_auction_statuses
    )
    refresh_button.pack(pady=10)
    show_auction_statuses()