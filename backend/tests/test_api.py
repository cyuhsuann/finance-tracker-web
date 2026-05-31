import pytest


# Authentication tests
def test_accounts_without_token_returns_401(client):
    response = client.get("/api/v1/accounts/")
    assert response.status_code == 401


def test_accounts_with_token_returns_200(auth_client):
    response = auth_client.get("/api/v1/accounts/")
    assert response.status_code == 200


# Data isolation tests
def test_user_cannot_see_another_user_accounts(auth_client, another_user, client):
    client.force_authenticate(user=another_user)
    client.post(
        "/api/v1/accounts/",
        {
            "name": "Another User Account",
            "account_type": "checking",
            "balance": "1000.00",
            "currency": "TWD",
        },
        format="json",
    )
    response = auth_client.get("/api/v1/accounts/")
    assert response.data["count"] == 0


# Basic CRUD tests
def test_create_account(auth_client):
    response = auth_client.post(
        "/api/v1/accounts/",
        {
            "name": "中華郵政",
            "account_type": "checking",
            "balance": "1000.00",
            "currency": "TWD",
        },
        format="json",
    )
    assert response.status_code == 201


def test_create_and_get_transaction(auth_client):
    account = auth_client.post(
        "/api/v1/accounts/",
        {
            "name": "中華郵政",
            "account_type": "checking",
            "balance": "1000.00",
            "currency": "TWD",
        },
        format="json",
    )
    response = auth_client.post(
        "/api/v1/transactions/",
        {
            "account": account.data["id"],
            "amount": "100.00",
            "transaction_type": "expense",
            "transaction_date": "2026-05-30",
        },
        format="json",
    )

    assert response.status_code == 201

    response = auth_client.get("/api/v1/transactions/")
    assert response.data["count"] == 1
