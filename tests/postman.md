# Guía de Pruebas Postman

## Configuración
1. Importar la colección `Lab_Ventas_Supabase.postman_collection.json`
2. Configurar environment variables:
   - SUPABASE_URL: https://tu-proyecto.supabase.co
   - SUPABASE_ANON_KEY: tu_anon_key

## Flujo de Pruebas
1. Ejecutar "User1 Auth"
2. Ejecutar secuencialmente los demás requests
3. Probar con User2 y User3 para verificar RLS

## Endpoints probados:
-  Productos por categoría (RLS aplica)
-  Clientes por país (RLS aplica)
-  Facturas con cliente embebido
-  Detalle con producto embebido (RLS doble)	
