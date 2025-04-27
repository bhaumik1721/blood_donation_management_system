# utils.py

import requests
import streamlit as st

API_BASE = "http://localhost:5000"  # your Flask backend URL

def register_user(username, password):
    url = f"{API_BASE}/register"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    return response

def login_user(username, password):
    url = f"{API_BASE}/login"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    return response

def add_donor_details(username, blood_group, contact, last_donated):
    url = f"{API_BASE}/add_donor_details"
    payload = {
        "username": username,
        "blood_group": blood_group,
        "contact": contact,
        "last_donated": last_donated
    }
    response = requests.post(url, json=payload)
    return response

def view_camps():
    url = f"{API_BASE}/view_camps"
    response = requests.get(url)
    return response

def signup_camp(username, camp_id):
    url = f"{API_BASE}/signup_camp"
    payload = {
        "username": username,
        "camp_id": camp_id
    }
    response = requests.post(url, json=payload)
    return response

def add_camp(camp_name, location, date, timing):
    url = f"{API_BASE}/add_camp"
    payload = {
        "camp_name": camp_name,
        "location": location,
        "date": date,
        "timing": timing
    }
    response = requests.post(url, json=payload)
    return response

def edit_camp(camp_id, camp_name, location, date, timing):
    url = f"{API_BASE}/edit_camp"
    payload = {
        "camp_id": camp_id,
        "camp_name": camp_name,
        "location": location,
        "date": date,
        "timing": timing
    }
    response = requests.put(url, json=payload)
    return response

def delete_camp(camp_id):
    url = f"{API_BASE}/delete_camp"
    payload = {"camp_id": camp_id}
    response = requests.delete(url, json=payload)
    return response

def get_camps():
    url = f"{API_BASE}/get_camps"
    response = requests.get(url)
    return response
