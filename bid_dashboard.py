import tkinter as tk


def open_bid(parent, conn, auction_id, buyer_login):

    # Create bid window
    bid_window = tk.Toplevel(parent)

    bid_window.title("Place Bid")
    bid_window.geometry("500x400")

    # Get current auction information

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            seller_login,
            current_highest_bid,
            auction_status
        FROM auction
        WHERE auction_id = %s;
        """,
        (auction_id,)
    )

    auction = cursor.fetchone()

    cursor.close()


    seller_login = auction[0]
    current_highest_bid = auction[1]
    auction_status = auction[2]


    # Place bid function

    def place_bid():

        bid_input = bid_entry.get()
        # Bid must be positive
        if bid_amount <= 0:
            status_label.config(
                text="Bid must be greater than $0"
            )
            return
        cursor = conn.cursor()

        # Get newest auction information
        cursor.execute(
            """
            SELECT
                seller_login,
                current_highest_bid,
                auction_status
            FROM auction
            WHERE auction_id = %s;
            """,
            (auction_id,)
        )
        current_auction = cursor.fetchone()
        current_seller = current_auction[0]
        current_bid = current_auction[1]
        current_status = current_auction[2]


        # Check auction status
        if current_status != "Active":
            status_label.config(
                text="This auction is closed"
            )

            cursor.close()

            return


        # Seller cannot bid on own auction

        if buyer_login == current_seller:

            status_label.config(
                text="You cannot bid on your own auction"
            )
            cursor.close()
            return
        # New bid must be higher
        if bid_amount <= current_bid:

            status_label.config(
                text="Bid must be higher than $" + str(current_bid)
            )

            cursor.close()

            return
        # Generate bid ID adds one to the current max of the bid and sets it as new bid_id
        cursor.execute(
            """
            SELECT COALESCE(MAX(bid_id), 0) + 1 
            FROM bid;
            """
        )

        bid_id = cursor.fetchone()[0]
        # Insert new bid
        cursor.execute(
            """
            INSERT INTO bid (
                bid_id,
                auction_id,
                buyer_login,
                buyer_role,
                bid_amount
            )
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                bid_id,
                auction_id,
                buyer_login,
                "Buyer",
                bid_amount
            )
        )
        # Update highest bid
        cursor.execute(
            """
            UPDATE auction
            SET current_highest_bid = %s
            WHERE auction_id = %s;
            """,
            (
                bid_amount,
                auction_id
            )
        )
        # Save changes
        conn.commit()
        cursor.close()
        # Update GUI
        current_bid_value.config(
            text="$" + str(bid_amount)
        )
        status_label.config(
            text="Bid placed successfully"
        )
    # GUI title
    title = tk.Label(
        bid_window,
        text="Place Bid",
        font=("Arial", 20)
    )

    title.grid(
        row=0,
        column=0,
        columnspan=2,
        pady=20
    )
    # Auction ID

    auction_label = tk.Label(
        bid_window,
        text="Auction ID:"
    )

    auction_label.grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )


    auction_value = tk.Label(
        bid_window,
        text=str(auction_id)
    )

    auction_value.grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )

    # Buyer

    buyer_label = tk.Label(
        bid_window,
        text="Buyer:"
    )

    buyer_label.grid(
        row=2,
        column=0,
        padx=10,
        pady=10
    )


    buyer_value = tk.Label(
        bid_window,
        text=buyer_login
    )

    buyer_value.grid(
        row=2,
        column=1,
        padx=10,
        pady=10
    )


    # Current highest bid

    current_bid_label = tk.Label(
        bid_window,
        text="Current Highest Bid:"
    )

    current_bid_label.grid(
        row=3,
        column=0,
        padx=10,
        pady=10
    )


    current_bid_value = tk.Label(
        bid_window,
        text="$" + str(current_highest_bid)
    )

    current_bid_value.grid(
        row=3,
        column=1,
        padx=10,
        pady=10
    )


    # New bid

    bid_label = tk.Label(
        bid_window,
        text="Your Bid:"
    )

    bid_label.grid(
        row=4,
        column=0,
        padx=10,
        pady=10
    )


    bid_entry = tk.Entry(
        bid_window,
        width=20
    )

    bid_entry.grid(
        row=4,
        column=1,
        padx=10,
        pady=10
    )


    # Place bid button

    bid_button = tk.Button(
        bid_window,
        text="Place Bid",
        command=place_bid
    )

    bid_button.grid(
        row=5,
        column=0,
        columnspan=2,
        pady=15
    )

    # Status message

    status_label = tk.Label(
        bid_window,
        text=""
    )

    status_label.grid(
        row=6,
        column=0,
        columnspan=2,
        pady=10
    )