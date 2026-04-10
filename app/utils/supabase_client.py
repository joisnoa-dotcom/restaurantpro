import os
from supabase import create_client, Client

_client = None

def get_supabase() -> Client:
    """Obtiene el cliente de Supabase con lazy initialization."""
    global _client
    if _client is None:
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Faltan las credenciales de Supabase en el entorno.")
        _client = create_client(url, key)
    return _client
