import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from openai import OpenAI
import os

# -----------------------------
# CONFIG
# -----------------------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.set_page_config(
    page_title="AI Financial Advisor Pro",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI Financial Advisor Pro")
st.markdown(
    "AI-powered personal finance dashboard with financial health analysis, goal planning, investment guidance, and AI coaching."
)

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("👤 Financial Profile")

user_type = st.sidebar.selectbox(
    "I am a:",
    ["Student", "Working Professional", "Retiree"]
)

name = st.sidebar.text_input("Your Name", "Vaikunth")

st.sidebar.header("💵 Monthly Finances")

income = st.sidebar.number_input(
    "Monthly Income (₹)",
    min_value=0,
    value=50000
)

rent = st.sidebar.number_input(
    "Rent (₹)",
    min_value=0,
    value=10000
)

food = st.sidebar.number_input(
    "Food (₹)",
    min_value=0,
    value=5000
)

transport = st.sidebar.number_input(
    "Transport (₹)",
    min_value=0,
    value=3000
)

entertainment = st.sidebar.number_input(
    "Entertainment (₹)",
    min_value=0,
    value=2000
)

other_expenses = st.sidebar.number_input(
    "Other Expenses (₹)",
    min_value=0,
    value=2000
)

savings = st.sidebar.number_input(
    "Current Savings (₹)",
    min_value=0,
    value=20000
)

debt = st.sidebar.number_input(
    "Total Debt (₹)",
    min_value=0,
    value=0
)

goal = st.sidebar.text_input(
    "Financial Goal",
    "Buy a Laptop"
)

goal_amount = st.sidebar.number_input(
    "Goal Amount (₹)",
    min_value=1,
    value=50000
)

# -----------------------------
# CALCULATIONS
# -----------------------------

total_expenses = (
    rent +
    food +
    transport +
    entertainment +
    other_expenses
)

monthly_savings = income - total_expenses

savings_rate = (
    (monthly_savings / income) * 100
    if income > 0 else 0
)

emergency_months = (
    savings / total_expenses
    if total_expenses > 0 else 0
)

annual_income = income * 12

dti = (
    (debt / annual_income) * 100
    if annual_income > 0 else 0
)

# -----------------------------
# FINANCIAL HEALTH SCORE
# -----------------------------

score = 100

if savings_rate < 10:
    score -= 30
elif savings_rate < 20:
    score -= 15

if dti > 50:
    score -= 25
elif dti > 35:
    score -= 15

if emergency_months < 3:
    score -= 20

score = max(score, 0)

# Financial Grade

if score >= 85:
    grade = "A"
elif score >= 70:
    grade = "B"
elif score >= 55:
    grade = "C"
else:
    grade = "D"

# Risk Profile

if user_type == "Student":
    risk_profile = "Aggressive"
elif user_type == "Working Professional":
    risk_profile = "Moderate"
else:
    risk_profile = "Conservative"


# Budget Recommendation

recommended_savings = income * 0.20
savings_difference = monthly_savings - recommended_savings

expense_ratio = (
    (total_expenses / income) * 100
    if income > 0 else 0
)

a1, a2, a3, a4, a5, a6 = st.columns(6)

with a1:
    st.metric("Financial Health Score", f"{score}/100")

with a2:
    st.metric("Financial Grade", grade)

with a3:
    st.metric("Emergency Fund", f"{emergency_months:.1f} Months")

with a4:
    st.metric("Debt-To-Income Ratio", f"{dti:.1f}%")

with a5:
    st.metric("Risk Profile", risk_profile)

with a6:
    st.metric("Expense Ratio", f"{expense_ratio:.1f}%")

# -----------------------------
# DASHBOARD METRICS
# -----------------------------

st.subheader("📊 Financial Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Monthly Income",
    f"₹{income:,.0f}"
)

col2.metric(
    "Monthly Expenses",
    f"₹{total_expenses:,.0f}"
)

col3.metric(
    "Monthly Savings",
    f"₹{monthly_savings:,.0f}"
)

col4.metric(
    "Savings Rate",
    f"{savings_rate:.1f}%"
)

st.divider()

# -----------------------------
# INSIGHTS
# -----------------------------

c1, c2 = st.columns(2)

with c1:

    st.subheader("📌 Financial Insights")

    if score >= 85:
        st.success("Excellent Financial Health")
    elif score >= 70:
        st.info("Good Financial Health")
    elif score >= 55:
        st.warning("Needs Improvement")
    else:
        st.error("High Financial Risk")

    if emergency_months < 3:
        st.error(
            "Emergency fund is below recommended levels."
        )
    elif emergency_months < 6:
        st.warning(
            "Emergency fund is decent but can be improved."
        )
    else:
        st.success(
            "Excellent emergency fund coverage."
        )

    if dti < 20:
        st.success("Debt level is healthy.")
    elif dti < 35:
        st.info("Debt level is manageable.")
    else:
        st.warning("Debt level is becoming risky.")

with c2:

    st.subheader("🎯 Goal Planner")

    if monthly_savings > 0:

        months_needed = goal_amount / monthly_savings

        progress = min(
            (savings / goal_amount) * 100,
            100
        )

        st.metric(
            "Months To Reach Goal",
            f"{months_needed:.1f}"
        )

        st.progress(int(progress))

        st.write(
            f"Goal Progress: {progress:.1f}%"
        )

    else:
        st.error(
            "Expenses exceed income."
        )

st.divider()

st.divider()

st.subheader("💡 Budget Recommendation")

b1, b2, b3 = st.columns(3)

b1.metric(
    "Target Savings (20%)",
    f"₹{recommended_savings:,.0f}"
)

b2.metric(
    "Actual Savings",
    f"₹{monthly_savings:,.0f}"
)

b3.metric(
    "Difference",
    f"₹{savings_difference:,.0f}"
)

if savings_difference >= 0:
    st.success(
        "You are saving more than the recommended 20%."
    )
else:
    st.warning(
        "Try increasing your savings rate toward 20%."
    )

# -----------------------------
# CHARTS
# -----------------------------

st.subheader("📈 Financial Visualizations")

chart1, chart2 = st.columns(2)

expense_df = pd.DataFrame({
    "Category": [
        "Rent",
        "Food",
        "Transport",
        "Entertainment",
        "Other"
    ],
    "Amount": [
        rent,
        food,
        transport,
        entertainment,
        other_expenses
    ]
})

expense_df = expense_df[
    expense_df["Amount"] > 0
]

with chart1:

    if not expense_df.empty:

        pie = px.pie(
            expense_df,
            values="Amount",
            names="Category",
            title="Expense Breakdown"
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

with chart2:

    compare_df = pd.DataFrame({
        "Category": [
            "Income",
            "Expenses",
            "Savings"
        ],
        "Amount": [
            income,
            total_expenses,
            monthly_savings
        ]
    })

    bar = px.bar(
        compare_df,
        x="Category",
        y="Amount",
        title="Income vs Expenses vs Savings"
    )

    st.plotly_chart(
        bar,
        use_container_width=True
    )

st.divider()

# -----------------------------
# INVESTMENT SUGGESTIONS
# -----------------------------

st.subheader("📚 Investment Suggestions")

if user_type == "Student":

    st.info("""
    • Build emergency fund first

    • Invest in skills & certifications

    • Start SIPs in Index Funds

    • Learn personal finance
    """)

elif user_type == "Working Professional":

    st.info("""
    • Emergency Fund

    • Index Funds

    • Mutual Funds

    • Retirement Planning

    • Tax Optimization
    """)

else:

    st.info("""
    • Capital Preservation

    • Fixed Income Assets

    • Debt Funds

    • Emergency Cash Reserve
    """)

st.divider()

# -----------------------------
# AI COACH
# -----------------------------

st.subheader("🤖 AI Financial Coach")

if st.button(
    "Generate Personalized Advice",
    type="primary"
):

    prompt = f"""
You are a professional financial advisor.

Name: {name}
User Type: {user_type}

Income: ₹{income}
Expenses: ₹{total_expenses}
Savings: ₹{savings}
Debt: ₹{debt}

Savings Rate: {savings_rate:.1f}%

Financial Goal:
{goal}

Provide:

1. Financial Health Assessment
2. Top 3 Savings Tips
3. Goal Achievement Strategy
4. Investment Suggestion
5. Biggest Financial Mistake To Avoid

Keep under 300 words.
"""

    with st.spinner("Analyzing finances..."):

        try:

            response = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            advice = (
                response
                .choices[0]
                .message
                .content
            )

            st.markdown("## 📋 Personalized Financial Report")
            st.markdown("---")
            st.markdown(advice)

        except Exception as e:

            st.error(f"Error: {e}")

st.divider()

# -----------------------------
# AI CHAT
# -----------------------------

st.subheader("💬 Ask The AI Advisor")

question = st.text_input(
    "Ask a financial question"
)

if st.button("Ask AI"):

    if question:

        try:

            response = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324",
                messages=[
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            answer = (
                response
                .choices[0]
                .message
                .content
            )

            st.markdown("### 🤖 AI Response")
            st.markdown(answer)

        except Exception as e:

            st.error(f"Error: {e}")

st.divider()

st.divider()

st.subheader("📄 Download Financial Report")

report = f"""
AI FINANCIAL ADVISOR REPORT

Name: {name}
User Type: {user_type}

Monthly Income: ₹{income:,.0f}
Monthly Expenses: ₹{total_expenses:,.0f}
Monthly Savings: ₹{monthly_savings:,.0f}

Savings Rate: {savings_rate:.1f}%
Financial Health Score: {score}/100
Financial Grade: {grade}

Emergency Fund: {emergency_months:.1f} Months
Debt-To-Income Ratio: {dti:.1f}%
Risk Profile: {risk_profile}

Goal: {goal}
Goal Amount: ₹{goal_amount:,.0f}

Recommended Savings (20%): ₹{recommended_savings:,.0f}

Generated using AI Financial Advisor Pro

------------------------------

Financial Summary
------------------------------

Monthly Income: ₹{income:,.0f}
Monthly Expenses: ₹{total_expenses:,.0f}
Monthly Savings: ₹{monthly_savings:,.0f}

Financial Grade: {grade}
Risk Profile: {risk_profile}

Goal: {goal}

Report generated on demand.
"""

st.download_button(
    label="📥 Download Financial Report",
    data=report,
    file_name="financial_report.txt",
    mime="text/plain"
)

st.caption(
    "Built with Streamlit, OpenRouter, DeepSeek, Plotly, Pandas, and Python"
)