# Backend — Supabase (Example)

By: 
 - David Chaves Mena
 - Sergio Zúñiga Castillo
 - Igancio Madriz Ortiz
 - Rachel Leiva
 - Rodrigo Donoso

**Short**: Example of a backend of a sales app using Supabase (Postgres + PostgREST + Auth) with a small Python client to exercise RLS and RPCs.

**Spec**: follows the [lab_instructions](Lab_Backend_Supabase_Spec.pdf) (tables, RLS, RPC, views, deliverables).

## Repo layout
See `/db`, `/app`, `/tests`, `/deliverables`.

## Repo structure
```bash
.
├─ README.md
├─ db/
│  ├─ schema.sql
│  ├─ seeds.sql
│  ├─ policies.sql
│  ├─ rpc_create_invoice.sql
│  └─ views.sql
├─ app/
│  ├─ main.py
│  └─ requirements.txt
├─ tests/
│  ├─ postman_collection.json
│  └─ postman.md
└─ deliverables/
    └─ video.mp4 
```

## Prerequisites
- Supabase project created (use Supabase Studio).  
- Python 3.10+ (`pip install -r app/requirements.txt`).
- Environment variables (set in your shell or `.env`):
  - `SUPABASE_URL` — your project URL
  - `SUPABASE_ANON_KEY` — anon/public key for the client app
  - `USER_EMAIL` / `USER_PASSWORD` — test user credentials (for app quick-demo)

## Quick start
### Run Python app:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```
