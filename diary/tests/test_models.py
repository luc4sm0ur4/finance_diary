# diary/tests/test_models.py

from django.test import TestCase
from django.contrib.auth.models import User
from diary.models import Category, Transaction, Goal
from datetime import date

class CategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lucas', password='123456')
        self.category = Category.objects.create(user=self.user, name='Educação', icon='school')

    def test_category_str(self):
        self.assertEqual(str(self.category), "Educação (lucas)")

    def test_unique_category_per_user(self):
        with self.assertRaises(Exception):
            Category.objects.create(user=self.user, name='Educação', icon='school')


class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lucas', password='123456')
        self.category = Category.objects.create(user=self.user, name='Transporte', icon='local_taxi')
        self.transaction = Transaction.objects.create(
            user=self.user,
            amount=150.50,
            description='Uber',
            date='2025-06-20',
            category=self.category,
            transaction_type='expense'
        )

    def test_transaction_str(self):
        self.assertIn('Uber', str(self.transaction))

    def test_transaction_is_income(self):
        self.transaction.transaction_type = 'income'
        self.assertTrue(self.transaction.is_income)

    def test_transaction_is_expense(self):
        self.transaction.transaction_type = 'expense'
        self.assertTrue(self.transaction.is_expense)


class GoalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lucas', password='123456')
        self.goal = Goal.objects.create(
            user=self.user,
            title='Comprar notebook',
            description='Meta para comprar notebook novo',
            target_amount=4000.00,
            current_amount=1000.00,
            target_date='2025-12-31'
        )

    def test_goal_str(self):
        self.assertEqual(str(self.goal), "Comprar notebook (lucas)")

    def test_goal_default_achieved(self):
        self.assertFalse(self.goal.achieved)
