import pytest


def test_service_revoke(client, create_service):
    data = {'service_uuid': create_service.uuid, 'username': 'mehmet'}
    response = client.put("/service/revoke", json=data)
    assert response.status_code == 200
    

def test_service_revoke_404(client, create_service):
    data = {'service_uuid': create_service.uuid, 'username': 'not-existent-user'}
    response = client.put("/service/revoke", json=data)
    assert response.status_code == 404
    
    
def test_service_revoke_400(client):
    data = {'username': 'mehmet'}
    response = client.put("/service/revoke", json=data)
    assert response.status_code == 400
    
    
def test_service_revoke_415(client):
    response = client.put("/service/revoke", json=None)
    assert response.status_code == 415
