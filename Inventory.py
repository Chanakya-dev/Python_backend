import os
import datetime

# Function to read inventory from the file
def read_inventory():
    inventory = {}
    try:
        with open("inventory.txt", "r") as file:
            for line in file:
                product, quantity, price = line.split()
                inventory[product] = {"quantity": int(quantity), "price": int(price)}
    except FileNotFoundError:
        print("Inventory file not found. Please make sure inventory.txt exists.")
    return inventory

# Function to write updated inventory to the file
def write_inventory(inventory):
    with open("inventory.txt", "w") as file:
        for product, details in inventory.items():
            file.write(f"{product} {details['quantity']} {details['price']}\n")

# Cart to store the user's selected products and quantities
cart = {}

# Function to apply seasonal discounts based on the current month
def apply_seasonal_discount():
    current_month = datetime.datetime.now().month  # Get the current month
    seasonal_discounts = {}

    # Apply seasonal discounts based on the month
    if current_month == 12:  # December - Holiday season
        seasonal_discounts = {
            "Milk": 20,  # 20% discount
            "Eggs": 10,  # 10% discount
            "Sugar": 10  # 10% discount
        }
    elif current_month == 6:  # June - Summer sale
        seasonal_discounts = {
            "Rice": 16.67,  # 16.67% discount
            "Flour": 12.5  # 12.5% discount
        }

    return seasonal_discounts

# Function to display available products
# Function to display available products with discounted products highlighted
def display_products(inventory, seasonal_discounts):
    print("\n--- Available Products ---")
    for product, details in inventory.items():
        price = details['price']
        discount_percentage = seasonal_discounts.get(product, 0)  # Get discount if available, else 0
        if discount_percentage > 0:
            discounted_price = price - (price * discount_percentage / 100)
            print(f"{product}: ₹{discounted_price:.2f} (Original Price: ₹{price} | Discount: {discount_percentage}%) (Stock: {details['quantity']})")
        else:
            print(f"{product}: ₹{price} (Stock: {details['quantity']})")


# Function to add a product to the cart
def add_to_cart(inventory):
    product_name = input("Enter the product name to add to cart: ").capitalize()
    if product_name in inventory:
        quantity = int(input(f"Enter quantity for {product_name}: "))
        if quantity <= inventory[product_name]["quantity"]:
            inventory[product_name]["quantity"] -= quantity
            if product_name in cart:
                cart[product_name]['quantity'] += quantity
            else:
                cart[product_name] = {'quantity': quantity, 'original_price': inventory[product_name]['price']}
            print(f"{quantity} {product_name}(s) added to your cart.")
            write_inventory(inventory)  # Save updated inventory
        else:
            print(f"Not enough stock. Only {inventory[product_name]['quantity']} available.")
    else:
        print("Product not found.")

# Function to remove a product from the cart
def remove_from_cart(inventory):
    product_name = input("Enter the product name to remove from cart: ").capitalize()
    if product_name in cart:
        quantity = int(input(f"Enter quantity to remove for {product_name}: "))
        if quantity >= cart[product_name]['quantity']:
            inventory[product_name]["quantity"] += cart[product_name]['quantity']
            del cart[product_name]
            print(f"All {product_name}(s) removed from your cart.")
        else:
            cart[product_name]['quantity'] -= quantity
            inventory[product_name]["quantity"] += quantity
            print(f"{quantity} {product_name}(s) removed from your cart.")
        write_inventory(inventory)  # Save updated inventory
    else:
        print("Product not found in cart.")

# Function to view the cart
def view_cart(inventory, seasonal_discounts):
    if cart:
        print("\n--- Your Cart ---")
        for product, details in cart.items():
            original_price = details['original_price']
            discounted_price = original_price
            discount_percentage = 0

            # Check if the product has a seasonal discount
            if product in seasonal_discounts:
                discount_percentage = seasonal_discounts[product]
                discounted_price = original_price - (original_price * discount_percentage / 100)

            print(f"{product}: {details['quantity']} x ₹{discounted_price:.2f} = ₹{discounted_price * details['quantity']:.2f} (Original Price: ₹{original_price} | Discount: {discount_percentage}%)")
    else:
        print("Your cart is empty.")

# Function to calculate the total bill with discounts, CGST, SGST, and show the discount percentage
def calculate_total(inventory, seasonal_discounts):
    total_original = 0
    total_discounted = 0
    discount_amount = 0
    cgst_amount = 0
    sgst_amount = 0
    cgst_rate = 9  # CGST rate (9%)
    sgst_rate = 9  # SGST rate (9%)

    for product, details in cart.items():
        original_price = details['original_price']
        discounted_price = original_price
        discount_percentage = 0

        # Check if the product has a seasonal discount
        if product in seasonal_discounts:
            discount_percentage = seasonal_discounts[product]
            discounted_price = original_price - (original_price * discount_percentage / 100)

        total_original += original_price * details['quantity']
        total_discounted += discounted_price * details['quantity']
        discount_amount += (original_price - discounted_price) * details['quantity']

    discount_percentage = (discount_amount / total_original) * 100 if total_original != 0 else 0

    # Calculate CGST and SGST
    cgst_amount = (total_discounted * cgst_rate) / 100
    sgst_amount = (total_discounted * sgst_rate) / 100

    total_with_tax = total_discounted + cgst_amount + sgst_amount

    return total_original, total_discounted, discount_amount, discount_percentage, cgst_amount, sgst_amount, total_with_tax

# Function to checkout
def checkout(inventory, seasonal_discounts):
    if not cart:
        print("Your cart is empty! Add items to your cart before checking out.")
        return

    print("\n--- Checkout ---")
    view_cart(inventory, seasonal_discounts)  # Pass inventory to view_cart
    total_original, total_discounted, discount_amount, discount_percentage, cgst_amount, sgst_amount, total_with_tax = calculate_total(inventory, seasonal_discounts)

    print(f"Original Total: ₹{total_original:.2f}")
    print(f"Discounted Total: ₹{total_discounted:.2f}")
    print(f"Total Discount: ₹{discount_amount:.2f} ({discount_percentage:.2f}%)")
    print(f"CGST (9%): ₹{cgst_amount:.2f}")
    print(f"SGST (9%): ₹{sgst_amount:.2f}")
    print(f"Total amount to pay after discount and taxes: ₹{total_with_tax:.2f}")
    
    print("Thank you for shopping with us!")
    cart.clear()  # Clear the cart after checkout

# Main menu for the supermarket system
def supermarket_system():
    inventory = read_inventory()  # Load inventory from file
    seasonal_discounts = apply_seasonal_discount()  # Apply seasonal discounts based on current month
    while True:
        print("\n--- Supermarket Menu ---")
        print("1. View Products")
        print("2. Add to Cart")
        print("3. Remove from Cart")
        print("4. View Cart")
        print("5. Checkout")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            display_products(inventory, seasonal_discounts)  # Pass both inventory and seasonal_discounts
        elif choice == "2":
            add_to_cart(inventory)
        elif choice == "3":
            remove_from_cart(inventory)
        elif choice == "4":
            view_cart(inventory, seasonal_discounts)  # Pass inventory to view_cart
        elif choice == "5":
            checkout(inventory, seasonal_discounts)  # Pass inventory to checkout
            break  # Stop the program after checkout
        elif choice == "6":
            print("Thank you for visiting! Visit Again!")
            break  # Stop the program when the user chooses to exit
        else:
            print("Invalid choice. Please try again.")


# Run the Supermarket system
if __name__ == "__main__":
    supermarket_system()
