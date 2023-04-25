import requests
import json 

responseTickets = requests.get(url = 'http://localhost:8080/api/ticket/1/message').json()
print(responseTickets)
newly_created_message = None
updated_message = None

def test_create_message_in_ticket():
    url = 'http://localhost:8080/api/ticket/1/message'
    params = {
        "user_id": 2,
        "content": "Newly Created",
        "ticket_id": 1
    }
    r = requests.post(url = url, json = params)
    # Sets up Message data for further test
    global newly_created_message
    newly_created_message = r.json()
    assert r.status_code == 201 and newly_created_message["content"] == params["content"]

def test_get_message_by_message_id():
    global newly_created_message
    url = 'http://localhost:8080/api/ticket/1/message/' + str(newly_created_message["message_id"])
    r = requests.get(url = url)
    data = r.json()
    assert r.status_code == 200 and data == newly_created_message

def test_update_message():
    global newly_created_message
    url = 'http://localhost:8080/api/ticket/1/message/' + str(newly_created_message["message_id"])
    params = {
        "user_id": 2,
        "content": "Newly Updated",
        "ticket_id": 1
    }
    r = requests.put(url = url, json = params)
    global updated_message
    updated_message = r.json()
    responseTickets.append(updated_message)
    assert r.status_code == 200 and updated_message["content"] == params["content"]


def test_get_messages_in_ticket():
    url = 'http://localhost:8080/api/ticket/1/message'
    r = requests.get(url = url)
    data = r.json()
    assert r.status_code == 200 and data == responseTickets

def test_delete_message():
    global newly_created_message
    url = 'http://localhost:8080/api/ticket/1/message/' + str(newly_created_message["message_id"])
    r = requests.delete(url = url)
    assert r.status_code == 200
