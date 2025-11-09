import os
import gdown
import joblib
import pandas as pd
import streamlit as st

# Google Drive IDs
FILE_ID_MODEL = "106e2YXB3MebGkndVCpJaqU7BYSfDMAN9"
FILE_ID_FEATS = "1OmP2n47KFjQ7iRMaRl6BN8GKXmVPkjfo"

# Local paths
MODEL_PATH = "assets/final_model.pkl"
FEAT_PATH  = "assets/final_features.csv"

def download_model():
    st.sidebar.title("Developer Controls")

    download_model = st.sidebar.checkbox(
        "Download latest model from Drive?",
        value=False
    )

    # Download only if user says so OR file doesn't exist
    if download_model or not os.path.exists(MODEL_PATH):
        st.warning("Downloading latest model from Google Drive…")
        gdown.download(f"https://drive.google.com/uc?id={FILE_ID_MODEL}", MODEL_PATH, quiet=True)
        gdown.download(f"https://drive.google.com/uc?id={FILE_ID_FEATS}", FEAT_PATH, quiet=True)

@st.cache_resource
def load_model_and_features():
    model = joblib.load(MODEL_PATH)
    selected_features = pd.read_csv(FEAT_PATH)["Feature"].tolist()
    return model, selected_features
