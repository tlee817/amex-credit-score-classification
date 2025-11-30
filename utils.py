import os
import gdown
import joblib
import pandas as pd
import streamlit as st


FILE_ID_MODEL = "1jsXLIOLQVsWAuryKWQUKcxvW2ig839lI"
FILE_ID_FEATS = "1OmP2n47KFjQ7iRMaRl6BN8GKXmVPkjfo"
MODEL_PATH = "assets/final_model.pkl"
FEAT_PATH  = "assets/final_features.csv"

def download_model():
    st.sidebar.title("Developer Controls")

    # Checkbox controls session state
    trigger = st.sidebar.checkbox(
        "Download latest model from Drive?",
        key="download_trigger",
        help="Re-fetch model weights and feature list from Google Drive"
    )

    # If button clicked OR files missing
    if trigger or not (os.path.exists(MODEL_PATH) and os.path.exists(FEAT_PATH)):
        with st.spinner("Downloading model & features..."):
            print("Downloading model.pkl…")
            gdown.download(f"https://drive.google.com/uc?id={FILE_ID_MODEL}", MODEL_PATH, quiet=True)
            print("Downloading final_features.csv…")
            gdown.download(f"https://drive.google.com/uc?id={FILE_ID_FEATS}", FEAT_PATH, quiet=True)

        st.sidebar.success("Model & features updated")
        st.success("Download complete")
        print("Download complete.")



@st.cache_resource
def load_model_and_features():
    model = joblib.load(MODEL_PATH)
    selected_features = pd.read_csv(FEAT_PATH)["Feature"].tolist()
    return model, selected_features
