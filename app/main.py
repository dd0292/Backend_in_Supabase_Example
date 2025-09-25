import os 
from supabase import create_client, Client 
from dotenv import load_dotenv
load_dotenv()


URL = os.getenv("SUPABASE_URL") 
KEY = os.getenv("SUPABASE_ANON_KEY") 
EMAIL = os.getenv("USER_EMAIL") 
PWD = os.getenv("USER_PASSWORD") 
 
def login() -> Client: 
    sb: Client = create_client(URL, KEY) 
    auth = sb.auth.sign_in_with_password({"email": EMAIL, "password": 
PWD}) 
    if not auth.session: 
        raise SystemExit("Login failed.") 
    print("Logged in:", auth.user.email) 
    return sb 
 
def list_my_products(sb: Client): 
    res = sb.table("products").select("*").execute() 
    print("Products (RLS applied):", res.data) 
 
def list_my_customers(sb: Client): 
    res = sb.table("customers").select("*").execute() 
    print("Customers (RLS applied):", res.data) 
 
def create_invoice(sb: Client, customer_id: int): 
    inv = sb.table("invoices").insert({"customer_id": 
customer_id}).select("*").execute() 
    print("Invoice:", inv.data) 
    return inv.data[0]["id"] 
 
def add_line(sb: Client, invoice_id: int, product_id: int, qty: float, 
unit_price: float): 
    line_total = round(qty * unit_price, 2) 
    line = { 
        "invoice_id": invoice_id, 
        "product_id": product_id, 
        "quantity": qty, 
        "unit_price": unit_price, 
        "line_total": line_total 
    } 
    res = sb.table("invoice_lines").insert(line).select("*").execute() 
    print("Line:", res.data) 
 
def show_invoice_with_lines(sb: Client, invoice_id: int): 
    inv = sb.table("invoices").select("*").eq("id", 
invoice_id).execute() 
    lines = sb.table("invoice_lines").select("*").eq("invoice_id", 
invoice_id).execute() 
    print("Invoice:", inv.data) 
    print("Lines:", lines.data) 
 
if __name__ == "__main__": 
    
    sb = login() 
    list_my_products(sb) 
    list_my_customers(sb) 
    # Completar: input() para IDs y crear factura + líneas