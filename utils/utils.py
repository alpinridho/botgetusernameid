import json
import os
from config import ADMIN_FILE

def ensure_admin_file_exists():
    """Memastikan file admin JSON tersedia."""
    if not os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, 'w') as f:
            json.dump([], f)

def load_admins():
    """Memuat daftar admin dari file JSON."""
    ensure_admin_file_exists()
    try:
        with open(ADMIN_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_admins(admins):
    """Menyimpan daftar admin ke file JSON."""
    with open(ADMIN_FILE, 'w') as f:
        json.dump(admins, f)
