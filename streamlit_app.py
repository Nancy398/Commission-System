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

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

import streamlit as st
import time

import streamlit as st

import streamlit as st

SHEET_NAME = "UserDatabase"
ACTIVATION_URL = "https://commission-system-moohousing.streamlit.app/?activate="  # 修改为你的 Streamlit 应用地址

# ---- Google Sheets 认证 ----
def authenticate_gspread():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_info(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"], scopes=scope)
    gc = gspread.authorize(credentials)
    return gc.open(SHEET_NAME).sheet1

# ---- 获取所有用户 ----
def get_users():
    sheet = authenticate_gspread()
    return sheet.get_all_records()

# ---- 查找用户 ----
def find_user(email):
    users = get_users()
    for user in users:
        if user["Email"] == email:
            return user
    return None

# ---- 添加新用户 ----
def add_user(email, name, role):
    sheet = authenticate_gspread()
    activation_code = f"ACT-{email}"  # 生成唯一激活码
    sheet.append_row([email, name, role, "temp_password", activation_code])
    return activation_code  # 返回激活码

# ---- 更新用户密码（激活账户） ----
def update_user_password(email, new_password):
    sheet = authenticate_gspread()
    users = sheet.get_all_values()
    for i, row in enumerate(users):
        if row[0] == email:  # Email 在第一列
            sheet.update_cell(i + 1, 4, new_password)  # 更新密码（列4）
            sheet.update_cell(i + 1, 5, "Activated")  # 移除激活码（列5）
            return True
    return False

# 获取 URL 参数
query_params = st.query_params
page = query_params.get("page", ["login"])  # 默认显示登录页面

# **🔹 主界面**
if page == "home":
    st.markdown('<div class="main-title">Welcome to Leasing Board!</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Manage your leasing data easily and securely</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="btn-container">
            <a href="?page=login" class="btn btn-login">Login</a>
            <a href="?page=leasing_data" class="btn btn-leasing">Leasing Data</a>
        </div>
    """, unsafe_allow_html=True)

# **🔹 登录页面**
elif page == "login":
    st.markdown('<div class="main-title">🔑 Login</div>', unsafe_allow_html=True)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.user_role = ""

    if not st.session_state.logged_in:
        email = st.text_input("Email", key="email_input")
        password = st.text_input("Password", type="password", key="password_input")
    
        if st.button("Login"):
            user = find_user(email)
            if user:
                if password == user["Password"]:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user["Name"]
                    st.session_state.user_role = user["Role"]
                    st.success(f"✅ Welcome, {user['Name']}!")
                    st.query_params.update({"page": st.session_state.user_role})
                    st.rerun()
                else:
                    st.error("❌ Invalid password.")
            else:
                st.error("❌ User not found.")

    # if st.button("Login"):
    #     if email in USER_DATABASE and USER_DATABASE[email][0] == password:
    #         role = USER_DATABASE[email][1]  # 获取用户角色
    #         st.success(f"✅ Logged in as {role.capitalize()}!")
    #         st.query_params.update({"page": role})  # **跳转到对应角色界面**
    #     else:
    #         st.error("❌ Invalid email or password")

# **🔹 Admin 页面**
elif page == "admin":
    st.markdown('<div class="main-title">⚙️ Admin Dashboard</div>', unsafe_allow_html=True)
    st.write("Welcome, Admin! Manage users and settings.")
    if st.button("Logout"):
        st.query_params.update({"page": "login"})  # 退出回到登录页

# **🔹 Sales 页面**
elif page == "sales":
    st.markdown('<div class="main-title">📈 Sales Dashboard</div>', unsafe_allow_html=True)
    st.write("Welcome, Sales team! View and manage sales data.")
    if st.button("Logout"):
        st.query_params.update({"page": "login"})  # 退出回到登录页

# **🔹 Super Admin 页面**
elif page == "superadmin":
    st.markdown('<div class="main-title">🛠️ Super Admin Panel</div>', unsafe_allow_html=True)
    st.write("Welcome, Super Admin! You have full access to the system.")
    if st.button("Logout"):
        st.query_params.update({"page": "login"})  # 退出回到登录页

# **🔹 版权信息**
st.markdown('<div class="footer">© 2025 Leasing Board - All rights reserved.</div>', unsafe_allow_html=True)





# # ---- Streamlit 界面 ----
# st.title("🔑 User Login")

# # ---- 处理激活链接 ----

# activation_params = st.query_params
# activation_code = activation_params.get("activate", [None])
# st.write(activation_code)
# # 如果 URL 里有 activation_code，则显示激活界面
# if activation_code:
#     st.title("🔓 Account Activation")
#     user_found = False
#     users = get_users()  # 获取用户数据

#     for user in users:
#         if user["ActivationCode"] == activation_code:  # 假设“激活码”列存的是激活码
#             user_found = True
#             new_password = st.text_input("Enter new password", type="password")
#             confirm_password = st.text_input("Confirm new password", type="password")

#             if st.button("Activate"):
#                 if new_password and new_password == confirm_password:
#                     update_user_password(user["Email"], new_password)  # 更新密码
#                     st.success("✅ Account activated! You can now log in.")
#                     st.rerun()  # **强制刷新 Streamlit 页面**
#                 else:
#                     st.error("❌ Passwords do not match.")
#             break

#     if not user_found:
#         st.error("❌ Invalid activation link.")
#     st.stop()


# # ---- 登录界面 ----
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
#     st.session_state.user_name = ""
#     st.session_state.user_role = ""

# if not st.session_state.logged_in:
#     email = st.text_input("Email", key="email_input")
#     password = st.text_input("Password", type="password", key="password_input")

#     if st.button("Login"):
#         user = find_user(email)
#         if user:
#             if password == user["Password"]:
#                 st.session_state.logged_in = True
#                 st.session_state.user_name = user["Name"]
#                 st.session_state.user_role = user["Role"]
#                 st.success(f"✅ Welcome, {user['Name']}!")
#                 st.rerun()
#             else:
#                 st.error("❌ Invalid password.")
#         else:
#             st.error("❌ User not found.")

# else:
#     st.sidebar.write(f"👤 Logged in as: **{st.session_state.user_name}** ({st.session_state.user_role})")

#     if st.session_state.user_role == "SuperAdmin":
#         page = st.radio("Choose an action", ["Super Admin Panel", "Add New User"])
        
#         if page == "Super Admin Panel":
#             st.subheader("🛠️ Super Admin Panel")
#             st.write("Welcome to the Super Admin Panel.")
        
#         elif page == "Add New User":
#             st.subheader("🛠️ Add New User")
#             new_email = st.text_input("User Email")
#             new_name = st.text_input("Full Name")
#             new_role = st.selectbox("Role", ["Admin", "Sales"])
            
#             if st.button("Add User"):
#                 if new_email and new_name:
#                     activation_code = add_user(new_email, new_name, new_role)
#                     activation_link = f"{ACTIVATION_URL}{activation_code}"
#                     st.success(f"✅ {new_name} ({new_role}) added successfully!")
#                     st.write(f"🔗 Activation Link: [Click here to activate]({activation_link})")
#                     st.code(activation_link)  # 显示纯文本链接，方便复制
#                 else:
#                     st.error("❌ Please fill in all fields.")

#     if st.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.user_name = ""
#         st.session_state.user_role = ""
#         st.rerun()

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


