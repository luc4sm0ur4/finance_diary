from rest_framework import serializers
from .models import Transaction, Category, Goal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']


class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'amount',
            'description',
            'date',
            'transaction_type',
            'category',
            'category_id',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            'id',
            'title',
            'description',
            'target_amount',
            'current_amount',
            'target_date',
            'achieved',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
