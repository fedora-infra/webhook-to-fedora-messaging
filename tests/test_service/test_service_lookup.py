import pytest


def test_service_lookup(client, create_service):
    data = {'service_uuid': create_service.uuid}
    response = client.get("/service/", json=data)
    assert response.status_code == 200
    
    
def test_service_404(client):
    data = {'service_uuid': "not-existent-uuid"}
    response = client.get("/service/", json=data)
    assert response.status_code == 404
    
    
def test_service_400(client):
    data = {'username': "username"}
    response = client.get("/service/", json=data)
    assert response.status_code == 400
    
    
def test_service_415(client):
    response = client.get("/service/", json=None)
    assert response.status_code == 415
