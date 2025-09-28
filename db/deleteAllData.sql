-- 1. DISABLE RLS ON ALL TABLES FIRST
ALTER TABLE public.countries DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.categories DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.products DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.customers DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.invoices DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.invoice_lines DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_allowed_country DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_allowed_category DISABLE ROW LEVEL SECURITY;

-- 2. DROP ALL RLS POLICIES
DROP POLICY IF EXISTS "products_by_user_category_select" ON public.products;
DROP POLICY IF EXISTS "products_by_user_category_insert" ON public.products;
DROP POLICY IF EXISTS "products_by_user_category_update" ON public.products;
DROP POLICY IF EXISTS "products_by_user_category_delete" ON public.products;
DROP POLICY IF EXISTS "customers_by_user_country_select" ON public.customers;
DROP POLICY IF EXISTS "invoices_by_user_country_select" ON public.invoices;
DROP POLICY IF EXISTS "lines_by_country_and_category_select" ON public.invoice_lines;
DROP POLICY IF EXISTS "lines_by_country_and_category_cud" ON public.invoice_lines;
DROP POLICY IF EXISTS "allow_read_user_allowed_category" ON public.user_allowed_category;
DROP POLICY IF EXISTS "allow_read_user_allowed_country" ON public.user_allowed_country;
DROP POLICY IF EXISTS "user_see_own_category_perms" ON public.user_allowed_category;
DROP POLICY IF EXISTS "user_see_own_country_perms" ON public.user_allowed_country;

-- 3. DELETE ALL DATA (in correct order due to foreign keys)
DELETE FROM public.invoice_lines;
DELETE FROM public.invoices;
DELETE FROM public.user_allowed_category;
DELETE FROM public.user_allowed_country;
DELETE FROM public.products;
DELETE FROM public.customers;
DELETE FROM public.categories;
DELETE FROM public.countries;

-- 4. RESET SEQUENCES (if you used serial IDs)
ALTER SEQUENCE IF EXISTS countries_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS categories_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS products_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS customers_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS invoices_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS invoice_lines_id_seq RESTART WITH 1;

-- 5. VERIFY EVERYTHING IS EMPTY
SELECT 'countries' as table_name, COUNT(*) as count FROM public.countries
UNION ALL
SELECT 'categories', COUNT(*) FROM public.categories
UNION ALL
SELECT 'products', COUNT(*) FROM public.products
UNION ALL
SELECT 'customers', COUNT(*) FROM public.customers
UNION ALL
SELECT 'invoices', COUNT(*) FROM public.invoices
UNION ALL
SELECT 'invoice_lines', COUNT(*) FROM public.invoice_lines
UNION ALL
SELECT 'user_allowed_country', COUNT(*) FROM public.user_allowed_country
UNION ALL
SELECT 'user_allowed_category', COUNT(*) FROM public.user_allowed_category;