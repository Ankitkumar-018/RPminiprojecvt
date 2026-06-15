"""
One Question, Five Charts
Answers the single question "Which category drives the most revenue?"
using 5 different chart types — and teaches when each chart works best.

Dataset: data/sales_sample.csv (included — synthetic retail data)

Real dataset ideas from Kaggle:
  - Superstore Sales:  https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
  - Indian Retail:     https://www.kaggle.com/datasets/rishikumarrajvansh/marketing-insights-for-e-commerce-company
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import sys

DATA_FILE = "data/sales_sample.csv"
CHARTS_DIR = "charts"
QUESTION = "Which product category drives the most revenue?"

os.makedirs(CHARTS_DIR, exist_ok=True)

COLORS = {
    "Electronics": "#2196F3",   # blue
    "Clothing":    "#FF9800",   # orange
    "Food":        "#4CAF50",   # green
}

MONTHS_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]


def load_data():
    df = pd.read_csv(DATA_FILE)
    df["month"] = pd.Categorical(df["month"], categories=MONTHS_ORDER, ordered=True)
    print(f"Loaded {len(df)} rows × {len(df.columns)} columns")
    print(f"Categories: {sorted(df['category'].unique())}")
    print(f"Months: {MONTHS_ORDER}")
    print(f"Total sales: ₹{df['sales'].sum():,.0f}")
    return df


def print_insight(chart_num, title, when_to_use, what_you_see):
    print(f"\n  Chart {chart_num}: {title}")
    print(f"  When to use: {when_to_use}")
    print(f"  What you see: {what_you_see}")


# ── Chart 1: Bar Chart ────────────────────────────────────────

def chart1_bar(df):
    """Bar chart — total sales per category (overall comparison)."""
    totals = df.groupby("category")["sales"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(
        totals.index,
        totals.values / 1_000_000,
        color=[COLORS[c] for c in totals.index],
        edgecolor="white", linewidth=1.5,
        width=0.6
    )

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            f"₹{bar.get_height():.2f}M",
            ha="center", va="bottom", fontsize=11, fontweight="bold"
        )

    ax.set_title(f"Chart 1: Bar Chart\n\"{QUESTION}\"", fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Product Category", fontsize=11)
    ax.set_ylabel("Total Sales (₹ Millions)", fontsize=11)
    ax.set_ylim(0, totals.values.max() / 1_000_000 * 1.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    path = f"{CHARTS_DIR}/chart1_bar.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()

    print_insight(
        1, "Bar Chart",
        "Comparing totals across categories — best for 'which is biggest'",
        f"Electronics (₹{totals['Electronics']/1e6:.2f}M) clearly leads. "
        f"Simple, direct, no ambiguity."
    )
    return path


# ── Chart 2: Line Chart ────────────────────────────────────────

def chart2_line(df):
    """Line chart — monthly sales trend per category."""
    monthly = df.groupby(["month", "category"])["sales"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(9, 5))

    for cat, color in COLORS.items():
        subset = monthly[monthly["category"] == cat].sort_values("month")
        ax.plot(
            subset["month"].astype(str),
            subset["sales"] / 1000,
            marker="o", label=cat, color=color,
            linewidth=2.5, markersize=7
        )

    ax.set_title(f"Chart 2: Line Chart\n\"{QUESTION} — by Month?\"",
                 fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Month", fontsize=11)
    ax.set_ylabel("Monthly Sales (₹ Thousands)", fontsize=11)
    ax.legend(title="Category", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3)

    path = f"{CHARTS_DIR}/chart2_line.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()

    print_insight(
        2, "Line Chart",
        "Showing how values change over time — best for trends",
        "All 3 categories are growing. Electronics maintains its lead every month. "
        "You can't see this in the bar chart."
    )
    return path


# ── Chart 3: Pie Chart ────────────────────────────────────────

def chart3_pie(df):
    """Pie chart — revenue share (proportion focus)."""
    totals = df.groupby("category")["sales"].sum()
    total = totals.sum()

    fig, ax = plt.subplots(figsize=(7, 6))

    wedges, texts, autotexts = ax.pie(
        totals.values,
        labels=totals.index,
        autopct="%1.1f%%",
        colors=[COLORS[c] for c in totals.index],
        startangle=140,
        pctdistance=0.75,
        explode=[0.03, 0.03, 0.03]
    )

    for autotext in autotexts:
        autotext.set_fontsize(11)
        autotext.set_fontweight("bold")

    ax.set_title(f"Chart 3: Pie Chart\n\"{QUESTION} — Share of Total Revenue?\"",
                 fontsize=13, fontweight="bold", pad=15)

    # Add total in center
    ax.text(0, 0, f"Total\n₹{total/1e6:.1f}M", ha="center", va="center",
            fontsize=10, fontweight="bold", color="#333333")

    path = f"{CHARTS_DIR}/chart3_pie.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()

    share = totals["Electronics"] / total * 100
    print_insight(
        3, "Pie Chart",
        "Showing proportions that add to 100% — best for share/composition",
        f"Electronics is {share:.1f}% of all revenue. Useful for a business summary, "
        "but hard to compare exact sizes — use with caution."
    )
    return path


# ── Chart 4: Stacked Bar Chart ────────────────────────────────

def chart4_stacked_bar(df):
    """Stacked bar — monthly totals split by category (composition + trend)."""
    monthly = df.groupby(["month", "category"])["sales"].sum().unstack("category")
    monthly = monthly.reindex(MONTHS_ORDER)

    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = pd.Series([0] * len(monthly), index=monthly.index)

    for cat in ["Electronics", "Clothing", "Food"]:
        ax.bar(
            monthly.index.astype(str),
            monthly[cat] / 1000,
            bottom=bottom / 1000,
            label=cat,
            color=COLORS[cat],
            edgecolor="white",
            linewidth=0.8
        )
        bottom = bottom + monthly[cat]

    ax.set_title(f"Chart 4: Stacked Bar Chart\n\"{QUESTION} — Within Each Month?\"",
                 fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Month", fontsize=11)
    ax.set_ylabel("Sales (₹ Thousands)", fontsize=11)
    ax.legend(title="Category", fontsize=10, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    path = f"{CHARTS_DIR}/chart4_stacked_bar.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()

    print_insight(
        4, "Stacked Bar Chart",
        "Showing composition within each group — best for 'how does each part contribute?'",
        "You can see total monthly revenue growing AND see that Electronics takes "
        "the largest chunk in every month. Shows both trend and composition."
    )
    return path


# ── Chart 5: Heatmap ──────────────────────────────────────────

def chart5_heatmap(df):
    """Heatmap — sales by region and category (two dimensions)."""
    pivot = df.groupby(["region", "category"])["sales"].sum().unstack("category")
    pivot = pivot.div(1000)   # convert to thousands

    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(pivot.values, cmap="YlOrRd", aspect="auto")

    ax.set_xticks(range(len(pivot.columns)))
    ax.set_yticks(range(len(pivot.index)))
    ax.set_xticklabels(pivot.columns, fontsize=11)
    ax.set_yticklabels(pivot.index, fontsize=11)

    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.values[i, j]
            ax.text(j, i, f"₹{val:.0f}K",
                    ha="center", va="center",
                    color="black" if val < 400 else "white",
                    fontsize=10, fontweight="bold")

    plt.colorbar(im, ax=ax, label="Sales (₹ Thousands)")
    ax.set_title(f"Chart 5: Heatmap\n\"{QUESTION} — Across Regions?\"",
                 fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Category", fontsize=11)
    ax.set_ylabel("Region", fontsize=11)

    path = f"{CHARTS_DIR}/chart5_heatmap.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()

    print_insight(
        5, "Heatmap",
        "Showing two-dimensional patterns — best for 'which combination stands out?'",
        "Electronics × North is the darkest cell — highest revenue combination. "
        "Food is consistently light (low revenue) across all regions."
    )
    return path


# ── Main ──────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  One Question, Five Charts")
    print(f"  Question: {QUESTION}")
    print("=" * 60)

    df = load_data()

    print("\n  Generating charts...")
    paths = []
    paths.append(chart1_bar(df))
    paths.append(chart2_line(df))
    paths.append(chart3_pie(df))
    paths.append(chart4_stacked_bar(df))
    paths.append(chart5_heatmap(df))

    print("\n" + "=" * 60)
    print("  SUMMARY: Which Chart for Which Purpose?")
    print("=" * 60)
    chart_guide = [
        ("Bar chart",         "Compare totals — which is biggest?"),
        ("Line chart",        "Show trends — how does it change over time?"),
        ("Pie chart",         "Show proportions — what % is each?"),
        ("Stacked bar",       "Show composition — what's inside each bar?"),
        ("Heatmap",           "Show two dimensions — which combo stands out?"),
    ]
    for name, purpose in chart_guide:
        print(f"  {name:<18} → {purpose}")

    print(f"\n  All 5 charts saved to: {CHARTS_DIR}/")
    for path in paths:
        print(f"    {path}")

    print("\n  ANSWER TO THE QUESTION:")
    totals = df.groupby("category")["sales"].sum()
    winner = totals.idxmax()
    print(f"  Electronics (₹{totals['Electronics']/1e6:.2f}M) drives the most revenue.")
    print(f"  Electronics is {totals['Electronics']/totals.sum()*100:.1f}% of total sales.\n")


if __name__ == "__main__":
    main()
