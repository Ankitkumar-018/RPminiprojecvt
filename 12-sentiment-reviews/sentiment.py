"""
Sentiment on Real Reviews — boAt / Mamaearth / Amazon India
Classifies product reviews as Positive / Negative / Neutral and
reports WHERE the model is unreliable.

Dataset options from Kaggle:
  boAt:       https://www.kaggle.com/datasets/deepcontractor/boat-earphones-reviews
  Amazon:     https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews
  Mamaearth:  Search "Mamaearth reviews" on Kaggle

Default: runs on data/reviews_sample.csv (40 rows, synthetic)
Real:    update DATA_FILE and REVIEW_COL / RATING_COL to match your dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import re
import warnings
import os

warnings.filterwarnings("ignore")

DATA_FILE   = "data/reviews_sample.csv"    # change to your downloaded file
REVIEW_COL  = "review"                     # column with review text
RATING_COL  = "rating"                     # column with numeric rating (1–5)
OUTPUT_DIR  = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Step 1: Load & Label ──────────────────────────────────────

def rating_to_sentiment(rating):
    """Map 1-5 star rating to sentiment label."""
    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    else:
        return "negative"


def load_data(filepath):
    df = pd.read_csv(filepath, encoding="latin-1")
    df = df[[REVIEW_COL, RATING_COL]].dropna()
    df.columns = ["review", "rating"]
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna(subset=["rating"])
    df["sentiment"] = df["rating"].apply(rating_to_sentiment)

    print(f"Loaded {len(df)} reviews")
    print(f"  Sentiment distribution:")
    for label, count in df["sentiment"].value_counts().items():
        print(f"    {label:<10} {count:>4} ({count/len(df)*100:.1f}%)")
    print()
    return df


# ── Step 2: Clean Text ────────────────────────────────────────

def clean_review(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)           # remove URLs
    text = re.sub(r"[^a-z\s]", "", text)          # keep only letters
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ── Step 3: Train Classifier ──────────────────────────────────

def train_classifier(df):
    df["clean_review"] = df["review"].apply(clean_review)

    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2),
                                  stop_words="english")
    X = vectorizer.fit_transform(df["clean_review"])
    y = df["sentiment"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000, C=1.0, multi_class="multinomial")
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)
    print("=" * 60)
    print("  Model: Logistic Regression + TF-IDF")
    print(f"  Overall Accuracy: {acc:.3f}")
    print("=" * 60)
    print()
    print("  Per-Class Report:")
    print(classification_report(y_test, preds, zero_division=0))

    return model, vectorizer, preds, y_test, df, X_test


# ── Step 4: Visualisations ────────────────────────────────────

def plot_sentiment_distribution(df):
    counts = df["sentiment"].value_counts()
    colors = {"positive": "#2ecc71", "neutral": "#f39c12", "negative": "#e74c3c"}
    bar_colors = [colors[s] for s in counts.index]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Sentiment Analysis — Product Reviews", fontsize=14, fontweight="bold")

    axes[0].bar(counts.index, counts.values, color=bar_colors, edgecolor="white")
    axes[0].set_title("Sentiment Distribution")
    axes[0].set_ylabel("Number of Reviews")

    axes[1].pie(counts.values, labels=counts.index, autopct="%1.1f%%",
                colors=bar_colors, startangle=90)
    axes[1].set_title("Sentiment Breakdown")

    plt.tight_layout()
    path = f"{OUTPUT_DIR}/sentiment_distribution.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Chart saved: {path}")


def plot_confusion_matrix(y_test, preds):
    labels = ["negative", "neutral", "positive"]
    cm = confusion_matrix(y_test, preds, labels=labels)

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(cm, cmap="Blues")
    plt.colorbar(im)

    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix — Sentiment Classifier", fontweight="bold")

    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    fontsize=14, fontweight="bold",
                    color="white" if cm[i, j] > cm.max() / 2 else "black")

    plt.tight_layout()
    path = f"{OUTPUT_DIR}/confusion_matrix.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Confusion matrix saved: {path}")


# ── Step 5: Report Where the Model Is Unreliable ─────────────

def report_unreliable_cases(df, model, vectorizer, y_test, preds):
    print("\n" + "=" * 60)
    print("  WHERE THE MODEL IS UNRELIABLE")
    print("=" * 60)

    test_df = df.loc[y_test.index].copy()
    test_df["predicted"] = preds
    test_df["correct"] = test_df["sentiment"] == test_df["predicted"]

    wrong = test_df[~test_df["correct"]]

    print(f"\n  Total wrong predictions: {len(wrong)} / {len(test_df)}")

    # Case 1: Sarcasm and irony
    print("""
  UNRELIABLE CASE 1 — SARCASM
  TF-IDF cannot detect tone. A review like:
    "Great product. Broke in 2 days. Absolutely love it!" (1 star)
  Contains positive words (great, love) but is sarcastic.
  The model predicts POSITIVE. Actual: NEGATIVE.

  UNRELIABLE CASE 2 — NEUTRAL/BORDERLINE REVIEWS
  3-star reviews are the hardest. They mix praise and criticism:
    "Sound is good but battery life is disappointing."
  The model often misclassifies these as positive or negative
  because it picks up only the strongest signal word.

  UNRELIABLE CASE 3 — HINGLISH (Hindi + English mixed)
  Indian reviews often contain Hinglish:
    "Bahut achha product hai but quality thodi kam hai"
  The model was trained on English words only.
  Non-English words are ignored → model has less information → unreliable.

  UNRELIABLE CASE 4 — SHORT REVIEWS
  Very short reviews carry little signal:
    "Ok"  →  3 words → TF-IDF has almost nothing to work with
  The model essentially guesses for reviews under 5 words.
""")

    if not wrong.empty:
        print("  Sample wrong predictions from your data:")
        print(f"  {'Actual':<10} {'Predicted':<10} Review")
        print(f"  {'-'*60}")
        for _, row in wrong.head(5).iterrows():
            review_short = str(row["review"])[:70]
            print(f"  {row['sentiment']:<10} {row['predicted']:<10} {review_short}...")

    print("\n  HOW TO IMPROVE:")
    print("  - Use a pre-trained language model (BERT, RoBERTa)")
    print("  - Fine-tune on Indian product reviews with Hinglish support")
    print("  - Add a 'mixed' label to separate true neutral from mixed-sentiment")


def main():
    print("=" * 60)
    print("  Sentiment Analysis — Product Reviews")
    print(f"  Data: {DATA_FILE}")
    print("=" * 60 + "\n")

    df = load_data(DATA_FILE)
    plot_sentiment_distribution(df)

    model, vectorizer, preds, y_test, df, X_test = train_classifier(df)
    plot_confusion_matrix(y_test, preds)
    report_unreliable_cases(df, model, vectorizer, y_test, preds)

    print("\n" + "=" * 60)
    print("  NOTE: Sample data is small — results will vary.")
    print("  Download a real Kaggle reviews dataset (1000+ reviews)")
    print("  for meaningful sentiment patterns.\n")


if __name__ == "__main__":
    main()
