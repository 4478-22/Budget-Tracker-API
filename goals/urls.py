from django.urls import path
from . import views

urlpatterns = [
    path('goals/', views.SavingsGoalListCreateView.as_view(), name='goals-list-create'),
    path('goals/<int:pk>/', views.SavingsGoalDetailView.as_view(), name='goals-detail'),
    path('goals/<int:pk>/update-amount/', views.SavingsGoalUpdateAmountView.as_view(), name='goals-update-amount'),
    path('goals/<int:goal_id>/add/', views.add_to_goal, name='goals-add-amount'),
    path('goals/summary/', views.goals_summary, name='goals-summary'),
]