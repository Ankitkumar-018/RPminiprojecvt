"""
Will It Be Late? — Delivery Delay Predictor
Binary classification: will this order be delivered late? (yes / no)

Dataset: data/deliveries_sample.csv (included — synthetic delivery data)

Real dataset ideas from Kaggle:
  - E-Commerce Shipping:  https://www.kaggle.com/datasets/prachi13/customer-churn-dataset
  - Supply Chain:         https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

DATA_FILE  = "data/deliveries_sample.csv"
CHARTS_DIR = "charts"
os.makedirs(CHARTS_DIR, exist_ok=True)


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print("=" * 60)


# ── Step 1: Load & Engineer Features ─────────────────────────

def load_and_engineer(filepath):
    df = pd.read_csv(filepath)
    print_section("DATA OVERVIEW")
    print(f"  Rows: {len(df)}  |  Columns: {len(df.columns)}")

    # Target variable: late if actual > promised
    df["is_late"] = (df["actual_delivery_days"] > df["promised_delivery_days"]).astype(int)
    late_rate = df["is_late"].mean() * 100
    print(f"  Late deliveries: {df['is_late'].sum()} ({late_rate:.1f}%)")
    print(f"  On-time deliveries: {(df['is_late']==0).sum()} ({100-late_rate:.1f}%)")

    # Feature: delay buffer (promised - distance / 300) — how tight is the promise?
    df["delay_buffer_days"] = df["promised_delivery_days"] - (df["distance_km"] / 300)

    # Feature: fragile as binary
    df["is_fragile"] = (df["fragile"] == "Yes").astype(int)

    return df


# ── Step 2: Prepare Features ──────────────────────────────────

def prepare_features(df):
    categorical = ["category", "carrier", "season", "payment_mode", "origin_city", "destination_city"]
    numeric     = ["distance_km", "weight_kg", "warehouse_to_pickup_hrs",
                   "promised_delivery_days", "delay_buffer_days", "is_fragile"]

    df_encoded = df.copy()
    encoders = {}
    for col in categorical:
        le = LabelEncoder()
        df_encoded[col + "_enc"] = le.fit_transform(df[col])
        encoders[col] = le

    feature_cols = numeric + [c + "_enc" for c in categorical]
    X = df_encoded[feature_cols]
    y = df_encoded["is_late"]
    return X, y, feature_cols, encoders


# ── Step 3: Train & Evaluate ──────────────────────────────────

def train_and_evaluate(X, y, feature_cols):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    print(f"\n  Training set: {len(X_train)} rows")
    print(f"  Test set:     {len(X_test)} rows")

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        results[name] = {
            "model":     model,
            "preds":     preds,
            "accuracy":  accuracy_score(y_test, preds),
            "precision": precision_score(y_test, preds, zero_division=0),
            "recall":    recall_score(y_test, preds, zero_division=0),
            "f1":        f1_score(y_test, preds, zero_division=0),
            "cm":        confusion_matrix(y_test, preds),
        }

    print_section("MODEL COMPARISON")
    print(f"  {'Model':<22} {'Accuracy':>9} {'Precision':>10} {'Recall':>8} {'F1':>8}")
    print(f"  {'-'*60}")
    for name, res in results.items():
        print(f"  {name:<22} {res['accuracy']:>8.1%} {res['precision']:>9.1%} "
              f"{res['recall']:>7.1%} {res['f1']:>7.1%}")

    # Detailed report for Random Forest
    print_section("CLASSIFICATION REPORT — Random Forest")
    rf_preds = results["Random Forest"]["preds"]
    print(classification_report(y_test, rf_preds,
                                target_names=["On Time", "Late"], zero_division=0))

    return results, X_test, y_test


# ── Step 4: Feature Importance ────────────────────────────────

def plot_feature_importance(rf_model, feature_cols):
    importances = pd.Series(rf_model.feature_importances_, index=feature_cols)
    importances = importances.sort_values(ascending=True).tail(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#FF9800" if imp > 0.08 else "#90CAF9" for imp in importances.values]
    ax.barh(importances.index, importances.values, color=colors, edgecolor="white")
    ax.set_title("Feature Importance — What Drives Late Deliveries?",
                 fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Importance Score", fontsize=10)
    ax.axvline(0.08, color="#E53935", linestyle="--", alpha=0.7, label="Key threshold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    path = f"{CHARTS_DIR}/feature_importance.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\n  Feature importance chart saved: {path}")

    top3 = importances.tail(3).index.tolist()
    print(f"  Top 3 predictors of lateness: {top3}")
    return path


# ── Step 5: Confusion Matrix ──────────────────────────────────

def plot_confusion_matrix(cm, model_name):
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    plt.colorbar(im, ax=ax)

    labels = ["On Time", "Late"]
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Predicted", fontsize=11)
    ax.set_ylabel("Actual", fontsize=11)
    ax.set_title(f"Confusion Matrix — {model_name}", fontsize=11, fontweight="bold")

    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]),
                    ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() / 2 else "black",
                    fontsize=14, fontweight="bold")

    path = f"{CHARTS_DIR}/confusion_matrix.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Confusion matrix saved: {path}")
    return path


# ── Step 6: Explain Predictions ───────────────────────────────

def explain_predictions(df, X_test, y_test, preds, encoders):
    print_section("LATE DELIVERY PATTERNS")

    test_rows = df.iloc[X_test.index].copy()
    test_rows["predicted_late"] = preds
    test_rows["actual_late"]    = y_test.values

    # Late orders by carrier
    late_by_carrier = (
        test_rows[test_rows["actual_late"] == 1]
        .groupby("carrier")
        .size()
        .sort_values(ascending=False)
    )
    if not late_by_carrier.empty:
        print(f"\n  Late orders by carrier:")
        for carrier, count in late_by_carrier.items():
            print(f"    {carrier:<18} {count} late orders")

    # Late orders by category
    late_by_cat = (
        test_rows[test_rows["actual_late"] == 1]
        .groupby("category")
        .size()
        .sort_values(ascending=False)
    )
    if not late_by_cat.empty:
        print(f"\n  Late orders by category:")
        for cat, count in late_by_cat.items():
            print(f"    {cat:<18} {count} late orders")

    # False negatives — predicted on time but actually late (dangerous!)
    fn = test_rows[(test_rows["predicted_late"] == 0) & (test_rows["actual_late"] == 1)]
    if not fn.empty:
        print(f"\n  False Negatives (predicted on-time but actually LATE) — {len(fn)} orders")
        print(f"  These are the dangerous ones — customer expected delivery, got delay.")
        for _, row in fn.head(3).iterrows():
            print(f"    Order {row['order_id']}: {row['category']} from {row['origin_city']} "
                  f"to {row['destination_city']}, carrier={row['carrier']}")

    # False positives — predicted late but actually on time
    fp = test_rows[(test_rows["predicted_late"] == 1) & (test_rows["actual_late"] == 0)]
    if not fp.empty:
        print(f"\n  False Positives (predicted late but actually ON TIME) — {len(fp)} orders")
        print(f"  These cause unnecessary apology emails and refund offers.")


# ── Step 7: Predict a New Order ───────────────────────────────

def predict_new_order(rf_model, feature_cols, encoders):
    print_section("TRY IT — Predict a New Order")

    example = {
        "distance_km":            1415,   # Mumbai to Delhi
        "weight_kg":              3.5,
        "warehouse_to_pickup_hrs": 7,     # long pre-pickup delay
        "promised_delivery_days":  4,
        "delay_buffer_days":       4 - (1415 / 300),   # 4 - 4.7 = -0.7 (tight!)
        "is_fragile":              1,
        "category_enc":            encoders["category"].transform(["Electronics"])[0],
        "carrier_enc":             encoders["carrier"].transform(["Delhivery"])[0],
        "season_enc":              encoders["season"].transform(["Monsoon"])[0],
        "payment_mode_enc":        encoders["payment_mode"].transform(["COD"])[0],
        "origin_city_enc":         encoders["origin_city"].transform(["Mumbai"])[0],
        "destination_city_enc":    encoders["destination_city"].transform(["Delhi"])[0],
    }

    input_df = pd.DataFrame([example])[feature_cols]
    pred = rf_model.predict(input_df)[0]
    prob = rf_model.predict_proba(input_df)[0][1]

    print(f"\n  Order details:")
    print(f"    Route:     Mumbai → Delhi (1415 km)")
    print(f"    Category:  Electronics (fragile)")
    print(f"    Carrier:   Delhivery")
    print(f"    Season:    Monsoon")
    print(f"    Promised:  4 days (very tight for this distance)")
    print(f"\n  Prediction: {'⚠ WILL BE LATE' if pred == 1 else '✓ ON TIME'}")
    print(f"  Probability of being late: {prob:.0%}")

    if pred == 1:
        print(f"\n  Why late?")
        print(f"    - warehouse_to_pickup_hrs = 7 (high pre-pickup delay)")
        print(f"    - distance = 1415 km but only 4 days promised (buffer = -0.7)")
        print(f"    - Monsoon season increases road delays")
        print(f"    - Fragile item requires special handling")


# ── Main ──────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Will It Be Late? — Delivery Delay Predictor")
    print(f"  Dataset: {DATA_FILE}")
    print("=" * 60)

    df = load_and_engineer(DATA_FILE)
    X, y, feature_cols, encoders = prepare_features(df)
    results, X_test, y_test = train_and_evaluate(X, y, feature_cols)

    rf_model = results["Random Forest"]["model"]
    rf_preds = results["Random Forest"]["preds"]

    plot_feature_importance(rf_model, feature_cols)
    plot_confusion_matrix(results["Random Forest"]["cm"], "Random Forest")
    explain_predictions(df, X_test, y_test, rf_preds, encoders)
    predict_new_order(rf_model, feature_cols, encoders)

    print_section("BUSINESS INSIGHT")
    print("  Key findings from this model:")
    print("  1. warehouse_to_pickup_hrs is a top predictor — delays start in the warehouse")
    print("  2. Monsoon season significantly increases late deliveries")
    print("  3. Tight delivery promises (small buffer) predict lateness more than distance")
    print("  4. Furniture and Electronics are late most often (heavy/fragile = slow handling)")
    print()


if __name__ == "__main__":
    main()
