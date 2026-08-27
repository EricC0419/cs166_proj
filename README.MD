# Online Auction and Bidding System

## Project Overview

This project implements an eBay-style auction platform with a Python Tkinter client and PostgreSQL database. The application supports Buyer, Seller, and Admin workflows.

## System Architecture

The application uses a client-server structure:

- The Tkinter GUI runs locally on the user's computer.
- PostgreSQL runs on the UCR CS166 server.
- VS Code port forwarding connects the local client to the remote database.

## Features

### All Users

- Log in
- Create a new Buyer account
- Search for items
- Search for auctions
- View auction statuses
- Update profile information

### Buyer

- Place bids on active auctions
- View auctions associated with their bids
- Receive validation for invalid or low bids

### Seller

- Create item and auction listings
- Update owned items
- View owned auctions
- Close owned auctions
- Assign the highest bidder as the winner

### Admin

- View every auction
- Change user roles
- Close active auctions
- View and remove items
- Update payment status
- Update shipment status and tracking information

## Project Files

- `Project Phase 2 - Solution.sql`: Creates all project tables and constraints.
- `indexes.sql`: Creates indexes for frequently searched columns.
- `seed_data.sql`: Inserts prepared demonstration data.
- `TEST_CASES.md`: Lists normal and edge cases for the presentation.
- `main.py`: Connects the client to PostgreSQL and launches the application.
- `login.py`: Handles user authentication and role-based dashboard routing.
- `register.py`: Creates new accounts with the default Buyer role.
- `buyer_dashboard.py`: Displays Buyer functions.
- `seller_dashboard.py`: Displays Seller functions.
- `admin_dashboard.py`: Displays Admin functions.
- `item_dashboard.py`: Searches for items by name or category.
- `auction_dashboard.py`: Searches for auctions and opens the bid screen.
- `bid_dashboard.py`: Validates and records bids.
- `status_list.py`: Displays auction statuses.
- `sell_item.py`: Creates listings and updates Seller-owned items.
- `close_auction.py`: Closes Seller-owned auctions and assigns winners.
- `edit_profile.py`: Updates user profile information.
- `manager.py`: Manages user roles and auctions.
- `admin_records.py`: Manages items, payments, and shipments.

## Database Setup on the CS166 Server

Replace `<NETID>` with the user's UCR NetID.

Connect to the server:

```bash
ssh <NETID>@cs166.cs.ucr.edu
```

Start PostgreSQL:

```bash
cs166_db_start
```

Check the assigned PostgreSQL port:

```bash
echo $PGPORT
```

Create the project database once:

```bash
createdb -h localhost -p $PGPORT <NETID>_project_DB
```

Create the tables:

```bash
cs166_psql <NETID>_project_DB < "Project Phase 2 - Solution.sql"
```

Create the indexes:

```bash
cs166_psql <NETID>_project_DB < indexes.sql
```

Load the demonstration data:

```bash
cs166_psql <NETID>_project_DB < seed_data.sql
```

## Reset Demonstration Data

The demonstration changes bids, profiles, roles, payments, shipments, and auction statuses. Reset the database before rehearsing or presenting:

```bash
cs166_psql <NETID>_project_DB < "Project Phase 2 - Solution.sql"
cs166_psql <NETID>_project_DB < indexes.sql
cs166_psql <NETID>_project_DB < seed_data.sql
```

## Local Python Setup

Create and activate a Python 3.12 Conda environment:

```bash
conda create -n cs166 python=3.12 -y
conda activate cs166
```

Install the required PostgreSQL driver:

```bash
python -m pip install -r requirements.txt
```

## Port Forwarding

In the VS Code window connected to the CS166 server:

1. Open the Ports tab.
2. Select **Forward a Port**.
3. Enter the PostgreSQL port shown by `echo $PGPORT`.
4. Keep the SSH connection open while using the application.

## Run the Application

Replace `<PORT>` with the PostgreSQL port shown by `echo $PGPORT`.

From the local project folder:

```bash
conda activate cs166
python main.py <NETID>_project_DB <PORT> <NETID>
```

## Demonstration Accounts

| Role | Login | Password |
|---|---|---|
| Buyer | `buyer1` | `buyerpass` |
| Buyer | `buyer2` | `buyerpass2` |
| Seller | `seller1` | `sellerpass` |
| Admin | `admin1` | `adminpass` |
| Unassociated User | `newuser` | `newpass` |

## Index Design

The project adds indexes to columns used frequently by item, auction, and bid queries:

- `item.seller_login`
- `auction.seller_login` and `auction.auction_status`
- `bid.auction_id` and `bid.bid_amount`
- `bid.buyer_login`
- `item.category`

PostgreSQL automatically creates indexes for primary-key columns.

## Error Handling

The application uses parameterized SQL queries, transaction commits, and rollbacks. It handles cases such as:

- Invalid login
- Blank required profile or registration fields
- Invalid auction IDs
- Bids below the current highest bid
- Bids on closed auctions
- Sellers bidding on their own auctions
- Duplicate item or auction IDs
- Unauthorized item updates
- Closing an already closed auction
- Admin actions without a selected record

## Assumptions and Limitations

- Passwords are stored as plain text for this course demonstration. A production system must hash passwords.
- Item and auction IDs are entered manually for the demonstration.
- Each account has one role at a time.
- Newly registered accounts receive the Buyer role by default.
- An Admin changes roles for Seller or Admin access.
- PostgreSQL must remain running on the CS166 server.
- The SSH connection and forwarded port must remain active while the local GUI is running.

## Team Contributions

### Eric Chang

- Designed and created the initial Tkinter application structure.
- Implemented the original login interface and role-based application flow.
- Implemented the original Buyer and Admin dashboard layouts.
- Implemented the original auction search workflow.
- Implemented the original item search workflow.
- Implemented the original bid interface and bidding workflow.
- Implemented the original auction-status interface.
- Developed the initial GUI design and navigation used throughout the final application.
- Helped define the Phase 2 database tables and the overall project structure.

### Chau Truong

- Integrated the Python client with the Phase 2 PostgreSQL schema.
- Connected the existing interfaces through consistent user and database parameters.
- Added database transactions, validation, and error handling.
- Implemented the Seller dashboard and Seller listing/update workflow.
- Implemented Seller auction closing and winner assignment.
- Implemented profile updates and new account registration.
- Implemented Admin role, auction, item, payment, and shipment management.
- Added database indexes and prepared demonstration data.
- Created the presentation test cases and project setup documentation.
- Set up and tested the local client, SSH connection, port forwarding, and PostgreSQL database.
- Performed end-to-end integration and runtime testing.