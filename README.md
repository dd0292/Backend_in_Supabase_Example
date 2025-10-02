# Backend — Supabase (Example)

By: David Chaves Mena, Sergio, Igancion, Rachel, Rodrigo Donoso

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
1. Open Supabase Studio → SQL editor.
2. Paste and run `db/schema.sql`.
3. Run `db/seeds.sql` to insert minimal demo data.
4. Run `db/policies.sql` to enable RLS and policies.
5. Run `db/rpc_create_invoice.sql` to install the RPC.
6. Run `db/views.sql` to install reporting views.
7. Create test users in Auth and populate `user_allowed_*` tables (see `/db/auth_seeds.md`).
8. Run Python app:
   ```bash
   cd app
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   export SUPABASE_URL=...
   export SUPABASE_ANON_KEY=...
   export USER_EMAIL=...
   export USER_PASSWORD=...
   python main.py
   ```
