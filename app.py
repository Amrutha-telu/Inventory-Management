"""
Inventory Management System
InfoBharat Items - Python Development Internship
(Now with product image support - displayed as ASCII art in terminal)
"""

import csv
import json
import os
from datetime import datetime

# ─────────────────────────────────────────────
# OPTIONAL DEPENDENCY: Pillow (for image display)
# ─────────────────────────────────────────────
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ─────────────────────────────────────────────
# FILE PATHS
# ─────────────────────────────────────────────
PRODUCTS_FILE = "products.csv"
SALES_FILE = "sales.csv"
LOW_STOCK_THRESHOLD = 10

# ASCII characters used for image rendering, from darkest to lightest
ASCII_CHARS = "@%#*+=-:. "


# ─────────────────────────────────────────────
# DATA STORAGE: CSV HELPERS
# ─────────────────────────────────────────────

def load_products():
    """Load products from CSV file."""
    products = []
    if not os.path.exists(PRODUCTS_FILE):
        return products
    try:
        with open(PRODUCTS_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["price"] = float(row["price"])
                row["quantity"] = int(row["quantity"])
                # Older CSV files may not have this column yet
                row["image_path"] = row.get("image_path", "") or ""
                products.append(row)
    except Exception as e:
        print(f"  [Error] Loading products: {e}")
    return products


def save_products(products):
    """Save products list to CSV file."""
    fieldnames = ["product_id", "name", "category", "price", "quantity",
                  "supplier", "image_path"]
    try:
        with open(PRODUCTS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in products:
                # Ensure every row has all fields, even older records
                row = {field: p.get(field, "") for field in fieldnames}
                writer.writerow(row)
    except Exception as e:
        print(f"  [Error] Saving products: {e}")


def load_sales():
    """Load sales records from CSV file."""
    sales = []
    if not os.path.exists(SALES_FILE):
        return sales
    try:
        with open(SALES_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not any(row.values()):
                    continue

                if "quantity_sold" not in row and "Quantity Sold" in row:
                    row["quantity_sold"] = row["Quantity Sold"]
                if "total_amount" not in row and "Amount" in row:
                    row["total_amount"] = row["Amount"]
                if "product_id" not in row and "Product ID" in row:
                    row["product_id"] = row["Product ID"]
                if "product_name" not in row and "Name" in row:
                    row["product_name"] = row["Name"]

                row["quantity_sold"] = int(row.get("quantity_sold", 0) or 0)
                row["total_amount"] = float(row.get("total_amount", 0.0) or 0.0)

                if "sale_id" not in row or not row["sale_id"]:
                    row["sale_id"] = f"SALE{len(sales) + 1:04d}"

                sales.append(row)
    except Exception as e:
        print(f"  [Error] Loading sales: {e}")
    return sales


def save_sales(sales):
    """Save sales records to CSV file."""
    fieldnames = ["sale_id", "product_id", "product_name", "quantity_sold",
                  "total_amount", "date"]
    try:
        with open(SALES_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sales)
    except Exception as e:
        print(f"  [Error] Saving sales: {e}")


# ─────────────────────────────────────────────
# IMAGE DISPLAY (ASCII ART IN TERMINAL)
# ─────────────────────────────────────────────

def display_image_ascii(image_path, width=60):
    """Render an image file as ASCII art directly in the terminal."""
    if not image_path:
        print("  [Info] No image set for this product.")
        return

    if not PIL_AVAILABLE:
        print("  [Error] Image display requires the 'Pillow' library.")
        print("          Install it with: pip install Pillow")
        return

    if not os.path.exists(image_path):
        print(f"  [Error] Image file not found: {image_path}")
        return

    try:
        img = Image.open(image_path).convert("L")  # grayscale

        # Maintain aspect ratio; terminal characters are taller than wide,
        # so we compress the height a bit (~0.5) to avoid a stretched look.
        aspect_ratio = img.height / img.width
        new_height = int(aspect_ratio * width * 0.5)
        img = img.resize((width, max(new_height, 1)))

        pixels = list(img.getdata())
        chars = [ASCII_CHARS[pixel * (len(ASCII_CHARS) - 1) // 255] for pixel in pixels]

        print()
        for row_start in range(0, len(chars), width):
            print("  " + "".join(chars[row_start:row_start + width]))
        print()
    except Exception as e:
        print(f"  [Error] Could not render image: {e}")


def view_product_image(products):
    """Prompt for a Product ID and display its image as ASCII art."""
    print("\n--- View Product Image ---")
    product_id = input("  Enter Product ID: ").strip()
    product = next((p for p in products if p["product_id"] == product_id), None)

    if not product:
        print(f"  [Error] Product ID '{product_id}' not found.")
        return

    print(f"  Product: {product['name']}")
    display_image_ascii(product.get("image_path", ""))


# ─────────────────────────────────────────────
# MODULE 1: PRODUCT MANAGEMENT
# ─────────────────────────────────────────────

def add_product(products):
    """Add a new product to inventory."""
    print("\n--- Add New Product ---")
    product_id = input("  Enter Product ID: ").strip()
    if not product_id:
        print("  [Error] Product ID cannot be empty.")
        return

    # Check for duplicate
    if any(p["product_id"] == product_id for p in products):
        print(f"  [Error] Product ID '{product_id}' already exists.")
        return

    name = input("  Enter Product Name: ").strip()
    if not name:
        print("  [Error] Product name cannot be empty.")
        return

    category = input("  Enter Category: ").strip()

    try:
        price = float(input("  Enter Price: "))
        if price < 0:
            raise ValueError
    except ValueError:
        print("  [Error] Invalid price. Must be a non-negative number.")
        return

    try:
        quantity = int(input("  Enter Quantity: "))
        if quantity < 0:
            raise ValueError
    except ValueError:
        print("  [Error] Invalid quantity. Must be a non-negative integer.")
        return

    supplier = input("  Enter Supplier Name: ").strip()

    image_path = input("  Enter Image Path (optional, Enter to skip): ").strip()
    if image_path and not os.path.exists(image_path):
        print(f"  [Warning] File not found at '{image_path}'. Saving path anyway.")

    product = {
        "product_id": product_id,
        "name": name,
        "category": category,
        "price": price,
        "quantity": quantity,
        "supplier": supplier,
        "image_path": image_path,
    }
    products.append(product)
    save_products(products)
    print(f"  [Success] Product '{name}' added successfully!")


def view_products(products):
    """Display all products in a tabular format."""
    print("\n--- All Products ---")
    if not products:
        print("  No products found.")
        return

    # Header
    print(f"  {'ID':<12} {'Name':<20} {'Category':<15} {'Price':>8} {'Qty':>6} {'Supplier':<20} {'Image':<6}")
    print("  " + "-" * 92)
    for p in products:
        has_image = "Yes" if p.get("image_path") else "No"
        print(f"  {p['product_id']:<12} {p['name']:<20} {p['category']:<15} "
              f"{p['price']:>8.2f} {p['quantity']:>6} {p['supplier']:<20} {has_image:<6}")
    print(f"\n  Total Products: {len(products)}")


def search_product(products):
    """Search products by ID or name."""
    print("\n--- Search Product ---")
    query = input("  Enter Product ID or Name to search: ").strip().lower()
    if not query:
        print("  [Error] Search query cannot be empty.")
        return

    results = [p for p in products if
               query in p["product_id"].lower() or query in p["name"].lower()]

    if not results:
        print(f"  [Not Found] No products matching '{query}'.")
        return

    print(f"\n  Found {len(results)} result(s):")
    print(f"  {'ID':<12} {'Name':<20} {'Category':<15} {'Price':>8} {'Qty':>6} {'Supplier':<20}")
    print("  " + "-" * 85)
    for p in results:
        print(f"  {p['product_id']:<12} {p['name']:<20} {p['category']:<15} "
              f"{p['price']:>8.2f} {p['quantity']:>6} {p['supplier']:<20}")


def update_product(products):
    """Update product details."""
    print("\n--- Update Product ---")
    product_id = input("  Enter Product ID to update: ").strip()
    product = next((p for p in products if p["product_id"] == product_id), None)

    if not product:
        print(f"  [Error] Product ID '{product_id}' not found.")
        return

    print(f"  Current: {product['name']} | {product['category']} | "
          f"₹{product['price']} | Qty: {product['quantity']}")

    name = input(f"  New Name (Enter to keep '{product['name']}'): ").strip()
    if name:
        product["name"] = name

    category = input(f"  New Category (Enter to keep '{product['category']}'): ").strip()
    if category:
        product["category"] = category

    price_str = input(f"  New Price (Enter to keep {product['price']}): ").strip()
    if price_str:
        try:
            price = float(price_str)
            if price < 0:
                raise ValueError
            product["price"] = price
        except ValueError:
            print("  [Error] Invalid price. Keeping original.")

    qty_str = input(f"  New Quantity (Enter to keep {product['quantity']}): ").strip()
    if qty_str:
        try:
            qty = int(qty_str)
            if qty < 0:
                raise ValueError
            product["quantity"] = qty
        except ValueError:
            print("  [Error] Invalid quantity. Keeping original.")

    current_image = product.get("image_path", "") or "(none)"
    image_str = input(f"  New Image Path (Enter to keep '{current_image}'): ").strip()
    if image_str:
        product["image_path"] = image_str

    save_products(products)
    print("  [Success] Product updated successfully!")


def delete_product(products):
    """Delete a product by Product ID."""
    print("\n--- Delete Product ---")
    product_id = input("  Enter Product ID to delete: ").strip()
    product = next((p for p in products if p["product_id"] == product_id), None)

    if not product:
        print(f"  [Error] Product ID '{product_id}' not found.")
        return

    confirm = input(f"  Are you sure you want to delete '{product['name']}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        products.remove(product)
        save_products(products)
        print("  [Success] Product deleted successfully!")
    else:
        print("  Deletion cancelled.")


# ─────────────────────────────────────────────
# MODULE 2: STOCK MANAGEMENT
# ─────────────────────────────────────────────

def add_stock(products):
    """Increase stock quantity for a product."""
    print("\n--- Add Stock ---")
    product_id = input("  Enter Product ID: ").strip()
    product = next((p for p in products if p["product_id"] == product_id), None)

    if not product:
        print(f"  [Error] Product ID '{product_id}' not found.")
        return

    try:
        qty = int(input(f"  Enter quantity to add (current: {product['quantity']}): "))
        if qty <= 0:
            raise ValueError
    except ValueError:
        print("  [Error] Quantity must be a positive integer.")
        return

    product["quantity"] += qty
    save_products(products)
    print(f"  [Success] Stock updated. New quantity: {product['quantity']}")


def check_low_stock(products):
    """Display products with quantity below threshold."""
    print(f"\n--- Low Stock Alert (Below {LOW_STOCK_THRESHOLD} units) ---")
    low = [p for p in products if p["quantity"] < LOW_STOCK_THRESHOLD]

    if not low:
        print("  All products have sufficient stock.")
        return

    print(f"  {'ID':<12} {'Name':<20} {'Quantity':>10}")
    print("  " + "-" * 45)
    for p in low:
        print(f"  {p['product_id']:<12} {p['name']:<20} {p['quantity']:>10}  ⚠️")


# ─────────────────────────────────────────────
# MODULE 3: SALES MANAGEMENT
# ─────────────────────────────────────────────

def record_sale(products, sales):
    """Record a sale transaction."""
    print("\n--- Record Sale ---")
    product_id = input("  Enter Product ID: ").strip()
    product = next((p for p in products if p["product_id"] == product_id), None)

    if not product:
        print(f"  [Error] Product ID '{product_id}' not found.")
        return

    print(f"  Product: {product['name']} | Available: {product['quantity']} | Price: ₹{product['price']}")

    try:
        qty = int(input("  Enter quantity to sell: "))
        if qty <= 0:
            raise ValueError
    except ValueError:
        print("  [Error] Quantity must be a positive integer.")
        return

    if qty > product["quantity"]:
        print(f"  [Error] Insufficient stock. Available: {product['quantity']}")
        return

    total = round(qty * product["price"], 2)
    sale_id = f"SALE{len(sales) + 1:04d}"

    sale = {
        "sale_id": sale_id,
        "product_id": product_id,
        "product_name": product["name"],
        "quantity_sold": qty,
        "total_amount": total,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    product["quantity"] -= qty
    sales.append(sale)
    save_products(products)
    save_sales(sales)

    print(f"  [Success] Sale recorded! Sale ID: {sale_id} | Total: ₹{total:.2f}")

    if product["quantity"] < LOW_STOCK_THRESHOLD:
        print(f"  ⚠️  Warning: Stock for '{product['name']}' is now low ({product['quantity']} units).")


def sales_summary(sales):
    """Display sales summary."""
    print("\n--- Sales Summary ---")
    if not sales:
        print("  No sales recorded yet.")
        return

    total_qty = sum(s["quantity_sold"] for s in sales)
    total_revenue = sum(s["total_amount"] for s in sales)

    # Most sold product
    from collections import Counter
    sold_counter = Counter()
    for s in sales:
        sold_counter[s["product_name"]] += s["quantity_sold"]
    most_sold = sold_counter.most_common(1)[0]

    print(f"  Total Products Sold : {total_qty}")
    print(f"  Total Revenue       : ₹{total_revenue:.2f}")
    print(f"  Most Sold Product   : {most_sold[0]} ({most_sold[1]} units)")


# ─────────────────────────────────────────────
# MODULE 5: REPORTING
# ─────────────────────────────────────────────

def inventory_report(products):
    """Display inventory report."""
    print("\n--- Inventory Report ---")
    if not products:
        print("  No products in inventory.")
        return

    categories = set(p["category"] for p in products)
    total_stock = sum(p["quantity"] for p in products)

    print(f"  Total Products    : {len(products)}")
    print(f"  Total Categories  : {len(categories)}")
    print(f"  Available Stock   : {total_stock} units")
    print(f"  Categories        : {', '.join(sorted(categories))}")


def sales_report(sales):
    """Display sales report."""
    print("\n--- Sales Report ---")
    if not sales:
        print("  No sales data available.")
        return

    from collections import Counter
    total_revenue = sum(s["total_amount"] for s in sales)
    total_sales = len(sales)

    sold_counter = Counter()
    for s in sales:
        sold_counter[s["product_name"]] += s["quantity_sold"]
    most_sold = sold_counter.most_common(1)[0]

    print(f"  Total Sales        : {total_sales} transactions")
    print(f"  Revenue Generated  : ₹{total_revenue:.2f}")
    print(f"  Most Sold Product  : {most_sold[0]} ({most_sold[1]} units)")


# ─────────────────────────────────────────────
# MODULE 6: MENU-DRIVEN INTERFACE
# ─────────────────────────────────────────────

def print_menu():
    print("\n" + "=" * 45)
    print("     INVENTORY MANAGEMENT SYSTEM")
    print("=" * 45)
    print("  1.  Add Product")
    print("  2.  View Products")
    print("  3.  Search Product")
    print("  4.  Update Product")
    print("  5.  Delete Product")
    print("  6.  Add Stock")
    print("  7.  Low Stock Alert")
    print("  8.  Record Sale")
    print("  9.  Sales Summary")
    print("  10. Inventory Report")
    print("  11. Sales Report")
    print("  12. View Product Image")
    print("  0.  Exit")
    print("=" * 45)


def main():
    products = load_products()
    sales = load_sales()

    print("\n  Welcome to Inventory Management System")
    print("  InfoBharat Items 🇮🇳")

    if not PIL_AVAILABLE:
        print("  [Notice] Install 'Pillow' (pip install Pillow) to enable image viewing.")

    while True:
        print_menu()
        choice = input("  Enter your choice: ").strip()

        if choice == "1":
            add_product(products)
        elif choice == "2":
            view_products(products)
        elif choice == "3":
            search_product(products)
        elif choice == "4":
            update_product(products)
        elif choice == "5":
            delete_product(products)
        elif choice == "6":
            add_stock(products)
        elif choice == "7":
            check_low_stock(products)
        elif choice == "8":
            record_sale(products, sales)
        elif choice == "9":
            sales_summary(sales)
        elif choice == "10":
            inventory_report(products)
        elif choice == "11":
            sales_report(sales)
        elif choice == "12":
            view_product_image(products)
        elif choice == "0":
            print("\n  Goodbye! Data saved. 👋\n")
            break
        else:
            print("  [Error] Invalid choice. Please enter a number from 0 to 12.")


if __name__ == "__main__":
    main()

SALES_FILE = "sales.csv"
PRODUCTS_FILE = "products.csv"


