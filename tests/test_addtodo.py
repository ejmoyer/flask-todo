import pytest

def test_add_todo(client):

    response = client.post('/', data={'newtask': 'get donuts'})

    assert b'get donuts' in response.data
