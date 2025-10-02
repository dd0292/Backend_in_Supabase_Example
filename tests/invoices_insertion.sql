INSERT INTO public.invoices (customer_id, invoice_date) 
VALUES
  (1, '2024-01-10'),  
  (1, '2024-01-15'),  
  (2, '2024-01-12'),  
  (2, '2024-01-18'),  
  (3, '2024-01-14'),  
  (3, '2024-01-20'),  
  (4, '2024-01-16'),  
  (4, '2024-01-22'),  
  (5, '2024-01-19'),  
  (5, '2024-01-25');  

-- Insertar líneas con IDs conocidos
INSERT INTO public.invoice_lines (invoice_id, product_id, quantity, unit_price, line_total) VALUES
  (1, 1, 1, 999.99, 999.99),
  (1, 2, 1, 699.99, 699.99),
  (2, 2, 1, 699.99, 699.99),
  (3, 4, 2, 19.99, 39.98),
  (3, 5, 1, 39.99, 39.99),
  (4, 3, 1, 149.99, 149.99),
  (5, 5, 1, 39.99, 39.99),
  (6, 4, 4, 19.99, 79.96),
  (7, 6, 1, 29.99, 29.99),
  (8, 4, 6, 19.99, 119.94),
  (9, 3, 1, 149.99, 149.99),
  (9, 6, 2, 19.99, 39.98),
  (10, 5, 1, 39.99, 39.99),
  (10, 4, 1, 19.99, 19.99);

-- Actualizar totales
UPDATE public.invoices i
SET total_amount = (
  SELECT COALESCE(SUM(line_total), 0)
  FROM public.invoice_lines il 
  WHERE il.invoice_id = i.id
);
