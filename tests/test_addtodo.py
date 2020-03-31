import pytest

def test_add_todo(client):
    response = client.post('/newtask', data={'newtask': 'get donuts'})

    assert response
