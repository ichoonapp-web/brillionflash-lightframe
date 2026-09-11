from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "Brillionflash is Live!",
        "version": "3.0.0",
        "app": "Brillionflash - Light Frame",
    })

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.user_auth.urls')),
    path('api/flasher/', include('apps.flasher.urls')),
    path('api/ai/', include('apps.ai.urls')),
    path('api/marketplace/', include('apps.marketplace.urls')),
    path('api/social/', include('apps.social.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]


