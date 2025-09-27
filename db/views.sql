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
    p.name as product_name,
    cat.name as category_name,
    count(il.id) as sales_count,
    sum(il.quantity) as total_quantity,
    sum(il.line_total) as total_sales
from public.invoices i
join public.invoice_lines il on il.invoice_id = i.id
join public.products p on p.id = il.product_id
join public.categories cat on cat.id = p.category_id
where i.invoice_date >= current_date - interval '30 days'
group by p.id, p.name, cat.name
order by total_sales desc;

-- Habilitar RLS en las vistas
alter view public.v_sales_fact enable row level security;
alter view public.v_sales_by_category enable row level security;
alter view public.v_sales_by_country enable row level security;
alter view public.v_top_products_30d enable row level security;

-- Políticas para las vistas (mismas restricciones que las tablas base)
create policy "v_sales_fact_select" on public.v_sales_fact for select to authenticated 
using (
    exists (
        select 1 from public.user_allowed_country u 
        where u.user_id = auth.uid() and u.country_code = v_sales_fact.country_code
    )
    and
    exists (
        select 1 from public.user_allowed_category u 
        where u.user_id = auth.uid() and u.category_id in (
            select category_id from public.products where name = v_sales_fact.product_name
        )
    )
);