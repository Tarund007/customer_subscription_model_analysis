# Subscription Conversion Propensity Model & Growth Analytics Dashboard

An end-to-end Product Analytics project that bridges data engineering, machine learning classification, relational databases, and business intelligence. This project predicts customer subscription propensity from e-commerce transaction records and operationalizes the insights into an executive-ready Power BI dashboard for growth marketing teams.

---

## 📌 Project Overview

In modern digital subscription and e-commerce platforms, maximizing lifetime value through subscription upgrades is critical. Traditional descriptive reporting tells you *what* happened in the past, but predictive analytics tells you *who* to target right now. 

This project implements a complete 4-stage data pipeline:
1. **Data Preparation & Cleaning:** Ingesting and preprocessing 3,900 customer shopping records in Python.
2. **Machine Learning Classification:** Training Random Forest and Logistic Regression models (achieving an ROC-AUC of **0.90–0.91**) to score customer subscription probability.
3. **Database Integration:** Storing transaction data and prediction outputs in a relational **PostgreSQL** database.
4. **Business Intelligence:** Designing an interactive **Power BI** executive dashboard featuring user segmentation, behavioral drivers, and a prioritized outreach list for growth marketing.

---

## 🏗️ Technical Architecture & Tech Stack

```
[ Raw CSV Data ] 
       │
       ▼
[ Python / Pandas / Scikit-Learn ] ──► Data Cleaning, Feature Engineering & ML Models (~0.90 ROC-AUC)
       │
       ▼
[ PostgreSQL / pgAdmin 4 ] ────────► Relational Storage & Analytical SQL Queries
       │
       ▼
[ Power BI Dashboard ] ────────────► Executive UI, Slicers, Donut Charts, & Actionable Target Table
```

* **Programming Language:** Python 3.x
* **Data Processing & ML:** Pandas, NumPy, Scikit-Learn (Random Forest Classifier, Logistic Regression, StandardScaler)
* **Database & SQL:** PostgreSQL, pgAdmin 4
* **Visualization & BI:** Power BI Desktop (DAX, Custom Conditional Formatting)
* **Presentation & Documentation:** Gamma (Case Study Deck), Microsoft Word (Technical & Interview Handbooks)

---

## 🔄 End-to-End Data Pipeline

### Stage 1: Data Preprocessing & Cleaning (Python)
* Loaded 3,900 customer records.
* Imputed 37 missing values in the `Review Rating` column using category-median imputation to preserve transaction data.
* Handled feature redundancy by removing redundant categorical mappings (`Promo Code Used`).
* Applied **One-Hot Encoding** (`pd.get_dummies`) on categorical attributes (`Gender`, `Category`, `Shipping Type`, `Payment Method`, `Color`).
* Created a binary target variable (`Subscription Status`: Yes/No, resulting in a ~27% positive class ratio).

### Stage 2: Machine Learning Modeling (Scikit-Learn)
* Performed an 80/20 stratified train-test split (yielding 780 test samples) to preserve class distribution.
* **Random Forest Classifier:** Captured complex non-linear feature interactions and evaluated feature importances.
* **Logistic Regression:** Trained on scaled data (`StandardScaler`) to inspect direct model coefficients and directional impact.
* **Model Performance:** Evaluated via **ROC-AUC** due to class imbalance, achieving an exceptional score of **0.90 to 0.91**.

### Stage 3: Database Integration & Storage (PostgreSQL)
* Structured relational tables in PostgreSQL to ingest raw transactions and model prediction outputs (`customer_subscription_predictions.csv`).
* Authored analytical queries to isolate high-intent non-subscribers and aggregate conversion probabilities by fulfillment type.

### Stage 4: Executive Dashboard (Power BI)
* Designed a professional dark-teal theme dashboard featuring:
  * **Interactive Slicers:** Dynamic filtering by `Subscription Status`, `Category`, and `Propensity Tier`.
  * **User Segmentation Donut Chart:** Visualizing the 780-test cohort across Low (60.13%), Medium (34.10%), and High (5.77% / 45 users) propensity tiers.
  * **Behavioral Bar Chart:** Highlighting that Express Shipping and Store Pickup users exhibit higher conversion intent (~0.27–0.28 vs. ~0.19 for Standard Shipping).
  * **Tier Health KPI Cards:** Displaying volume counts, percentage shares, and historical engagement (~28.38 previous purchases for high-intent users).
  * **Actionable Growth Target List:** An operational data table filtering for high-propensity non-subscribers sorted by conversion probability.

---

## 💻 Database & SQL Integration

Relational tables and queries used to manage predictions and drive marketing campaigns:

```sql
-- 1. Table Schema for Predictions
CREATE TABLE customer_predictions (
    customer_id SERIAL PRIMARY KEY,
    age INT,
    gender VARCHAR(50),
    category VARCHAR(50),
    item_purchased VARCHAR(100),
    purchase_amount NUMERIC,
    shipping_type VARCHAR(50),
    subscription_status VARCHAR(10),
    previous_purchases INT,
    subscription_probability NUMERIC,
    propensity_tier VARCHAR(50)
);

-- 2. Extracting High-Intent Non-Subscribers for Growth Marketing
SELECT 
    age,
    gender,
    category,
    purchase_amount,
    subscription_probability
FROM customer_predictions
WHERE subscription_status = 'No' 
  AND propensity_tier = 'High'
ORDER BY subscription_probability DESC;

-- 3. Aggregating Average Conversion Probability by Fulfillment Method
SELECT 
    shipping_type,
    COUNT(*) AS total_customers,
    ROUND(AVG(subscription_probability), 4) AS avg_probability
FROM customer_predictions
GROUP BY shipping_type
ORDER BY avg_probability DESC;
```

---

## 📈 Strategic Business Impact & Recommendations

1. **Precision Outreach over Broad Discounting:** With only 45 high-propensity non-subscribers identified in the test cohort (5.77%), broad marketing campaigns are inefficient. Budget should be concentrated exclusively on high-intent targets.
2. **Leverage Fulfillment Behavior:** Express shipping and store pickup users show higher conversion intent (~0.28), indicating that subscription upsell prompts should be integrated directly into fast-shipping checkout flows.
3. **Repeat Buyer Activation:** High-propensity customers average ~28 previous purchases, proving they are loyal brand advocates who simply require a tailored subscription incentive (such as free shipping or exclusive member perks) to convert.

---

## 📂 Repository Structure
```text
├── data/
│   ├── customer_shopping_behavior.csv
│   └── customer_subscription_predictions.csv
├── scripts/
│   ├── data_preprocessing.py
│   └── ml_model_training.py
├── sql/
│   └── postgresql_queries.sql
├── dashboard/
│   └── subscription_propensity_dashboard.pbix
└── docs/
    ├── Subscription_Conversion_Propensity_Complete_Handbook.docx
    └── Candidate_Interview_Masterclass_Guide.docx
```

---

## 👤 Author
Built as a professional portfolio-grade product analytics project demonstrating full-stack competencies in Python machine learning, PostgreSQL database engineering, and executive Power BI business intelligence.
