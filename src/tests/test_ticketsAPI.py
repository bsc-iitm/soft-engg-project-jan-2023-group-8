import requests

responseTickets = requests.get(url = 'http://localhost:8080/api/user/4/ticket').json()
newly_created_ticket = None
updated_ticket = None

def test_create_ticket():
    url = 'http://localhost:8080/api/user/4/ticket'
    params = {
        "user_id": 4,
        "subject": "Newly Created",
        "category": 1,
        "is_resolved": "N", 
        "likes": 0,
    }
    r = requests.post(url = url, json = params)
    global newly_created_ticket
    newly_created_ticket = r.json()
    assert r.status_code == 201 and newly_created_ticket["subject"] == params["subject"]

def test_get_ticket_by_ticket_id():
    global newly_created_ticket
    url = 'http://localhost:8080/api/user/4/ticket/' + str(newly_created_ticket["ticket_id"])
    r = requests.get(url = url)
    data = r.json()
    assert r.status_code == 200 and data == newly_created_ticket

def test_update_ticket():
    global newly_created_ticket
    url = 'http://localhost:8080/api/user/4/ticket/' + str(newly_created_ticket["ticket_id"])
    params = {
        "subject": "Newly Updated",
        "category": 1,
    }
    r = requests.put(url = url, json = params)
    global updated_ticket
    updated_ticket = r.json()
    responseTickets.append(updated_ticket)
    assert r.status_code == 200 and updated_ticket["subject"] == params["subject"]


def test_get_ticket():
    url = 'http://localhost:8080/api/user/4/ticket'
    r = requests.get(url = url)
    data = r.json()
    assert r.status_code == 200 and data == responseTickets

def test_delete_message():
    global newly_created_ticket
    url = 'http://localhost:8080/api/user/4/ticket/' + str(newly_created_ticket["ticket_id"])
    r = requests.delete(url = url)
    assert r.status_code == 200
