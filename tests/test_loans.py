import json
import pytest

from django.contrib.auth import get_user_model
from django.conf import settings
from django.apps import apps

from rest_framework.test import APIClient
from rest_framework.test import RequestsClient

@pytest.fixture
def get_url():
    return "http://localhost:8000/"


@pytest.fixture
def get_customer_body():
    return {
        "external_id_character": "external_03",
        "score": 6000.0,
        "preapproved_at": "2023-02-12T22:29:27.177914Z",
        "status": 1
    }


@pytest.fixture
def get_loan_body():
    return {
        "external_id_character": "external_01-01",
        "amount": 2000.0,
        "maximum_payment_date": "2025-08-24T14:15:22Z",
        "taken_at": "2025-04-15T14:15:22Z",
        "outstanding": 0.0,
        "contract_version_character": "string",
        "status": 1,
        "customer": "external_03"
    }

@pytest.fixture
def create_superuser():
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        return User.objects.create_superuser('demo', 'demo@example.com', 'demo')


@pytest.fixture
def get_client():
    return RequestsClient()


@pytest.fixture
def get_token(get_client, get_url):
    response = get_client.post(f"{get_url}customers-token-auth/", data={"username": "demo", "password": "demo"})
    return json.loads(response.content).get("token")


@pytest.fixture
def create_customer(create_superuser, get_client, get_token, get_url, get_customer_body):
    create_superuser
    client = get_client
    response = client.post(
        f"{get_url}api/v1/customer/", 
        data=get_customer_body, 
        headers={"Authorization": f"Token {get_token}"}
    )
    
    response_content = json.loads(response.content)
    return response_content


@pytest.fixture
def create_loan(create_superuser, get_client, get_token, get_url, get_loan_body):
    create_superuser
    client = get_client
    response = client.post(
        f"{get_url}api/v1/loan/", 
        data=get_loan_body, 
        headers={"Authorization": f"Token {get_token}"}
    )
    
    response_content = json.loads(response.content)
    return response_content


@pytest.mark.django_db
def test_list_loans(create_superuser, get_client, get_token, get_url):
    create_superuser
    client = get_client
    response = client.get(f"{get_url}api/v1/loan/", headers={"Authorization": f"Token {get_token}"})
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_loan(create_superuser, create_customer, get_client, get_token, get_url, get_loan_body):
    create_customer
    create_superuser
    client = get_client
    response = client.post(
        f"{get_url}api/v1/loan/", 
        data=get_loan_body,
        headers={"Authorization": f"Token {get_token}"}
    )
    
    response_content = json.loads(response.content)
    
    assert response.status_code == 201
    assert response_content.get("external_id_character") == "external_01-01"


@pytest.mark.django_db
def test_get_loans_by_customer(create_superuser, get_client, get_token, create_customer, get_url):
    create_superuser
    customer_external_id = create_customer.get("external_id_character")
    client = get_client
    response = client.get(f"{get_url}api/v1/loan/?customer={customer_external_id}", headers={"Authorization": f"Token {get_token}"})
    assert response.status_code == 200
