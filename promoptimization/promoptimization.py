# =========================================
# 1. IMPORT LIBRARIES
# =========================================

import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error


# =========================================
# 2. LOAD DATA
# =========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "promotional_data.csv")

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError as e:
    raise FileNotFoundError(f"Could not open {csv_path}. cwd={os.getcwd()}") from e

print("Dataset Preview:")
print(df.head())
print("\nDataset Info:")
print(df.info())
print("\nDataset Description:")
print(df.describe())    



# =========================================
# 3. FEATURE SELECTION
# =========================================

features = [
    "Promo Depth %",
    "Traffic",
    "Conversion %",
    "AOV",
    "Base Price",
    "Unit Cost"
]

target = "Units Sold"

X = df[features]
y = df[target]

# =========================================
# 4. TRAIN-TEST SPLIT
# =========================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================================
# 5. TRAIN LINEAR REGRESSION MODEL
# =========================================

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

y_pred_lr = lr_model.predict(X_test)

print("\n--- Linear Regression Performance ---")
print("R2 Score:", r2_score(y_test, y_pred_lr))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred_lr)))


# =========================================
# 6. TRAIN RANDOM FOREST MODEL
# =========================================

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)

print("\n--- Random Forest Performance ---")
print("R2 Score:", r2_score(y_test, y_pred_rf))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred_rf)))


# =========================================
# 7. DEFINE FINANCIAL CALCULATION
# =========================================

def calculate_profit(row, predicted_units, promo_depth):
    base_price = row["Base Price"]
    unit_cost = row["Unit Cost"]
    
    realized_price = base_price * (1 - promo_depth)
    revenue = predicted_units * realized_price
    cogs = predicted_units * unit_cost
    profit = revenue - cogs
    
    return profit


# =========================================
# 8. PROMO OPTIMISATION FUNCTION
# =========================================

def find_best_promo(row, model, features):
    promo_options = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30]

    best_profit = -np.inf
    best_promo = None

    for promo in promo_options:
        temp_row = row.copy()
        temp_row["Promo Depth %"] = promo

        # Build a 1-row DataFrame with correct columns
        input_df = pd.DataFrame([temp_row[features].values], columns=features)

        predicted_units = model.predict(input_df)[0]

        profit = calculate_profit(temp_row, predicted_units, promo)

        if profit > best_profit:
            best_profit = profit
            best_promo = promo

    return best_promo, best_profit


# =========================================
# 9. TEST OPTIMISATION ON SAMPLE DATA
# =========================================

print("\n--- Promo Optimisation Results ---")

for i in range(min(5, len(df))):
    
    row = df.iloc[i]
    
    best_promo, best_profit = find_best_promo(row, rf_model, features)
    
    print(f"\nSKU Index: {i}")
    print("Best Promo Depth:", best_promo)
    print("Expected Profit:", round(best_profit, 2))