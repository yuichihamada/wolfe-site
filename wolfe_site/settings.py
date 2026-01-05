import dj_database_url
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
  DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / '.env')

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = [h.strip() for h in env('ALLOWED_HOSTS').split(',') if h.strip()] or ['*']

raw = env("CSRF_TRUSTED_ORIGINS")
CSRF_TRUSTED_ORIGINS = [x.strip() for x in raw.split(",") if x.strip()]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  "markdownx",
  'content',
  'storages',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'wolfe_site.middleware.AccessGateMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wolfe_site.urls'
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'content' / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]
WSGI_APPLICATION = 'wolfe_site.wsgi.application'

DATABASES = {
    "default": dj_database_url.config(
        default=env("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'content' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

USE_R2 = env.bool("USE_R2", default=False)

if USE_R2:
    AWS_ACCESS_KEY_ID = env("R2_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("R2_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("R2_BUCKET_NAME")

    # API endpoint（アップロード用）
    AWS_S3_ENDPOINT_URL = env("R2_ENDPOINT_URL")
    AWS_S3_REGION_NAME = "auto"
    AWS_S3_ADDRESSING_STYLE = "path"

    # 配信用ドメイン（表示用）: https://pub-xxxx.r2.dev/
    R2_MEDIA_URL = env("R2_MEDIA_URL").rstrip("/")  # 末尾スラッシュ除去
    AWS_S3_CUSTOM_DOMAIN = R2_MEDIA_URL.replace("https://", "").replace("http://", "")

    AWS_QUERYSTRING_AUTH = False  # 署名付きURLを使わない（公開配信前提）

    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
    }
    MEDIA_URL = R2_MEDIA_URL + "/"
else:
    # ローカル開発用
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

MARKDOWNX_MEDIA_PATH = "roadmap_md"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WOLFE_GATE_PASSWORD = env('WOLFE_GATE_PASSWORD')
GATE_VERSION = env.str('WOLFE_GATE_VERSION')

# ゲートのURLと除外URL（正規表現）
ACCESS_GATE_URL = '/gate/'
ACCESS_GATE_EXEMPT_URLS = [
    r'^/gate/',            # ゲートページ自身
    r'^/static/',          # 静的ファイル
    r'^/favicon\.ico$',    # favicon
    r'^/robots\.txt$',     # 任意
    r'^/admin/',           # AdminはDjangoのログインに任せる（必要に応じて外してもOK）
]

# 「覚えておく」期間（24時間）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24
