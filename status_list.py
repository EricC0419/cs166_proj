# updated names
import tkinter as tk


def open_auction_statuses(parent, connection, login):

    status_window = tk.Toplevel(parent)
    status_window.title("Auction Statuses")
    status_window.geometry("700x450")

    title_label = tk.Label(
        status_window,
        text="Auction Statuses",
        font=("Arial", 18, "bold")
    )
    title_label.pack(pady=15)

    status_text = tk.Text(
        status_window,
        width=80,
        height=17
    )
    status_text.pack(pady=10)

    def show_auction_statuses():

        try:
            cursor = connection.cursor()

            # Find the role of the currently logged-in user.
            cursor.execute(
                """
                SELECT role
                FROM users
                WHERE login = %s;
                """,
                (login,)
            )

            role_result = cursor.fetchone()

            if not role_result:
                raise ValueError("User not found")

            role = role_result[0]

            # Admins can monitor every auction.
            if role == "Admin":
                cursor.execute(
                    """
                    SELECT
                        a.auction_id,
                        i.item_name,
                        a.auction_status,
                        a.current_highest_bid,
                        a.seller_login,
                        a.winner_login
                    FROM auction AS a
                    JOIN item AS i
                        ON a.item_id = i.item_id
                    ORDER BY a.auction_id;
                    """
                )

            # Buyers and Sellers only see auctions connected to them.
            else:
                cursor.execute(
                    """
                    SELECT DISTINCT
                        a.auction_id,
                        i.item_name,
                        a.auction_status,
                        a.current_highest_bid,
                        a.seller_login,
                        a.winner_login
                    FROM auction AS a
                    JOIN item AS i
                        ON a.item_id = i.item_id
                    LEFT JOIN bid AS b
                        ON a.auction_id = b.auction_id
                    WHERE a.seller_login = %s
                       OR b.buyer_login = %s
                    ORDER BY a.auction_id;
                    """,
                    (login, login)
                )

            results = cursor.fetchall()
            cursor.close()

        except Exception as error:
            connection.rollback()

            status_text.delete(
                "1.0",
                tk.END
            )

            status_text.insert(
                tk.END,
                f"Unable to load auctions: {error}"
            )
            return

        # Clear previous results.
        status_text.delete(
            "1.0",
            tk.END
        )

        if len(results) == 0:
            status_text.insert(
                tk.END,
                "You are not associated with any auctions."
            )

        else:
            for result in results:
                auction_id = result[0]
                item_name = result[1]
                auction_status = result[2]
                highest_bid = result[3]
                seller_login = result[4]
                winner_login = result[5] or "None"

                status_text.insert(
                    tk.END,
                    (
                        f"Auction {auction_id} | "
                        f"{item_name} | "
                        f"{auction_status} | "
                        f"Highest Bid: ${highest_bid} | "
                        f"Seller: {seller_login} | "
                        f"Winner: {winner_login}\n"
                    )
                )

    refresh_button = tk.Button(
        status_window,
        text="Refresh",
        command=show_auction_statuses
    )
    refresh_button.pack(pady=10)

    show_auction_statuses()