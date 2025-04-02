import streamlit as st
import pandas as pd

from google.oauth2.service_account import Credentials
import pandas as pd
import gspread
import os
from gspread_dataframe import set_with_dataframe
from datetime import datetime
from datetime import datetime, timedelta
import time

import bcrypt
import uuid

# Sheet name for User Database
SHEET_NAME = "UserDatabase" 

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

SHEET_NAME = "UserDatabase"

# Authenticate Google Sheets
def authenticate_gspread():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_info(
        st.secrets["GOOGLE_APPLICATION_CREDENTIALS"], 
        scopes=scope
    )
    gc = gspread.authorize(credentials)
    return gc.open(SHEET_NAME).sheet1

# Get all users from Google Sheets
def get_users():
    sheet = authenticate_gspread()
    return sheet.get_all_records()

# Find user in Google Sheets
def find_user(email):
    users = get_users()
    for user in users:
        if user["Email"] == email:
            return user
    return None

# Add a new user
def add_user(email, name, role, password_hashed):
    sheet = authenticate_gspread()
    sheet.append_row([email, name, role, password_hashed])

# ---- Streamlit Interface ----

st.title("🔑 User Login")

# Add a login form
email = st.text_input("Email", key="email_input")
password = st.text_input("Password", type="password", key="password_input")

# Button to submit login credentials
if st.button("Login"):
    user = find_user(email)
    
    if user:
        stored_password = user["Password"]  # Assuming you have plaintext passwords here for now
        if password == stored_password:
            st.session_state.logged_in = True
            st.session_state.user_name = user["Name"]
            st.session_state.user_role = user["Role"]
            st.success(f"✅ Welcome, {user['Name']}!")
        else:
            st.error("❌ Invalid password.")
    else:
        st.error("❌ User not found.")

# Check if the user is logged in
if "logged_in" in st.session_state and st.session_state.logged_in:
    # Show the user different sections based on their role
    role = st.session_state.user_role
    if role == "SuperAdmin":
        page = st.radio("Choose an action", ["Super Admin Panel", "Add New User", "Other"])
        
        if page == "Super Admin Panel":
            st.subheader("🛠️ Super Admin Panel")
            st.write("You are in the Super Admin Panel.")
        
        elif page == "Add New User":
            st.subheader("🛠️ Add New User")
            new_email = st.text_input("User Email")
            new_name = st.text_input("Full Name")
            new_role = st.selectbox("Role", ["Admin", "Sales"])
            
            if st.button("Add User"):
                if new_email and new_name:
                    add_user(new_email, new_name, new_role, "temp_password")
                    st.success(f"✅ {new_name} ({new_role}) added successfully!")
                else:
                    st.error("❌ Please fill in all fields.")
        
        elif page == "Other":
            st.write("Other SuperAdmin actions here.")
            
    elif role == "Admin":
        page = st.radio("Choose an action", ["Admin Panel", "Other"])
        
        if page == "Admin Panel":
            st.subheader("🛠️ Admin Panel")
            # Admin-specific options
            st.write("Admin options will go here.")
        
        elif page == "Other":
            st.write("Other Admin actions here.")
    
    elif role == "Sales":
        page = st.radio("Choose an action", ["Sales Panel", "Other"])
        
        if page == "Sales Panel":
            st.subheader("💼 Sales Panel")
            # Sales-specific options
            st.write("Sales options will go here.")
        
        elif page == "Other":
            st.write("Other Sales actions here.")

else:
    st.write("Please log in to access the panels.")
    
# # @st.cache_data(ttl=300)
# def read_file(name,sheet):
#   scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#   credentials = Credentials.from_service_account_info(
#   st.secrets["GOOGLE_APPLICATION_CREDENTIALS"], 
#   scopes=scope)
#   gc = gspread.authorize(credentials)
#   worksheet = gc.open(name).worksheet(sheet)
#   rows = worksheet.get_all_values()
#   df = pd.DataFrame.from_records(rows)
#   df = pd.DataFrame(df.values[1:], columns=df.iloc[0])
#   return df


# Commission = read_file("Leasing Database","Sheet2")
# Commission['Number of beds'] = Commission['Number of beds'].astype(int)
# Commission.loc[Commission['Term Catorgy'] == 'Short','Owner Charge'] = 300 * Commission['Number of beds']
# Commission.loc[Commission['Term Catorgy'] == 'Long','Owner Charge'] = 600 * Commission['Number of beds']
# Commission['Signed Date'] = pd.to_datetime(Commission['Signed Date'],format='mixed')
# Commission_own = Commission.loc[Commission['Property Type'] == 'Own Property']

# start_date = datetime(2024, 9, 1)  # 2024年11月1日
# end_date = datetime(2025, 4, 30) 
# col1, col2 = st.columns(2)
# with col1:
#     start_selected = st.date_input(
#         "From:",
#         value=start_date,
#         min_value=start_date,
#         max_value=end_date
#     )
# with col2:
#     end_selected = st.date_input(
#         "To:",
#         value=end_date,
#         min_value=start_date,
#         max_value=end_date
#     )


# start_selected = pd.Timestamp(start_selected)
# end_selected = pd.Timestamp(end_selected)
# df_filtered = Commission_own[Commission_own["Signed Date"].between(start_selected,end_selected)]
                                                                  
# Bill_Charge = pd.DataFrame()
# Bill_Charge['Bill Property Code'] = df_filtered['Property Name']
# Bill_Charge['Bill Unit Name'] = ' '
# Bill_Charge['Vendor Payee Name'] = "Moo Housing Inc"
# Bill_Charge['Amount'] = df_filtered['Owner Charge']
# Bill_Charge['Bill Account'] = '6112'
# Bill_Charge['Description'] = df_filtered['Property']
# Bill_Charge['Bill Date'] = end_selected
# Bill_Charge['Due Date'] = end_selected

# st.dataframe(
#     Bill_Charge,
#     use_container_width=True,
# )

# csv_data = Bill_Charge.to_csv(index=False).encode('utf-8')
# st.download_button(
#     label="📥 Download Owner Charge CSV",
#     data=csv_data,
#     file_name="Owner Charge.csv",
#     mime="text/csv"
# )


