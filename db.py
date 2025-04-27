import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Bhaumik@123',
        database='blood_donation_db'
    )
    return connection

