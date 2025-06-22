from rest_framework import serializers
from .models import SavingsGoal


class SavingsGoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()
    remaining_amount = serializers.ReadOnlyField()
    formatted_target_amount = serializers.ReadOnlyField()
    formatted_current_amount = serializers.ReadOnlyField()
    formatted_remaining_amount = serializers.ReadOnlyField()
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = SavingsGoal
        fields = [
            'id', 'title', 'target_amount', 'current_amount', 'deadline',
            'is_completed', 'progress_percentage', 'remaining_amount',
            'formatted_target_amount', 'formatted_current_amount', 
            'formatted_remaining_amount', 'user_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'is_completed', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        if data.get('current_amount', 0) < 0:
            raise serializers.ValidationError("Current amount cannot be negative")
        
        if data.get('target_amount', 0) <= 0:
            raise serializers.ValidationError("Target amount must be greater than zero")
        
        return data


class SavingsGoalUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating current amount in savings goals"""
    
    class Meta:
        model = SavingsGoal
        fields = ['current_amount']

    def validate_current_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Current amount cannot be negative")
        return value