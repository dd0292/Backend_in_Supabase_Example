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

-- Nota: Los usuarios de Auth se deben crear manualmente en Supabase Studio
-- y luego insertar sus autorizaciones aquí (reemplazar los UUIDs con los reales)
/*
-- Ejemplo de inserción de autorizaciones (ejecutar después de crear usuarios en Auth)
insert into public.user_allowed_country (user_id, country_code) values
('uuid-usuario-1', 'US'),
('uuid-usuario-1', 'CR'),
('uuid-usuario-2', 'MX'),
('uuid-usuario-2', 'BR');

insert into public.user_allowed_category (user_id, category_id) values
('uuid-usuario-1', 1),
('uuid-usuario-1', 2),
('uuid-usuario-2', 3),
('uuid-usuario-2', 4);
*/