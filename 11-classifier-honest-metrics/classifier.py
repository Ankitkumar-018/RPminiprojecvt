"""
Classifier with Honest Metrics — SMS Spam Detector
Builds a spam classifier and reports Precision & Recall (not just accuracy),
then explains one real case it gets wrong and why.

Dataset: SMS Spam Collection from Kaggle
  https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset
  Download spam.csv and place in data/ folder

Default: runs on data/sms_sample.csv (40 rows, synthetic sample)
Real:    set DATA_FILE = "data/spam.csv" after downloading
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)
import warnings
import os

warnings.filterwarnings("ignore")

DATA_FILE = "data/sms_sample.csv"       # change to "data/spam.csv" for real data
OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Step 1: Load Data ─────────────────────────────────────────

def load_data(filepath):
    df = pd.read_csv(filepath, encoding="latin-1")

    # Handle both column naming conventions
    if "v1" in df.columns and "v2" in df.columns:
        df = df[["v1", "v2"]].rename(columns={"v1": "label", "v2": "message"})
    else:
        df = df[["label", "message"]]

    df = df.dropna()
    df["label_num"] = (df["label"] == "spam").astype(int)

    spam_count = df["label_num"].sum()
    ham_count = len(df) - spam_count
    print(f"Loaded {len(df)} messages")
    print(f"  Ham (not spam): {ham_count} ({ham_count/len(df)*100:.1f}%)")
    print(f"  Spam:           {spam_count} ({spam_count/len(df)*100:.1f}%)\n")
    return df


# ── Step 2: Feature Extraction (TF-IDF) ──────────────────────

def extract_features(df):
    vectorizer = TfidfVectorizer(
        max_features=3000,
        ngram_range=(1, 2),     # unigrams + bigrams
        stop_words="english",
        lowercase=True,
    )
    X = vectorizer.fit_transform(df["message"])
    y = df["label_num"]
    return X, y, vectorizer


# ── Step 3: Train + Evaluate ──────────────────────────────────

def train_and_evaluate(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    models = {
        "Naive Bayes":        MultinomialNB(alpha=0.1),
        "Logistic Regression": LogisticRegression(max_iter=1000, C=1.0),
    }

    results = {}
    print("=" * 65)
    print(f"  {'Model':<24} {'Accuracy':>9} {'Precision':>10} {'Recall':>8} {'F1':>8}")
    print("=" * 65)

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        acc  = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, zero_division=0)
        rec  = recall_score(y_test, preds, zero_division=0)
        f1   = f1_score(y_test, preds, zero_division=0)

        print(f"  {name:<24} {acc:>8.3f} {prec:>10.3f} {rec:>8.3f} {f1:>8.3f}")
        results[name] = {
            "model": model, "preds": preds,
            "y_test": y_test, "X_test": X_test,
            "accuracy": acc, "precision": prec,
            "recall": rec, "f1": f1
        }

    print("=" * 65)
    return results, X_train, X_test, y_train, y_test


# ── Step 4: Why Precision & Recall > Accuracy ────────────────

def explain_metrics(results):
    print("\n" + "=" * 65)
    print("  WHY ACCURACY IS MISLEADING HERE")
    print("=" * 65)
    print("""
  Dataset is imbalanced: ~87% ham, ~13% spam.
  A model that predicts EVERY message as "ham" (not spam) gets:
    Accuracy = 87%  ← looks great!
    Recall   = 0%   ← catches ZERO spam (useless)

  For spam detection, the two metrics that matter are:

  PRECISION = Of messages flagged as spam, how many actually are?
    Low precision → legitimate emails go to spam (annoying user)

  RECALL = Of all actual spam, how many did we catch?
    Low recall → spam slips through into inbox (dangerous)

  The tradeoff: high precision = fewer false alarms
                high recall   = catches more real spam
  F1 Score balances both.
""")


# ── Step 5: Confusion Matrix ──────────────────────────────────

def plot_confusion_matrix(y_test, preds, model_name):
    cm = confusion_matrix(y_test, preds)
    fig, ax = plt.subplots(figsize=(6, 5))

    im = ax.imshow(cm, cmap="Blues")
    plt.colorbar(im)

    classes = ["Ham (Not Spam)", "Spam"]
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(classes)
    ax.set_yticklabels(classes)
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    ax.set_title(f"Confusion Matrix — {model_name}", fontweight="bold")

    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]),
                    ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() / 2 else "black",
                    fontsize=16, fontweight="bold")

    # Annotate cells
    labels = [["True Neg\n(Ham→Ham)", "False Pos\n(Ham→Spam)"],
              ["False Neg\n(Spam→Ham)", "True Pos\n(Spam→Spam)"]]
    for i in range(2):
        for j in range(2):
            ax.text(j, i + 0.35, labels[i][j], ha="center", va="center",
                    fontsize=7, color="gray")

    plt.tight_layout()
    safe_name = model_name.replace(" ", "_").lower()
    path = f"{OUTPUT_DIR}/confusion_{safe_name}.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Confusion matrix saved: {path}")


# ── Step 6: Find and Explain Wrong Predictions ────────────────

def explain_wrong_prediction(df, results, vectorizer):
    print("\n" + "=" * 65)
    print("  HONEST LOOK: One Wrong Prediction Explained")
    print("=" * 65)

    best_model_name = max(results, key=lambda k: results[k]["f1"])
    res = results[best_model_name]

    test_indices = res["y_test"].index
    test_df = df.loc[test_indices].copy()
    test_df["predicted"] = res["preds"]
    test_df["actual"] = res["y_test"].values

    # False Negatives: spam predicted as ham (most dangerous error)
    false_negatives = test_df[(test_df["actual"] == 1) & (test_df["predicted"] == 0)]
    # False Positives: ham predicted as spam (annoying error)
    false_positives = test_df[(test_df["actual"] == 0) & (test_df["predicted"] == 1)]

    print(f"\n  Model: {best_model_name}")
    print(f"  False Negatives (spam that slipped through): {len(false_negatives)}")
    print(f"  False Positives (ham wrongly marked spam):   {len(false_positives)}")

    if not false_negatives.empty:
        example = false_negatives.iloc[0]
        print(f"\n  FALSE NEGATIVE EXAMPLE (spam that got through):")
        print(f"  Message: \"{example['message'][:200]}\"")
        print(f"  Why the model missed it: The message may avoid obvious spam")
        print(f"  trigger words. Modern spam is written to sound like a normal")
        print(f"  message while still being deceptive.")

    if not false_positives.empty:
        example = false_positives.iloc[0]
        print(f"\n  FALSE POSITIVE EXAMPLE (ham marked as spam):")
        print(f"  Message: \"{example['message'][:200]}\"")
        print(f"  Why the model was wrong: This ham message may contain words")
        print(f"  common in spam (like 'free', 'win', 'prize') but used in a")
        print(f"  legitimate context that TF-IDF cannot distinguish.")

    print(f"\n  KEY LIMITATION: TF-IDF treats every word independently.")
    print(f"  It cannot understand context, sarcasm, or intent.")
    print(f"  'Win a prize' looks the same whether legitimate or spam.")


def main():
    print("=" * 65)
    print("  Classifier with Honest Metrics — SMS Spam Detector")
    print(f"  Data: {DATA_FILE}")
    print("=" * 65 + "\n")

    df = load_data(DATA_FILE)
    X, y, vectorizer = extract_features(df)
    results, X_train, X_test, y_train, y_test = train_and_evaluate(X, y)

    explain_metrics(results)

    best_name = max(results, key=lambda k: results[k]["f1"])
    plot_confusion_matrix(results[best_name]["y_test"],
                          results[best_name]["preds"], best_name)

    explain_wrong_prediction(df, results, vectorizer)

    print("\n" + "=" * 65)
    print("  NOTE: Run with real data (spam.csv from Kaggle, 5572 messages)")
    print("  for meaningful precision/recall values.\n")


if __name__ == "__main__":
    main()
