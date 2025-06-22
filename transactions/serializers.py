from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    formatted_amount = serializers.ReadOnlyField()
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'amount', 'type', 'category', 'description', 
            'date', 'formatted_amount', 'user_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TransactionSummarySerializer(serializers.Serializer):
    month = serializers.CharField()
    year = serializers.IntegerField()
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)
    net_savings = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_count = serializers.IntegerField()
    
    # Category breakdown
    category_breakdown = serializers.DictField()