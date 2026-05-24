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
csv_path = os.path.join(BASE_DIR, "final.csv")

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError as e:
    raise FileNotFoundError(
        f"Could not open {csv_path}. cwd={os.getcwd()}"
    ) from e


# =========================================
# 3. DATA CLEANING
# =========================================

# Remove unwanted Excel columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Convert numeric columns stored as text
numeric_cols = [
    "Traffic",
    "AOV",
    "Base Price",
    "Unit Cost"
]

for col in numeric_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

# Ensure proper numeric types
df["Promo Depth %"] = pd.to_numeric(df["Promo Depth %"])
df["Conversion %"] = pd.to_numeric(df["Conversion %"])
df["Units Sold"] = pd.to_numeric(df["Units Sold"])


# =========================================
# 4. DATA VALIDATION
# =========================================

print("Dataset Preview:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nCleaned Dataset Info:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDataset Description:")
print(df.describe())


# =========================================
# 5. FEATURE SELECTION
# =========================================

features = [
    "Promo Depth %",
    "AOV",
    "Base Price",
    "Unit Cost"
]

target = "Units Sold"

X = df[features]
y = df[target]


# =========================================
# 6. TRAIN-TEST SPLIT
# =========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# =========================================
# 7. TRAIN LINEAR REGRESSION MODEL
# =========================================

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

y_pred_lr = lr_model.predict(X_test)

print("\n--- Linear Regression Performance ---")
print("R2 Score:", r2_score(y_test, y_pred_lr))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred_lr)))


# =========================================
# 8. TRAIN RANDOM FOREST MODEL
# =========================================

rf_model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)

print("\n--- Random Forest Performance ---")
print("R2 Score:", r2_score(y_test, y_pred_rf))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred_rf)))


# =========================================
# 9. DEFINE FINANCIAL CALCULATION
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
# 10. PROMO OPTIMISATION FUNCTION
# =========================================

def find_best_promo(row, model, features):

    promo_options = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30]

    best_profit = -np.inf
    best_promo = None

    for promo in promo_options:

        temp_row = row.copy()
        temp_row["Promo Depth %"] = promo

        # Build prediction row
        input_df = pd.DataFrame(
            [temp_row[features].values],
            columns=features
        )

        predicted_units = model.predict(input_df)[0]

        profit = calculate_profit(
            temp_row,
            predicted_units,
            promo
        )

        if profit > best_profit:
            best_profit = profit
            best_promo = promo

    return best_promo, best_profit


# =========================================
# 11. TEST PROMO OPTIMISATION
# =========================================

print("\n--- Promo Optimisation Results ---")

# Change model here if needed:
selected_model = rf_model
# selected_model = lr_model

for i in range(min(5, len(df))):

    row = df.iloc[i]

    best_promo, best_profit = find_best_promo(
        row,
        selected_model,
        features
    )

    print(f"\nSKU Index: {i}")
    print("SKU:", row["SKU"])
    print("Current Promo Depth:",
          row["Promo Depth %"])
    print("Best Promo Depth:",
          best_promo)
    print("Expected Profit:",
          round(best_profit, 2))
    

    print("\n--- Detailed Promo Debug ---")

row = df.iloc[0]   # AN201

print("\nSKU:", row["SKU"])
print("Current Promo:", row["Promo Depth %"])

promo_options = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30]

for promo in promo_options:

    temp_row = row.copy()
    temp_row["Promo Depth %"] = promo

    input_df = pd.DataFrame(
        [temp_row[features].values],
        columns=features
    )

    predicted_units = rf_model.predict(input_df)[0]

    realized_price = (
        temp_row["Base Price"] * (1 - promo)
    )

    revenue = predicted_units * realized_price

    cogs = (
        predicted_units *
        temp_row["Unit Cost"]
    )

    profit = revenue - cogs

    print(
        f"Promo={promo:.0%} | "
        f"Predicted Units={predicted_units:.2f} | "
        f"Price={realized_price:.2f} | "
        f"Profit={profit:.2f}"
    )


    sample_rows = [0, 100, 500, 1000, 2000]

for idx in sample_rows:

    row = df.iloc[idx]

    print("\n----------------------")
    print("SKU:", row["SKU"])

    for promo in [0, 0.05, 0.10, 0.15, 0.20, 0.30]:

        temp_row = row.copy()
        temp_row["Promo Depth %"] = promo

        input_df = pd.DataFrame(
            [temp_row[features].values],
            columns=features
        )

        predicted_units = rf_model.predict(input_df)[0]

        profit = calculate_profit(
            temp_row,
            predicted_units,
            promo
        )

        print(
            f"Promo={promo:.0%} | "
            f"Units={predicted_units:.2f} | "
            f"Profit={profit:.2f}"
        )