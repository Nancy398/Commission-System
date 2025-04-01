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

import streamlit as st

# 保存数据
def save_data(df, file_path):
    df.to_csv(file_path, index=False)
    
USERS_FILE = "users.csv"
DEALS_FILE = "deals.csv"  

# @st.cache_data(ttl=300)
def read_file(name,sheet):
  scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
  credentials = Credentials.from_service_account_info(
  st.secrets["GOOGLE_APPLICATION_CREDENTIALS"], 
  scopes=scope)
  gc = gspread.authorize(credentials)
  worksheet = gc.open(name).worksheet(sheet)
  rows = worksheet.get_all_values()
  df = pd.DataFrame.from_records(rows)
  df = pd.DataFrame(df.values[1:], columns=df.iloc[0])
  return df
Commission = read_file("Leasing Database","Sheet2")
Commission['Number of beds'] = Commission['Number of beds'].astype(int)
Commission['Signed Date'] = pd.to_datetime(Commission['Signed Date'],format='mixed')
Commission_own = Commission.loc[Commission['Property Type'] == 'Own Property']
Commission_own = Commission_own.copy()
Commission_own.loc[Commission_own['Term'].eq('Long'), 'Owner Bill'] = 600
Commission_own.loc[Commission_own['Term'].eq('Short'), 'Owner Bill'] = 300

st.dataframe(
    Commission_own,
    use_container_width=True,
)

start_date = datetime(2024, 9, 1)  # 2024年11月1日
end_date = datetime(2025, 4, 30) 
col1, col2 = st.columns(2)
with col1:
    start_selected = st.date_input(
        "From:",
        value=start_date,
        min_value=start_date,
        max_value=end_date
    )
with col2:
    end_selected = st.date_input(
        "To:",
        value=end_date,
        min_value=start_date,
        max_value=end_date
    )


start_selected = pd.Timestamp(start_selected)
end_selected = pd.Timestamp(end_selected)
df_filtered = Commission_own[Commission_own["Signed Date"].between(start_selected,end_selected)]
                                                                  
Bill_Charge = pd.DataFrame()
Bill_Charge['Bill Property Code'] = df_filtered['Property Name']
Bill_Charge['Bill Unit Name'] = ' '
Bill_Charge['Payee Name'] = "Moo Housing Inc"
Bill_Charge['Amount'] = df_filtered['Owner Bill']
Bill_Charge['Bill Account'] = '6112'
Bill_Charge['Desc'] = '6112'
Bill_Charge['Description'] = df_filtered['Property']
Bill_Charge['Bill Date'] = end_selected
Bill_Charge['Due Date'] = end_selected

st.dataframe(
    Bill_Charge,
    use_container_width=True,
)
# # 数据文件路径
# USERS_FILE = "users.csv"
# DEALS_FILE = "deals.csv"
# # FEEDBACKS_FILE = "data/feedbacks.csv"

# # 读取数据
# users_df = pd.read_csv(USERS_FILE)
# # deals_df = pd.read_csv(DEALS_FILE)
# # feedbacks_df = pd.read_csv(FEEDBACKS_FILE)

# # 保存数据
# def save_data(df, file_path):
#     df.to_csv(file_path, index=False)

# # Streamlit 应用主入口
# def main():
#     st.title("Commission System")

#     # 登录或注册界面选择
#     if "logged_in" not in st.session_state:
#         st.session_state.logged_in = False

#     if not st.session_state.logged_in:
#         option = st.sidebar.selectbox("Choose", ["Log in", "Register"])

#         if option == "Log in":
#             login()
#         elif option == "Register":
#             register()
#         return

#     # 已登录用户界面
#     st.sidebar.header(f"Welcome, {st.session_state.user['name']}")
#     if st.sidebar.button("Sign out"):
#         st.session_state.logged_in = False
#         return

#     # 根据角色显示对应界面
#     if st.session_state.user["role"] == "admin":
#         admin_dashboard()
#     else:
#         sales_dashboard()

# # 登录功能
# def login():
#     st.sidebar.header("Log in")
#     username = st.sidebar.text_input("User")
#     password = st.sidebar.text_input("Password", type="password")
#     if st.sidebar.button("Log in "):
#         user = authenticate(username, password)
#         if user:
#             st.session_state.logged_in = True
#             st.session_state.user = user
#             st.success(f"Welcome {user['name']}！")
#         else:
#             st.sidebar.error("User Name or Password wrong！")

# # 注册功能
# def register():
#     st.sidebar.header("Register")
#     name = st.sidebar.text_input("Name")
#     username = st.sidebar.text_input("Username")
#     password = st.sidebar.text_input("Password", type="password")
#     role = st.sidebar.radio("角色", ["sales", "admin"], format_func=lambda x: "Sales" if x == "sales" else "Admin")

#     if st.sidebar.button("Register"):
#         if not name or not username or not password:
#             st.sidebar.error("Please fill out all the blank")
#         elif username_exists(username):
#             st.sidebar.error("User Name already exist")
#         else:
#             new_user = {"username": username, "password": password, "name": name, "role": role}
#             add_user(new_user)
#             st.sidebar.success("Success! Please back to log in!")

# # 检查用户名是否存在
# def username_exists(username):
#     return not users_df[users_df["username"] == username].empty

# # 添加新用户
# def add_user(user):
#     global users_df
#     new_user = pd.DataFrame([user])
#     users_df = pd.concat([users_df, new_user], ignore_index=True)
#     save_data(users_df, USERS_FILE)

# # 用户身份验证
# def authenticate(username, password):
#     user = users_df[(users_df["username"] == username) & (users_df["password"] == password)]
#     if not user.empty:
#         return user.iloc[0].to_dict()
#     return None

# # 销售界面
# def sales_dashboard():
#     global deals_df, feedbacks_df
#     user = st.session_state.user
#     st.header("销售界面")

#     # 查看自己的成单
#     user_deals = deals_df[deals_df["sales"] == user["username"]]
#     st.subheader("我的成单")
#     st.table(user_deals)

#     # 提交反馈
#     st.subheader("提交反馈")
#     selected_deal_id = st.selectbox("选择要反馈的成单", user_deals["id"])
#     feedback = st.text_area("反馈内容", "")
#     if st.button("提交反馈"):
#         if feedback:
#             new_feedback = {"id": len(feedbacks_df) + 1, "sales": user["username"], "deal_id": selected_deal_id, "feedback": feedback, "status": "待处理"}
#             feedbacks_df = feedbacks_df.append(new_feedback, ignore_index=True)
#             save_data(feedbacks_df, FEEDBACKS_FILE)
#             st.success("反馈提交成功！")
#         else:
#             st.warning("请输入反馈内容。")

#     # 查看自己提交的反馈
#     st.subheader("我的反馈")
#     user_feedbacks = feedbacks_df[feedbacks_df["sales"] == user["username"]]
#     st.table(user_feedbacks)

# # 管理员界面
# def admin_dashboard():
#     global feedbacks_df
#     st.header("管理员界面")

#     # 查看所有反馈
#     st.subheader("所有反馈")
#     all_feedbacks = feedbacks_df
#     st.table(all_feedbacks)

#     # 更新反馈处理状态
#     st.subheader("处理反馈")
#     feedback_id = st.selectbox("选择反馈ID", all_feedbacks["id"])
#     feedback_status = st.radio("反馈状态", ["待处理", "已处理"], index=0 if all_feedbacks[all_feedbacks["id"] == feedback_id]["status"].values[0] == "待处理" else 1)
#     if st.button("更新状态"):
#         feedbacks_df.loc[feedbacks_df["id"] == feedback_id, "status"] = feedback_status
#         save_data(feedbacks_df, FEEDBACKS_FILE)
#         st.success("反馈状态更新成功！")

# if __name__ == "__main__":
#     main()
