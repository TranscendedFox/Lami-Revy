import requests

BASE_URL = "http://localhost:8000"


def register_user(username, first_name, last_name, email, phone, address_city, address_country, password):
    url = f"{BASE_URL}/user/"
    payload = {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "address_city": address_city,
        "address_country": address_country,
        "password": password
    }
    response = requests.post(url, json=payload)
    return response


def get_jwt_token(username, password):
    url = f"{BASE_URL}/auth/token"
    form_data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=form_data)
    return response.json().get("jwt_token")


def search_items(search_input):
    url = f"{BASE_URL}/items/search/{search_input}"
    response = requests.get(url)
    return response.json()


def get_all_items():
    url = f"{BASE_URL}/items"
    response = requests.get(url)
    return response.json()

