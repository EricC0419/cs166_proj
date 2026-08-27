# main.py
import tkinter as tk
import psycopg2

from login import open_login


# # Connect to PostgreSQL
# conn = psycopg2.connect(
#     dbname="your_database",
#     user="your_username",
#     password="your_password",
#     host="localhost",
#     port="5432"
# )


# Create main window
root = tk.Tk()

open_login(root, conn)

root.mainloop()


# Close database connection when app ends
conn.close()