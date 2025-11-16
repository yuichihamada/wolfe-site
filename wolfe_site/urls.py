from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth import get_user_model

def run_migrate(request):
    # マイグレーション実行
    call_command("migrate", interactive=False)

    # スーパーユーザー作成（存在しなければ）
    User = get_user_model()
    username = "yuichihamada"
    email = "ilovemrchildrensazan@gmail.com"
    password = "好きなパスワードここに"  # あとで変えたければ admin から変更可

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)

    return HttpResponse("Migration & superuser done.")

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('content.urls')),
  path("run-migrate/", run_migrate),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)