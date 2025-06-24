# diary/tests/test_api.py

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from diary.models import Transaction, Category, Goal
from datetime import date

class FinanceDiaryAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lucas', password='123456')
        self.client.login(username='lucas', password='123456')
        self.category = Category.objects.create(user=self.user, name='Alimentação', icon='restaurant')
        self.transaction = Transaction.objects.create(
            user=self.user,
            amount=100.00,
            description='Mercado',
            date='2025-06-25',
            transaction_type='expense',
            category=self.category
        )
        self.goal = Goal.objects.create(
            user=self.user,
            title='Economizar para férias',
            target_amount=3000.00,
            current_amount=1000.00,
            target_date='2025-12-01'
        )

    # === TRANSAÇÕES ===
    def test_list_transactions(self):
        url = reverse('diary:api-transaction-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_transaction(self):
        url = reverse('diary:api-transaction-list')
        data = {
            "amount": 250.00,
            "description": "Compra online",
            "date": "2025-06-26",
            "transaction_type": "expense",
            "category": self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)

    def test_update_transaction(self):
        url = reverse('diary:api-transaction-detail', args=[self.transaction.id])
        response = self.client.patch(url, {"description": "Supermercado"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.description, "Supermercado")

    def test_delete_transaction(self):
        url = reverse('diary:api-transaction-detail', args=[self.transaction.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)

    # === CATEGORIAS ===
    def test_list_categories(self):
        url = reverse('diary:api-category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        url = reverse('diary:api-category-list')
        data = {"name": "Transporte", "icon": "local_taxi"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    # === METAS ===
    def test_list_goals(self):
        url = reverse('diary:api-goal-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_goal(self):
        url = reverse('diary:api-goal-list')
        data = {
            "title": "Poupança emergencial",
            "target_amount": 2000.00,
            "current_amount": 500.00,
            "target_date": "2025-11-30"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Goal.objects.count(), 2)

    def test_update_goal(self):
        url = reverse('diary:api-goal-detail', args=[self.goal.id])
        response = self.client.patch(url, {"current_amount": 1500.00}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.current_amount, 1500.00)

    def test_delete_goal(self):
        url = reverse('diary:api-goal-detail', args=[self.goal.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Goal.objects.count(), 0)
