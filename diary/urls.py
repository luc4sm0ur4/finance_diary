from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import views_api

from rest_framework.routers import DefaultRouter

app_name = 'diary'

# Router para ViewSets da API
router = DefaultRouter()
router.register(r'api/transactions', views_api.TransactionViewSet, basename='api-transaction')
router.register(r'api/categories', views_api.CategoryViewSet, basename='api-category')
router.register(r'api/goals', views_api.GoalViewSet, basename='api-goal')

urlpatterns = [
    # Dashboard e relatórios
    path('', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    path('reports/data/<str:report_type>/', views.get_report_data, name='get_report_data'),

    # Transações
    path('transaction/add/', views.add_transaction, name='add_transaction'),
    path('transaction/delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('transaction/edit/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),

    # Categorias
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),

    # Perfil
    path('profile/', views.profile, name='profile'),

    # Metas financeiras
    path('goals/', views.goal_list, name='goal_list'),
    path('goals/add/', views.add_goal, name='add_goal'),
    path('goals/edit/<int:pk>/', views.edit_goal, name='edit_goal'),
    path('goals/delete/<int:pk>/', views.delete_goal, name='delete_goal'),
    path('goals/toggle/<int:pk>/', views.toggle_goal_status, name='toggle_goal_status'),

    # Rotas da API RESTful com ViewSets
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
