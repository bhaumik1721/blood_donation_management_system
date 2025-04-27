# utils.py

import requests

BASE_URL = "http://127.0.0.1:5000"  # Your Flask backend URL

# User registration
def register_user(username, password):
    url = f"{BASE_URL}/register"
    payload = {"username": username, "password": password}
    return requests.post(url, json=payload)

# User login
def login_user(username, password):
    url = f"{BASE_URL}/login"
    payload = {"username": username, "password": password}
    return requests.post(url, json=payload)

# Add donor details (optional, if needed later)
def add_donor_details(username, blood_group, age, contact):
    url = f"{BASE_URL}/add_donor"
    payload = {"username": username, "blood_group": blood_group, "age": age, "contact": contact}
    return requests.post(url, json=payload)

# Get list of all camps
def get_camps():
    url = f"{BASE_URL}/get_camps"
    return requests.get(url)

# Sign up for a camp
def signup_camp(username, camp_id):
    url = f"{BASE_URL}/signup_camp"
    payload = {"username": username, "camp_id": camp_id}
    return requests.post(url, json=payload)

# Admin: Add new camp
def add_camp(camp_name, location, date, timing):
    url = f"{BASE_URL}/add_camp"
    payload = {
        "camp_name": camp_name,
        "location": location,
        "date": date,
        "timing": timing
    }
    return requests.post(url, json=payload)

# Admin: Edit camp details
def edit_camp(camp_id, camp_name, location, date, timing):
    url = f"{BASE_URL}/edit_camp/{camp_id}"
    payload = {
        "camp_name": camp_name,
        "location": location,
        "date": date,
        "timing": timing
    }
    return requests.put(url, json=payload)

# Admin: Delete camp
def delete_camp(camp_id):
    url = f"{BASE_URL}/delete_camp/{camp_id}"
    return requests.delete(url)
