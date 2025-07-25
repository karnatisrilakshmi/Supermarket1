import tkinter as tk
from tkinter import messagebox
import datetime
import os

# Function to add item to the bill
def add_item():
    item_name = item_name_var.get()
    price = price_var.get()
    quantity = quantity_var.get()
    
    if item_name == "" or price == "" or quantity == "":
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    try:
        price = float(price)
        quantity = int(quantity)
        total_price = price * quantity
        
        # Add to listbox
        bill_listbox.insert(tk.END, f"{item_name} - {quantity} x {price:.2f} = {total_price:.2f}")
        
        # Update total
        total_var.set(total_var.get() + total_price)
        
        # Clear fields
        item_name_var.set("")
        price_var.set("")
        quantity_var.set("")
    except ValueError:
        messagebox.showerror("Error", "Price must be a number and Quantity must be an integer!")

# Function to clear the bill
def clear_bill():
    bill_listbox.delete(0, tk.END)
    total_var.set(0.0)
    bill_text.delete("1.0", tk.END)
    customer_name_var.set("")
    customer_phone_var.set("")

# Function to generate final bill
def generate_bill():
    global last_bill_file
    if customer_name_var.get() == "" or customer_phone_var.get() == "":
        messagebox.showwarning("Customer Info Missing", "Please enter customer name and phone number.")
        return

    if bill_listbox.size() == 0:
        messagebox.showwarning("Empty Bill", "No items in the bill!")
        return
    
    receipt = "       SUPERMARKET BILL\n"
    receipt += "-"*35 + "\n"
    receipt += f"Customer: {customer_name_var.get()}\n"
    receipt += f"Phone: {customer_phone_var.get()}\n"
    receipt += "-"*35 + "\n"
    
    for i in range(bill_listbox.size()):
        receipt += bill_listbox.get(i) + "\n"
        
    receipt += "-"*35 + f"\nTotal Amount: Rs {total_var.get():.2f}\n"
    receipt += f"Date: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
    receipt += "-"*35 + "\nThank You! Visit Again!\n"

    # Display receipt in text box
    bill_text.delete("1.0", tk.END)
    bill_text.insert(tk.END, receipt)
    
    # Save bill as a text file
    last_bill_file = f"bill_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(last_bill_file, "w", encoding="utf-8") as file:
        file.write(receipt)
    
    messagebox.showinfo("Bill Saved", f"Bill saved as {last_bill_file}")

# Function to print the bill
def print_bill():
    if not last_bill_file:
        messagebox.showwarning("No Bill", "Please generate a bill before printing.")
        return
    try:
        os.startfile(last_bill_file, "print")
        messagebox.showinfo("Printing", "The bill is being sent to the printer.")
    except Exception as e:
        messagebox.showerror("Print Error", f"Could not print the bill: {e}")

# GUI Setup
root = tk.Tk()
root.title("Supermarket Bill Generator")
root.geometry("600x700")
root.config(bg="#2C3E50")

last_bill_file = None  # To store the latest bill file

# Variables
item_name_var = tk.StringVar()
price_var = tk.StringVar()
quantity_var = tk.StringVar()
total_var = tk.DoubleVar(value=0.0)
customer_name_var = tk.StringVar()
customer_phone_var = tk.StringVar()

# Title
tk.Label(root, text="Supermarket Billing System", font=("Helvetica", 18, "bold"), bg="#2C3E50", fg="white").pack(pady=10)

# Customer Details Frame
customer_frame = tk.Frame(root, bg="#34495E", bd=5, relief="ridge")
customer_frame.pack(pady=5, padx=10, fill="x")

tk.Label(customer_frame, text="Customer Name:", font=("Arial", 12), bg="#34495E", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Entry(customer_frame, textvariable=customer_name_var, font=("Arial", 12), width=20).grid(row=0, column=1, padx=10, pady=5)

tk.Label(customer_frame, text="Phone Number:", font=("Arial", 12), bg="#34495E", fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
tk.Entry(customer_frame, textvariable=customer_phone_var, font=("Arial", 12), width=20).grid(row=1, column=1, padx=10, pady=5)

# Item Entry Frame
entry_frame = tk.Frame(root, bg="#34495E", bd=5, relief="ridge")
entry_frame.pack(pady=10, padx=10, fill="x")

tk.Label(entry_frame, text="Item Name:", font=("Arial", 12), bg="#34495E", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Entry(entry_frame, textvariable=item_name_var, font=("Arial", 12), width=20).grid(row=0, column=1, padx=10, pady=5)

tk.Label(entry_frame, text="Price (Rs):", font=("Arial", 12), bg="#34495E", fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
tk.Entry(entry_frame, textvariable=price_var, font=("Arial", 12), width=20).grid(row=1, column=1, padx=10, pady=5)

tk.Label(entry_frame, text="Quantity:", font=("Arial", 12), bg="#34495E", fg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
tk.Entry(entry_frame, textvariable=quantity_var, font=("Arial", 12), width=20).grid(row=2, column=1, padx=10, pady=5)

tk.Button(entry_frame, text="Add Item", command=add_item, bg="green", fg="white", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=10)

# Bill Frame
bill_frame = tk.Frame(root, bg="#ECF0F1", bd=5, relief="ridge")
bill_frame.pack(pady=10, padx=10, fill="both", expand=True)

tk.Label(bill_frame, text="Bill Details", font=("Arial", 14, "bold"), bg="#ECF0F1").pack(pady=5)
bill_listbox = tk.Listbox(bill_frame, font=("Arial", 12), height=8)
bill_listbox.pack(padx=10, pady=5, fill="both", expand=True)

# Total & Buttons
total_frame = tk.Frame(root, bg="#2C3E50")
total_frame.pack(pady=10, fill="x")

tk.Label(total_frame, text="Total Amount (Rs):", font=("Arial", 14, "bold"), bg="#2C3E50", fg="white").pack(side="left", padx=10)
tk.Label(total_frame, textvariable=total_var, font=("Arial", 14, "bold"), bg="#2C3E50", fg="yellow").pack(side="left")

button_frame = tk.Frame(root, bg="#2C3E50")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Generate Bill", command=generate_bill, bg="#2980B9", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Clear Bill", command=clear_bill, bg="#C0392B", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Print Bill", command=print_bill, bg="#8E44AD", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10)

# Bill Receipt Box
tk.Label(root, text="Generated Bill Receipt", font=("Arial", 12, "bold"), bg="#2C3E50", fg="white").pack(pady=5)
bill_text = tk.Text(root, height=10, font=("Arial", 11))
bill_text.pack(padx=10, pady=5, fill="both")

root.mainloop()
