# Amex: Credit Score Classification

This project aims to develop a supervised machine learning model that classifies customers into credit score brackets using their historical credit and bank data. The main goal is to automate the credit score segmentation process, reducing manual work and ensuring consistent, data-driven assessments.

![GUI Demo](assets/demo_video.gif)

[Click here for full demo video](https://youtu.be/fZO_7D8GT_8)

## Disclaimer

All dataset records in this repository are synthetic and do not represent real individuals, accounts, or financial activity. Predictions are for demonstration only and should not be used for actual credit decisions.

## Overview

- **Predict From Existing Data** : This page is for exploring credit scores of existing customers.

  Enter or pick a customer ID to:

  1. See a list of matching customers.
  2. Select one to view their monthly financial timeline.
  3. Generate a credit standing prediction (Poor / Standard / Good) for each month with probability indicators.

- **Predict From New Data** : Use this when evaluating a hypothetical or newly onboarded customer by filling out a short form (age, income, debts, counts of cards/loans, etc.).
- **ml_pipeline_notebook** : Consists of the machine learning pipeline from data preprocessing to model training & evaluation.

---

## Requirements

- Python 3.9+
- Install dependencies after creating a virtual environment.

#### Setup (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### Setup (macOS / Linux Bash or zsh)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Before Running Locally

#### 1. Download `test_clean.csv`

Download from Amex1A/Data in Google Drive

#### 2. Create a `data/` directory (if not present)

```bash
mkdir data
```

#### 3. Place the file in the directory

Move the downloaded file into:

```
project_root/data/test_clean.csv
```

## Run the Streamlit App

```bash
streamlit run app.py
```

## Troubleshooting: XGBoost on macOS

If you see an error like "libxgboost.dylib could not be loaded" that references a missing `libomp.dylib`, macOS usually needs the OpenMP runtime installed. On macOS (Intel or Apple Silicon) the quickest fix is:

1. Install libomp with Homebrew:

```bash
brew install libomp
```

2. Activate your project virtualenv and verify XGBoost loads:

```bash
source .venv/bin/activate
python -c "import xgboost; print('xgboost', xgboost.__version__)"
```

If `brew` is not available, the alternative is to use a conda environment (conda installs OpenMP/compilers) or reinstall xgboost from a wheel that bundles runtimes. If problems persist, try:

```bash
pip uninstall -y xgboost
pip install --no-cache-dir xgboost
```

Add this section to help other developers who run into the same macOS XGBoost / libomp issue.
