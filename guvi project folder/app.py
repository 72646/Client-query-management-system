
#import mysql.connector


# import mysql.connector

# # connect to MySQL (without database first)
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root"
# )

# cursor = conn.cursor()

# # Create database
# cursor.execute("CREATE DATABASE IF NOT EXISTS query_system")
# cursor.execute("USE query_system")

# # Create users table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     user_id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(100),
#     hashed_password VARCHAR(256),
#     role VARCHAR(20)
# )
# """)

# # Create queries table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS queries (
#     query_id INT AUTO_INCREMENT PRIMARY KEY,
#     mail_id VARCHAR(100),
#     mobile_number VARCHAR(15),
#     query_heading VARCHAR(200),
#     query_description TEXT,
#     status VARCHAR(20),
#     query_created_time DATETIME,
#     query_closed_time DATETIME
# )
# """)

# conn.commit()
# conn.close()

# print("Database and tables created successfully")


#------------ testing fro ontime user creation--------------
# from auth import register_user,login_user
# register_user("admin","1234","Support")
# print("Admin user created")
# user = login_user("ameen","12345")
# print("user")


import streamlit as st
import pandas as pd
from datetime import datetime
from auth import login_user, register_user
from db import get_connection

st.set_page_config(page_title="Client Query Management System")

# ---------------- SESSION DEFAULTS ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- SIDEBAR ----------------
st.sidebar.title("Client Query System")
menu = st.sidebar.radio("Menu", ["Login", "Register", "Logout"])

# ---------------- TITLE ----------------
st.title("Client Query Management System")

# ---------------- LOGOUT ----------------
if menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.clear()
    st.success("Logged out successfully")
    st.stop()

# ---------------- REGISTER PAGE ----------------
if menu == "Register" and not st.session_state.logged_in:
    st.subheader("Register New User")

    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Client", "Support"])

    if st.button("Register"):
        if new_username and new_password:
            register_user(new_username, new_password, role)
            st.success("User registered successfully. Please login.")
        else:
            st.error("Please fill all fields")

# ---------------- LOGIN PAGE ----------------
if menu == "Login" and not st.session_state.logged_in:
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")

# ---------------- AFTER LOGIN ----------------
if st.session_state.logged_in:
    st.success(f"Welcome {st.session_state.username}")

    # ================= CLIENT PAGE =================
    if st.session_state.role == "Client":
        st.subheader("Submit a Query")

        mail = st.text_input("Email ID")
        mobile = st.text_input("Mobile Number")
        heading = st.text_input("Query Heading")
        description = st.text_area("Query Description")

        if st.button("Submit Query"):
            if mail and mobile and heading and description:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO queries
                    (mail_id, mobile_number, query_heading, query_description,
                    status, query_created_time)
                    VALUES (%s, %s, %s, %s, 'Open', %s)
                """, (mail, mobile, heading, description, datetime.now()))

                conn.commit()
                conn.close()

                st.success("Query submitted successfully")
            else:
                st.error("Please fill all fields")

    # ================= SUPPORT DASHBOARD =================
    elif st.session_state.role == "Support":
        st.subheader("Support Dashboard")

        conn = get_connection()

        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Open", "Closed"]
        )

        if status_filter == "All":
            df = pd.read_sql("SELECT * FROM queries", conn)
        else:
            df = pd.read_sql(
                "SELECT * FROM queries WHERE status=%s",
                conn,
                params=(status_filter,)
            )

        st.dataframe(df)

        st.divider()

        st.subheader("Close a Query")

        query_id = st.number_input("Enter Query ID", min_value=1, step=1)

        if st.button("Close Query"):
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE queries
                SET status='Closed',
                    query_closed_time=%s
                WHERE query_id=%s
            """, (datetime.now(), query_id))

            conn.commit()
            st.success(f"Query {query_id} closed successfully")
            st.rerun()


        conn.close()
