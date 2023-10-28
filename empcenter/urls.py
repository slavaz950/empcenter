from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('api/', include('api.urls')),    # Приложение  api
    path('', include('main.urls')),       # Приложение main  
    path ('accounts', include("django.contrib.auth.urls"))  # from video
]

 
if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
Статические файлы сайта не будут кэшироваться веб-обозревателем - 
так как работа над таблицей ещё не завершена


if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
"""