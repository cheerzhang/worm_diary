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
    login_, logout_ = st.sidebar.columns(2)
    with login_:
        if st.button("Login"):
            role = authenticate_user(username, password)
            if role:
                st.session_state["role"] = role
                st.session_state["logged_in"] = True
                st.sidebar.success("Login successful!")
            else:
                st.sidebar.error("Invalid username or password")
    with logout_:
        if st.button('Logout'):
            logout()

def logout():
    role = "guest"
    st.session_state["role"] = role
    st.session_state["logged_in"] = False
    st.sidebar.success("Logout successful!")


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
    st.write(df)
    try:
        df.to_csv(CSV_FILE, index=False)
        st.success("Data saved successfully!")
    except Exception as e:
        st.error(f"Failed to save data: {e}")


# 页面显示数据
def show_data_page():
    st.title("Worm Diary - View Data")
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


# 页面添加数据
def add_data_page():
    st.title("Worm Diary - Add Data")
    if st.session_state["role"] == "admin":
        with st.form("entry_form"):
            date = st.date_input("Date", datetime.now())
            food = st.text_input("Food")
            food_type = st.selectbox("Food type", ["Vegetables", "Fruits", "Coffee Grounds", "Paper", "Others"])
            quantity = st.number_input("Quantity (g)", min_value=0)
            decomposition = st.checkbox("Fully decomposed")
            submit = st.form_submit_button("Add Entry")

            if submit:
                new_entry = pd.DataFrame({
                    "date": [date],
                    "food": [food],
                    "food_type": [food_type],
                    "quantity": [quantity],
                    "decomposition": [decomposition]
                })
                
                df = load_data()
                df = pd.concat([df, new_entry], ignore_index=True)
                
                save_data(df)
    else:
        st.warning("You must be logged in as admin to add data.")



# 运行应用
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["role"] = "guest"
    login()
    

    page = st.sidebar.selectbox("Select Page", ["View Data", "Add Data"])

    if page == "View Data":
        show_data_page()
    elif page == "Add Data":
        add_data_page()



# 运行应用
if __name__ == "__main__":
    main()