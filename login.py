import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

SHEET_NAME = "UserDatabase"

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

# ---- Streamlit 登录界面 ----
st.title("🔑 User Login")

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
            if password == user["Password"]:  # 这里假设密码是明文存储，生产环境应使用哈希密码
                st.session_state.logged_in = True
                st.session_state.user_name = user["Name"]
                st.session_state.user_role = user["Role"]
                st.success(f"✅ Welcome, {user['Name']}!")
                st.rerun()
            else:
                st.error("❌ Invalid password.")
        else:
            st.error("❌ User not found.")

else:
    st.sidebar.write(f"👤 Logged in as: **{st.session_state.user_name}** ({st.session_state.user_role})")

    if st.session_state.user_role == "SuperAdmin":
        st.subheader("🛠️ Super Admin Panel")
        st.write("Welcome to the Super Admin Panel.")
    
    elif st.session_state.user_role == "Admin":
        st.subheader("🛠️ Admin Panel")
        st.write("Welcome to the Admin Panel.")
    
    elif st.session_state.user_role == "Sales":
        st.subheader("💼 Sales Panel")
        st.write("Welcome to the Sales Panel.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.user_role = ""
        st.rerun()
