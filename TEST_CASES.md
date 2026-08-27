# Online Auction System Presentation Test Cases

Run the Phase 2 schema, `indexes.sql`, and `seed_data.sql` before testing.

Because bidding, profile updates, role changes, and auction closing modify the
database, recreate the database before the final presentation rehearsal.

---

## 1. Login

### Normal Case

- Input: `buyer1` / `buyerpass`
- Expected: The Buyer Dashboard opens and displays `buyer1`.

### Edge Case

- Input: `buyer1` / `wrongpassword`
- Expected: The login screen displays `Invalid login`.
- The program does not open a dashboard or crash.

---

## 2. Item Search

### Normal Case

- Input: Search for `Laptop`
- Expected: The Gaming Laptop and auction 201 appear.

### Edge Case

- Input: Search for `NonexistentXYZ`
- Expected: The table remains empty and displays `No matching items`.

---

## 3. Auction Search

### Normal Case

- Input: Search for auction `201` as `buyer1`
- Expected: The Gaming Laptop auction details appear.
- The Place Bid button is enabled because the auction is active.

### Edge Case

- Input: Search for `abc`
- Expected: The screen displays `Auction ID must be a whole number`.
- The program does not crash.

---

## 4. Place Bid

### Normal Case

- Login: `buyer2` / `buyerpass2`
- Auction: `201`
- Bid: `130`
- Expected: The bid is accepted and the highest bid becomes `$130.00`.

### Edge Case

- Auction: `201`
- Bid: `110`
- Expected: The bid is rejected because it is not higher than the current bid.
- No bid is inserted.

---

## 5. Auction Statuses

### Normal Case

- Login: `buyer1` / `buyerpass`
- Expected: Auction 201 appears because buyer1 placed a bid.

### Edge Case

- Login: `newuser` / `newpass`
- Expected: The screen displays:
  `You are not associated with any auctions.`

---

## 6. Profile Update

### Normal Case

- Login: `buyer1` / `buyerpass`
- Change the address to `100 Updated Road`.
- Expected: The screen displays `Profile updated successfully`.
- The new address remains after reopening the window.

### Edge Case

- Clear the phone-number field and select Save Changes.
- Expected: The screen displays:
  `Phone number and address are required`.
- The database remains unchanged.

---

## 7. Create Seller Listing

### Normal Case

- Login: `seller1` / `sellerpass`
- Item ID: `105`
- Auction ID: `205`
- Item Name: `Wireless Mouse`
- Category: `Electronics`
- Starting Price: `20`
- Condition: `New`
- Expected: The item and active auction are created.

### Edge Case

- Reuse Item ID `101`.
- Expected: The database displays a duplicate-key error.
- Neither a partial item nor a partial auction is committed.

---

## 8. Update Seller Item

### Normal Case

- Select Item ID `103`.
- Change its condition to `Used - Excellent`.
- Expected: The screen displays `Item updated successfully`.
- The updated value remains after refreshing.

### Edge Case

- Enter Item ID `999`.
- Expected: The screen displays:
  `Item not found or you do not own it`.
- No database row changes.

---

## 9. Close Seller Auction

### Normal Case

- Login: `seller1` / `sellerpass`
- Close Auction `201`.
- Expected: The auction becomes `Closed`.
- The highest bidder becomes the winner.

### Edge Case

- Try to close Auction `202`.
- Expected: The screen displays `Auction is already closed`.
- The database remains unchanged.

### Boundary Case

- Close Auction `203`, which has no bids.
- Expected: The auction closes and displays:
  `Auction closed with no bids`.

---

## 10. Admin Role Management

### Normal Case

- Login: `admin1` / `adminpass`
- Select `newuser`.
- Change the role from Buyer to Seller.
- Expected: The role table refreshes and displays Seller.

### Edge Case

- Do not select a user.
- Select Update Selected User's Role.
- Expected: The screen displays `Select a user first`.
- No user role changes.

---

## 11. Admin Auction Management

### Normal Case

- Select active Auction `204`.
- Select Terminate Selected Auction.
- Confirm the action.
- Expected: Auction 204 changes from `Active` to `Closed`.

### Edge Case

- Select already closed Auction `202`.
- Expected: The screen displays:
  `Only an active auction can be terminated`.
- The auction remains closed.

---

# Suggested Ten-Minute Presentation Order

1. Introduce the PostgreSQL auction system and its three roles.
2. Demonstrate one invalid and one valid Buyer login.
3. Search for an item and auction.
4. Place one invalid bid and one valid bid.
5. Show Buyer auction status and profile update.
6. Log in as Seller and create or update an item.
7. Close an auction.
8. Log in as Admin and show role and auction management.
9. Briefly explain the indexes and transaction rollback.
10. End by mentioning that every major function has normal and edge tests.