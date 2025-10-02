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
 
def login() -> Client: 
    
    sb: Client = create_client(URL, KEY) 
    auth = sb.auth.sign_in_with_password({"email": EMAIL_01, "password":PWD_01}) #Change access here
    
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

if __name__ == "__main__": 
    
    sb = login() 
    debug_user_permissions(sb)
    products = list_my_products(sb) 
    customers = list_my_customers(sb) 
    # Completar: input() para IDs y crear factura + líneas
    while True:
        print("\nMenu:")
        print("1. Create invoice")
        print("2. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            create_invoice_menu(sb, customers, products)
        elif choice == "2":
            break
        else:
            print("Invalid option.")

    

    """ 
    CRUD	básico	de	categorías	y	productos.
    CRUD	básico	de	países	y	clientes.
    Registro	de	facturas	y	detalle	de	factura	(líneas).
    Listados	y	filtros	(por	categoría,	por	país,	por	rango	de	fechas). 
    """

    
    