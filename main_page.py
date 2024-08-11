import streamlit as st
import pandas as pd
from datetime import datetime
import os
import hashlib


# 配置文件路径
CSV_FILE = "worm_diary.csv"

# 用户角色定义
def authenticate_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if username == "admin" and password_hash == "75836b220eaf45c58c6e030620a6b5853bd1fc1021f7b74ec3150644918a8bd8":
        return "admin"
    elif username == "guest":
        return "guest"
    else:
        return None

# 用户登录
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        role = authenticate_user(username, password)
        if role:
            st.session_state["role"] = role
            st.session_state["logged_in"] = True
            st.sidebar.success("Login successful!")
        else:
            st.sidebar.error("Invalid username or password")

# 数据加载与保存
def load_data():
    if os.stat(CSV_FILE).st_size == 0:
        df = pd.DataFrame(columns=["date", "food", "food_type", "quantity", "decomposition"])
    else:
        df = pd.read_csv(CSV_FILE)
    required_columns = ["date", "food", "food_type", "quantity", "decomposition"]
    for col in required_columns:
        if col not in df.columns:
            df[col] = None
    df['quantity'] = df['quantity'].fillna(0)
    df['decomposition'] = df['decomposition'].fillna(False).astype(bool)
    return df


def save_data(df):
    df.to_csv(CSV_FILE, index=False)

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["role"] = "guest"

    # 显示登录表单
    st.sidebar.title("Login")
    if st.session_state["logged_in"]:
        st.sidebar.success(f"Already logged in as {st.session_state['role']}")
        if st.sidebar.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["role"] = "guest"
            st.sidebar.info("Logged out successfully!")
    else:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            role = authenticate_user(username, password)
            if role:
                st.session_state["role"] = role
                st.session_state["logged_in"] = True
                st.sidebar.success(f"Login successful! Logged in as {role}")
            else:
                st.sidebar.error("Invalid username or password")

    # 显示当前数据
    st.title("Worm Diary")
    df = load_data()
    
    st.dataframe(df)
    

    # 数据过滤
    st.subheader("Filter")
    food_type_filter = st.multiselect("Filter by food type", options=df["food_type"].unique())
    if food_type_filter:
        df = df[df["food_type"].isin(food_type_filter)]
        st.dataframe(df)

    # 待分解食物总量统计
    pending_decomposition = df[~df["decomposition"]]["quantity"].sum()
    st.subheader(f"Total food pending decomposition: {pending_decomposition} g")

    if pending_decomposition < 50:
        st.warning("Feeding is low, consider adding more food!")
    elif pending_decomposition > 200:
        st.warning("Feeding is too high, avoid adding more food!")

    # 理论产生蚯蚓肥的计算
    df['generated_fertilizer'] = df.apply(
        lambda row: row['quantity'] * 1.5 if row['decomposition'] else 0, axis=1)
    total_fertilizer = df['generated_fertilizer'].sum()
    st.subheader(f"Total theoretical worm fertilizer produced: {total_fertilizer:.2f} g")

    if st.session_state["role"] == "admin":
        with st.form("entry_form"):
            date = st.date_input("Date", datetime.now())
            food = st.text_input("Food")
            food_type = st.selectbox("Food type", ["Vegetables", "Fruits", "Coffee Grounds", "Paper", "Others"])
            quantity = st.number_input("Quantity (g)", min_value=0)
            decomposition = st.checkbox("Fully decomposed")
            submit = st.form_submit_button("Add Entry")

            if submit:
                new_entry = {
                    "date": date,
                    "food": food,
                    "food_type": food_type,
                    "quantity": quantity,
                    "decomposition": decomposition
                }
                df = df.append(new_entry, ignore_index=True)
                save_data(df)
                st.success("Entry added successfully!")


# 运行应用
if __name__ == "__main__":
    main()