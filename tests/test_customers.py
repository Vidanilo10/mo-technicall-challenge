import json
import pytest

from django.contrib.auth import get_user_model
from django.conf import settings
from django.apps import apps

from rest_framework.test import APIClient
from rest_framework.test import RequestsClient


@pytest.fixture
def create_superuser():
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        return User.objects.create_superuser('demo', 'demo@example.com', 'demo')


@pytest.fixture
def get_client():
    return RequestsClient()


@pytest.fixture
def get_token(get_client):
    response = get_client.post("http://localhost:8000/customers-token-auth/", data={"username": "demo", "password": "demo"})
    return json.loads(response.content).get("token")


@pytest.fixture
def create_customer(create_superuser, get_client, get_token):
    client = get_client
    response = client.post(
        "http://localhost:8000/api/v1/customer/", 
        data={
            "external_id_character": "external_03",
            "score": 6000.0,
            "preapproved_at": "2023-02-12T22:29:27.177914Z",
            "status": 1
        }, 
        headers={"Authorization": f"Token {get_token}"}
    )
    
    response_content = json.loads(response.content)
    return response_content


@pytest.mark.django_db
def test_list_customers(create_superuser, get_client, get_token):
    client = get_client
    response = client.get("http://localhost:8000/api/v1/customer/", headers={"Authorization": f"Token {get_token}"})
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_customer(create_superuser, get_client, get_token):
    client = get_client
    response = client.post(
        "http://localhost:8000/api/v1/customer/", 
        data={
            "external_id_character": "external_03",
            "score": 6000.0,
            "preapproved_at": "2023-02-12T22:29:27.177914Z",
            "status": 1
        }, 
        headers={"Authorization": f"Token {get_token}"}
    )
    
    response_content = json.loads(response.content)
    
    assert response.status_code == 201
    assert response_content.get("external_id_character") == "external_03"


@pytest.mark.django_db
def test_get_customer_balance(create_superuser, get_client, get_token, create_customer):
    customer_external_id = create_customer.get("external_id_character")
    client = get_client
    response = client.get(f"http://localhost:8000/api/v1/customer/{customer_external_id}/get_customer_balance/", headers={"Authorization": f"Token {get_token}"})
    assert response.status_code == 200