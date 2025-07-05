import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# データベース設定
DATABASE_URL = os.getenv("DATABASE_URL")

# データベースURLが設定されていない場合のデフォルト値
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# その他の設定
class Settings:
    DATABASE_URL: str = DATABASE_URL
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "POS App"

settings = Settings() 