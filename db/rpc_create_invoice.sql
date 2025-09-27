-- Función RPC para crear factura y líneas en una transacción atómica
create or replace function public.create_invoice(
    customer_id bigint,
    items jsonb
)
returns jsonb
language plpgsql
security invoker
as $$
declare
    new_invoice_id bigint;
    item_record jsonb;
    product_record record;
    total_amount numeric(14,2) := 0;
    line_total numeric(14,2);
begin
    -- Verificar que el cliente existe y el usuario tiene permisos (RLS aplica)
    if not exists (select 1 from public.customers where id = customer_id) then
        return json_build_object('error', 'Customer not found or access denied');
    end if;

    -- Insertar la factura
    insert into public.invoices (customer_id, total_amount)
    values (customer_id, 0)
    returning id into new_invoice_id;

    -- Procesar cada item
    for item_record in select * from jsonb_array_elements(items)
    loop
        -- Obtener información del producto (RLS aplica)
        select * into product_record 
        from public.products 
        where id = (item_record->>'product_id')::bigint;

        if not found then
            rollback;
            return json_build_object('error', 'Product not found or access denied: ' || (item_record->>'product_id'));
        end if;

        -- Calcular total de línea
        line_total := (item_record->>'quantity')::numeric(12,2) * 
                     coalesce((item_record->>'unit_price')::numeric(12,2), product_record.unit_price);
        
        total_amount := total_amount + line_total;

        -- Insertar línea de factura
        insert into public.invoice_lines (
            invoice_id, 
            product_id, 
            quantity, 
            unit_price, 
            line_total
        ) values (
            new_invoice_id,
            (item_record->>'product_id')::bigint,
            (item_record->>'quantity')::numeric(12,2),
            coalesce((item_record->>'unit_price')::numeric(12,2), product_record.unit_price),
            line_total
        );
    end loop;

    -- Actualizar el total de la factura
    update public.invoices 
    set total_amount = total_amount 
    where id = new_invoice_id;

    return json_build_object(
        'invoice_id', new_invoice_id,
        'total_amount', total_amount,
        'message', 'Invoice created successfully'
    );
end;
$$;