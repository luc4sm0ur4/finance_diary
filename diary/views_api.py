from rest_framework import viewsets, permissions
from .models import Transaction, Category, Goal
from .serializers import TransactionSerializer, CategorySerializer, GoalSerializer

# Permissão personalizada: só permite acessar/editar dados do próprio usuário
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

# ========================
#        VIEWSETS
# ========================

# TRANSAÇÕES
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# CATEGORIAS
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by('name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# METAS FINANCEIRAS
class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).order_by('-target_date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
