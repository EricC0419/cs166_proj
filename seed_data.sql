-- Test accounts for each role.
INSERT INTO users (
    login,
    password,
    phone_num,
    address,
    role,
    favorite_category
)
VALUES
    (
        'buyer1',
        'buyerpass',
        '555-1001',
        '1 Buyer Way',
        'Buyer',
        'Electronics'
    ),
    (
        'buyer2',
        'buyerpass2',
        '555-1002',
        '2 Buyer Way',
        'Buyer',
        'Cameras'
    ),
    (
        'seller1',
        'sellerpass',
        '555-2001',
        '10 Seller Street',
        'Seller',
        'Electronics'
    ),
    (
        'admin1',
        'adminpass',
        '555-9001',
        '99 Admin Avenue',
        'Admin',
        NULL
    ),
    (
        'newuser',
        'newpass',
        '555-3001',
        '3 New User Road',
        'Buyer',
        NULL
    );


-- Sample items owned by seller1.
INSERT INTO item (
    item_id,
    item_name,
    category,
    starting_price,
    image_url,
    item_condition,
    description,
    seller_login,
    seller_role
)
VALUES
    (
        101,
        'Gaming Laptop',
        'Electronics',
        100.00,
        NULL,
        'Used - Good',
        'Demo laptop listing',
        'seller1',
        'Seller'
    ),
    (
        102,
        'Film Camera',
        'Cameras',
        75.00,
        NULL,
        'Used - Excellent',
        'Demo camera listing',
        'seller1',
        'Seller'
    ),
    (
        103,
        'Mechanical Keyboard',
        'Electronics',
        25.00,
        NULL,
        'New',
        'Demo keyboard listing',
        'seller1',
        'Seller'
    ),
    (
        104,
        'Desk Lamp',
        'Home',
        15.00,
        NULL,
        'Used - Good',
        'Demo lamp listing',
        'seller1',
        'Seller'
    );


-- Active, closed, and no-bid auctions.
INSERT INTO auction (
    auction_id,
    item_id,
    seller_login,
    seller_role,
    current_highest_bid,
    auction_status,
    winner_login,
    winner_role
)
VALUES
    (
        201,
        101,
        'seller1',
        'Seller',
        120.00,
        'Active',
        NULL,
        NULL
    ),
    (
        202,
        102,
        'seller1',
        'Seller',
        90.00,
        'Closed',
        'buyer2',
        'Buyer'
    ),
    (
        203,
        103,
        'seller1',
        'Seller',
        25.00,
        'Active',
        NULL,
        NULL
    ),
    (
        204,
        104,
        'seller1',
        'Seller',
        15.00,
        'Active',
        NULL,
        NULL
    );


-- Existing bids for bid and auction-status testing.
INSERT INTO bid (
    bid_id,
    auction_id,
    buyer_login,
    buyer_role,
    bid_amount
)
VALUES
    (
        301,
        201,
        'buyer1',
        'Buyer',
        120.00
    ),
    (
        302,
        202,
        'buyer2',
        'Buyer',
        90.00
    );


-- Completed payment for the closed auction.
INSERT INTO payment (
    payment_id,
    auction_id,
    buyer_login,
    buyer_role,
    amount,
    payment_status
)
VALUES
    (
        401,
        202,
        'buyer2',
        'Buyer',
        90.00,
        'Completed'
    );


-- Existing shipment for the closed auction.
INSERT INTO shipment (
    shipment_id,
    auction_id,
    address,
    shipment_status,
    tracking_number
)
VALUES
    (
        501,
        202,
        '2 Buyer Way',
        'Shipped',
        'DEMO-TRACK-202'
    );