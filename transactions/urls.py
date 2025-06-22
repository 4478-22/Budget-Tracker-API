from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('summary/monthly/', views.monthly_summary, name='monthly-summary'),
    path('transactions/stats/', views.transaction_stats, name='transaction-stats'),
]