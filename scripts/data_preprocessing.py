"""
data_preprocessing.py
---------------------
Handles loading the raw customer shopping behavior dataset, cleaning missing values,
encoding categorical features, and preparing the dataframe for machine learning.
"""

import pandas as pd
import numpy as np
import os

def load_and_preprocess_data(filepath="customer_shopping_behavior.csv"):
    print("[-] Loading raw dataset from:", filepath)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find dataset at {filepath}. Please ensure it is in the correct directory.")
    
    df = pd.read_csv(filepath)
    print(f"    Raw dataset shape: {df.shape}")

    # 1. Handle Missing Values in 'Review Rating' via Category-Median Imputation
    if 'Review Rating' in df.columns and 'Category' in df.columns:
        missing_count = df['Review Rating'].isnull().sum()
        if missing_count > 0:
            print(f"[-] Imputing {missing_count} missing review ratings using category medians...")
            df['Review Rating'] = df['Review Rating'].fillna(
                df.groupby('Category')['Review Rating'].transform('median')
            )

    # 2. Drop Redundant or Unnecessary Columns
    # 'Promo Code Used' often mirrors 'Discount Applied'
    if 'Promo Code Used' in df.columns:
        df = df.drop(columns=['Promo Code Used'])
        print("[-] Dropped redundant column: 'Promo Code Used'")

    # 3. Standardize Target Variable ('Subscription Status' -> Binary 0/1)
    if 'Subscription Status' in df.columns:
        df['Target'] = df['Subscription Status'].apply(lambda x: 1 if str(x).strip().lower() in ['yes', 'true', '1'] else 0)
    else:
        raise ValueError("Target column 'Subscription Status' not found in dataset.")

    # 4. One-Hot Encoding for Categorical Features
    categorical_cols = ['Gender', 'Category', 'Shipping Type', 'Payment Method', 'Location', 'Size', 'Color', 'Season', 'Frequency of Purchases']
    categorical_cols = [col for col in categorical_cols if col in df.columns]
    
    print(f"[-] One-hot encoding categorical features: {categorical_cols}")
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # 5. Export cleaned dataset
    output_path = "cleaned_customer_shopping.csv"
    df_encoded.to_csv(output_path, index=False)
    print(f"[+] Preprocessing complete! Cleaned data saved to {output_path}. Shape: {df_encoded.shape}")
    
    return df, df_encoded

if __name__ == "__main__":
    load_and_preprocess_data()
