from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


def robots_txt(request):
  return HttpResponse("User-agent: *\nDisallow: /\n", content_type="text/plain")


urlpatterns = [
  path('robots.txt', robots_txt),
  path('admin/', admin.site.urls),
  path("markdownx/", include("markdownx.urls")),
  path('', include('content.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)