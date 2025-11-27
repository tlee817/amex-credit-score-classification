# Amex: Credit Score Classification

### 👥 **Team Members**

| Name          | GitHub Handle  | Contribution                                                             |
| ------------- | -------------- | ------------------------------------------------------------------------ |
|               | @              | Model evaluation, performance analysis, results interpretation           |
|               | @              | Model evaluation, performance analysis, results interpretation           |
|               | @              | Model evaluation, performance analysis, results interpretation           |
|               | @              | Model evaluation, performance analysis, results interpretation           |
|               | @              | Model evaluation, performance analysis, results interpretation           |
|               | @              | Model evaluation, performance analysis, results interpretation           |
| Shizuka Takao | @shizuka-takao | Data preprocessing, model training (XGBoost), implementing Streamlit App |

## 🎯 **Project Highlights**

- Developed a machine learning model using `[model type/technique]` to address `[challenge project task]`.
- Achieved `[key metric or result]`, demonstrating `[value or impact]` for `[host company]`.
- Generated actionable insights to inform business decisions at `[host company or stakeholders]`.
- Implemented `[specific methodology]` to address industry constraints or expectations.

## 🏗️ **Project Overview**

This project aims to develop a supervised machine learning model that classifies customers into credit score brackets using their historical credit and bank data. The main goal is to automate the credit score segmentation process, reducing manual work and ensuring consistent, data-driven assessments.

![GUI Demo](assets/demo_video.gif)

[Click here for full demo video](https://youtu.be/fZO_7D8GT_8)

### Disclaimer

All dataset records in this repository are synthetic and do not represent real individuals, accounts, or financial activity. Predictions are for demonstration only and should not be used for actual credit decisions.

### Project Components

- **Predict From Existing Data** : This page is for exploring credit scores of existing customers.

  Enter or pick a customer ID to:

  1. See a list of matching customers.
  2. Select one to v\*iew their monthly financial timeline.
  3. Generate a credit standing prediction (Poor / Standard / Good) for each month with probability indicators.

- **Predict From New Data** : Use this when evaluating a hypothetical or newly onboarded customer by filling out a short form (age, income, debts, counts of cards/loans, etc.).
- **ml_pipeline_notebook** : Consists of the machine learning pipeline from data preprocessing to model training & evaluation.

## 👩🏽‍💻 **Setup and Installation**

### Clone the Repository

To clone this repository and navigate into the project directory, run:

```bash
git clone
cd
```

### Installation

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

### Before Running Locally

#### 1. Download `test_clean.csv`

Download from Amex1A/Data in Google Drive:
https://drive.google.com/file/d/1sY2GjJEdTgpigA2lvhyi7ZwNUc-Jf1cA/view?usp=sharing

#### 2. Create a `data/` directory (if not present)

```bash
mkdir data
```

#### 3. Place the file in the directory

Move the downloaded file into:

```
project_root/data/test_clean.csv
```

### Run the Streamlit App

```bash
streamlit run app.py
```

## Troubleshooting: XGBoost on macOS

If you see an error like

1. Install libomp with Homebrew:

```bash
brew install libomp
```

2. Activate your project v"libxgboost.dylib could not be loaded" that references a missing `libomp.dylib`, macOS usually needs the OpenMP runtime installed. On macOS (Intel or Apple Silicon) the quickest fix is:
   irtualenv and verify XGBoost loads:

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

---

## 📊 **Data Exploration**

**You might consider describing the following (as applicable):**

- The dataset(s) used: origin, format, size, type of data
- Data exploration and preprocessing approaches
- Insights from your Exploratory Data Analysis (EDA)
- Challenges and assumptions when working with the dataset(s)

**Potential visualizations to include:**

- Plots, charts, heatmaps, feature visualizations, sample dataset images

---

## 🧠 **Model Development**

**You might consider describing the following (as applicable):**

- Model(s) used (e.g., CNN with transfer learning, regression models)
- Feature selection and Hyperparameter tuning strategies
- Training setup (e.g., % of data for training/validation, evaluation metric, baseline performance)

---

## 📈 **Results & Key Findings**

**You might consider describing the following (as applicable):**

- Performance metrics (e.g., Accuracy, F1 score, RMSE)
- How your model performed
- Insights from evaluating model fairness

**Potential visualizations to include:**

- Confusion matrix, precision-recall curve, feature importance plot, prediction distribution, outputs from fairness or explainability tools

---

## 🚀 **Next Steps**

**You might consider addressing the following (as applicable):**

- What are some of the limitations of your model?
- What would you do differently with more time/resources?
- What additional datasets or techniques would you explore?

---

## 📝 **License**

If applicable, indicate how your project can be used by others by specifying and linking to an open source license type (e.g., MIT, Apache 2.0). Make sure your Challenge Advisor approves of the selected license type.

**Example:**
This project is licensed under the MIT License.

---

## 📄 **References** (Optional but encouraged)

Cite relevant papers, articles, or resources that supported your project.

---

## 🙏 **Acknowledgements** (Optional but encouraged)

Thank your Challenge Advisor, host company representatives, TA, and others who supported your project.
