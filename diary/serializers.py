from rest_framework import serializers
from .models import Transaction, Category, Goal


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'user',
            'amount',
            'description',
            'date',
            'category',
            'transaction_type',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'user',
            'name',
            'icon',
        ]
        read_only_fields = ['id', 'user']


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            'id',
            'user',
            'title',
            'description',
            'target_amount',
            'current_amount',
            'target_date',
            'achieved',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
