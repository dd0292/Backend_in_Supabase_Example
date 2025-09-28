-- Insertar países
insert into public.countries (code, name) values
('US', 'United States'),
('CR', 'Costa Rica'),
('MX', 'Mexico'),
('BR', 'Brazil'),
('ES', 'Spain');

-- Insertar categorías
insert into public.categories (name) values
('Electronics'),
('Furniture'),
('Clothing'),
('Books'),
('Sports');

-- Insertar productos
insert into public.products (name, category_id, unit_price) values
('Laptop', 1, 999.99),
('Smartphone', 1, 699.99),
('Desk Chair', 2, 149.99),
('T-Shirt', 3, 19.99),
('Programming Book', 4, 39.99),
('Basketball', 5, 29.99);

-- Insertar clientes
insert into public.customers (name, email, country_code) values
('John Doe', 'john@example.com', 'US'),
('Maria Rodriguez', 'maria@example.com', 'CR'),
('Carlos Silva', 'carlos@example.com', 'MX'),
('Ana Costa', 'ana@example.com', 'BR'),
('Pedro Garcia', 'pedro@example.com', 'ES');

-- Note: Authentication users must be created manually in Supabase Studio 
-- and then insert your authorizations here (replace the UUIDs with the real ones)
/*
-- Example of inserting authorizations (running after creating users in Auth)

insert into public.user_allowed_country (user_id, country_code) values
('UUID-01', 'US'),
('UUID-01', 'CR'),
('UUID-01', 'MX'),
('UUID-01', 'BR'),
('UUID-01', 'ES'),

('UUID-02', 'US'),
('UUID-02', 'CR'),
('UUID-02', 'MX'),

('UUID-03', 'BR'),
('UUID-03', 'ES');

insert into public.user_allowed_category (user_id, category_id) values
('UUID-01', '1'),
('UUID-01', '2'),
('UUID-01', '3'),
('UUID-01', '4'),
('UUID-01', '5'),

('UUID-02', '1'),
('UUID-02', '2'),
('UUID-02', '3'),

('UUID-03', '4'),
('UUID-03', '5');
*/