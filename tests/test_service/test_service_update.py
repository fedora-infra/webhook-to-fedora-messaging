import pytest


def test_service_update(client, create_service):
    data = {'service_uuid': create_service.uuid, 'username': 'mehmet', 'name': 'new name'}
    response = client.put("/service/", json=data)
    assert response.status_code == 200
    
    
def test_service_update_404(client):
    data = {'service_uuid': "not-existent-uuid", 'username': 'mehmet', 'name': 'new name'}
    response = client.put("/service/", json=data)
    assert response.status_code == 404
    
    
def test_service_update_400(client):
    data = {'username': 'mehmet', 'name': 'new name'}
    response = client.put("/service/", json=data)
    assert response.status_code == 400
    
    
def test_service_update_415(client):
    response = client.put("/service/", json=None)
    assert response.status_code == 415
