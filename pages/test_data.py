import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import download_model, load_model_and_features

# ---  Session State ---
if "results" not in st.session_state:
    st.session_state.results = pd.DataFrame()
if "search_value" not in st.session_state:
    st.session_state.search_value = ""
if "view" not in st.session_state:
    st.session_state.view = "main"   # main or detail
if "selected_customer" not in st.session_state:
    st.session_state.selected_customer = None

# --- Load Data & Model ---
TEST_PATH = "data/test_clean.csv"
test_df = pd.read_csv(TEST_PATH)
download_model()
model, selected_features = load_model_and_features()



# --- Customer Info ---
if st.session_state.view == "detail":

    cid = st.session_state.selected_customer
    cust_df = test_df[test_df["Customer_ID"] == cid].copy()

    # Order months
    month_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]

    cust_df["Month"] = pd.Categorical(cust_df["Month"], categories=month_order, ordered=True)
    cust_df = cust_df.sort_values("Month")

    st.markdown(f"## Customer Financial Timeline: **{cid}**")
    
    # Card styling
    st.markdown("""
    <style>
    .metric-card {
        padding: 15px;
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Plot function
    def plot_card(column, title):
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
        st.plotly_chart(fig, use_container_width=True)

    # Layout - 2 rows, 3 charts each
    cols = st.columns(3)
    with cols[0]: 
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        plot_card("Credit_Utilization_Ratio", "Credit Utilization (%)")
        st.markdown("</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        plot_card("Num_Credit_Inquiries", "Credit Inquiries")
        st.markdown("</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        plot_card("Outstanding_Debt", "Outstanding Debt ($)")
        st.markdown("</div>", unsafe_allow_html=True)


    cols2 = st.columns(3)
    with cols2[0]:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        plot_card("Total_EMI_per_month", "Monthly EMI ($)")
        st.markdown("</div>", unsafe_allow_html=True)

    with cols2[1]:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        plot_card("Monthly_Balance", "Monthly Balance ($)")
        st.markdown("</div>", unsafe_allow_html=True)

    with cols2[2]:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        plot_card("Num_of_Delayed_Payment", "Delayed Payments")
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("### Raw Data")
    st.dataframe(cust_df, height=200)

    if st.button("⬅ Back"):
        st.session_state.view = "main"
        st.rerun()



# --- Main Logic ---
else :
    st.header("Banker Credit Review Dashboard")
    with st.form("search_form"):
        search = st.text_input("Search customers by ID, Name, or Age",
                            value=st.session_state.search_value)
        submitted = st.form_submit_button("Search")

    if submitted and search.strip():
        st.session_state.search_value = search
        st.session_state.results = test_df[
            test_df["Customer_ID"].astype(str).str.contains(search, case=False) |
            test_df["Name"].astype(str).str.contains(search, case=False) |
            test_df["Age"].astype(str).str.contains(search, case=False)
        ]

    results = st.session_state.results  

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
        print("DEBUG:", results.shape)


        if st.button("Predict"):
            print("predicting...")

            preds = []
            probs_list = []
            skip_cols = ["Name", "Customer_ID", "Month"]
            # Predict for each month row
            for idx, row_data in selected_row.iterrows():
                row = {feat: 0 for feat in selected_features}

                for col in selected_row.columns:
                    if col in row and col not in skip_cols:
                        row[col] = row_data[col]

                df = pd.DataFrame([row])[selected_features]
                print("DEBUG:", df.shape)

                pred = model.predict(df)[0]
                probs = model.predict_proba(df)[0]

                preds.append((row_data["Month"], pred))
                probs_list.append((row_data["Month"], probs))

            # Display month-wise results
            label_map = {0: "Poor", 1: "Standard", 2: "Good"}
            color_map = {"Poor":"#ff4d4d", "Standard":"#e6b800", "Good":"#4CAF50"}

            st.write("## Monthly Credit Score Predictions")

            cols = st.columns(3)  # 3 cards per row
            card_index = 0

            for (month, pred), (_, probs) in zip(preds, probs_list):

                with cols[card_index]:
                    pred_label = label_map[pred]

                    st.markdown(f"### {month}")
                    st.markdown(f"**Prediction:** <span style='color:{color_map[pred_label]};font-size:18px;'>{pred_label}</span>", unsafe_allow_html=True)

                    order = ["Poor", "Standard", "Good"]
                    prob_ordered = [probs[0], probs[1], probs[2]]
                    colors = ["#ff4d4d", "#e6b800", "#4CAF50"] 
                    fig = go.Figure(go.Bar(
                        x=order,
                        y=prob_ordered,
                        marker=dict(color=colors),
                        text=[f"{real:.1%}" for real in [probs[0], probs[1], probs[2]]],
                        textposition="outside"
                    ))

                    fig.update_layout(
                        height=240,
                        margin=dict(l=0, r=0, t=10, b=0),
                        yaxis=dict(range=[0,1], title="", tickformat=".0%"),
                        xaxis=dict(title="", tickangle=0),
                        showlegend=False,
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",)

                    st.plotly_chart(fig, use_container_width=True)


                card_index = (card_index + 1) % 3

        if st.button("More Info on Customer"):
            st.session_state.selected_customer = selected_id
            st.session_state.view = "detail"
            st.rerun()