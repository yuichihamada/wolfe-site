from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
  DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / '.env')

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY', default='dev-key')
ALLOWED_HOSTS = [h.strip() for h in env('ALLOWED_HOSTS', default='').split(',') if h.strip()] or ['*']

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'content',
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
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
  }
}

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'content' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ここから下を末尾などに追記
WOLFE_GATE_PASSWORD = env('WOLFE_GATE_PASSWORD', default='wolfe-education')

GATE_VERSION = env.str('WOLFE_GATE_VERSION', default='v1')

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