import streamlit as st

# BEFORE RUNNING LOCALLY:
# Download test_clean.csv from GDrive/Amex1A/Data and store in the data/ directory (create data directory if it doesn't exist)

st.set_page_config(layout="wide")

header_col1, header_col2, header_col3 = st.columns([1,2,1])

with header_col2:
    st.markdown(
        """<h1 style='text-align:center; margin-top: 5px;'>
            Credit Score Classification
        </h1>""",
        unsafe_allow_html=True
    )

    st.markdown(
        """<p style='text-align:center; font-size:18px; color:#666; margin-top:-10px;'>
            Machine Learning–Powered Credit Risk Prediction
        </p>""",
        unsafe_allow_html=True
    )

st.write("")

st.markdown(
    """
    <div style='text-align:center; max-width:700px; margin:auto; font-size:17px; color:#444;'>
        Welcome! This tool predicts a customer's credit score category using a trained 
        <b>XGBoost</b> model. Select an option below to begin.
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")
st.write("")

col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.markdown(
            "<div style='text-align:center'>"
            "<h3>📁 Predict From Existing Data</h3>"
            "<p>Search existing customers and predict their credit scores</p>"
            "</div>",
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.page_link("pages/Predict_From_Existing_Data.py", label="Go →")
with col2:
    with st.container(border=True):
        st.markdown(
            "<div style='text-align:center'>"
            "<h3>📝 Predict From New Data</h3>"
            "<p>Manually enter a new customer's financial information to predict credit score</p>"
            "</div>",
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.page_link("pages/Predict_From_New_Data.py", label="Go →")
