from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'diary'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    path('transaction/add/', views.add_transaction, name='add_transaction'),
    path('transaction/delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('reports/data/<str:report_type>/', views.get_report_data, name='get_report_data'),

    # Categorias
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),

    # Perfil
    path('profile/', views.profile, name='profile'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
