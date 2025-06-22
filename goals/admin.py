from django.contrib import admin
from .models import SavingsGoal


@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'target_amount', 'current_amount', 'progress_percentage', 'is_completed', 'deadline', 'created_at')
    list_filter = ('is_completed', 'created_at', 'deadline')
    search_fields = ('title', 'user__username', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('is_completed', 'progress_percentage', 'remaining_amount', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Goal Details', {
            'fields': ('user', 'title', 'target_amount', 'current_amount', 'deadline')
        }),
        ('Progress', {
            'fields': ('is_completed', 'progress_percentage', 'remaining_amount'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )