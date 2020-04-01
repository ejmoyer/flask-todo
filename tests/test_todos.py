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

def test_edit_task(client):
    exist_response = client.get('/') # Check if Edit link exists in Index
    assert b'Edit</a>' in exist_response.data

    page_response = client.get('/1/edittask') # Check if the Edit Page exists
    assert page_response

    change_response = client.post('/1/edittask', data={'newdesc': 'test change'}) # Test editting a todo
    assert change_response
    assert b'test change' in client.get('/').data
