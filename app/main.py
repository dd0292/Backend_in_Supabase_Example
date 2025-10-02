import os 
import json
from supabase import create_client, Client 
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv("SUPABASE_URL") 
KEY = os.getenv("SUPABASE_ANON_KEY") 
EMAIL = os.getenv("USER_EMAIL") 
PWD = os.getenv("USER_PASSWORD") 

# For multiple users (to test RLS):
EMAIL_01 = os.getenv("USER01_EMAIL")
PWD_01 = os.getenv("USER01_PASSWORD")
EMAIL_02 = os.getenv("USER02_EMAIL")
PWD_02 = os.getenv("USER02_PASSWORD")
EMAIL_03 = os.getenv("USER03_EMAIL")
PWD_03 = os.getenv("USER03_PASSWORD")
 
def login(user_email:str,user_passowrd:str) -> Client: 
    
    sb: Client = create_client(URL, KEY) 
    auth = sb.auth.sign_in_with_password({"email": user_email, "password":user_passowrd}) #Change access here
    
    if not auth.session: 
        raise SystemExit("Login failed.") 
    print("Logged in:", auth.user.email) 
    print("User ID:", auth.user.id) 
    return sb 
 
def list_my_products(sb: Client): 
    products = sb.table("products").select("id, name, category_id", "unit_price").execute()
    category_details = sb.table("categories").select("*").execute()
    cat_map = {cat["id"]: cat["name"] for cat in category_details.data}
    print("Products (RLS applied):", [(prod["id"], prod["name"], cat_map.get(prod["category_id"])) for prod in products.data]) 
    return products.data

def list_my_customers(sb: Client): 
    customers = sb.table("customers").select("*").execute() 
    print("Customers (RLS applied):", [(cx["id"],cx["name"], cx["country_code"]) for cx in customers.data]) 
    return customers.data
 
def create_invoice(sb: Client, customer_id: int): 
    inv = sb.table("invoices").insert({"customer_id": customer_id}).execute() 
    print("Invoice:", inv.data) 
    return inv.data[0]["id"] 
 
def add_line(sb: Client, invoice_id: int, product_id: int, qty: float, unit_price: float): 
    line_total = round(qty * unit_price, 2) 
    line = { 
        "invoice_id": invoice_id, 
        "product_id": product_id, 
        "quantity": qty, 
        "unit_price": unit_price, 
        "line_total": line_total 
    } 
    res = sb.table("invoice_lines").insert(line).execute() 
    print("Line:", res.data) 
 
def show_invoice_with_lines(sb: Client, invoice_id: int): 
    inv = sb.table("invoices").select("*").eq("id", invoice_id).execute() 

    lines = sb.table("invoice_lines").select("*").eq("invoice_id", invoice_id).execute() 
    print("Invoice:", inv.data) 
    print("Lines:", lines.data) 
 
def debug_user_permissions(sb: Client):
    user_id = sb.auth.get_user().user.id
    
    # Country permissions
    countries = sb.table("user_allowed_country").select("*").eq("user_id", user_id).execute()
    print(f"Country permissions:", [country["country_code"] for country in countries.data])
    
    # Category permissions  
    categories = sb.table("user_allowed_category").select("*").eq("user_id", user_id).execute()
    category_ids = [category["category_id"] for category in categories.data]
    category_details = sb.table("categories").select("*").in_("id", category_ids).execute()
    print(f"Category permissions:", [cat["name"] for cat in category_details.data])
    
def create_invoice_menu(sb: Client, customers, products):
    # Select customer
    try:
        customer_id = int(input("Enter customer ID for the invoice: "))
    except ValueError:
        print("Invalid input.")
        return
    if not any(c["id"] == customer_id for c in customers):
        print("Customer ID not found.")
        return

    # Build items list
    items = []
    while True:
        if not products:
            print("No products available.")
            break
        print("\nProducts:")
        for p in products:
            print(f"{p['id']}: {p['name']} (${p['unit_price']})")
        try:
            product_id = int(input("Enter product ID to add (or 0 to finish): "))
        except ValueError:
            print("Invalid input.")
            continue
        if product_id == 0:
            break
        if not any(p["id"] == product_id for p in products):
            print("Product ID not found.")
            continue
        try:
            qty = float(input("Enter quantity: "))
            unit_price_input = input("Enter unit price (leave blank to use default): ")
            item = {"product_id": product_id, "quantity": qty}
            if unit_price_input.strip():
                item["unit_price"] = float(unit_price_input)
            items.append(item)
            print("Item added.")
        except ValueError:
            print("Invalid number.")
            continue

    if not items:
        print("No items to invoice.")
        return

    # Build payload
    payload = {
        "customer_id": customer_id,
        "items": items
    }

    # Call the RPC function
    try:
        print("Creating invoice with payload:", payload)
        response = sb.rpc("create_invoice", payload).execute() #ESTO SE EJECUTA NO PROBLEMO; PERO IGUAL SE CAE!
        data = response.data
        
    except Exception as e:
        if (e.__getattribute__('code')!= 200):
            print("Error creating invoice:", e)
        else:
            print("Invoice created successfully.") #I THINK

def list_invoices(sb: Client):
    invoices = sb.table("invoices").select("*").execute()

    if not invoices:
        print("No invoices found.")
        return

    for inv in invoices.data:
        customer_name = sb.table("customers").select("name").eq("id", inv["customer_id"]).execute().data[0]["name"]
        print(f"\nInvoice for {customer_name} : ${inv['total_amount']}")
        # Get lines for this invoice
        lines = sb.table("invoice_lines").select("*").eq("invoice_id", inv["id"]).execute().data
        for line in lines:
            product_name, default_unit_price = sb.table("products").select("name, unit_price").eq("id", line["product_id"]).execute().data[0].values()
            print(f"- {line['quantity']} {product_name} : ${line['line_total']} (${line['unit_price']})")

def list_invoices_by_customer(sb: Client, customers):
    try:
        customer_id = int(input("Enter customer ID to filter invoices: "))
    except ValueError:
        print("Invalid input.")
        return
    
    if not any(c["id"] == customer_id for c in customers):
        print("Customer ID not found.")
        return

    # Fetch invoices for this customer
    invoices = sb.table("invoices").select("*").eq("customer_id", customer_id).execute()
    if not invoices.data:
        print("No invoices found for this customer.")
        return

    customer_name = sb.table("customers").select("name").eq("id", customer_id).execute().data[0]["name"]
    print(f"\nInvoices for {customer_name}:")

    for inv in invoices.data:
        print(f"Invoice {inv['id']} on {inv['invoice_date']} - Total: ${inv['total_amount']}")
        lines = sb.table("invoice_lines").select("*").eq("invoice_id", inv["id"]).execute().data
        for line in lines:
            product = sb.table("products").select("name").eq("id", line["product_id"]).execute().data[0]
            print(f"  - {line['quantity']} x {product['name']} @ ${line['unit_price']} = ${line['line_total']}")

def list_invoices_by_product(sb: Client, products):
    try:
        product_id = int(input("Enter product ID to filter invoices: "))
    except ValueError:
        print("Invalid input.")
        return
    
    if not any(p["id"] == product_id for p in products):
        print("Product ID not found.")
        return

    product_name = sb.table("products").select("name").eq("id", product_id).execute().data[0]["name"]

    # Find all invoice_lines that contain this product
    lines = sb.table("invoice_lines").select("invoice_id, quantity, unit_price, line_total").eq("product_id", product_id).execute()
    if not lines.data:
        print(f"No invoices found containing product {product_name}.")
        return

    print(f"\nInvoices containing product '{product_name}':")
    for line in lines.data:
        inv = sb.table("invoices").select("*").eq("id", line["invoice_id"]).execute().data[0]
        customer_name = sb.table("customers").select("name").eq("id", inv["customer_id"]).execute().data[0]["name"]
        print(f"Invoice {inv['id']} for {customer_name} - Date {inv['invoice_date']} - Total ${inv['total_amount']}")
        print(f"  -> {line['quantity']} x {product_name} @ ${line['unit_price']} = ${line['line_total']}")

def list_invoices_by_country(sb: Client, customers):
    country_code = input("Enter country code (e.g., US, CR): ").strip().upper()
    if not any(c["country_code"].upper() == country_code for c in customers):
        print("No customers found in that country.")
        return

    # Get all customers in this country
    customer_ids = [c["id"] for c in customers if c["country_code"].upper() == country_code]

    invoices = sb.table("invoices").select("*").in_("customer_id", customer_ids).execute()
    if not invoices.data:
        print(f"No invoices found for customers in {country_code}.")
        return

    print(f"\nInvoices for customers in {country_code}:")
    for inv in invoices.data:
        customer_name = sb.table("customers").select("name").eq("id", inv["customer_id"]).execute().data[0]["name"]
        print(f"Invoice {inv['id']} for {customer_name} - Date {inv['invoice_date']} - Total ${inv['total_amount']}")
        lines = sb.table("invoice_lines").select("*").eq("invoice_id", inv["id"]).execute().data
        for line in lines:
            product_name = sb.table("products").select("name").eq("id", line["product_id"]).execute().data[0]["name"]
            print(f"  -> {line['quantity']} x {product_name} @ ${line['unit_price']} = ${line['line_total']}")

def list_invoices_by_date_range(sb: Client):
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()

    invoices = sb.table("invoices").select("*").gte("invoice_date", start_date).lte("invoice_date", end_date).execute()
    if not invoices.data:
        print(f"No invoices found between {start_date} and {end_date}.")
        return

    print(f"\nInvoices from {start_date} to {end_date}:")
    for inv in invoices.data:
        customer_name = sb.table("customers").select("name").eq("id", inv["customer_id"]).execute().data[0]["name"]
        print(f"Invoice {inv['id']} for {customer_name} - Date {inv['invoice_date']} - Total ${inv['total_amount']}")
        lines = sb.table("invoice_lines").select("*").eq("invoice_id", inv["id"]).execute().data
        for line in lines:
            product_name = sb.table("products").select("name").eq("id", line["product_id"]).execute().data[0]["name"]
            print(f"  -> {line['quantity']} x {product_name} @ ${line['unit_price']} = ${line['line_total']}")


if __name__ == "__main__": 
    print("Choose user to log in:")
    print("1. User 1")
    print("2. User 2")
    print("3. User 3")
    print("4. Admin!")
    choice = input("Enter choice (1-4): ")
    if choice == "1":   
        em, pwd = EMAIL_01, PWD_01
    elif choice == "2":
        em, pwd = EMAIL_02, PWD_02
    elif choice == "3":
        em, pwd = EMAIL_03, PWD_03
    elif choice == "4":
        em, pwd = EMAIL, PWD
    else:
        print("Invalid choice.")
        exit(1)

    sb = login(em, pwd)
    debug_user_permissions(sb)
    products = list_my_products(sb) 
    customers = list_my_customers(sb) 
    
    # Completar: input() para IDs y crear factura + líneas
    while True:
        print("\nMenu:")
        print("1. Create invoice")
        print("2. List invoices")
        print("3. Filter invoices by customer")
        print("4. Filter invoices by product")
        print("5. Filter invoices by country")
        print("6. Filter invoices by date range")
        print("7. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            create_invoice_menu(sb, customers, products)
        elif choice == "2":
            list_invoices(sb)
        elif choice == "3":
            list_invoices_by_customer(sb, customers)
        elif choice == "4":
            list_invoices_by_product(sb, products)
        elif choice == "5":
            list_invoices_by_country(sb, customers)
        elif choice == "6":
            list_invoices_by_date_range(sb)
        elif choice == "7":
            break
        else:
            print("Invalid option.")

    


    
    