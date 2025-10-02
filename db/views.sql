-- 11.2 Vista general de ventas
create or replace view public.v_sales_fact as
select 
    i.id as invoice_id,
    i.invoice_date,
    i.total_amount,
    c.name as customer_name,
    c.country_code,
    p.name as product_name,
    cat.name as category_name,
    cat.id as category_id,  -- Added for RLS filtering
    il.quantity,
    il.unit_price,
    il.line_total
from public.invoices i
join public.customers c on c.id = i.customer_id
join public.invoice_lines il on il.invoice_id = i.id
join public.products p on p.id = il.product_id
join public.categories cat on cat.id = p.category_id;

-- Ventas por categoría
create or replace view public.v_sales_by_category as
select 
    cat.id as category_id,  -- Added for RLS filtering
    cat.name as category_name,
    count(distinct i.id) as invoice_count,
    count(il.id) as line_count,
    sum(il.quantity) as total_quantity,
    sum(il.line_total) as total_sales
from public.invoices i
join public.invoice_lines il on il.invoice_id = i.id
join public.products p on p.id = il.product_id
join public.categories cat on cat.id = p.category_id
group by cat.id, cat.name;

-- Ventas por país
create or replace view public.v_sales_by_country as
select 
    c.country_code,
    co.name as country_name,
    count(distinct i.id) as invoice_count,
    count(il.id) as line_count,
    sum(il.quantity) as total_quantity,
    sum(il.line_total) as total_sales
from public.invoices i
join public.customers c on c.id = i.customer_id
join public.countries co on co.code = c.country_code
join public.invoice_lines il on il.invoice_id = i.id
group by c.country_code, co.name;

-- Top productos últimos 30 días
create or replace view public.v_top_products_30d as
select 
    p.id as product_id,  -- Added for RLS filtering
    p.name as product_name,
    cat.id as category_id,  -- Added for RLS filtering
    cat.name as category_name,
    count(il.id) as sales_count,
    sum(il.quantity) as total_quantity,
    sum(il.line_total) as total_sales
from public.invoices i
join public.invoice_lines il on il.invoice_id = i.id
join public.products p on p.id = il.product_id
join public.categories cat on cat.id = p.category_id
where i.invoice_date >= current_date - interval '30 days'
group by p.id, p.name, cat.id, cat.name
order by total_sales desc;

-- En su lugar, usar security_barrier y security_invoker
alter view public.v_sales_fact set (security_barrier = true);
alter view public.v_sales_by_category set (security_barrier = true);
alter view public.v_sales_by_country set (security_barrier = true);
alter view public.v_top_products_30d set (security_barrier = true);