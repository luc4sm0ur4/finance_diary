# diary/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from diary.models import Transaction, Category, Goal
from datetime import date

class ViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='lucas', password='123456')
        self.client.login(username='lucas', password='123456')
        self.category = Category.objects.create(user=self.user, name='Saúde', icon='local_hospital')

    def test_dashboard_view(self):
        response = self.client.get(reverse('diary:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Finance Diary')

    def test_add_transaction_post(self):
        data = {
            'amount': 200.00,
            'description': 'Consulta médica',
            'date': '2025-06-24',
            'transaction_type': 'expense',
            'category': self.category.id
        }
        response = self.client.post(reverse('diary:add_transaction'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_goal_list_view(self):
        response = self.client.get(reverse('diary:goal_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Metas Financeiras')

    def test_add_goal_post(self):
        data = {
            'title': 'Viajar',
            'target_amount': 5000.00,
            'current_amount': 1500.00,
            'target_date': '2025-11-01'
        }
        response = self.client.post(reverse('diary:add_goal'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Goal.objects.count(), 1)

    def test_toggle_goal_status(self):
        goal = Goal.objects.create(
            user=self.user,
            title='Estudar inglês',
            target_amount=2000.00,
            current_amount=200.00,
            target_date='2025-12-01',
            achieved=False
        )
        url = reverse('diary:toggle_goal_status', args=[goal.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        goal.refresh_from_db()
        self.assertTrue(goal.achieved)
