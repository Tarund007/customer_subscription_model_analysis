"""
ml_model_training.py
--------------------
Trains Random Forest and Logistic Regression classification models on preprocessed customer data,
evaluates ROC-AUC performance, assigns propensity tiers, and exports prediction outputs.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report
import os

def train_propensity_models(cleaned_filepath="cleaned_customer_shopping.csv", raw_filepath="customer_shopping_behavior.csv"):
    print("[-] Loading data for modeling...")
    if not os.path.exists(cleaned_filepath):
        raise FileNotFoundError(f"Cleaned dataset not found at {cleaned_filepath}. Run data_preprocessing.py first.")
    
    df_encoded = pd.read_csv(cleaned_filepath)
    df_raw = pd.read_csv(raw_filepath) # Retain raw columns for easy dashboard reporting

    # Define Feature Matrix (X) and Target Vector (y)
    # Drop target and original text columns if present in encoded df
    drop_cols = ['Target', 'Subscription Status', 'Customer ID', 'Item Purchased']
    drop_cols = [c for c in drop_cols if c in df_encoded.columns]
    
    X = df_encoded.drop(columns=drop_cols)
    y = df_encoded['Target']

    # Stratified 80/20 Train-Test Split (preserving 27% positive class ratio)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"[-] Training set size: {X_train.shape[0]} rows | Test set size: {X_test.shape[0]} rows (780 test samples)")

    # Feature Scaling for Logistic Regression
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 1. Train Random Forest Classifier
    print("[-] Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_preds_proba = rf_model.predict_proba(X_test)[:, 1]
    rf_roc_auc = roc_auc_score(y_test, rf_preds_proba)
    print(f"    Random Forest ROC-AUC Score: {rf_roc_auc:.4f}")

    # 2. Train Logistic Regression
    print("[-] Training Logistic Regression Classifier...")
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train_scaled, y_train)
    lr_preds_proba = lr_model.predict_proba(X_test_scaled)[:, 1]
    lr_roc_auc = roc_auc_score(y_test, lr_preds_proba)
    print(f"    Logistic Regression ROC-AUC Score: {lr_roc_auc:.4f}")

    # Select best model predictions (Random Forest or ensemble) for operational deployment
    test_indices = X_test.index
    results_df = df_raw.loc[test_indices].copy()
    results_df['Subscription_Probability'] = rf_preds_proba

    # 3. Assign Propensity Tiers based on probability thresholds
    # High: Top intent tier, Medium: Moderate, Low: Low intent
    def assign_propensity_tier(prob):
        if prob >= 0.65:
            return 'High'
        elif prob >= 0.40:
            return 'Medium'
        else:
            return 'Low'

    results_df['Propensity_Tier'] = results_df['Subscription_Probability'].apply(assign_propensity_tier)
    
    print("\n[-] Propensity Tier Distribution in Test Cohort:")
    print(results_df['Propensity_Tier'].value_counts())

    # 4. Export Final Predictions for Power BI & PostgreSQL
    output_filepath = "customer_subscription_predictions.csv"
    results_df.to_csv(output_filepath, index=False)
    print(f"\n[+] Model training & export complete! Predictions saved to '{output_filepath}'.")

    return results_df

if __name__ == "__main__":
    train_propensity_models()
