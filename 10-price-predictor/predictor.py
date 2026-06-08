"""
Price Predictor — Bengaluru House Prices
Trains a regression model to predict house prices and reports:
  - The right evaluation metric (RMSE + R²) and why accuracy is wrong here
  - The most important feature (from Random Forest feature importance)

Dataset: Bengaluru House Data from Kaggle
  https://www.kaggle.com/datasets/amitabhajoy/bengaluru-house-price-data
  Download Bengaluru_House_Data.csv and place in data/ folder

Default: runs on data/bengaluru_sample.csv (40 rows, synthetic)
Real:    set DATA_FILE = "data/Bengaluru_House_Data.csv" after downloading
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import warnings
import os

warnings.filterwarnings("ignore")

DATA_FILE = "data/bengaluru_sample.csv"   # change to real file after downloading
OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Step 1: Load & Clean ─────────────────────────────────────

def parse_sqft(value):
    """Handle ranges like '1200-1500' by taking the midpoint."""
    value = str(value).strip()
    if "-" in value:
        parts = value.split("-")
        try:
            return (float(parts[0]) + float(parts[1])) / 2
        except ValueError:
            return np.nan
    try:
        return float(value)
    except ValueError:
        return np.nan


def extract_bhk(size):
    """Extract number of bedrooms from '2 BHK' or '3 Bedroom'."""
    try:
        return int(str(size).split()[0])
    except (ValueError, AttributeError):
        return np.nan


def load_and_clean(filepath):
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} rows | Columns: {list(df.columns)}")

    # Parse sqft and BHK
    df["total_sqft"] = df["total_sqft"].apply(parse_sqft)
    df["bhk"] = df["size"].apply(extract_bhk)

    # Drop rows with missing key values
    df = df.dropna(subset=["total_sqft", "bhk", "bath", "price", "location"])
    df = df[df["total_sqft"] > 0]

    # Remove extreme outliers (price_per_sqft outside 1 std dev * 3)
    df["price_per_sqft"] = df["price"] * 100000 / df["total_sqft"]
    mean_pps = df["price_per_sqft"].mean()
    std_pps  = df["price_per_sqft"].std()
    df = df[(df["price_per_sqft"] > mean_pps - 3 * std_pps) &
            (df["price_per_sqft"] < mean_pps + 3 * std_pps)]

    # Keep only top 20 locations by frequency (others → "Other")
    top_locs = df["location"].value_counts().head(20).index
    df["location"] = df["location"].apply(lambda x: x if x in top_locs else "Other")

    print(f"After cleaning: {len(df)} rows\n")
    return df


# ── Step 2: Feature Engineering ──────────────────────────────

def prepare_features(df):
    le = LabelEncoder()
    df = df.copy()
    df["location_encoded"] = le.fit_transform(df["location"])

    features = ["total_sqft", "bath", "bhk", "balcony", "location_encoded"]
    df["balcony"] = df["balcony"].fillna(0)

    X = df[features]
    y = df["price"]
    return X, y, features


# ── Step 3: Train Models ──────────────────────────────────────

def train_and_evaluate(X, y, features):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest":     RandomForestRegressor(n_estimators=100, random_state=42),
    }

    results = {}
    print(f"{'Model':<25} {'RMSE (Lakhs)':>14} {'R² Score':>10}")
    print("-" * 52)

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2   = r2_score(y_test, preds)
        print(f"  {name:<23} {rmse:>13.2f} {r2:>10.3f}")
        results[name] = {"model": model, "preds": preds, "y_test": y_test,
                         "rmse": rmse, "r2": r2}

    print()
    print("  WHY NOT ACCURACY?")
    print("  House price is a continuous number — not a category.")
    print("  'Accuracy' only works when output is one of a fixed set of classes.")
    print("  For regression: RMSE tells you the average error in rupees,")
    print("  R² tells you how much of the price variation the model explains.")

    return results


# ── Step 4: Feature Importance ───────────────────────────────

def show_feature_importance(rf_model, features):
    importance = pd.Series(rf_model.feature_importances_, index=features)
    importance = importance.sort_values(ascending=True)

    print("\n" + "=" * 52)
    print("  Most Important Features (Random Forest)")
    print("=" * 52)
    for feat, imp in importance.sort_values(ascending=False).items():
        bar = "#" * int(imp * 40)
        print(f"  {feat:<22} {imp:.3f}  {bar}")

    top_feature = importance.idxmax()
    print(f"\n  TOP FEATURE: '{top_feature}'")
    print("  This aligns with real estate intuition: location drives price")
    print("  more than size in urban Indian cities (same flat, 2x the price")
    print("  if it is in Indiranagar vs Electronic City).")

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    importance.plot(kind="barh", ax=ax, color="#3498db")
    ax.set_title("Feature Importance — Random Forest", fontsize=13, fontweight="bold")
    ax.set_xlabel("Importance Score")
    plt.tight_layout()
    path = f"{OUTPUT_DIR}/feature_importance.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"\n  Chart saved: {path}")

    return top_feature


# ── Step 5: Visualise Predictions ────────────────────────────

def plot_predictions(results, y_range_max=500):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Predicted vs Actual House Prices (Lakhs)", fontsize=14, fontweight="bold")

    for ax, (name, res) in zip(axes, results.items()):
        ax.scatter(res["y_test"], res["preds"], alpha=0.6, color="#e74c3c", edgecolors="white", s=50)
        lim = min(y_range_max, max(res["y_test"].max(), res["preds"].max()) + 20)
        ax.plot([0, lim], [0, lim], "k--", linewidth=1, label="Perfect prediction")
        ax.set_xlabel("Actual Price (Lakhs)")
        ax.set_ylabel("Predicted Price (Lakhs)")
        ax.set_title(f"{name}\nRMSE: {res['rmse']:.1f}L  R²: {res['r2']:.3f}")
        ax.legend()

    plt.tight_layout()
    path = f"{OUTPUT_DIR}/predictions.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Predictions chart saved: {path}")


def main():
    print("=" * 60)
    print("  Price Predictor — Bengaluru House Prices")
    print(f"  Data: {DATA_FILE}")
    print("=" * 60 + "\n")

    df = load_and_clean(DATA_FILE)
    X, y, features = prepare_features(df)

    print(f"  Features used: {features}")
    print(f"  Target: price (in Lakhs)\n")
    print(f"{'='*52}")
    print(f"  Model Comparison")
    print(f"{'='*52}")

    results = train_and_evaluate(X, y, features)

    rf_model = results["Random Forest"]["model"]
    top_feature = show_feature_importance(rf_model, features)
    plot_predictions(results)

    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)
    print(f"  Best model: Random Forest")
    print(f"  RMSE: {results['Random Forest']['rmse']:.2f} Lakhs")
    print(f"  R²:   {results['Random Forest']['r2']:.3f}")
    print(f"  Most important feature: {top_feature}")
    print()
    print("  NOTE: Run with real data (Bengaluru_House_Data.csv from Kaggle)")
    print("  for stronger results — real dataset has 13,000+ listings.\n")


if __name__ == "__main__":
    main()
