from openai import OpenAI
from dotenv import load_dotenv
import os

import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3


# -----------------------------------
# LOAD ENVIRONMENT VARIABLES
# -----------------------------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)




from main import (
    predict_revenue,
    accuracy
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Enterprise AI Insights Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    div.block-container {
        padding-top: 1.5rem;
    }

    [data-testid="stSidebar"] {
        width: 260px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

connection = sqlite3.connect(
    "ai_enterprise.db"
)

customers_df = pd.read_sql(
    "SELECT * FROM customers",
    connection
)

employees_df = pd.read_sql(
    "SELECT * FROM employees",
    connection
)

operations_df = pd.read_sql(
    "SELECT * FROM operations",
    connection
)

sales_df = pd.read_sql(
    "SELECT * FROM sales",
    connection
)

revenue_df = pd.read_sql(
    "SELECT * FROM revenue",
    connection
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("AI Dashboard Filters")

selected_industry = st.sidebar.multiselect(
    "Select Industry",
    customers_df["industry"].unique()
)

selected_department = st.sidebar.multiselect(
    "Select Department",
    employees_df["department"].unique()
)

selected_city = st.sidebar.multiselect(
    "Select City",
    customers_df["city"].unique()
)

# -----------------------------------
# DEFAULT FILTERS
# -----------------------------------

if not selected_industry:
    selected_industry = (
        customers_df["industry"].unique()
    )

if not selected_department:
    selected_department = (
        employees_df["department"].unique()
    )

if not selected_city:
    selected_city = (
        customers_df["city"].unique()
    )

# -----------------------------------
# FILTER DATA
# -----------------------------------

filtered_customers = customers_df[
    (
        customers_df["industry"].isin(
            selected_industry
        )
    )
    &
    (
        customers_df["city"].isin(
            selected_city
        )
    )
]

filtered_employees = employees_df[
    employees_df["department"].isin(
        selected_department
    )
]

# -----------------------------------
# HEADER
# -----------------------------------

st.title(
    "Enterprise AI Insights Assistant"
)

st.write(
    """
    AI powered enterprise intelligence platform
    for UK business analytics and predictive insights.
    """
)

# -----------------------------------
# EXECUTIVE SUMMARY
# -----------------------------------

st.subheader("Executive AI Summary")

top_industry = (
    filtered_customers.groupby("industry")[
        "annual_revenue_gbp"
    ].mean().idxmax()
)

top_city = (
    filtered_customers.groupby("city")[
        "annual_revenue_gbp"
    ].mean().idxmax()
)

st.info(
    f"""
    Highest Revenue Industry:
    {top_industry}

    Highest Revenue City:
    {top_city}

    AI Prediction Accuracy:
    {accuracy * 100:.1f}%
    """
)


# -----------------------------------
# AI BUSINESS RECOMMENDATIONS
# -----------------------------------

st.subheader(
    "AI Generated Business Recommendations"
)

highest_churn_city = (
    filtered_customers.groupby("city")[
        "churn_risk"
    ].mean().idxmax()
)

highest_revenue_industry = (
    filtered_customers.groupby("industry")[
        "annual_revenue_gbp"
    ].mean().idxmax()
)

lowest_satisfaction_industry = (
    filtered_customers.groupby("industry")[
        "customer_satisfaction"
    ].mean().idxmin()
)

best_department = (
    filtered_employees.groupby("department")[
        "productivity_score"
    ].mean().idxmax()
)

st.success(
    f"""
    AI Insight:
    
    {highest_revenue_industry} companies are currently
    generating the strongest average enterprise revenue.
    """
)

st.warning(
    f"""
    AI Alert:
    
    Customer churn risk appears highest in {highest_churn_city}.
    Additional retention strategies are recommended.
    """
)

st.info(
    f"""
    AI Recommendation:
    
    The {best_department} department demonstrates
    the strongest operational productivity.
    """
)

st.error(
    f"""
    AI Risk Analysis:
    
    {lowest_satisfaction_industry} customers show
    lower satisfaction levels and may require
    improved customer engagement strategies.
    """
)



# -----------------------------------
# KPI CARDS
# -----------------------------------

total_customers = len(filtered_customers)

total_revenue = filtered_customers[
    "annual_revenue_gbp"
].sum()

avg_satisfaction = filtered_customers[
    "customer_satisfaction"
].mean()

avg_productivity = filtered_employees[
    "productivity_score"
].mean()

avg_churn_risk = (
    filtered_customers[
        "churn_risk"
    ].mean() * 100
)

col1, col2, col3, col4, col5 = (
    st.columns(5)
)

col1.metric(
    "Customers",
    total_customers,
    delta="+12%"
)

col2.metric(
    "Revenue",
    f"£{total_revenue:,.0f}",
    delta="+18%"
)

col3.metric(
    "Satisfaction",
    f"{avg_satisfaction:.1f}%",
    delta="+5%"
)

col4.metric(
    "Productivity",
    f"{avg_productivity:.1f}%",
    delta="+7%"
)

col5.metric(
    "Churn Risk",
    f"{avg_churn_risk:.1f}%",
    delta="-3%"
)

st.divider()

# -----------------------------------
# TABS
# -----------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Customer Intelligence",
    "Sales Analytics",
    "Operations Intelligence",
    "Employee Insights"
])

# -----------------------------------
# CUSTOMER INTELLIGENCE
# -----------------------------------

with tab1:

    col1, col2 = st.columns(2)

    with col1:

        industry_chart = px.pie(
            filtered_customers,
            names="industry",
            title="Customer Industry Distribution"
        )

        industry_chart.update_layout(
            height=450
        )

        st.plotly_chart(
            industry_chart,
            use_container_width=True
        )

    with col2:

        city_chart = px.bar(
            filtered_customers,
            x="city",
            y="annual_revenue_gbp",
            color="industry",
            title="Revenue by City"
        )

        city_chart.update_layout(
            height=450
        )

        st.plotly_chart(
            city_chart,
            use_container_width=True
        )

# -----------------------------------
# SALES ANALYTICS
# -----------------------------------

with tab2:

    sales_chart = px.scatter(
        sales_df,
        x="deal_value_gbp",
        y="conversion_probability",
        color="sales_stage",
        size="deal_value_gbp",
        title="Sales Conversion Analysis"
    )

    sales_chart.update_layout(
        height=500
    )

    st.plotly_chart(
        sales_chart,
        use_container_width=True
    )

    stage_summary = (
        sales_df.groupby(
            "sales_stage"
        )["deal_value_gbp"]
        .mean()
        .reset_index()
    )

    st.dataframe(
        stage_summary,
        use_container_width=True
    )

# -----------------------------------
# OPERATIONS INTELLIGENCE
# -----------------------------------

with tab3:

    operations_chart = px.bar(
        operations_df,
        x="department",
        y="efficiency_score",
        color="department",
        title="Operational Efficiency"
    )

    operations_chart.update_layout(
        height=500
    )

    st.plotly_chart(
        operations_chart,
        use_container_width=True
    )

# -----------------------------------
# EMPLOYEE INSIGHTS
# -----------------------------------

with tab4:

    productivity_chart = px.scatter(
        filtered_employees,
        x="tasks_completed",
        y="sales_closed",
        size="productivity_score",
        color="department",
        title="Employee Productivity Analysis"
    )

    productivity_chart.update_layout(
        height=500
    )

    st.plotly_chart(
        productivity_chart,
        use_container_width=True
    )

# -----------------------------------
# AI PREDICTION ENGINE
# -----------------------------------

st.divider()

st.header(
    "AI Revenue Prediction Engine"
)

st.write(
    """
    Predict annual customer revenue using
    enterprise AI analytics.
    """
)

col1, col2 = st.columns(2)

with col1:

    deal_value = st.number_input(
        "Deal Value (£)",
        min_value=1000,
        value=50000
    )

    conversion_probability = st.slider(
        "Conversion Probability",
        1,
        100,
        60
    )

with col2:

    industry = st.selectbox(
        "Industry",
        customers_df["industry"].unique()
    )

st.metric(
    "AI Model Accuracy",
    f"{accuracy * 100:.1f}%"
)

if st.button(
    "Predict Customer Revenue"
):

    prediction = predict_revenue(
        deal_value,
        conversion_probability / 100,
        industry
    )

    st.success(
        f"Predicted Annual Revenue: £{prediction:,.0f}"
    )

    st.success(
        """
        AI Insight:

        Customers with higher conversion
        probability and larger deal sizes
        tend to generate stronger annual revenue.
        """
    )

# -----------------------------------
# AI REVENUE FORECASTING
# -----------------------------------

st.divider()

st.header(
    "AI Revenue Forecasting"
)

st.write(
    """
    Predict future enterprise revenue trends
    using forecasting analytics.
    """
)

forecast_df = revenue_df.copy()

forecast_df["month_number"] = np.arange(
    len(forecast_df)
)

X_forecast = forecast_df[
    ["month_number"]
]

y_forecast = forecast_df[
    "revenue_gbp"
]

from sklearn.linear_model import LinearRegression

forecast_model = LinearRegression()

forecast_model.fit(
    X_forecast,
    y_forecast
)

future_months = np.arange(
    len(forecast_df),
    len(forecast_df) + 6
).reshape(-1, 1)

future_predictions = (
    forecast_model.predict(
        future_months
    )
)

future_df = pd.DataFrame({
    "Future Month": [
        "Month 1",
        "Month 2",
        "Month 3",
        "Month 4",
        "Month 5",
        "Month 6"
    ],
    "Predicted Revenue": future_predictions
})

forecast_chart = px.line(
    future_df,
    x="Future Month",
    y="Predicted Revenue",
    markers=True,
    title="6 Month AI Revenue Forecast"
)

forecast_chart.update_layout(
    height=500
)

st.plotly_chart(
    forecast_chart,
    use_container_width=True
)

highest_prediction = (
    future_df["Predicted Revenue"].max()
)

st.success(
    f"""
    AI Forecast Insight:
    
    Projected peak revenue across the next
    six months may reach approximately
    £{highest_prediction:,.0f}.
    """
)

# -----------------------------------
# ENTERPRISE AI ASSISTANT
# -----------------------------------

st.divider()

st.header(
    "Ask Enterprise AI Assistant"
)

st.write(
    """
    Ask the AI assistant business questions
    about enterprise performance and insights.
    """
)

question = st.selectbox(
    "Select a Business Question",
    [
        "Which industry generates the highest revenue?",
        "Which city has the highest churn risk?",
        "Which department is most productive?",
        "What business area needs improvement?",
        "Which customers are highest value?",
        "What is the current AI prediction accuracy?"
    ]
)

if st.button(
    "Ask AI Assistant"
):

    if question == (
        "Which industry generates the highest revenue?"
    ):

        top_industry = (
            filtered_customers.groupby(
                "industry"
            )["annual_revenue_gbp"]
            .mean()
            .idxmax()
        )

        st.success(
            f"""
            Enterprise AI Response:
            
            {top_industry} currently generates
            the highest average customer revenue
            across the enterprise portfolio.
            """
        )

    elif question == (
        "Which city has the highest churn risk?"
    ):

        risk_city = (
            filtered_customers.groupby(
                "city"
            )["churn_risk"]
            .mean()
            .idxmax()
        )

        st.warning(
            f"""
            Enterprise AI Response:
            
            Customer churn risk is currently
            highest in {risk_city}.
            Additional customer retention
            strategies are recommended.
            """
        )

    elif question == (
        "Which department is most productive?"
    ):

        best_department = (
            filtered_employees.groupby(
                "department"
            )["productivity_score"]
            .mean()
            .idxmax()
        )

        st.info(
            f"""
            Enterprise AI Response:
            
            The {best_department} department
            demonstrates the strongest
            operational productivity levels.
            """
        )

    elif question == (
        "What business area needs improvement?"
    ):

        weak_area = (
            filtered_customers.groupby(
                "industry"
            )["customer_satisfaction"]
            .mean()
            .idxmin()
        )

        st.error(
            f"""
            Enterprise AI Response:
            
            Customer satisfaction levels are
            lowest within the {weak_area} sector.
            Improved engagement strategies
            are recommended.
            """
        )

    elif question == (
        "Which customers are highest value?"
    ):

        top_customers = (
            filtered_customers.sort_values(
                by="annual_revenue_gbp",
                ascending=False
            )
            .head(5)
        )

        st.dataframe(
            top_customers[
                [
                    "customer_name",
                    "industry",
                    "annual_revenue_gbp"
                ]
            ],
            use_container_width=True
        )

    elif question == (
        "What is the current AI prediction accuracy?"
    ):

        st.success(
            f"""
            Enterprise AI Response:
            
            Current machine learning prediction
            accuracy is {accuracy * 100:.1f}%.
            """
        )


# -----------------------------------
# OPENAI EXECUTIVE AI INSIGHTS
# -----------------------------------

st.divider()

st.header(
    "OpenAI Executive Insights"
)

st.write(
    """
    Generate AI powered executive business
    recommendations using enterprise data.
    """
)

if st.button(
    "Generate Executive AI Report"
):

    total_revenue_ai = (
        filtered_customers[
            "annual_revenue_gbp"
        ].sum()
    )

    avg_satisfaction_ai = (
        filtered_customers[
            "customer_satisfaction"
        ].mean()
    )

    avg_churn_ai = (
        filtered_customers[
            "churn_risk"
        ].mean() * 100
    )

    best_department_ai = (
        filtered_employees.groupby(
            "department"
        )["productivity_score"]
        .mean()
        .idxmax()
    )

    top_industry_ai = (
        filtered_customers.groupby(
            "industry"
        )["annual_revenue_gbp"]
        .mean()
        .idxmax()
    )

    prompt = f"""
    You are an enterprise AI strategy assistant.

    Analyze the following UK enterprise metrics
    and provide:

    1. Executive summary
    2. Key business risks
    3. Growth opportunities
    4. Strategic recommendations

    Data:

    Total Revenue:
    £{total_revenue_ai:,.0f}

    Average Customer Satisfaction:
    {avg_satisfaction_ai:.1f}%

    Average Churn Risk:
    {avg_churn_ai:.1f}%

    Best Performing Department:
    {best_department_ai}

    Highest Revenue Industry:
    {top_industry_ai}

    Keep the response concise,
    professional, and executive focused.
    """

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional "
                        "enterprise AI consultant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        ai_response = (
            response.choices[0]
            .message.content
        )

        st.success(
            "Executive AI Report Generated"
        )

        st.markdown(ai_response)

    except Exception as error:

        st.error(
            f"OpenAI API Error: {error}"
        )



# -----------------------------------
# DOWNLOAD REPORTS
# -----------------------------------

st.divider()

st.subheader(
    "Download Enterprise Reports"
)

csv = (
    filtered_customers.to_csv(
        index=False
    ).encode("utf-8")
)

st.download_button(
    label="Download Customer Intelligence Report",
    data=csv,
    file_name="customer_intelligence_report.csv",
    mime="text/csv"
)

# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    """
    Built with Streamlit, SQLite,
    Plotly, Pandas, and Scikit-learn
    """
)

