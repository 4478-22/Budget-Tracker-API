from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Q, Count
from django.utils import timezone
from datetime import datetime
import calendar
from .models import Transaction
from .serializers import TransactionSerializer, TransactionSummarySerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    """List all transactions for the authenticated user or create a new transaction"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Filter by type
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(type=transaction_type)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=end_date)
            except ValueError:
                pass
        
        return queryset


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific transaction"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return Transaction.objects.filter(user=self.request.user)
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Transaction.objects.none()  # return an empty queryset
        return Transaction.objects.filter(user=self.request.user)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_summary(request):
    """Get monthly summary of income, expenses, and savings"""
    user = request.user
    
    # Get month and year from query params, default to current month
    month = request.query_params.get('month', timezone.now().month)
    year = request.query_params.get('year', timezone.now().year)
    
    try:
        month = int(month)
        year = int(year)
    except (ValueError, TypeError):
        return Response(
            {'error': 'Invalid month or year parameter'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Filter transactions for the specified month and year
    transactions = Transaction.objects.filter(
        user=user,
        date__month=month,
        date__year=year
    )
    
    # Calculate totals
    income_total = transactions.filter(type='income').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    expense_total = transactions.filter(type='expense').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    net_savings = income_total - expense_total
    transaction_count = transactions.count()
    
    # Category breakdown for expenses
    category_breakdown = {}
    for category_code, category_name in Transaction.CATEGORIES:
        category_total = transactions.filter(
            type='expense', 
            category=category_code
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        if category_total > 0:
            category_breakdown[category_name] = float(category_total)
    
    # Prepare response data
    summary_data = {
        'month': calendar.month_name[month],
        'year': year,
        'total_income': income_total,
        'total_expenses': expense_total,
        'net_savings': net_savings,
        'transaction_count': transaction_count,
        'category_breakdown': category_breakdown
    }
    
    serializer = TransactionSummarySerializer(summary_data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_stats(request):
    """Get overall transaction statistics for the user"""
    user = request.user
    
    total_transactions = Transaction.objects.filter(user=user).count()
    total_income = Transaction.objects.filter(
        user=user, type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_expenses = Transaction.objects.filter(
        user=user, type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Most used category
    most_used_category = Transaction.objects.filter(
        user=user
    ).values('category').annotate(
        count=Count('category')
    ).order_by('-count').first()
    
    return Response({
        'total_transactions': total_transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_total': total_income - total_expenses,
        'most_used_category': most_used_category['category'] if most_used_category else None,
        'average_transaction_amount': (total_income + total_expenses) / total_transactions if total_transactions > 0 else 0
    })