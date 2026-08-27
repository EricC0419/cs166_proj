import tkinter as tk


# Bid window
def open_bid(parent, conn, auction_id):

    bid_window = tk.Toplevel(parent)

    bid_window.title("Place Bid")
    bid_window.geometry("500x400")


    auction_label = tk.Label(
        bid_window,
        text="Auction ID: " + str(auction_id)
    )

    auction_label.grid(
        row=0,
        column=0,
        padx=20,
        pady=20
    )


    bid_label = tk.Label(
        bid_window,
        text="Bid Amount:"
    )

    bid_label.grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )


    bid_entry = tk.Entry(
        bid_window,
        width=20
    )

    bid_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )


# Auction search window


def open_auction_search(dashboard, conn):

    search_window = tk.Toplevel(dashboard)

    search_window.title("Search Auction")
    search_window.geometry("500x500")


    # --------------------------------------------------
    # Search function
    # --------------------------------------------------

    def search_auction():

        # Get value from GUI
        auction_id = auction_entry.get()
        # Create cursor
        cursor = conn.cursor()
        # Search database
        cursor.execute(
            """
            SELECT
                auction.auction_id,
                item.item_name,
                item.category,
                item.starting_price,
                auction.current_highest_bid,
                auction.auction_status,
                auction.seller_login
            FROM auction
            JOIN item
                ON auction.item_id = item.item_id
            WHERE auction.auction_id = %s;
            """,
            (auction_id,)
        )


        # Get one auction
        auction = cursor.fetchone()

        cursor.close()


        # --------------------------------------------------
        # Auction found
        # --------------------------------------------------

        if auction:

            result_label.config(
                text=
                    "Auction ID: " + str(auction[0]) +
                    "\nItem Name: " + str(auction[1]) +
                    "\nCategory: " + str(auction[2]) +
                    "\nStarting Price: $" + str(auction[3]) +
                    "\nCurrent Highest Bid: $" + str(auction[4]) +
                    "\nAuction Status: " + str(auction[5]) +
                    "\nSeller: " + str(auction[6])
            )


            # Enable Place Bid button
            bid_button.config(
                state="normal", #this lets you click on it 

                command=lambda: open_bid(
                    search_window,
                    conn,
                    auction[0]
                )
            )


        # Auction not found
        else:
            result_label.config(
                text="Auction not found"
            )
            bid_button.config(
                state="disabled"
            )


    # Title

    title = tk.Label(
        search_window,
        text="Search Auction",
        font=("Arial", 20)
    )

    title.grid(
        row=0,
        column=0,
        columnspan=2,
        pady=20
    )


    # Auction ID label

    auction_label = tk.Label(
        search_window,
        text="Auction ID:"
    )

    auction_label.grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )


    # Auction ID entry

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


    # Search button

    search_button = tk.Button(
        search_window,
        text="Search",
        command=search_auction
    )

    search_button.grid(
        row=2,
        column=0,
        columnspan=2,
        pady=10
    )


    
    # Search results

    result_label = tk.Label(
        search_window,
        text="",
        justify="left"
    )

    result_label.grid(
        row=3,
        column=0,
        columnspan=2,
        padx=20,
        pady=20
    )


    # Place Bid button

    bid_button = tk.Button(
        search_window,
        text="Place Bid",

        # Cannot place bid until valid auction is found
        state="disabled"
    )

    bid_button.grid(
        row=4,
        column=0,
        columnspan=2,
        pady=10
    )