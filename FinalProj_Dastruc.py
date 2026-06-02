import time
import os
import winsound


class Item:  # Sumagang
    def __init__(self, item_id, name, category, stock, threshold, price):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.stock = stock
        self.threshold = threshold
        self.price = price
        self.left = None
        self.right = None


class Warehouse:  # Sumagang
    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root is None

    def insert(self, root, item):
        if root is None:
            return item
        if item.item_id < root.item_id:
            root.left = self.insert(root.left, item)
        elif item.item_id > root.item_id:
            root.right = self.insert(root.right, item)
        return root

    def add_item(self, item_id, name, category, stock, threshold, price):
        new_item = Item(item_id, name, category, stock, threshold, price)
        self.root = self.insert(self.root, new_item)
        return True

    # ----------- Update and Delete Functions (SARAYAN) -----------
    def update_item(self, item_id, name=None, category=None, stock=None, threshold=None, price=None):
        current = self.root
        while current is not None:
            if item_id == current.item_id:

                if name is not None:
                    current.name = name

                if category is not None:
                    current.category = category

                if stock is not None:
                    current.stock = stock

                if threshold is not None:
                    current.threshold = threshold

                if price is not None:
                    current.price = price

                print(f" ✅ Item ID {item_id} updated successfully.")
                return True

            elif item_id < current.item_id:
                current = current.left
            else:
                current = current.right

        print(f" ⚠ ERROR: Cannot Update. Item Id {item_id} Not found.")
        return False

    def delete_item(self, item_id):
        current = self.root
        found = False
        while current is not None:
            if item_id == current.item_id:
                found = True
                break
            elif item_id < current.item_id:
                current = current.left
            else:
                current = current.right

        if not found:
            return False
        self.root = self._delete_node(self.root, item_id)


    def _delete_node(self, root, item_id):
        if root is None:
            return root
        if item_id < root.item_id:
            root.left = self._delete_node(root.left, item_id)
        elif item_id > root.item_id:
            root.right = self._delete_node(root.right, item_id)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            temp = root.right
            while temp.left is not None:
                temp = temp.left

            root.item_id, root.name = temp.item_id, temp.name
            root.category, root.stock = temp.category, temp.stock
            root.threshold, root.price = temp.threshold, temp.price
            root.right = self._delete_node(root.right, temp.item_id)
        return root

    # ----------- Search ID and Price Range (ENANO) -----------

    def search_item_by_id(self, target_id):
        found_node = self._search_id_helper(self.root, target_id)
        return found_node

    def _search_id_helper(self, current_node, target_id):
        if current_node is None or current_node.item_id == target_id:
            return current_node

        if target_id < current_node.item_id:
            return self._search_id_helper(current_node.left, target_id)
        else:
            return self._search_id_helper(current_node.right, target_id)

    def search_by_price_range(self, min_price, max_price):
        print(f"\n--- Items between ₱{min_price:.2f} and ₱{max_price:.2f} ---")
        tracker = {"found": False}
        self._price_range_helper(self.root, min_price, max_price, tracker)

        if not tracker["found"]:
            print(" ❌ No items found within this price range.")

    def _price_range_helper(self, current_node, min_price, max_price, tracker):
        if current_node is None:
            return

        self._price_range_helper(current_node.left, min_price, max_price, tracker)

        if min_price <= current_node.price <= max_price:
            print(f" ID: {current_node.item_id} | Name: {current_node.name} | Price: ₱{current_node.price:.2f}")
            tracker["found"] = True
        self._price_range_helper(current_node.right, min_price, max_price, tracker)

        # In-Order Traversal for Display (JOB)

    def inorder_traversal(self):
        if self.root is None:
            print(" 📭 Inventory is empty!")
            return

        print("\n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("              INVENTORY ITEMS SORTED BY ITEM ID")
        print(" ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        self._inorder_helper(self.root)

        print(" ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    def _inorder_helper(self, root):
        if root:
            self._inorder_helper(root.left)

            print(f" ID: {root.item_id:<4} | "
                  f"Name: {root.name:<20} | "
                  f"Category: {root.category:<12} | "
                  f"Stock: {root.stock:<5} | "
                  f"Price: ₱{root.price:.2f} | "
                  f"Threshold: {root.threshold:<5}")

            self._inorder_helper(root.right)

    # Display All - (PIO)
    def display_all(self):
        if self.root is None:
            print(" 📭 Inventory is empty!")
            return

        # Collect all items via in-order traversal
        all_items = []
        self._collect_all(self.root, all_items)

        # Group items by category
        categories = {}
        for item in all_items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)

        print("\n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("                 ALL INVENTORY ITEMS BY CATEGORY")
        print(" ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        for category, items in sorted(categories.items()):
            print(f"\n  📂 [{category.upper()}]  ({len(items)} item/s)")
            print(f"  {'─' * 90}")
            for item in items:
                print(f"  ID: {item.item_id:<4} | "
                      f"Name: {item.name:<20} | "
                      f"Stock: {item.stock:<5} | "
                      f"Price: ₱{item.price:.2f} | "
                      f"Threshold: {item.threshold:<5}")
            print(f"  {'─' * 90}")

        print(f"\n  📦 Total Items: {len(all_items)}")
        print(" ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    def _collect_all(self, root, result):
        if root:
            self._collect_all(root.left, result)
            result.append(root)
            self._collect_all(root.right, result)


    # ----------- Low Stock Alert (Martin) -----------
    def low_stock(self, root):
        low_items = []
        self._low_stock_helper(root, low_items)
        return low_items

    def _low_stock_helper(self, root, low_items):
        if root:
            self._low_stock_helper(root.left, low_items)
            if root.stock <= root.threshold:
                low_items.append(f"  ⚠  ID: {root.item_id:<4} | {root.name:<16} | Stock: {root.stock}")
            self._low_stock_helper(root.right, low_items)


# Animation (Sumagang)
def loading_animation_in():
    print("⏳ Inventory Loading", end="", flush=True)
    for _ in range(4):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print()
    print("✅ Inventory Loaded!")
    time.sleep(0.5)


def loading_animation_out():
    print("⏳  Exiting...", end="", flush=True)
    for _ in range(4):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print()


def returning_menu_animation():
    print("⏳ Returning to Main Menu", end="", flush=True)
    for _ in range(4):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print()


#  Clear Automatic Terminal (Sumagang)
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Main Menu (Sumagang)
def title():
    print("┌───────────────────────────────────────────────────────┐")
    print("│    📦 WAREHOUSE INVENTORY MANAGEMENT SYSTEM 📦        │")
    print("└───────────────────────────────────────────────────────┘")
    time.sleep(0.8)


def menu_options():
    print("┌───────────────────────────────────────────────────────┐")
    print("│   ⬇️   PLEASE CHOOSE YOUR OPTION BELOW!(0-8) ⬇️       │")
    print("└───────────────────────────────────────────────────────┘")
    time.sleep(0.9)
    print("""
  ┌─ INVENTORY OPERATIONS ──────────────────┐
  │  [0]  Insert New Item                   │
  │  [1]  Update Stock                      │
  │  [2]  Delete Item                       │
  ├─ SEARCH OPERATIONS ─────────────────────┤
  │  [3]  Search Item by ID                 │
  │  [4]  Search Items by Price Range       │
  ├─ DISPLAY OPERATIONS ────────────────────┤
  │  [5] Display All Items                  │
  │  [6] Traversal In Order(BY:ID)          │
  ├─ ALERTS & ANALYTICS ────────────────────┤
  │  [7]  Low-Stock Alert                   │                                        
  ├─────────────────────────────────────────┤
  │  [8]  Exit                              │
  └─────────────────────────────────────────┘""")


# Error Handling - Sumagang
def get_int(prompt):
    # """INVALID INPUT: keeps asking until a valid non-negative integer is entered."""
    while True:
        raw = input(f"  {prompt}").strip()
        if not raw:
            print("  ⚠  ERROR (Invalid Input): Field cannot be blank. Please enter a number.")
            continue
        try:
            value = int(raw)
            if value < 0:
                print("  ⚠  ERROR (Invalid Input): Value cannot be negative. Enter 0 or greater.")
                continue
            return value
        except ValueError:
            print(f"  ⚠  ERROR (Invalid Input): '{raw}' is not a valid whole number (e.g. 50).")


def get_positive_int(prompt):
    # """INVALID INPUT: requires an integer > 0 (used for Item ID)."""
    while True:
        raw = input(f"  {prompt}").strip()
        if not raw:
            print("  ⚠  ERROR (Invalid Input): Item ID cannot be blank.")
            continue
        try:
            value = int(raw)
            if value <= 0:
                print("  ⚠  ERROR (Invalid Input): Item ID must be greater than 0.")
                continue
            return value
        except ValueError:
            print(f"  ⚠  ERROR (Invalid Input): '{raw}' is not valid. Enter a positive whole number (e.g. 101).")


def get_float(prompt):
    # """INVALID INPUT: keeps asking until a valid non-negative decimal is entered."""
    while True:
        raw = input(f"  {prompt}").strip()
        if not raw:
            print("  ⚠  ERROR (Invalid Input): Price cannot be blank.")
            continue
        try:
            value = float(raw)
            if value < 0:
                print("  ⚠  ERROR (Invalid Input): Price cannot be negative.")
                continue
            return value
        except ValueError:
            print(f"  ⚠  ERROR (Invalid Input): '{raw}' is not a valid number (e.g. 99.50).")


def get_text(prompt):
    # """INVALID INPUT: ensures non-blank text with letters/spaces only."""
    while True:
        raw = input(f"  {prompt}").strip()
        if not raw:
            print("  ⚠  ERROR (Invalid Input): This field cannot be blank.")
            continue
        if not all(c.isalpha() or c.isspace() or c in "-_." for c in raw):
            print(f"  ⚠  ERROR (Invalid Input): '{raw}' has invalid characters. Use letters and spaces only.")
            continue
        return raw


# Main - Sumagang/Sarayan
def main():
    warehouse = Warehouse()

    warehouse_item = [
        (100, "Bolt M8", "Hardware", 1, 10, 2.50),
        (101, "Safety Gloves", "PPE", 20, 10, 85.00),
        (102, "Pallet Jacks", "Equipment", 10, 1, 320.00),
        (103, "Stretch Wrap", "Packaging", 100, 50, 950.00),
        (104, "Corrugated Boxes", "Packaging", 500, 100, 12.75),
        (105, "Dunnage", "Packaging", 1000, 100, 12.75),
    ]

    for item_data in warehouse_item:
        warehouse.add_item(*item_data)

    while True:
        clear()
        title()
        menu_options()
        choice = input("\nEnter your choice (0-8): ")

        # Invalid Menu Option Error Handling
        if choice not in ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
            print("⚠  ERROR: Invalid choice! Please select a number between 0 and 8.")
            time.sleep(1.5)
            continue


        #  ── 0. Insert Stock ── (Sumagang)
        if choice == "0":
            clear()
            print("\n --- INSERT ITEM ---")
            while True:
                item_id = get_positive_int("Enter New item ID: ")
                if warehouse.search_item_by_id(item_id):
                    print(" ❗ Duplicate ID detected. Please try again.")
                    continue
                else:
                    break

            name = input(f"{'Enter item name: ':>17} ")
            category = get_text("Enter item category: ")

            stock = get_int("Enter New item stock: ")
            while True:
                threshold = get_int("Enter New item threshold: ")

                # BOUNDARY: threshold cannot exceed stock
                if threshold > stock:
                    print("  ⚠  ERROR (Boundary): Threshold cannot be greater than Stock Count. Please try again.")
                else:
                    break

            price = get_float("Price (₱)    : ")

            success = warehouse.add_item(item_id, name, category, stock, threshold, price)
            if success:
                print(f"✅ Item {item_id} added successfully.")
                returning_menu_animation()


        # ── 1. Update Stock ── (Sarayan)
        elif choice == "1":
            while True:
                clear()
                title()
                print("\n --- UPDATE ITEM ---")
                item_id = get_positive_int("Enter item ID to Update: ")

                item_node = warehouse.search_item_by_id(item_id)
                if not item_node:
                    print(f" ⚠ ERROR: Item ID {item_id} not found.")
                else:
                    # 1. Name Input (Allows numbers and symbols)
                    name_input = input(f"  Enter New Name [{item_node.name}]: ").strip()
                    new_name = name_input if name_input else None

                    # 2. Category Validation (Strict alphanumeric & space check; rejects punctuation/special characters)
                    while True:
                        category_input = input(f"  Enter New Category [{item_node.category}]: ").strip()
                        if not category_input:
                            new_category = None
                            break


                        # Checks if the entry contains only letters, numbers, or spaces (rejects symbols like /';,,)
                        if all(c.isalpha() or c.isspace() for c in category_input):
                            new_category = category_input
                            break
                        else:
                            print(
                                f"  ⚠  ERROR (Invalid Input): '{category_input}' contains Invalid characters. Only letters, numbers, and spaces are allowed.")

                    # 3. Stock Validation
                    while True:
                        stock_input = input(f"  Enter New Stock Count [{item_node.stock}]: ").strip()
                        if not stock_input:
                            new_stock = None
                            break
                        if stock_input.isdigit():
                            new_stock = int(stock_input)
                            break
                        else:
                            print(
                                "  ⚠  ERROR (Invalid Input): Must be a valid positive whole number. Special characters, Letters and negative values are not allowed.")

                    # 4. Threshold Validation
                    while True:
                        thresh_input = input(f"  Enter New Threshold [{item_node.threshold}]: ").strip()
                        if not thresh_input:
                            new_threshold = None
                            break
                        if thresh_input.isdigit():
                            temp_thresh = int(thresh_input)
                            target_stock = new_stock if new_stock is not None else item_node.stock
                            if temp_thresh > target_stock:
                                print(
                                    f"  ⚠  ERROR (Boundary Check): Threshold ({temp_thresh}) cannot exceed the Stock Count ({target_stock}).")
                            else:
                                new_threshold = temp_thresh
                                break
                        else:
                            print("  ⚠  ERROR (Invalid Input): Must be a valid positive whole number.")

                    # 5. Price Validation
                    while True:
                        price_input = input(f"  Enter New Price [{item_node.price:.2f}]: ").strip()
                        if not price_input:
                            new_price = None
                            break
                        try:
                            temp_price = float(price_input)
                            if temp_price < 0:
                                print("  ⚠  ERROR (Invalid Input): Price cannot be negative.")
                            else:
                                new_price = temp_price
                                break
                        except ValueError:
                            print(
                                "  ⚠  ERROR (Invalid Input): Please enter a valid positive decimal or whole number (e.g., 15000 or 99.50).")

                    # Finalize data submission
                    warehouse.update_item(
                        item_id=item_id,
                        name=new_name,
                        category=new_category,
                        stock=new_stock,
                        threshold=new_threshold,
                        price=new_price
                    )

                while True:
                    again = input("\nDo you want to update another item? (Yes/No): ").strip().lower()
                    if again in ['yes', 'no']:
                        break
                    print("  ⚠  ERROR: Invalid input. Please enter only 'Yes' or 'No'.")

                if again == 'no':
                    returning_menu_animation()
                    break


        #  ── 2. Delete ── (Sarayan)
        elif choice == "2":
            while True  :
                print("\n --- DELETE ITEM ---")
                item_id = get_positive_int("Enter item ID to Delete: ")


                if not warehouse.search_item_by_id(item_id):
                    print(f" ⚠ ERROR: Cannot Delete. Item ID {item_id} not found.")
                elif warehouse.search_item_by_id(item_id):
                    print(f" ✅ Item ID {item_id} deleted successfully.")
                    warehouse.delete_item(item_id)

                    while True:
                        again = input("\nDo you want to delete another item? (Yes/No): ").strip().lower()
                        if again in ['yes', 'no']:
                            break
                        print("  ⚠  ERROR: Invalid input. Please enter only 'Yes' or 'No'.")

                    if again == 'no':
                        returning_menu_animation()
                        break




        #  ── 3. Search by ID ── (Enano)
        elif choice == '3':
            # EMPTY: search on empty structure (Enano)
            if warehouse.is_empty():
                print(" 📭 Cannot search. The warehouse inventory is completely empty!")
            else:
                while True:
                    clear()
                    title()
                    print("\n ──── 🔍 [SEARCH OPERATIONS] Search Item by ID ────")
                    try:
                        target_id = get_positive_int(" 👉 Enter Item ID to lookup: ")
                    except ValueError:
                        print(" ⚠ ERROR: Invalid input. Please enter a valid Item ID (positive whole number).")
                        input("\nPress Enter to try again...")
                        continue

                    result_node = warehouse.search_item_by_id(target_id)

                    if result_node:
                        print("\n ✅ ITEM FOUND ")
                        print(f" ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"  ID:        {result_node.item_id}")
                        print(f"  Name:      {result_node.name}")
                        print(f"  Category:  {result_node.category}")
                        print(f"  Stock:     {result_node.stock}")
                        print(f"  Threshold: {result_node.threshold}")
                        print(f"  Price:     ₱{result_node.price:.2f}")
                        print(f" ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                    else:
                        print(f" ❌ Item ID {target_id} does not exist in the inventory.")
                    while True:
                        again = input("\nDo you want to search for another ID? (Yes/No): ").strip().lower()
                        if again in ['yes', 'no']:
                            break
                        print("  ⚠  ERROR: Invalid input. Please enter only 'Yes' or 'No'.")

                    if again == 'no':
                        returning_menu_animation()
                        break

        # ── 4. Price Range ── (Enano)
        elif choice == '4':
            if warehouse.is_empty():
                print(" 📭 Cannot search. The warehouse inventory is completely empty!")
            else:
                while True:
                    clear()
                    title()
                    print("\n ──── 🔍 [SEARCH OPERATIONS] Search Item by Price Range ────")
                    try:
                        min_price = get_float(" 👉 Enter Minimum Price (₱): ")
                        max_price = get_float(" 👉 Enter Maximum Price (₱): ")
                    except ValueError:
                        print(" ⚠ ERROR: Invalid input. Please enter valid numbers for price.")
                        input("\nPress Enter to try again...")
                        continue

                    if min_price > max_price:
                        print(" ⚠ ERROR: Minimum price cannot be greater than maximum price.")
                    else:
                        warehouse.search_by_price_range(min_price, max_price)

                    while True:
                        again = input("\nDo you want to search for another Price Range? (Yes/No): ").strip().lower()
                        if again in ['yes', 'no']:
                            break
                        print("  ⚠  ERROR: Invalid input. Please enter only 'Yes' or 'No'.")

                    if again == 'no':
                        returning_menu_animation()
                        break

        # ── 5. Display All  ── (Pio)
        elif choice == "5":
            clear()
            title()
            print("\n ──── 📋 [DISPLAY OPERATIONS] Display All Items ────")
            warehouse.display_all()
            input("\n  Press Enter to return to Main Menu...")
            returning_menu_animation()

        #    ── 6. Traversal In Order(BYID)  ── (JOB)
        elif choice == "6":
            clear()
            title()
            print("\n ──── 📋 [DISPLAY OPERATIONS] Traversal In Order (BY ID) ────")
            warehouse.inorder_traversal()
            input("\n  Press Enter to return to Main Menu...")
            returning_menu_animation()

        # ── 7. Low Stock ── (Martin)
        elif choice == "7":
            clear()
            title()
            print("\n ──── 🚨 [ALERTS] Low Stock Analysis ────")
            if warehouse.is_empty():
                print(" 📭 The warehouse inventory is completely empty!")
            else:
                low_items = warehouse.low_stock(warehouse.root)
                if low_items:
                    print("\n --- LOW STOCK ITEMS ---")
                    for item_str in low_items:
                        print(item_str)
                        winsound.Beep(500, 2000)
                else:
                    print(" 📭 No items are low in stock!")
            input("\n  Press Enter to return to Main Menu...")
            returning_menu_animation()

        # ── 8. Exit ──
        elif choice == "8":
            print("\nGoodbye! Thank you for using us!👋\n")
            loading_animation_out()
            break


if __name__ == "__main__":
    loading_animation_in()
    main()