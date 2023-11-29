def test_login(client):
    json = {
        'name': 'admin',
        'password': "admin"
    }
    response = client.post('/auth/login', json=json)
    assert response.status_code == 200
    assert "token" in response.json
    assert "refresh" in response.json
    assert "expires_in" in response.json
