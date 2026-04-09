import os
from supabase import create_client, Client
from flask import current_app

def get_supabase() -> Client:
    # Obtener variables desde entorno puro
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Faltan las credenciales de Supabase en el entorno.")
    return create_client(url, key)

# Cliente instanciado genérico para storage y bd
supabase_client = get_supabase()
