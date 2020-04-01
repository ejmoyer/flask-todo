import pytest

def test_todo_list(client):
    # View the home page and check to see the header and a to-do item
    response = client.get('/')
    assert b'clean room' in response.data

    # Mock data should show three to-do items, one of which is complete
    assert response.data.count(b'<li class="">') == 2
    assert response.data.count(b'<li class="completed">') == 1


def test_delete(client):
    response = client.post('/deletetask', data={'task_to_delete': 'do homework'})

    assert  response.data.count(b'<li class="completed">') == 0

def test_mark_complete(client):
    response = client.post('/done', data={'done': 'do homework'})
    assert response