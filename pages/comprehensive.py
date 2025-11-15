import streamlit as st
import joblib
import numpy as np
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
    step=1000,
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

interest_rate = st.number_input(
    "Interest Rate (%)",
    min_value=0,
    max_value=100,
    value=10,
    step=1,
    help="Average interest rate applied across the customer's credit products."
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

changed_credit_limit = st.number_input(
    "Changed Credit Limit ($)",
    min_value=0,
    step=10,
    value=0,
    help="Change in the customer's credit limit."
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

credit_mix = st.selectbox(
    "Credit Mix",
    [
        "Credit_Mix_Unknown",
        "Credit_Mix_Good",
        "Credit_Mix_Standard",
        "Credit_Mix_Bad"
    ],
    help="Overall quality of the applicant's credit history."
)

loan_types = st.multiselect(
    "Select all applicable loan types:",
    ["Credit-Builder Loan", "Personal Loan", "Payday Loan", "Auto Loan"],
    help="Select all loan types currently held by the customer."
)

payment_min_amount = st.selectbox(
    "Payment of Minimum Amount",
    ["Yes", "No", "NM"],
    help="Indicates whether the customer pays at least the minimum amount due each month. 'NM' means not mentioned."
)
# Map selections to numeric values
payment_min_map = {"Yes": 1, "No": 0, "NM": np.nan}

num_bank_accounts = st.number_input(
    "Number of Bank Accounts",
    min_value=0,
    step=1,
    value=0,
    help="Total number of bank accounts the customer currently holds."
)

total_emi_per_month = st.number_input(
    "Total EMI per Month ($)",
    min_value=0.0,
    step=100.0,
    value=0.0,
    help="Total monthly EMI payments made by the customer."
)

delay_from_due_date = st.number_input(
    "Delay from Due Date (days)",
    min_value=0,
    step=1,
    value=0,
    help="Average number of days the customer delays payments beyond the due date."
)

monthly_salary_report_count = st.number_input(
    "Monthly Salary Report Count",
    min_value=0,
    step=1,
    value=0,
    help="Number of times the customer's salary is reported per month."
)

month_num = st.number_input(
    "Month (1–12)",
    min_value=1,
    max_value=12,
    step=1,
    value=1,
    help="Numeric month representation (1 for January, 12 for December)."
)
at_risk_flag = st.number_input(
    "At Risk Flag (0 = No, 1 = Yes)",
    min_value=0,
    max_value=1,
    step=1,
    value=0,
    help="Indicates whether the customer is currently considered at risk (1 = Yes, 0 = No)."
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
safe_set(row, "Interest_Rate", interest_rate)
safe_set(row, "Changed_Credit_Limit", changed_credit_limit)
safe_set(row, "Payment_of_Min_Amount", payment_min_map[payment_min_amount])
safe_set(row, "Num_Bank_Accounts", num_bank_accounts)
safe_set(row, "Total_EMI_per_month", total_emi_per_month)
safe_set(row, "Delay_from_due_date", delay_from_due_date)
safe_set(row, "Monthly_Salary_Report_Count", monthly_salary_report_count)
safe_set(row, "Month_Num", month_num)
safe_set(row, "At_Risk_Flag", at_risk_flag)

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

#------------------------------------
# Credit_mix dropdown
credit_mix_cols = [c for c in selected_features if c.startswith("Credit_Mix_")]
for col in credit_mix_cols:
    safe_set(row, col, 0)

# Set the chosen one to 1 directly
if credit_mix in credit_mix_cols:
    safe_set(row, credit_mix, 1)

#------------------------------------
# Loan Type
# One-hot encode selected loan types
loan_cols = [c for c in selected_features if c.endswith(" Loan")]

# Initialize all to 0
for col in loan_cols:
    safe_set(row, col, 0)

# Mark selected loans as 1
for loan in loan_types:
    if loan in loan_cols:
        safe_set(row, loan, 1)
#------------------------------------


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
        