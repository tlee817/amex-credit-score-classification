import streamlit as st
import joblib
import pandas as pd

# Load model and feature list
model = joblib.load('xgb_final_weighted.pkl')
selected_features = pd.read_csv("final_features_weighted.csv")["Feature"].tolist()
print("Features needed for model: ", selected_features)

# App Specifications
st.title("💳 Credit Score Classification App")
st.write("Enter customer details below to predict credit score standing (Good / Standard / Poor).")

# User input fields
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

num_delayed_payments = st.number_input(
    "Number of delayed payments",
    min_value=0,
    value=0,
    help="Total number of delayed payments recorded for the customer.",
)


# Build a single-row feature dict with zeros for all expected features
row = {feat: 0 for feat in selected_features}

# Fill numeric fields 
row["Num_Credit_Card"] = num_credit_cards
row["Num_of_Loan"] = num_loans
row["Num_of_Delayed_Payment"] = num_delayed_payments


# Occupation dropdown -> one-hot columns
occupation_cols = [c for c in selected_features if c.startswith("Occupation_")]
pretty_to_key = {c.replace("Occupation_", "").replace("_", " "): c for c in occupation_cols}
pretty_options = ["(none)"] + sorted(pretty_to_key.keys())
occ_choice = st.selectbox("Occupation", options=pretty_options, index=0)

# Set occupation one-hots
for k in occupation_cols:
    row[k] = 0
if occ_choice != "(none)":
    row[pretty_to_key[occ_choice]] = 1


# Prediction
if st.button("Predict"):
    st.info("Model prediction placeholder.")
