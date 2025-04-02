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

SHEET_NAME = "UserDatabase" 

def authenticate_gspread():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_info(
    st.secrets["GOOGLE_APPLICATION_CREDENTIALS"], 
    scopes=scope)
    gc = gspread.authorize(credentials)
    return gc.open(SHEET_NAME).sheet1

def get_users():
    sheet = authenticate_gspread()
    return sheet.get_all_records()

# 查找用户
def find_user(email):
    users = get_users()
    for user in users:
        if user["Email"] == email:
            return user
    return None

# 添加用户
def add_user(email, name, role, username, password_hashed):
    sheet = authenticate_gspread()
    sheet.append_row([email, name, role, username, password_hashed])

# 更新用户密码（用于激活账户）
def update_user_password(email, new_password):
    sheet = authenticate_gspread()
    users = sheet.get_all_values()

    for i, row in enumerate(users):
        if row[0] == email:  # Email 在第一列
            sheet.update_cell(i+1, 5, new_password)  # 密码在第5列
            return True
    return False

# ---- Streamlit 界面 ----
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["Login", "Super Admin", "Activate"])

# ---- 登录页面 ----
if page == "Login":
    st.title("🔑 User Login")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = find_user(email)
        
        if user:
            stored_password = user["Password"]  # 明文密码
            if password == stored_password:
                st.success(f"✅ Welcome, {user['Name']} ({user['Role']})!")
            else:
                st.error("❌ Invalid password.")
        else:
            st.error("❌ User not found.")

# ---- Super Admin 页面 ----
elif page == "Super Admin":
    st.title("🛠️ Super Admin Panel")
    
    email = st.text_input("Super Admin Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login as Super Admin"):
        user = find_user(email)
        
        if user and user["Role"] == "SuperAdmin":
            stored_password = user["Password"]  # 明文密码
            if password == stored_password:
                st.success("✅ Super Admin Logged In!")
                
                # Super Admin 创建用户
                st.subheader("Add New User")
                new_email = st.text_input("User Email")
                new_name = st.text_input("Full Name")
                new_role = st.selectbox("Role", ["Admin", "Sales"])
                new_username = new_name.split()[0] + str(len(new_name))
                
                if st.button("Add User"):
                    # 直接存储明文密码，实际使用中应采取更安全的密码存储方式
                    add_user(new_email, new_name, new_role, new_username, "temp_password")
                    st.success(f"✅ {new_name} ({new_role}) added successfully!")
            else:
                st.error("❌ Incorrect password.")
        else:
            st.error("❌ Access Denied. Only Super Admin can access this panel.")

# ---- 账户激活页面 ----
elif page == "Activate":
    st.title("🔐 Activate Your Account")
    
    email = st.text_input("Enter your email")
    
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


