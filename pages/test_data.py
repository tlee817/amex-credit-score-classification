import streamlit as st
import pandas as pd
from utils import download_model, load_model_and_features

st.header("Banker Credit Review Dashboard")

# Load data
TEST_PATH = "data/test_clean.csv"
test_df = pd.read_csv(TEST_PATH)

# Download + load model
download_model()
model, selected_features = load_model_and_features()

# Search form
with st.form("search_form"):
    search = st.text_input("Search customers by ID, Name, or Age")
    submitted = st.form_submit_button("Search")

# Handle search results
if submitted and search.strip():
    results = test_df[
        test_df["Customer_ID"].astype(str).str.contains(search, case=False) |
        test_df["Name"].astype(str).str.contains(search, case=False) |
        test_df["Age"].astype(str).str.contains(search, case=False)
    ]
else:
    results = pd.DataFrame()

# Display results
if results.empty:
    st.warning("No results")
else:
    st.dataframe(results[["Customer_ID", "Month", "Name","Age"]])
    unique_customers = results["Customer_ID"].unique()

    selected_id = st.selectbox(
        "Select Customer ID to predict",
        options=unique_customers
    )

    selected_row = results[results["Customer_ID"] == selected_id]

    if st.button("Predict Selected Customer"):
        # Prepare row for model
        row = {feat: 0 for feat in selected_features}

        for col in selected_row.columns:
            if col in row:
                row[col] = selected_row.iloc[0][col]

        df = pd.DataFrame([row])[selected_features]

        pred = model.predict(df)[0]
        probs = model.predict_proba(df)[0]

        label_map = {0: "Poor", 1: "Standard", 2: "Good"}

        st.success(f"Credit Status: **{label_map[pred]}**")

        st.write("### Probability Breakdown")
        for cls, p in zip(["Poor","Standard","Good"], probs):
            st.write(f"{cls}: {p:.2%}")
            st.progress(float(p))
