import os 
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
    auth = sb.auth.sign_in_with_password({"email": EMAIL_02, "password":PWD_02}) #Change access here
    
    if not auth.session: 
        raise SystemExit("Login failed.") 
    print("Logged in:", auth.user.email) 
    print("User ID:", auth.user.id) 
    return sb 
 
def list_my_products(sb: Client): 
    # Check all products and their categories
    products = sb.table("products").select("id, name, category_id").execute()
    category_details = sb.table("categories").select("*").execute()
    cat_map = {cat["id"]: cat["name"] for cat in category_details.data}
    res = sb.table("products").select("*").execute() 
    print("Products (RLS applied):", [(prod["name"], cat_map.get(prod["category_id"])) for prod in products.data]) 
 
def list_my_customers(sb: Client): 
    res = sb.table("customers").select("*").execute() 
    print("Customers (RLS applied):", [(cx["name"], cx["country_code"]) for cx in res.data]) 
 
def create_invoice(sb: Client, customer_id: int): 
    inv = sb.table("invoices").insert({"customer_id": customer_id}).select("*").execute() 
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
    res = sb.table("invoice_lines").insert(line).select("*").execute() 
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
    
    

if __name__ == "__main__": 
    
    sb = login() 
    debug_user_permissions(sb)
    list_my_products(sb) 
    list_my_customers(sb) 
    # Completar: input() para IDs y crear factura + líneas
    
    """ 
    CRUD	básico	de	categorías	y	productos.
    CRUD	básico	de	países	y	clientes.
    Registro	de	facturas	y	detalle	de	factura	(líneas).
    Listados	y	filtros	(por	categoría,	por	país,	por	rango	de	fechas). 
    """
    
    