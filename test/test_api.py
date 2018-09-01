import pytest

import requests
import json

BASE_URL = "https://reqres.in"
SINGLE_USER_ID = 2
USER_NOT_FOUND_ID = 23
SINGLE_RESOURCE_ID = 2
RESOURCE_NOT_FOUND_ID = 23
USERS_LISTS_PARAMS = {'page': 2}
DELAY_RESPONSE = {'delay': 3}
CREATE_USER_PARAMS = {
    "name": "morpheus",
    "job": "leader"
}
SUCCESSFUL_REGISTER = {
    "email": "sydney@fife",
    "password": "pistol"
}
UNSUCCESSFUL_REGISTER = {
    "email": "sydney@fife"
}
SUCCESSFUL_LOGIN = {
    "email": "peter@klaven",
    "password": "cityslicka"
}
UNSUCCESSFUL_LOGIN = {
    "email": "peter@klaven"
}


def test_get_users_list():
    response = requests.get('{}/api/users'.format(BASE_URL), params=USERS_LISTS_PARAMS)
    assert response.status_code == 200
    assert json.loads(response.text)["total_pages"] == 4


def test_get_single_user():
    response = requests.get('{}/api/users/{}'.format(BASE_URL, SINGLE_USER_ID))
    assert response.status_code == 200
    assert json.loads(response.text)["data"]["first_name"] == "Janet"
    assert json.loads(response.text)["data"]["last_name"] == "Weaver"


def test_get_not_found_user():
    response = requests.get('{}/api/users/{}'.format(BASE_URL, USER_NOT_FOUND_ID))
    assert response.status_code == 404


def test_get_resource_list():
    response = requests.get('{}/api/unknown'.format(BASE_URL))
    assert response.status_code == 200
    assert json.loads(response.text)["total_pages"] == 4


def test_get_single_resource():
    response = requests.get('{}/api/unknown/{}'.format(BASE_URL, SINGLE_RESOURCE_ID))
    assert response.status_code == 200
    assert json.loads(response.text)["data"]["name"] == "fuchsia rose"
    assert json.loads(response.text)["data"]["year"] == 2001


def test_get_not_found_resource():
    response = requests.get('{}/api/unknown/{}'.format(BASE_URL, USER_NOT_FOUND_ID))
    assert response.status_code == 404


def test_delete_user():
    response = requests.delete('{}/api/user/{}'.format(BASE_URL, SINGLE_USER_ID))
    assert response.status_code == 204


def test_create_user():
    response = requests.post('{}/api/users'.format(BASE_URL), params=CREATE_USER_PARAMS)
    assert response.status_code == 201


def test_register_successful():
    with requests.Session() as s:
        response = s.post('{}/api/register'.format(BASE_URL), data=SUCCESSFUL_REGISTER)
        assert response.status_code == 201


def test_register_unsuccessful():
    with requests.Session() as s:
        response = s.post('{}/api/login'.format(BASE_URL), data=UNSUCCESSFUL_REGISTER)
        assert response.status_code == 400
        assert json.loads(response.text)["error"] == "Missing password"


def test_login_successful():
    with requests.Session() as s:
        response = s.post('{}/api/login'.format(BASE_URL), data=SUCCESSFUL_LOGIN)
        assert response.status_code == 200


def test_login_unsuccessful():
    with requests.Session() as s:
        response = s.post('{}/api/login'.format(BASE_URL), data=UNSUCCESSFUL_LOGIN)
        assert response.status_code == 400
        assert json.loads(response.text)["error"] == "Missing password"


def test_delay_response():
    response = requests.get('{}/api/users'.format(BASE_URL), params=DELAY_RESPONSE)
    assert response.status_code == 200
    assert json.loads(response.text)["total_pages"] == 4