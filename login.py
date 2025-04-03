import streamlit as st
from google.oauth2.service_account import Credentials
import gspread

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
def find_user(email, password):
    users = get_users()
    for user in users:
        if user["Email"] == email and user["Password"] == password:
            return user
    return None

# ---- 页面标题和样式 ----
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #2c3e50;
            font-size: 36px;
            font-weight: bold;
            margin-top: 50px;
        }
        .sub-title {
            text-align: center;
            color: #7f8c8d;
            font-size: 20px;
            margin-bottom: 30px;
        }
        .form-container {
            background-color: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.15);
            max-width: 400px;
            margin: auto;
        }
        .btn {
            width: 100%;
            padding: 12px;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            border-radius: 30px;
            border: none;
            background-color: #A7C7E7;
            color: white;
            cursor: pointer;
            transition: all 0.4s ease;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.15);
            margin-top: 15px;
        }
        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.25);
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            font-size: 14px;
            color: #95a5a6;
        }
        .back-link {
            display: block;
            text-align: center;
            margin-top: 15px;
            color: #2980b9;
            font-weight: bold;
            text-decoration: none;
        }
        .back-link:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# ---- 显示标题 ----
st.markdown('<div class="main-title">🔑 Login</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Enter your credentials to continue</div>', unsafe_allow_html=True)

# ---- 登录表单 ----
st.markdown('<div class="form-container">', unsafe_allow_html=True)

email = st.text_input("Email", key="email_input")
password = st.text_input("Password", type="password", key="password_input")

if st.button("Login", key="login_button"):
    user = find_user(email, password)
    
    if user:
        st.success("✅ Login successful! Redirecting...")
        st.session_state.logged_in = True
        st.session_state.user_name = user["Name"]
        st.session_state.user_role = user["Role"]
        st.session_state.user_email = user["Email"]
        
        # **根据角色跳转**
        if user["Role"] == "SuperAdmin":
            st.switch_page("superadmin.py")
        elif user["Role"] == "Admin":
            st.switch_page("admin.py")
        elif user["Role"] == "Sales":
            st.switch_page("sales.py")
        else:
            st.error("❌ Role not recognized.")
    else:
        st.error("❌ Invalid email or password.")

st.markdown('</div>', unsafe_allow_html=True)

# ---- 返回主页链接 ----
st.markdown('<a href="?page=home" class="back-link">⬅ Back to Home</a>', unsafe_allow_html=True)

# ---- 页面底部 ----
st.markdown('<div class="footer">© 2025 Leasing Board - Secure Login</div>', unsafe_allow_html=True)
