import random
import time
import os

# ATM Simulation with Registration, OTP, and PIN Reset

# Initialize account details
account_details_file = "account_details.txt"
otp_expiry_time = 30  # OTP validity time in seconds
otp_length = 4  # Length of OTP

# Function to generate OTP with timestamp
def generate_otp():
    otp = str(random.randint(10**(otp_length-1), (10**otp_length)-1))
    otp_generated_time = time.time()
    return otp, otp_generated_time

# Function to register a new user
def register():
    print("\n--- Account Registration ---")
    name = input("Enter your full name: ")
    phone = input("Enter your mobile number: ")
    if len(phone) != 10 or not phone.isdigit():
        print("Invalid phone number. Registration failed.\n")
        return
    
    try:
        initial_balance = float(input("Enter initial deposit amount: ₹"))
        if initial_balance <= 0:
            print("Deposit amount must be greater than ₹0.\n")
            return
    except ValueError:
        print("Invalid amount entered. Registration failed.\n")
        return
    
    while True:
        pin = input("Set your 4-digit PIN: ")
        if len(pin) == 4 and pin.isdigit():
            confirm_pin = input("Confirm your 4-digit PIN: ")
            if pin == confirm_pin:
                break
            else:
                print("PINs do not match. Try again.")
        else:
            print("Invalid PIN format. PIN must be 4 digits.")

    # Save account details to the file in append mode
    with open(account_details_file, "a") as file:
        file.write(f"{name},{phone},{initial_balance},{pin}\n")
    print("Account registered successfully!\n")

# Function to load account details (load all accounts)
def load_account_details():
    if not os.path.exists(account_details_file):
        print("No registered account found. Please register first.\n")
        return None
    
    with open(account_details_file, "r") as file:
        data = file.readlines()  # Read all lines
        if not data:
            return None
        return data  # Return all account details lines

# Function to update account balance in the file (rewriting the entire file)
def update_balance_in_file(account_details):
    with open(account_details_file, "r") as file:
        lines = file.readlines()

    # Modify the account balance for the correct account
    with open(account_details_file, "w") as file:
        for line in lines:
            data = line.strip().split(",")
            if data[1] == account_details["phone"]:  # Match account by phone number
                file.write(f"{data[0]},{data[1]},{account_details['balance']},{data[3]}\n")
            else:
                file.write(line)  # Write other accounts as they are

# Function to validate PIN directly (no phone number check)
# Function to validate PIN directly (no phone number check)
def validate_pin():
    pin = input("Enter your 4-digit PIN: ")
    accounts = load_account_details()

    if accounts is None:
        print("No accounts found.")
        return None

    for line in accounts:
        data = line.strip().split(",")
        if data[3] == pin:  # Compare the entered PIN with the stored PIN
            print(f"PIN Verified. Welcome, {data[0]}!\n")  # Display the holder's name
            return {"name": data[0], "phone": data[1], "balance": float(data[2]), "pin": data[3]}
    
    print("Incorrect PIN. Exiting system.")
    return None

# Function to reset PIN with OTP
def reset_pin(account_details):
    print("\n--- Reset PIN ---")
    phone = input("Enter your registered phone number: ")
    if phone != account_details["phone"]:
        print("Phone number not registered. Cannot reset PIN.")
        return

    otp, otp_time = generate_otp()
    print(f"OTP has been generated. (OTP saved in 'otp.txt' for testing purposes)\n")
    with open("otp.txt", "w") as file:
        file.write(otp)
    
    while True:
        user_otp = input("Enter the OTP (or type 'exit' to cancel): ")
        if user_otp.lower() == "exit":
            print("OTP verification canceled.")
            return

        if time.time() - otp_time > otp_expiry_time:
            print("The OTP has expired. Please try again.")
            return
        
        if user_otp == otp:
            new_pin = input("Enter your new 4-digit PIN: ")
            confirm_pin = input("Re-enter your new 4-digit PIN: ")
            if new_pin == confirm_pin and len(new_pin) == 4 and new_pin.isdigit():
                with open(account_details_file, "r") as file:
                    data = file.readlines()
                with open(account_details_file, "w") as file:
                    for line in data:
                        data_line = line.strip().split(",")
                        if data_line[1] == account_details["phone"]:
                            file.write(f"{data_line[0]},{data_line[1]},{data_line[2]},{new_pin}\n")
                        else:
                            file.write(line)
                print("PIN has been reset successfully!\n")
                return
            else:
                print("PINs do not match or invalid format. Try again.")
        else:
            print("Invalid OTP. Please try again.")

# Function to check balance
def check_balance(account_details):
    print(f"Your current balance is: ₹{account_details['balance']}")

# Function to deposit cash
def deposit_cash(account_details):
    try:
        amount = float(input("Enter amount to deposit: ₹"))
        if amount > 0:
            account_details["balance"] += amount
            update_balance_in_file(account_details)
            print(f"₹{amount} deposited successfully!")
            check_balance(account_details)
        else:
            print("Invalid amount. Please enter a positive number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Function to withdraw cash
def withdraw_cash(account_details):
    try:
        amount = float(input("Enter amount to withdraw: ₹"))
        if amount <= 0:
            print("Invalid amount. Please enter a positive number.")
        elif amount > account_details["balance"]:
            print("Insufficient balance!")
        else:
            account_details["balance"] -= amount
            update_balance_in_file(account_details)
            print(f"₹{amount} withdrawn successfully!")
            check_balance(account_details)
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Function to display ATM menu
def display_menu(account_details):
    print("\nATM Operations:")
    print("1. Check Balance")
    print("2. Deposit Cash")
    print("3. Withdraw Cash")
    print("4. Reset PIN")
    print("5. Exit")
    choice = input("Choose an operation (1-5): ")

    if choice == "1":
        check_balance(account_details)
    elif choice == "2":
        deposit_cash(account_details)
    elif choice == "3":
        withdraw_cash(account_details)
    elif choice == "4":
        reset_pin(account_details)
    elif choice == "5":
        print("Thank you for using the ATM. Goodbye!")
    else:
        print("Invalid choice. Exiting system.")

# Main ATM Logic
# Main ATM Logic
def atm_logic():
    
        print("\n--- Welcome to the ATM ---")
        print("1. Register Account")
        print("2. Enter PIN")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            register()
        elif choice == "2":
            account_details = validate_pin()
            if account_details:
                # Show ATM menu after successful PIN validation
                display_menu(account_details)
        elif choice == "3":
            print("Thank you for visiting. Goodbye!")
            
        else:
            print("Invalid choice. Please try again.")


# Run the ATM logic
if __name__ == "__main__":
    atm_logic()
