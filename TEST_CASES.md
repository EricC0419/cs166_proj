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

## 12. Account Registration

### Normal Case

- Login: `demo_buyer`
- Password and Confirmation: `demopass`
- Phone: `555-7777`
- Address: `7 Demo Street`
- Expected: The account is created with the default Buyer role.
- The new user can log in and open the Buyer Dashboard.

### Edge Case

- Enter different values for Password and Confirm Password.
- Expected: The screen displays `Passwords do not match`.
- No account is inserted.

---

## 13. Admin Item Management

### Normal Case

- Select a disposable demo item.
- Click Remove Selected Item and confirm.
- Expected: The item and its related auction records are removed.

### Edge Case

- Do not select an item.
- Click Remove Selected Item.
- Expected: The screen displays `Select an item first`.
- No data is deleted.

---

## 14. Admin Payment Management

### Normal Case

- Select Payment `401`.
- Change its status to `Pending`.
- Expected: The table refreshes and displays `Pending`.

### Edge Case

- Do not select a payment.
- Click Update Payment Status.
- Expected: The screen displays `Select a payment first`.
- No payment changes.

---

## 15. Admin Shipment Management

### Normal Case

- Select Shipment `501`.
- Change its status to `Delivered`.
- Enter tracking number `DEMO-DELIVERED-501`.
- Expected: The updated status and tracking number appear after refresh.

### Edge Case

- Do not select a shipment.
- Click Update Shipment.
- Expected: The screen displays `Select a shipment first`.
- No shipment changes.