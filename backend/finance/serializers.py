from rest_framework import serializers
from .models import Account, Category, Transaction, Investment


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "name", "account_type", "balance", "currency", "created_at"]
        read_only_fields = ["id", "balance", "created_at"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "color", "is_default"]
        read_only_fields = ["id", "is_default"]


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "category",
            "category_name",
            "amount",
            "transaction_type",
            "description",
            "transaction_date",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class InvestmentSerializer(serializers.ModelSerializer):
    market_value = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    gain_loss = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = Investment
        fields = [
            "id",
            "account",
            "symbol",
            "name",
            "quantity",
            "avg_cost",
            "current_price",
            "market_value",
            "gain_loss",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]
