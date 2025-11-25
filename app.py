import streamlit as st
import joblib
import pandas as pd
import gdown
import os

# BEFORE RUNNING LOCALLY:
# Download test_clean.csv from GDrive/Amex1A/Data and store in the data/ directory (create data directory if it doesn't exist)

# --- LANDING PAGE ---
st.title("💳 Credit Score Classification Main Page")
st.write("Select a page from the left sidebar.")


