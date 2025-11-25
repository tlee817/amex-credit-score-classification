import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import download_model, load_model_and_features

TEST_PATH = "data/test_clean.csv"
LABEL_MAP = {0: "Poor", 1: "Standard", 2: "Good"}
COLOR_MAP = {"Poor": "#ff4d4d", "Standard": "#e6b800", "Good": "#4CAF50"}

# --- HELPER FUNCTIONS ---
def order_month(df: pd.DataFrame, customer_id: str) -> pd.DataFrame:
    month_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    out = df[df["Customer_ID"] == customer_id].copy()
    out["Month"] = pd.Categorical(out["Month"], categories=month_order, ordered=True)
    return out.sort_values("Month")

def plot_card(cust_df: pd.DataFrame, column: str, title: str):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=cust_df["Month"],
            y=cust_df[column],
            mode="lines+markers",
            line=dict(color="#1E88E5", width=3),
            marker=dict(size=9, color="#1E88E5"),
            hovertemplate=f"{title}<br>%{{x}}: %{{y}}<extra></extra>"
        )
    )
    fig.update_layout(
        title=title,
        height=260,
        margin=dict(l=10,r=10,t=40,b=10),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.3)", title=""),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    # Add a unique key per card based on the title
    st.plotly_chart(fig, use_container_width=True, key=f"card_{title}")

def render_search_form():
    with st.form("search_form"):
        search = st.text_input("Search customers by ID or Name", value=st.session_state.search_value)
        submitted = st.form_submit_button("Search")
    return search, submitted

def update_results_on_submit(test_df: pd.DataFrame, search: str, submitted: bool) -> pd.DataFrame:
    if submitted and search.strip():
        st.session_state.search_value = search
        st.session_state.results = test_df[
            test_df["Customer_ID"].astype(str).str.contains(search, case=False) |
            test_df["Name"].astype(str).str.contains(search, case=False)
        ]
    return st.session_state.results

def select_customer(results: pd.DataFrame):
    if results.empty:
        st.warning("No results")
        return None, None
    st.dataframe(results[["Customer_ID", "Month", "Name","Age"]])
    selected_id = st.selectbox("Select Customer ID to predict", options=results["Customer_ID"].unique())
    return selected_id, results[results["Customer_ID"] == selected_id]

def predict_monthly(selected_row: pd.DataFrame, model, selected_features: list[str]):
    preds, probs_list = [], []
    skip_cols = ["Name", "Customer_ID", "Month"]
    for _, row_data in selected_row.iterrows():
        row = {feat: 0 for feat in selected_features}
        for col in selected_row.columns:
            if col in row and col not in skip_cols:
                row[col] = row_data[col]
        df = pd.DataFrame([row])[selected_features]
        pred = model.predict(df)[0]
        probs = model.predict_proba(df)[0]
        preds.append((row_data["Month"], pred))
        probs_list.append((row_data["Month"], probs))
    return preds, probs_list

def render_prediction_cards(preds, probs_list):
    st.write("## Monthly Credit Score Predictions")
    cols, card_index = st.columns(3), 0
    for (month, pred), (_, probs) in zip(preds, probs_list):
        with cols[card_index]:
            pred_label = LABEL_MAP[pred]
            st.markdown(f"### {month}")
            st.markdown(f"**Prediction:** <span style='color:{COLOR_MAP[pred_label]};font-size:18px;'>{pred_label}</span>",
                        unsafe_allow_html=True)
            order = ["Poor", "Standard", "Good"]
            prob_ordered = [probs[0], probs[1], probs[2]]
            colors = [COLOR_MAP[o] for o in order]
            fig = go.Figure(go.Bar(
                x=order, y=prob_ordered, marker=dict(color=colors),
                text=[f"{p:.1%}" for p in prob_ordered], textposition="outside"
            ))
            fig.update_layout(
                height=240, margin=dict(l=0, r=0, t=10, b=0),
                yaxis=dict(range=[0,1], title="", tickformat=".0%"),
                xaxis=dict(title="", tickangle=0), showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            # Add a unique key per month for prediction bar charts
            st.plotly_chart(fig, use_container_width=True, key=f"pred_bar_{month}")
        card_index = (card_index + 1) % 3

# --- MAIN LOGIC ---
test_df = pd.read_csv(TEST_PATH)
download_model()
model, selected_features = load_model_and_features()

if "results" not in st.session_state:
    st.session_state.results = pd.DataFrame()
if "search_value" not in st.session_state:
    st.session_state.search_value = ""
if "view" not in st.session_state:
    st.session_state.view = "main"   # main or detail
if "selected_customer" not in st.session_state:
    st.session_state.selected_customer = None

# Customer Info Page
if st.session_state.view == "detail":
    cid = st.session_state.selected_customer
    st.markdown(f"## Customer Financial Timeline: **{cid}**")
    cust_df = order_month(test_df, cid)

    cols = st.columns(3)
    with cols[0]: 
        plot_card(cust_df, "Credit_Utilization_Ratio", "Credit Utilization (%)")  
    with cols[1]:
        plot_card(cust_df, "Num_Credit_Inquiries", "Credit Inquiries") 
    with cols[2]:
        plot_card(cust_df, "Outstanding_Debt", "Outstanding Debt ($)")  

    cols2 = st.columns(3)
    with cols2[0]:
        plot_card(cust_df, "Total_EMI_per_month", "Monthly EMI ($)")  
    with cols2[1]:
        plot_card(cust_df, "Monthly_Balance", "Monthly Balance ($)")
    with cols2[2]:
        plot_card(cust_df, "Num_of_Delayed_Payment", "Delayed Payments") 

    st.write("### Raw Data")
    st.dataframe(cust_df, height=200)

    if st.button("⬅ Back"):
        st.session_state.view = "main"
        st.rerun()

# Search & Predict Page
else :
    st.header("Credit Review Dashboard")
    search, submitted = render_search_form()
    results = update_results_on_submit(test_df, search, submitted)
    selected_id, selected_row = select_customer(results)
    if selected_row is not None and st.button("Predict"):
        preds, probs_list = predict_monthly(selected_row, model, selected_features)
        render_prediction_cards(preds, probs_list)
    if selected_row is not None and st.button("More Info on Customer"):
        st.session_state.selected_customer = selected_id
        st.session_state.view = "detail"
        st.rerun()