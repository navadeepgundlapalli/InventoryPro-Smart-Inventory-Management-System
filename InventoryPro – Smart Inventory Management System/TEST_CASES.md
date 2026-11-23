# InventoryPro Test Cases

| ID | Test | Steps | Expected |
|---|---|---|---|
| TC01 | Admin login | Use admin / Admin@123 | Dashboard appears |
| TC02 | Invalid login | Enter wrong password | Error shown |
| TC03 | Staff registration | Create staff with 8+ char password | Account created |
| TC04 | Add supplier | Enter supplier name and save | Supplier listed |
| TC05 | Add product | Enter unique SKU and valid values | Product saved |
| TC06 | Duplicate SKU | Reuse an existing SKU | Database rejects duplicate |
| TC07 | Stock-in | Add 10 units | Quantity increases by 10 |
| TC08 | Stock-out | Remove available units | Quantity decreases |
| TC09 | Excess stock-out | Remove more than available | Validation error; quantity unchanged |
| TC10 | CSV export | Export inventory | CSV file created |
| TC11 | Role access | Sign in as staff | User Accounts and delete action hidden |
