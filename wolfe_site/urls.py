from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.core.management import call_command

def run_migrate(request):
    call_command("migrate")
    call_command("createsuperuser", 
                 username="yuichihamada",
                 email="ilovemrchildrensazan@gmail.com",
                 interactive=False)
    return HttpResponse("Migration & superuser done.")

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('content.urls')),
  path("run-migrate/", run_migrate),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)