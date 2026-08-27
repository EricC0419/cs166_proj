-- Speeds up loading all items owned by a specific Seller.
CREATE INDEX IF NOT EXISTS idx_item_seller_login
ON item (seller_login);


-- Speeds up searches for a Seller's active or closed auctions.
CREATE INDEX IF NOT EXISTS idx_auction_seller_status
ON auction (seller_login, auction_status);


-- Speeds up loading bids for an auction and finding its highest bid.
CREATE INDEX IF NOT EXISTS idx_bid_auction_amount
ON bid (auction_id, bid_amount DESC);


-- Speeds up loading auctions associated with a specific Buyer.
CREATE INDEX IF NOT EXISTS idx_bid_buyer_login
ON bid (buyer_login);


-- Speeds up filtering and grouping items by category.
CREATE INDEX IF NOT EXISTS idx_item_category
ON item (category);