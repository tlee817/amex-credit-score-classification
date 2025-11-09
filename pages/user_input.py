import streamlit as st
import joblib
import pandas as pd
import gdown
import os
from utils import download_model, load_model_and_features

# --- HELPER ----
# Ensure only features that are in selected_features are assigned a value
def safe_set(row_dict, feature_name, value):
    if feature_name in selected_features:
        row_dict[feature_name] = value


download_model()
model, selected_features = load_model_and_features()
st.write("Enter customer details below to predict credit score standing (Good / Standard / Poor).")
# User input fields
age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=30,
    help="Applicant's age."
)

salary = st.number_input(
    "Annual Income ($)",
    min_value=0,
    value=50000,
    step=0,
    help="Applicant's annual income before taxes."
)

num_credit_cards = st.number_input(
    "Number of credit cards",
    min_value=0,
    value=0,
    help="Total count of active credit cards the customer holds.",
)

num_loans = st.number_input(
    "Number of loans",
    min_value=0,
    value=0,
    help="Total count of loans currently in the customer's profile.",
)

debt = st.number_input(
    "Outstanding Debt ($)",
    min_value=0,
    value=0,
    step=500,
    help="Total outstanding debt across all loans and credit cards."
)


num_delayed_payments = st.number_input(
    "Number of delayed payments",
    min_value=0,
    value=0,
    help="Total number of delayed payments recorded for the customer.",
)

num_credit_inquiries = st.number_input(
    "Number of Credit Inquiries",
    min_value=0,
    step=1,
    help="Total credit applications the customer has made recently. Higher values may signal higher risk."
)

credit_history_age = st.number_input(
    "Credit History Age (in months)",
    min_value=0,
    step=1,
    help="Total months since the customer's first credit account."
)

payment_behaviour = st.selectbox(
    "Payment Behaviour",
    [
        "high_spent_medium_value_payments",
        "low_spent_small_value_payments",
        "high_spent_large_value_payments",
        "low_spent_large_value_payments",
        "low_spent_medium_value_payments",
        "high_spent_small_value_payments"
    ],
    help="Spending and repayment pattern derived from historical transactions."
)


# Build a single-row feature dict with zeros for all expected features
row = {feat: 0 for feat in selected_features}


# Fill numeric fields 
safe_set(row, "Age", age)
safe_set(row, "Annual_Income", salary)
safe_set(row, "Num_Credit_Card", num_credit_cards)
safe_set(row, "Num_of_Loan", num_loans)
safe_set(row, "Num_of_Delayed_Payment", num_delayed_payments)
safe_set(row, "Num_Credit_Inquiries", num_credit_inquiries)
safe_set(row, "Credit_History_Age", credit_history_age)
safe_set(row, "Outstanding_Debt", debt)


# Occupation dropdown -> one-hot columns
occupation_cols = [c for c in selected_features if c.startswith("Occupation_")]
pretty_to_key = {c.replace("Occupation_", "").replace("_", " "): c for c in occupation_cols}
pretty_options = ["(none)"] + sorted(pretty_to_key.keys())
occ_choice = st.selectbox("Occupation", options=pretty_options, index=0)

# Set occupation one-hots
for k in occupation_cols:
    safe_set(row, k, 0)
if occ_choice != "(none)":
    safe_set(row, pretty_to_key[occ_choice], 1)

# encode payment behavior
payment_cols = [c for c in selected_features if c.startswith("Payment_Behaviour_")]
for k in payment_cols:
    safe_set(row, k, 0)
behaviour_col = "Payment_Behaviour_" + payment_behaviour
if behaviour_col in payment_cols:
    safe_set(row, behaviour_col, 1)

# Prediction
if st.button("Predict"):
    df = pd.DataFrame([row])
    df_ordered = df[selected_features]

    print("\n--- BEFORE REORDERING ---")
    print(list(df.columns))
    print("\n--- AFTER REORDERING ---")
    print(list(df_ordered.columns))
    print(f"\nShape: {df_ordered.shape}") # expected (1, 39)

    pred_class = model.predict(df)[0]
    label_map = {
    0: "Poor",
    1: "Standard",
    2: "Good"}
    pred_label = label_map[pred_class]

    pred_prob = model.predict_proba(df_ordered)[0]
    classes = ["Poor", "Standard", "Good"]
    probabilities = {classes[i]: pred_prob[i] for i in range(len(classes))}

    st.success(f"Predicted Credit Category: {pred_label}")
    st.write("### Confidence Breakdown")
    for cls, p in probabilities.items():
        st.write(f"**{cls}:** {p:.2%}")
        st.progress(float(p))
