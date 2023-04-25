import requests

responseUsers = requests.get(url = 'http://localhost:8080/api/user').json()
newly_created_user = None
updated_user = None

def test_create_user():
    url = 'http://localhost:8080/api/user'
    params = {
        "email": "xzy@987.com",
        "password": "12345",
        "role": 1,
        "username": "TestUser"
    }
    r = requests.post(url = url, json = params)
    # Sets up Message data for further test
    global newly_created_user
    newly_created_user = r.json()
    assert r.status_code == 201 and newly_created_user["username"] == params["username"]

def test_get_user_by_user_id():
    global newly_created_user
    url = 'http://localhost:8080/api/user/' + str(newly_created_user["user_id"])
    r = requests.get(url = url)
    data = r.json()
    assert r.status_code == 200 and data == newly_created_user

def test_update_user():
    global newly_created_user
    url = 'http://localhost:8080/api/user/' + str(newly_created_user["user_id"])
    params = {
        "username": "Update Username",
    }
    r = requests.put(url = url, json = params)
    global updated_user
    updated_user = r.json()
    responseUsers.append(updated_user)
    assert r.status_code == 200 and updated_user["username"] == params["username"]

def test_delete_message():
    global newly_created_user
    url = 'http://localhost:8080/api/user/' + str(newly_created_user["user_id"])
    r = requests.delete(url = url)
    assert r.status_code == 200
