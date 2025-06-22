from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from goals.models import SavingsGoal
from decimal import Decimal

User = get_user_model()


class SavingsGoalsTestCase(TestCase):
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
        
        self.goal_data = {
            'title': 'Emergency Fund',
            'target_amount': '5000.00',
            'current_amount': '1000.00'
        }

    def test_create_savings_goal(self):
        """Test creating a new savings goal"""
        url = reverse('goals-list-create')
        response = self.client.post(url, self.goal_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SavingsGoal.objects.count(), 1)
        
        goal = SavingsGoal.objects.first()
        self.assertEqual(goal.user, self.user)
        self.assertEqual(goal.title, 'Emergency Fund')
        self.assertEqual(goal.target_amount, Decimal('5000.00'))

    def test_goal_progress_calculation(self):
        """Test savings goal progress calculation"""
        goal = SavingsGoal.objects.create(
            user=self.user,
            title='Test Goal',
            target_amount=Decimal('1000.00'),
            current_amount=Decimal('250.00')
        )
        
        self.assertEqual(goal.progress_percentage, 25.0)
        self.assertEqual(goal.remaining_amount, Decimal('750.00'))

    def test_goal_completion(self):
        """Test goal auto-completion when target is reached"""
        goal = SavingsGoal.objects.create(
            user=self.user,
            title='Test Goal',
            target_amount=Decimal('1000.00'),
            current_amount=Decimal('500.00')
        )
        
        self.assertFalse(goal.is_completed)
        
        # Update to reach target
        goal.current_amount = Decimal('1000.00')
        goal.save()
        
        self.assertTrue(goal.is_completed)

    def test_add_to_goal(self):
        """Test adding amount to savings goal"""
        goal = SavingsGoal.objects.create(
            user=self.user,
            title='Test Goal',
            target_amount=Decimal('1000.00'),
            current_amount=Decimal('100.00')
        )
        
        url = reverse('goals-add-amount', kwargs={'goal_id': goal.id})
        response = self.client.post(url, {'amount': '50.00'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        goal.refresh_from_db()
        self.assertEqual(goal.current_amount, Decimal('150.00'))

    def test_goals_summary(self):
        """Test goals summary endpoint"""
        SavingsGoal.objects.create(
            user=self.user,
            title='Goal 1',
            target_amount=Decimal('1000.00'),
            current_amount=Decimal('1000.00')  # Completed
        )
        SavingsGoal.objects.create(
            user=self.user,
            title='Goal 2',
            target_amount=Decimal('2000.00'),
            current_amount=Decimal('500.00')  # Active
        )
        
        url = reverse('goals-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_goals'], 2)
        self.assertEqual(response.data['completed_goals'], 1)
        self.assertEqual(response.data['active_goals'], 1)