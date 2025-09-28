-- 6 Habilitar RLS en todas las tablas
alter table public.countries enable row level security;
alter table public.categories enable row level security;
alter table public.products enable row level security;
alter table public.customers enable row level security;
alter table public.invoices enable row level security;
alter table public.invoice_lines enable row level security;
alter table public.user_allowed_country enable row level security;
alter table public.user_allowed_category enable row level security;

-- 6.1 por categoría (products)
create policy "products_by_user_category_select" 
on public.products for select 
to authenticated 
using (exists ( 
  select 1 from public.user_allowed_category u 
  where u.user_id = auth.uid() and u.category_id = products.category_id 
)); 
 
create policy "products_by_user_category_insert" 
on public.products for insert 
to authenticated 
with check (exists ( 
  select 1 from public.user_allowed_category u 
  where u.user_id = auth.uid() and u.category_id = products.category_id 
)); 
 
create policy "products_by_user_category_update" 
on public.products for update 
to authenticated 
using (exists ( 
  select 1 from public.user_allowed_category u 
  where u.user_id = auth.uid() and u.category_id = products.category_id 
)) 
with check (exists ( 
  select 1 from public.user_allowed_category u 
  where u.user_id = auth.uid() and u.category_id = products.category_id 
)); 
 
create policy "products_by_user_category_delete" 
on public.products for delete 
to authenticated 
using (exists ( 
  select 1 from public.user_allowed_category u 
  where u.user_id = auth.uid() and u.category_id = products.category_id 
));


-- 6.2 por país (customers)
create policy "customers_by_user_country_select" 
on public.customers for select 
to authenticated 
using (exists ( 
  select 1 from public.user_allowed_country u 
  where u.user_id = auth.uid() and u.country_code = 
customers.country_code 
));

-- 6.3 invoices (pais de cliente)

create policy "invoices_by_user_country_select" 
on public.invoices for select 
to authenticated 
using (exists ( 
  select 1 
  from public.customers c 
  join public.user_allowed_country u 
    on u.country_code = c.country_code and u.user_id = auth.uid() 
  where c.id = invoices.customer_id 
));

-- 6.4 invoice_lines (pais y categoria)
create policy "lines_by_country_and_category_select" 
on public.invoice_lines for select 
to authenticated 
using ( 
  exists ( 
    select 1 
    from public.invoices i 
    join public.customers c on c.id = i.customer_id 
    join public.user_allowed_country uc 
      on uc.country_code = c.country_code and uc.user_id = auth.uid() 
    where i.id = invoice_lines.invoice_id 
  ) 
  and 
  exists ( 
    select 1 
    from public.products p 
    join public.user_allowed_category ug 
      on ug.category_id = p.category_id and ug.user_id = auth.uid() 
    where p.id = invoice_lines.product_id 
  ) 
); 
 
create policy "lines_by_country_and_category_cud" 
on public.invoice_lines for all 
to authenticated 
using ( 
  exists ( 
    select 1 
    from public.invoices i 
    join public.customers c on c.id = i.customer_id 
    join public.user_allowed_country uc 
      on uc.country_code = c.country_code and uc.user_id = auth.uid() 
    where i.id = invoice_lines.invoice_id 
  ) 
  and 
  exists ( 
    select 1 
    from public.products p 
    join public.user_allowed_category ug 
      on ug.category_id = p.category_id and ug.user_id = auth.uid() 
    where p.id = invoice_lines.product_id 
  ) 
) 
with check ( 
  exists ( 
    select 1 
    from public.invoices i 
    join public.customers c on c.id = i.customer_id 
    join public.user_allowed_country uc 
      on uc.country_code = c.country_code and uc.user_id = auth.uid() 
    where i.id = invoice_lines.invoice_id 
  ) 
  and 
  exists ( 
    select 1 
    from public.products p 
    join public.user_allowed_category ug 
      on ug.category_id = p.category_id and ug.user_id = auth.uid() 
    where p.id = invoice_lines.product_id 
  ) 
);

create policy"user_see_own_category_perms" 
on public.user_allowed_categoryforR select 
to authenticated using (user_id = auth.uid());

create policy"user_see_own_country_perms" 
on public.user_allowed_country for select 
to authenticated using (user_id = auth.uid());