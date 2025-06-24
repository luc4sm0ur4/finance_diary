from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs do app de autenticação
    path('users/', include(('users.urls', 'users'), namespace='users')),
    
    # URLs principais do diário financeiro
    path('', include(('diary.urls', 'diary'), namespace='diary')),
]

# Servindo arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
