from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Avg
from .models import SavingsGoal
from .serializers import SavingsGoalSerializer, SavingsGoalUpdateSerializer


class SavingsGoalListCreateView(generics.ListCreateAPIView):
    """List all savings goals for the authenticated user or create a new goal"""
    serializer_class = SavingsGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return SavingsGoal.objects.none()  # For schema generation
            
        queryset = SavingsGoal.objects.filter(user=self.request.user)
        
        # Filter by completion status
        is_completed = self.request.query_params.get('completed')
        if is_completed is not None:
            if is_completed.lower() in ['true', '1']:
                queryset = queryset.filter(is_completed=True)
            elif is_completed.lower() in ['false', '0']:
                queryset = queryset.filter(is_completed=False)
        
        return queryset


class SavingsGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific savings goal"""
    serializer_class = SavingsGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return SavingsGoal.objects.none()  # For schema generation
        return SavingsGoal.objects.filter(user=self.request.user)


class SavingsGoalUpdateAmountView(generics.UpdateAPIView):
    """Update only the current amount of a savings goal"""
    serializer_class = SavingsGoalUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return SavingsGoal.objects.none()  # For schema generation
        return SavingsGoal.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def goals_summary(request):
    """Get summary statistics for user's savings goals"""
    user = request.user
    goals = SavingsGoal.objects.filter(user=user)
    
    total_goals = goals.count()
    completed_goals = goals.filter(is_completed=True).count()
    active_goals = goals.filter(is_completed=False).count()
    
    total_target_amount = goals.aggregate(
        total=Sum('target_amount')
    )['total'] or 0
    
    total_saved_amount = goals.aggregate(
        total=Sum('current_amount')
    )['total'] or 0
    
    average_progress = goals.aggregate(
        avg_progress=Avg('current_amount')
    )['avg_progress'] or 0
    
    # Calculate overall progress percentage
    overall_progress = 0
    if total_target_amount > 0:
        overall_progress = (total_saved_amount / total_target_amount) * 100
    
    return Response({
        'total_goals': total_goals,
        'completed_goals': completed_goals,
        'active_goals': active_goals,
        'total_target_amount': total_target_amount,
        'total_saved_amount': total_saved_amount,
        'remaining_amount': max(total_target_amount - total_saved_amount, 0),
        'overall_progress_percentage': round(overall_progress, 2),
        'completion_rate': round((completed_goals / total_goals) * 100, 2) if total_goals > 0 else 0
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_goal(request, goal_id):
    """Add amount to a specific savings goal"""
    try:
        goal = SavingsGoal.objects.get(id=goal_id, user=request.user)
    except SavingsGoal.DoesNotExist:
        return Response(
            {'error': 'Savings goal not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    amount = request.data.get('amount')
    if not amount:
        return Response(
            {'error': 'Amount is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        amount = float(amount)
        if amount <= 0:
            return Response(
                {'error': 'Amount must be greater than zero'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    except (ValueError, TypeError):
        return Response(
            {'error': 'Invalid amount format'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Add amount to current amount
    goal.current_amount += amount
    goal.save()
    
    serializer = SavingsGoalSerializer(goal)
    return Response({
        'message': f'Successfully added ${amount:.2f} to {goal.title}',
        'goal': serializer.data
    })