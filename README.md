# REBIRTH Connect Site (Django)

## 1) セットアップ
```bash
python -m venv .venv && source .venv/bin/activate # Windowsは .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser # 管理ユーザ作成
python manage.py runserver