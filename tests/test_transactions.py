from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from transactions.models import Transaction
from decimal import Decimal

User = get_user_model()


class TransactionsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!',
            first_name='Test',
            last_name='User'
        )
        self.client.force_authenticate(user=self.user)
        
        self.transaction_data = {
            'amount': '100.50',
            'type': 'expense',
            'category': 'food',
            'description': 'Grocery shopping'
        }

    def test_create_transaction(self):
        """Test creating a new transaction"""
        url = reverse('transaction-list-create')
        response = self.client.post(url, self.transaction_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.amount, Decimal('100.50'))

    def test_list_transactions(self):
        """Test listing user's transactions"""
        # Create some transactions
        Transaction.objects.create(
            user=self.user,
            amount=Decimal('50.00'),
            type='income',
            category='other'
        )
        Transaction.objects.create(
            user=self.user,
            amount=Decimal('25.00'),
            type='expense',
            category='food'
        )
        
        url = reverse('transaction-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_transaction_filtering(self):
        """Test filtering transactions by type and category"""
        Transaction.objects.create(
            user=self.user,
            amount=Decimal('50.00'),
            type='income',
            category='other'
        )
        Transaction.objects.create(
            user=self.user,
            amount=Decimal('25.00'),
            type='expense',
            category='food'
        )
        
        url = reverse('transaction-list-create')
        
        # Filter by type
        response = self.client.get(url, {'type': 'income'})
        self.assertEqual(len(response.data['results']), 1)
        
        # Filter by category
        response = self.client.get(url, {'category': 'food'})
        self.assertEqual(len(response.data['results']), 1)

    def test_monthly_summary(self):
        """Test monthly summary endpoint"""
        # Create transactions for current month
        Transaction.objects.create(
            user=self.user,
            amount=Decimal('1000.00'),
            type='income',
            category='other'
        )
        Transaction.objects.create(
            user=self.user,
            amount=Decimal('300.00'),
            type='expense',
            category='food'
        )
        
        url = reverse('monthly-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_income'], Decimal('1000.00'))
        self.assertEqual(response.data['total_expenses'], Decimal('300.00'))
        self.assertEqual(response.data['net_savings'], Decimal('700.00'))