import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score

# -----------------------------------
# LOAD DATA
# -----------------------------------

sales_df = pd.read_csv(
    "datasets/sales.csv"
)

customers_df = pd.read_csv(
    "datasets/customers.csv"
)

# -----------------------------------
# MERGE DATA
# -----------------------------------

merged_df = sales_df.merge(
    customers_df,
    on="customer_id"
)

# -----------------------------------
# ENCODERS
# -----------------------------------

industry_encoder = LabelEncoder()

merged_df["industry_encoded"] = (
    industry_encoder.fit_transform(
        merged_df["industry"]
    )
)

# -----------------------------------
# FEATURES
# -----------------------------------

X = merged_df[
    [
        "deal_value_gbp",
        "conversion_probability",
        "industry_encoded"
    ]
]

y = merged_df["annual_revenue_gbp"]

# -----------------------------------
# TRAIN TEST SPLIT
# -----------------------------------

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )
)

# -----------------------------------
# MODEL
# -----------------------------------

model = LinearRegression()

model.fit(X_train, y_train)

# -----------------------------------
# ACCURACY
# -----------------------------------

predictions = model.predict(X_test)

accuracy = r2_score(
    y_test,
    predictions
)

# -----------------------------------
# PREDICTION FUNCTION
# -----------------------------------

def predict_revenue(
    deal_value_gbp,
    conversion_probability,
    industry
):

    industry_value = (
        industry_encoder.transform(
            [industry]
        )[0]
    )

    prediction = model.predict([
        [
            deal_value_gbp,
            conversion_probability,
            industry_value
        ]
    ])

    return prediction[0]

