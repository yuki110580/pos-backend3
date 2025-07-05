# pos-backend3/supabase_client.py

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # .envファイルから環境変数を読み込み

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SupabaseのURLまたはKEYが設定されていません")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
