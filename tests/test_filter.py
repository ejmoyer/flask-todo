import pytest

def test_filter(client):
    assert client.get('/All')
    assert client.get('/Completed')
    assert client.get('/Uncompleted')
