import sys
import tkinter as tk
from tkinter import messagebox

import psycopg2

from login import open_login


def connect_database():
    if len(sys.argv) != 4:
        raise ValueError(
            f"Usage: python3 {sys.argv[0]} <dbname> <port> <user>"
        )

    return psycopg2.connect(
        dbname=sys.argv[1],
        port=sys.argv[2],
        user=sys.argv[3],
        host="localhost"
    )


def main():
    root = tk.Tk()
    root.title("Online Auction and Bidding System")
    root.geometry("420x240")

    try:
        connection = connect_database()
    except Exception as error:
        messagebox.showerror("Database Connection Error", str(error))
        root.destroy()
        return

    def close_app():
        connection.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", close_app)

    open_login(root, connection)
    root.mainloop()


if __name__ == "__main__":
    main()