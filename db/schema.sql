-- 4 Models / Tables

--4.1  Dominios
create table if not exists public.countries (
    code text primary key,
    name text not null
);

create table if not exists public.categories (
    id bigint generated always as identity primary key,
    name text not null unique
);

-- 4.2 Comercial
create table if not exists public.products (
    id bigint generated always as identity primary key,
    name text not null,
    category_id bigint not null references public.categories(id),
    unit_price numeric(12,2) not null check (unit_price >= 0),
    created_at timestamptz default now()
);

create table if not exists public.customers (
    id bigint generated always as identity primary key,
    name text not null,
    email text,
    country_code text not null references public.countries(code),
    created_at timestamptz default now()
);

create table if not exists public.invoices (
    id bigint generated always as identity primary key,
    customer_id bigint not null references public.customers(id),
    invoice_date date not null default current_date,
    total_amount numeric(14,2) not null default 0,
    created_at timestamptz default now()
);

create table if not exists public.invoice_lines (
    id bigint generated always as identity primary key,
    invoice_id bigint not null references public.invoices(id) on delete cascade,
    product_id bigint not null references public.products(id),
    quantity numeric(12,2) not null check (quantity > 0),
    unit_price numeric(12,2) not null check (unit_price >= 0),
    line_total numeric(14,2) not null check (line_total >= 0)
);

-- 4.3 Tablas de Autorización (para RLS)
create table if not exists public.user_allowed_country (
    user_id uuid references auth.users(id) on delete cascade,
    country_code text not null references public.countries(code),
    primary key (user_id, country_code)
);

create table if not exists public.user_allowed_category (
    user_id uuid references auth.users(id) on delete cascade,
    category_id bigint not null references public.categories(id),
    primary key (user_id, category_id)
);

-- (Optional): Index
create index if not exists idx_products_category_id on public.products(category_id);
create index if not exists idx_customers_country_code on public.customers(country_code);
create index if not exists idx_invoices_customer_id on public.invoices(customer_id);
create index if not exists idx_invoice_lines_invoice_id on public.invoice_lines(invoice_id);
create index if not exists idx_invoice_lines_product_id on public.invoice_lines(product_id);
create index if not exists idx_user_allowed_country_user_id on public.user_allowed_country(user_id);
create index if not exists idx_user_allowed_category_user_id on public.user_allowed_category(user_id);
