import pytest


def test_service_refresh(client, create_service):
    data = {'service_uuid': create_service.uuid}
    response = client.post("/service/token", json=data)
    assert response.status_code == 200
    
    
def test_service_refresh_404(client):
    data = {'service_uuid': "not-existent-uuid"}
    response = client.post("/service/token", json=data)
    assert response.status_code == 404


def test_service_refresh_400(client):
    data = {"username": "mehmet", "type": "Github", "desc": "Github Demo"}
    response = client.post("/service/token", json=data)
    assert response.status_code == 400
    
    
def test_service_refresh_415(client):
    response = client.post("/service/token", json=None)
    assert response.status_code == 415