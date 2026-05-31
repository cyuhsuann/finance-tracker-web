import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"


class Account(models.Model):
    ACCOUNT_TYPES = [
        ("checking", "Checking"),
        ("savings", "Savings"),
        ("credit", "Credit Card"),
        ("investment", "Investment"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    currency = models.CharField(max_length=3, default="TWD")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounts"

    def __str__(self):
        return f"{self.user.email} - {self.name}"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="categories", null=True, blank=True
    )
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#6366f1")
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
        ("transfer", "Transfer"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TYPES)
    description = models.CharField(max_length=255, blank=True)
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"
        ordering = ["-transaction_date", "-created_at"]

    def __str__(self):
        return f"{self.transaction_type}: {self.amount}"


class Investment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="investments"
    )
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=15, decimal_places=6)
    avg_cost = models.DecimalField(max_digits=12, decimal_places=4)
    current_price = models.DecimalField(
        max_digits=12, decimal_places=4, default=Decimal("0")
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "investments"
        unique_together = ["account", "symbol"]

    @property
    def market_value(self):
        return self.quantity * self.current_price

    @property
    def gain_loss(self):
        return (self.current_price - self.avg_cost) * self.quantity
