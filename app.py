# app.py

import streamlit as st
from utils import (
    register_user, login_user, add_donor_details,
    get_camps, signup_camp, add_camp, edit_camp,
    delete_camp, get_camps
)
from datetime import datetime

# Streamlit Page Config
st.set_page_config(page_title="Blood Donation Management System", page_icon="🩸", layout="centered")

# Session State to store login info
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# Navbar / Sidebar
st.sidebar.title("🩸 Blood Donation System")
page = st.sidebar.selectbox("Navigate", ["Home", "Register", "Login", "View Camps", "Manage Camps", "Logout"])


# Functions
def home_page():
    st.title("🩸 Welcome to Blood Donation Management System")
    st.write("Saving Lives, One Donation at a Time!")
    st.image("https://img.freepik.com/premium-vector/flat-blood-donation-background_23-2149018423.jpg",
             use_column_width=True)


def register_page():
    st.title("📝 Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username and password:
            response = register_user(username, password)
            st.success(response.json()['message']) if response.status_code == 201 else st.error(
                response.json()['message'])
        else:
            st.warning("Please fill all fields.")


def login_page():
    st.title("🔑 Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if username and password:
            response = login_user(username, password)
            if response.status_code == 200:
                st.success(response.json()['message'])
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = response.json()['role']
                st.experimental_rerun()
            else:
                st.error(response.json()['message'])
        else:
            st.warning("Please fill all fields.")


def view_camps_page():
    st.title("🏥 Available Camps")
    response = get_camps()

    if response.status_code == 200:
        camps = response.json()['camps']
        for camp in camps:
            st.subheader(f"{camp['camp_name']} ({camp['location']})")
            st.write(f"📅 Date: {camp['date']} | 🕒 Time: {camp['timing']}")
            if st.session_state.logged_in:
                if st.button(f"Sign Up for {camp['camp_name']}", key=camp['camp_id']):
                    signup_response = signup_camp(st.session_state.username, camp['camp_id'])
                    if signup_response.status_code == 200:
                        st.success("Signed up successfully!")
                    else:
                        st.error(signup_response.json()['error'])
            st.markdown("---")
    else:
        st.error("Failed to fetch camps!")


def manage_camps_page():
    if not st.session_state.logged_in or st.session_state.role != 'admin':
        st.warning("You must be an admin to access this page.")
        return

    st.title("🛠 Manage Camps (Admin)")

    tab1, tab2, tab3 = st.tabs(["➕ Add Camp", "✏️ Edit Camp", "🗑️ Delete Camp"])

    with tab1:
        st.subheader("Add a New Camp")
        camp_name = st.text_input("Camp Name")
        location = st.text_input("Location")
        date = st.date_input("Date")
        timing = st.time_input("Timing")

        if st.button("Add Camp"):
            response = add_camp(camp_name, location, date.strftime('%Y-%m-%d'), timing.strftime('%H:%M:%S'))
            if response.status_code == 201:
                st.success("Camp added successfully!")
            else:
                st.error(response.json().get('error', 'Error adding camp'))

    with tab2:
        st.subheader("Edit Existing Camp")
        camps = get_camps()
        if camps.status_code == 200:
            camp_list = camps.json()['camps']
            camp_options = {f"{c['camp_name']} ({c['location']})": c['camp_id'] for c in camp_list}
            selected_camp = st.selectbox("Select a Camp to Edit", list(camp_options.keys()))
            selected_id = camp_options[selected_camp]

            new_name = st.text_input("New Camp Name")
            new_location = st.text_input("New Location")
            new_date = st.date_input("New Date")
            new_timing = st.time_input("New Timing")

            if st.button("Update Camp"):
                response = edit_camp(selected_id, new_name, new_location, new_date.strftime('%Y-%m-%d'),
                                     new_timing.strftime('%H:%M:%S'))
                if response.status_code == 200:
                    st.success("Camp updated successfully!")
                else:
                    st.error(response.json().get('error', 'Error updating camp'))

    with tab3:
        st.subheader("Delete Camp")
        camps = get_camps()
        if camps.status_code == 200:
            camp_list = camps.json()['camps']
            camp_options = {f"{c['camp_name']} ({c['location']})": c['camp_id'] for c in camp_list}
            selected_camp = st.selectbox("Select a Camp to Delete", list(camp_options.keys()), key="delete_camp")
            selected_id = camp_options[selected_camp]

            if st.button("Delete Camp"):
                response = delete_camp(selected_id)
                if response.status_code == 200:
                    st.success("Camp deleted successfully!")
                else:
                    st.error(response.json().get('error', 'Error deleting camp'))


def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.success("Logged out successfully!")


# ---------------------------------
# Main Logic
if page == "Home":
    home_page()
elif page == "Register":
    register_page()
elif page == "Login":
    login_page()
elif page == "View Camps":
    view_camps_page()
elif page == "Manage Camps":
    manage_camps_page()
elif page == "Logout":
    logout()
