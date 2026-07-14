# Inventory Management System

A menu-driven, terminal-based inventory and sales management tool built for the **InfoBharat Items — Python Development Internship**. Data is stored in local CSV files, so no database setup is required.

## Features

- **Product Management** — add, view, search, update, and delete products
- **Stock Management** — add stock and get low-stock alerts
- **Sales Management** — record sales and view sales summaries
- **Reporting** — inventory and sales reports
- **Product Images** — attach an image to each product and view it as ASCII art directly in the terminal

## Requirements

- Python 3.7+
- [Pillow](https://pypi.org/project/Pillow/) (only needed for the image-viewing feature)

Install Pillow with:

```bash
pip install Pillow
```

The rest of the program works fine without Pillow — image viewing will just be disabled with a notice.

## Getting Started

1. Make sure `inventory_management.py` is in your working directory.
2. Run the program:

   ```bash
   python inventory_management.py
   ```

3. On first run, `products.csv` and `sales.csv` will be created automatically as you add data.

## Menu Options

| # | Option              | Description                                      |
|---|---------------------|---------------------------------------------------|
| 1 | Add Product         | Create a new product record                        |
| 2 | View Products       | List all products in a table                       |
| 3 | Search Product      | Search by Product ID or Name                       |
| 4 | Update Product      | Edit an existing product's details                 |
| 5 | Delete Product      | Remove a product (with confirmation)               |
| 6 | Add Stock           | Increase quantity for an existing product          |
| 7 | Low Stock Alert     | List products below the stock threshold            |
| 8 | Record Sale         | Log a sale and reduce stock accordingly            |
| 9 | Sales Summary       | Totals and best-selling product                    |
| 10| Inventory Report    | Overview of stock and categories                   |
| 11| Sales Report        | Overview of transactions and revenue               |
| 12| View Product Image  | Display a product's image as ASCII art             |
| 0 | Exit                | Save and quit                                      |

## Data Files

### `products.csv`
| Column       | Description                          |
|--------------|---------------------------------------|
| product_id   | Unique identifier                     |
| name         | Product name                          |
| category     | Product category                      |
| price        | Unit price                            |
| quantity     | Units in stock                        |
| supplier     | Supplier name                         |
| image_path   | Path to an image file (optional)      |

### `sales.csv`
| Column          | Description                        |
|-----------------|--------------------------------------|
| sale_id         | Auto-generated sale ID (e.g. SALE0001) |
| product_id      | ID of the product sold                |
| product_name    | Name of the product sold              |
| quantity_sold   | Units sold                            |
| total_amount    | Total transaction value               |
| date            | Timestamp of the sale                 |

## Notes on Product Images

- When adding or updating a product, you can enter a path to a local image file (e.g. `images/laptop.jpg`).
- The image itself is **not stored inside the CSV** — only the file path is saved, so the image file must remain at that location to be viewable later.
- ASCII rendering is a lightweight text approximation, not a true image render — best used as a quick visual reference rather than a high-fidelity photo.

## Low Stock Threshold

By default, products with quantity below **10** trigger a low-stock alert. This can be changed by editing the `LOW_STOCK_THRESHOLD` constant near the top of `inventory_management.py`.
## Author
Name:Telu Amrutha
Project: Inventory Management
## License
This project was developed for educational and academic purpose
