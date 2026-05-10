import pandas as pd
import random
from faker import Faker

fake = Faker("en_GB")

# -----------------------------------
# SETTINGS
# -----------------------------------

NUM_CUSTOMERS = 120
NUM_EMPLOYEES = 40
NUM_SALES = 300
NUM_OPERATIONS = 250
NUM_REVENUE = 12

# -----------------------------------
# DATA LISTS
# -----------------------------------

industries = [
    "FinTech",
    "Retail",
    "Healthcare",
    "Logistics",
    "Real Estate",
    "Consulting",
    "SaaS",
    "E-commerce"
]

cities = [
    "London",
    "Manchester",
    "Birmingham",
    "Liverpool",
    "Leeds",
    "Bristol"
]

departments = [
    "Sales",
    "Marketing",
    "Operations",
    "Customer Success",
    "Data Analytics"
]

roles = [
    "Sales Executive",
    "Marketing Specialist",
    "Operations Manager",
    "CRM Analyst",
    "Customer Success Manager",
    "Business Intelligence Analyst"
]

sales_stages = [
    "Lead",
    "Qualified",
    "Proposal",
    "Negotiation",
    "Closed Won",
    "Closed Lost"
]

# -----------------------------------
# CUSTOMERS DATASET
# -----------------------------------

customers = []

for i in range(NUM_CUSTOMERS):

    customers.append({
        "customer_id": i + 1,
        "company_name": fake.company(),
        "industry": random.choice(industries),
        "city": random.choice(cities),
        "annual_revenue_gbp": random.randint(50000, 5000000),
        "customer_satisfaction": round(random.uniform(60, 100), 2),
        "churn_risk": round(random.uniform(0, 1), 2)
    })

customers_df = pd.DataFrame(customers)

customers_df.to_csv(
    "datasets/customers.csv",
    index=False
)

# -----------------------------------
# EMPLOYEES DATASET
# -----------------------------------

employees = []

for i in range(NUM_EMPLOYEES):

    employees.append({
        "employee_id": i + 1,
        "employee_name": fake.name(),
        "department": random.choice(departments),
        "role": random.choice(roles),
        "productivity_score": round(random.uniform(50, 100), 2),
        "tasks_completed": random.randint(20, 300),
        "sales_closed": random.randint(1, 50)
    })

employees_df = pd.DataFrame(employees)

employees_df.to_csv(
    "datasets/employees.csv",
    index=False
)

# -----------------------------------
# SALES DATASET
# -----------------------------------

sales = []

for i in range(NUM_SALES):

    sales.append({
        "sale_id": i + 1,
        "customer_id": random.randint(1, NUM_CUSTOMERS),
        "sales_stage": random.choice(sales_stages),
        "deal_value_gbp": random.randint(1000, 150000),
        "conversion_probability": round(random.uniform(0.1, 1.0), 2),
        "sales_rep_id": random.randint(1, NUM_EMPLOYEES)
    })

sales_df = pd.DataFrame(sales)

sales_df.to_csv(
    "datasets/sales.csv",
    index=False
)

# -----------------------------------
# OPERATIONS DATASET
# -----------------------------------

operations = []

for i in range(NUM_OPERATIONS):

    operations.append({
        "operation_id": i + 1,
        "department": random.choice(departments),
        "operational_cost_gbp": random.randint(1000, 50000),
        "efficiency_score": round(random.uniform(50, 100), 2),
        "issues_reported": random.randint(0, 20)
    })

operations_df = pd.DataFrame(operations)

operations_df.to_csv(
    "datasets/operations.csv",
    index=False
)

# -----------------------------------
# REVENUE DATASET
# -----------------------------------

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

revenue = []

for month in months:

    revenue_amount = random.randint(
        100000,
        1000000
    )

    expenses = random.randint(
        50000,
        500000
    )

    profit = revenue_amount - expenses

    revenue.append({
        "month": month,
        "revenue_gbp": revenue_amount,
        "expenses_gbp": expenses,
        "profit_gbp": profit
    })

revenue_df = pd.DataFrame(revenue)

revenue_df.to_csv(
    "datasets/revenue.csv",
    index=False
)

print("Enterprise AI datasets generated successfully.")

