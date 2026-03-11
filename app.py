import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
import plotly.express as px
import pandas as pd

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="AI Financial Advisor", page_icon="💰", layout="wide")
st.title("💰 AI Financial Advisor")
st.markdown("Personalized financial guidance powered by Gemini 2.0 Flash")

st.sidebar.header("Your Financial Profile")
user_type = st.sidebar.selectbox("I am a:", ["Student", "Working Professional", "Retiree"])
name = st.sidebar.text_input("Your Name", "Alex")

st.sidebar.header("Monthly Finances")
income = st.sidebar.number_input("Monthly Income", min_value=0, value=50000)
rent = st.sidebar.number_input("Rent", min_value=0, value=10000)
food = st.sidebar.number_input("Food", min_value=0, value=5000)
transport = st.sidebar.number_input("Transport", min_value=0, value=3000)
entertainment = st.sidebar.number_input("Entertainment", min_value=0, value=2000)
other_expenses = st.sidebar.number_input("Other Expenses", min_value=0, value=2000)
savings = st.sidebar.number_input("Current Savings", min_value=0, value=20000)
debt = st.sidebar.number_input("Total Debt", min_value=0, value=0)
goal = st.sidebar.text_input("Your Goal", "Save for a laptop in 6 months")

total_expenses = rent + food + transport + entertainment + other_expenses
monthly_savings = income - total_expenses
savings_rate = (monthly_savings / income * 100) if income > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Monthly Income", f"Rs {income:,}")
col2.metric("Total Expenses", f"Rs {total_expenses:,}")
col3.metric("Monthly Savings", f"Rs {monthly_savings:,}")
col4.metric("Savings Rate", f"{savings_rate:.1f}%")

st.divider()
col_chart, col_advice = st.columns([1, 1])

with col_chart:
    st.subheader("Expense Breakdown")
    df = pd.DataFrame({
        "Category": ["Rent", "Food", "Transport", "Entertainment", "Other"],
        "Amount": [rent, food, transport, entertainment, other_expenses]
    })
    df = df[df["Amount"] > 0]
    if not df.empty:
        fig = px.pie(df, values="Amount", names="Category",
                     color_discrete_sequence=px.colors.sequential.Teal)
        st.plotly_chart(fig, use_container_width=True)

with col_advice:
    st.subheader("AI Financial Advice")
    if st.button("Get My Personalized Advice", type="primary"):
        with st.spinner("Analyzing your finances..."):
            prompt = f"You are a friendly financial advisor. User: {name}, Type: {user_type}, Income: Rs {income}, Expenses: Rs {total_expenses}, Savings: Rs {savings}, Debt: Rs {debt}, Goal: {goal}. Give 1) financial health assessment 2) top 3 saving tips 3) plan to achieve goal 4) one investment suggestion. Under 300 words."
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            st.write(response.text)

st.divider()
st.subheader("Goal Progress Tracker")
goal_amount = st.number_input("How much do you need for your goal? (Rs)", min_value=0, value=50000)
if monthly_savings > 0 and goal_amount > 0:
    months_needed = goal_amount / monthly_savings
    already_saved_pct = min((savings / goal_amount) * 100, 100)
    c1, c2 = st.columns(2)
    c1.metric("Months to Reach Goal", f"{months_needed:.1f} months")
    c2.metric("Already Saved", f"{already_saved_pct:.1f}%")
    st.progress(int(already_saved_pct))
elif monthly_savings <= 0:
    st.warning("Your expenses exceed your income!")

st.divider()
st.subheader("Ask the AI Advisor Anything")
user_question = st.text_input("Type your financial question here...")
if st.button("Ask"):
    if user_question:
        with st.spinner("Thinking..."):
            chat_prompt = f"You are a helpful financial advisor. User is a {user_type} with income Rs {income}/month. Answer in under 150 words: {user_question}"
            chat_response = client.models.generate_content(model="gemini-2.0-flash", contents=chat_prompt)
            st.info(chat_response.text)

st.caption("Built with Streamlit and Gemini 2.0 Flash")