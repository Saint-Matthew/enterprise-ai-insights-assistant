import sqlite3
import pandas as pd

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

connection = sqlite3.connect(
    "ai_enterprise.db"
)

# -----------------------------------
# LOAD DATASETS
# -----------------------------------

customers_df = pd.read_csv(
    "datasets/customers.csv"
)

employees_df = pd.read_csv(
    "datasets/employees.csv"
)

operations_df = pd.read_csv(
    "datasets/operations.csv"
)

sales_df = pd.read_csv(
    "datasets/sales.csv"
)

revenue_df = pd.read_csv(
    "datasets/revenue.csv"
)

# -----------------------------------
# SAVE TO DATABASE
# -----------------------------------

customers_df.to_sql(
    "customers",
    connection,
    if_exists="replace",
    index=False
)

employees_df.to_sql(
    "employees",
    connection,
    if_exists="replace",
    index=False
)

operations_df.to_sql(
    "operations",
    connection,
    if_exists="replace",
    index=False
)

sales_df.to_sql(
    "sales",
    connection,
    if_exists="replace",
    index=False
)

revenue_df.to_sql(
    "revenue",
    connection,
    if_exists="replace",
    index=False
)

connection.commit()

connection.close()

print("Enterprise AI database created successfully.")

