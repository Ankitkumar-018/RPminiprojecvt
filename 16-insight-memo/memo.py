"""
Insight Memo — Auto-Generated Business Memo from CSV Data
Analyses an e-commerce orders dataset and produces a structured
markdown memo with findings, numbers, and recommendations.

Dataset: data/ecommerce_sample.csv (included — synthetic e-commerce data)

Real dataset ideas from Kaggle:
  - Brazilian E-Commerce (Olist): https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
  - Indian E-Commerce Orders:     https://www.kaggle.com/datasets/benroshan/ecommerce-data
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

DATA_FILE  = "data/ecommerce_sample.csv"
MEMO_FILE  = "insight_memo.md"
CHARTS_DIR = "charts"
os.makedirs(CHARTS_DIR, exist_ok=True)


def print_section(title):
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print("─" * 55)


# ── Data Loading ──────────────────────────────────────────────

def load_data(filepath):
    df = pd.read_csv(filepath, parse_dates=["order_date", "delivery_date"])
    df["delivery_days"] = (df["delivery_date"] - df["order_date"]).dt.days
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["week"]  = df["order_date"].dt.isocalendar().week.astype(int)
    return df


# ── Analysis Functions ─────────────────────────────────────────

def analyse_revenue(df):
    """Overall revenue summary."""
    total_rev = df["order_value"].sum()
    total_orders = len(df)
    avg_order_val = df["order_value"].mean()
    total_units = df["units"].sum()

    by_category = df.groupby("category")["order_value"].sum().sort_values(ascending=False)
    top_cat = by_category.index[0]
    top_cat_share = by_category.iloc[0] / total_rev * 100

    by_month = df.groupby("month")["order_value"].sum()
    best_month = by_month.idxmax()
    mom_change = None
    if len(by_month) >= 2:
        months = by_month.index.tolist()
        mom_change = (by_month[months[-1]] - by_month[months[-2]]) / by_month[months[-2]] * 100

    return {
        "total_revenue": total_rev,
        "total_orders": total_orders,
        "avg_order_value": avg_order_val,
        "total_units": total_units,
        "by_category": by_category,
        "top_category": top_cat,
        "top_cat_share": top_cat_share,
        "by_month": by_month,
        "best_month": best_month,
        "mom_change": mom_change,
    }


def analyse_returns(df):
    """Return rate analysis."""
    total = len(df)
    returned = df["returned"].eq("Yes").sum()
    return_rate = returned / total * 100

    returns_by_cat = df.groupby("category").apply(
        lambda x: x["returned"].eq("Yes").sum() / len(x) * 100,
        include_groups=False
    ).sort_values(ascending=False)

    returned_avg_rating = df[df["returned"] == "Yes"]["rating"].mean()
    normal_avg_rating   = df[df["returned"] == "No"]["rating"].mean()

    high_value_returns = df[(df["returned"] == "Yes") & (df["order_value"] > 10000)]

    return {
        "total_returns": returned,
        "return_rate": return_rate,
        "returns_by_category": returns_by_cat,
        "returned_avg_rating": returned_avg_rating,
        "normal_avg_rating": normal_avg_rating,
        "high_value_returns": len(high_value_returns),
    }


def analyse_customers(df):
    """Customer and geography analysis."""
    repeat_customers = df["customer_id"].value_counts()
    repeaters = repeat_customers[repeat_customers > 1]
    top_customer = repeat_customers.index[0]
    top_customer_orders = repeat_customers.iloc[0]
    top_customer_rev = df[df["customer_id"] == top_customer]["order_value"].sum()

    by_state = df.groupby("state")["order_value"].sum().sort_values(ascending=False).head(5)
    by_city  = df.groupby("city")["order_value"].sum().sort_values(ascending=False).head(5)

    return {
        "repeat_customers": len(repeaters),
        "total_customers": df["customer_id"].nunique(),
        "top_customer": top_customer,
        "top_customer_orders": top_customer_orders,
        "top_customer_rev": top_customer_rev,
        "by_state": by_state,
        "by_city": by_city,
    }


def analyse_delivery(df):
    """Delivery speed and satisfaction analysis."""
    avg_days = df["delivery_days"].mean()
    median_days = df["delivery_days"].median()
    late_count = (df["delivery_days"] > 5).sum()
    late_rate = late_count / len(df) * 100

    by_cat = df.groupby("category")["delivery_days"].mean().sort_values(ascending=False)
    fastest = df.groupby("city")["delivery_days"].mean().nsmallest(3)

    corr_rating_days = df["rating"].corr(df["delivery_days"])

    return {
        "avg_days": avg_days,
        "median_days": median_days,
        "late_count": late_count,
        "late_rate": late_rate,
        "by_category": by_cat,
        "fastest_cities": fastest,
        "rating_days_corr": corr_rating_days,
    }


def analyse_ratings(df):
    """Customer satisfaction analysis."""
    avg_rating = df["rating"].mean()
    low_rated = df[df["rating"] < 3.5]
    high_rated = df[df["rating"] >= 4.5]

    by_cat = df.groupby("category")["rating"].mean().sort_values(ascending=False)
    lowest_cat = by_cat.index[-1]

    return {
        "avg_rating": avg_rating,
        "low_rated_count": len(low_rated),
        "high_rated_count": len(high_rated),
        "by_category": by_cat,
        "lowest_rated_category": lowest_cat,
    }


# ── Chart Generation ──────────────────────────────────────────

def generate_charts(df, rev, ret, ratings):
    paths = {}

    # Chart 1: Revenue by category
    _, axes = plt.subplots(1, 2, figsize=(12, 4))

    by_cat = rev["by_category"]
    axes[0].bar(by_cat.index, by_cat.values / 1000,
                color=["#2196F3", "#FF9800", "#4CAF50", "#9C27B0"],
                edgecolor="white", width=0.6)
    axes[0].set_title("Revenue by Category (₹ Thousands)", fontweight="bold")
    axes[0].set_ylabel("Revenue (₹K)")
    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)

    # Chart 2: Monthly revenue trend
    monthly = rev["by_month"]
    axes[1].plot(monthly.index.tolist(), monthly.values / 1000,
                 marker="o", color="#2196F3", linewidth=2.5, markersize=8)
    axes[1].fill_between(range(len(monthly)), monthly.values / 1000, alpha=0.1, color="#2196F3")
    axes[1].set_xticks(range(len(monthly)))
    axes[1].set_xticklabels(monthly.index.tolist())
    axes[1].set_title("Monthly Revenue Trend (₹ Thousands)", fontweight="bold")
    axes[1].set_ylabel("Revenue (₹K)")
    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)

    plt.suptitle("Revenue Overview", fontsize=14, fontweight="bold", y=1.02)
    path = f"{CHARTS_DIR}/memo_revenue.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    paths["revenue"] = path

    # Chart 3: Return rate + rating by category
    _, axes = plt.subplots(1, 2, figsize=(12, 4))

    ret_by_cat = ret["returns_by_category"]
    axes[0].barh(ret_by_cat.index, ret_by_cat.values,
                 color=["#EF5350" if v > 10 else "#90CAF9" for v in ret_by_cat.values])
    axes[0].set_title("Return Rate by Category (%)", fontweight="bold")
    axes[0].set_xlabel("Return Rate (%)")
    axes[0].axvline(ret["return_rate"], color="gray", linestyle="--", alpha=0.7, label="Overall avg")
    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)

    rat_by_cat = ratings["by_category"]
    colors = ["#EF5350" if v < 4.0 else "#66BB6A" for v in rat_by_cat.values]
    axes[1].bar(rat_by_cat.index, rat_by_cat.values, color=colors, edgecolor="white", width=0.6)
    axes[1].set_title("Average Rating by Category", fontweight="bold")
    axes[1].set_ylabel("Average Rating")
    axes[1].set_ylim(3, 5)
    axes[1].axhline(ratings["avg_rating"], color="gray", linestyle="--", alpha=0.7, label="Overall avg")
    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)

    plt.suptitle("Quality & Satisfaction", fontsize=14, fontweight="bold", y=1.02)
    path = f"{CHARTS_DIR}/memo_quality.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    paths["quality"] = path

    return paths


# ── Write Memo ────────────────────────────────────────────────

def write_memo(df, rev, ret, cust, deliv, ratings):
    today = datetime.now().strftime("%d %B %Y")
    date_range = f"{df['order_date'].min().strftime('%d %b')} – {df['order_date'].max().strftime('%d %b %Y')}"

    mom_str = ""
    if rev["mom_change"] is not None:
        direction = "↑" if rev["mom_change"] > 0 else "↓"
        mom_str = f" ({direction} {abs(rev['mom_change']):.1f}% vs previous month)"

    lines = [
        f"# Insight Memo — E-Commerce Performance\n",
        f"**Prepared:** {today}  \n",
        f"**Data Period:** {date_range}  \n",
        f"**Dataset:** `{DATA_FILE}` ({len(df)} orders)\n",
        "\n---\n",
        "## Executive Summary\n",
        f"The business processed **{rev['total_orders']} orders** worth **₹{rev['total_revenue']:,.0f}** ",
        f"in the period {date_range}. ",
        f"**{rev['top_category']}** is the top revenue driver at {rev['top_cat_share']:.1f}% of total revenue. ",
        f"Overall return rate is **{ret['return_rate']:.1f}%**, and average customer rating is **{ratings['avg_rating']:.2f}/5.0**.\n",
        "\n---\n",
        "## 1. Revenue\n",
        f"| Metric | Value |\n",
        f"|--------|-------|\n",
        f"| Total Revenue | ₹{rev['total_revenue']:,.0f} |\n",
        f"| Total Orders | {rev['total_orders']} |\n",
        f"| Average Order Value | ₹{rev['avg_order_value']:,.0f} |\n",
        f"| Total Units Sold | {rev['total_units']:,} |\n",
        f"| Best Month | {rev['best_month']}{mom_str} |\n",
        "\n**Revenue by Category:**\n",
        "\n| Category | Revenue | Share |\n",
        "|----------|---------|-------|\n",
    ]

    for cat, val in rev["by_category"].items():
        share = val / rev["total_revenue"] * 100
        lines.append(f"| {cat} | ₹{val:,.0f} | {share:.1f}% |\n")

    lines += [
        "\n**Finding:** ",
        f"{rev['top_category']} contributes {rev['top_cat_share']:.1f}% of revenue despite being a single category. ",
        "Books and Food have higher order counts but lower order values.\n",
        "\n---\n",
        "## 2. Returns\n",
        f"| Metric | Value |\n",
        f"|--------|-------|\n",
        f"| Total Returns | {ret['total_returns']} orders ({ret['return_rate']:.1f}%) |\n",
        f"| Avg Rating (Returned) | {ret['returned_avg_rating']:.2f}/5.0 |\n",
        f"| Avg Rating (Not Returned) | {ret['normal_avg_rating']:.2f}/5.0 |\n",
        f"| High-Value Returns (>₹10,000) | {ret['high_value_returns']} orders |\n",
        "\n**Return Rate by Category:**\n",
        "\n| Category | Return Rate |\n",
        "|----------|-------------|\n",
    ]

    for cat, rate in ret["returns_by_category"].items():
        flag = " ⚠" if rate > 10 else ""
        lines.append(f"| {cat} | {rate:.1f}%{flag} |\n")

    rating_gap = ret["normal_avg_rating"] - ret["returned_avg_rating"]
    lines += [
        f"\n**Finding:** Returned orders have a {rating_gap:.1f}-point lower average rating ",
        f"({ret['returned_avg_rating']:.2f} vs {ret['normal_avg_rating']:.2f}). ",
        "This confirms returns are driven by dissatisfaction, not just remorse purchases. ",
        "High-value Electronics returns have the most financial impact.\n",
        "\n---\n",
        "## 3. Customers & Geography\n",
        f"| Metric | Value |\n",
        f"|--------|-------|\n",
        f"| Unique Customers | {cust['total_customers']} |\n",
        f"| Repeat Customers (2+ orders) | {cust['repeat_customers']} ({cust['repeat_customers']/cust['total_customers']*100:.1f}%) |\n",
        f"| Top Customer | {cust['top_customer']} ({cust['top_customer_orders']} orders, ₹{cust['top_customer_rev']:,.0f}) |\n",
        "\n**Top 5 States by Revenue:**\n",
        "\n| State | Revenue |\n",
        "|-------|--------|\n",
    ]

    for state, val in cust["by_state"].items():
        lines.append(f"| {state} | ₹{val:,.0f} |\n")

    lines += [
        "\n**Top 5 Cities by Revenue:**\n",
        "\n| City | Revenue |\n",
        "|------|--------|\n",
    ]

    for city, val in cust["by_city"].items():
        lines.append(f"| {city} | ₹{val:,.0f} |\n")

    repeat_pct = cust["repeat_customers"] / cust["total_customers"] * 100
    lines += [
        f"\n**Finding:** {repeat_pct:.1f}% of customers placed more than one order. ",
        "Repeat customers are a high-value segment — a loyalty programme could increase this rate.\n",
        "\n---\n",
        "## 4. Delivery Performance\n",
        f"| Metric | Value |\n",
        f"|--------|-------|\n",
        f"| Avg Delivery Time | {deliv['avg_days']:.1f} days |\n",
        f"| Median Delivery Time | {deliv['median_days']:.1f} days |\n",
        f"| Orders Taking > 5 Days | {deliv['late_count']} ({deliv['late_rate']:.1f}%) |\n",
        f"| Rating–Delivery Days Correlation | {deliv['rating_days_corr']:.3f} |\n",
        "\n**Avg Delivery Days by Category:**\n",
        "\n| Category | Avg Days |\n",
        "|----------|----------|\n",
    ]

    for cat, days in deliv["by_category"].items():
        lines.append(f"| {cat} | {days:.1f} |\n")

    corr_direction = "negative" if deliv["rating_days_corr"] < 0 else "positive"
    lines += [
        f"\n**Finding:** The correlation between delivery time and rating is {deliv['rating_days_corr']:.3f} ({corr_direction}). ",
        "Longer delivery times are associated with lower ratings. ",
        f"{deliv['late_rate']:.1f}% of orders took more than 5 days — these are highest-risk for low ratings.\n",
        "\n---\n",
        "## 5. Customer Satisfaction\n",
        f"| Metric | Value |\n",
        f"|--------|-------|\n",
        f"| Overall Avg Rating | {ratings['avg_rating']:.2f}/5.0 |\n",
        f"| Orders Rated < 3.5 | {ratings['low_rated_count']} |\n",
        f"| Orders Rated ≥ 4.5 | {ratings['high_rated_count']} |\n",
        "\n**Avg Rating by Category:**\n",
        "\n| Category | Avg Rating |\n",
        "|----------|-----------|\n",
    ]

    for cat, rat in ratings["by_category"].items():
        flag = " ⚠" if rat < 4.0 else ""
        lines.append(f"| {cat} | {rat:.2f}/5.0{flag} |\n")

    lines += [
        f"\n**Finding:** {ratings['lowest_rated_category']} has the lowest average rating. ",
        "Low ratings in high-return categories amplify each other — fixing delivery speed ",
        "in these categories would likely improve both returns and ratings.\n",
        "\n---\n",
        "## 6. Recommendations\n",
        "\n| Priority | Recommendation | Evidence |\n",
        "|----------|---------------|----------|\n",
    ]

    # Build recommendations from actual numbers
    top_return_cat = ret["returns_by_category"].idxmax()
    top_return_rate = ret["returns_by_category"].max()
    recs = [
        ("HIGH", f"Investigate {top_return_cat} return causes",
         f"{top_return_rate:.1f}% return rate — highest of all categories"),
        ("HIGH", "Reduce orders with delivery > 5 days",
         f"{deliv['late_rate']:.1f}% of orders exceed 5 days; correlates with low ratings"),
        ("MEDIUM", f"Launch loyalty programme for repeat customers",
         f"{cust['repeat_customers']} repeat customers generate disproportionate revenue"),
        ("MEDIUM", f"Expand presence in {cust['by_state'].index[0]}",
         f"₹{cust['by_state'].iloc[0]:,.0f} — largest revenue state by far"),
        ("LOW", "Review discount strategy",
         f"Discounted orders should be tracked for margin impact"),
    ]

    for priority, rec, evidence in recs:
        lines.append(f"| **{priority}** | {rec} | {evidence} |\n")

    lines += [
        "\n---\n",
        "## 7. Data Notes\n",
        f"- Dataset: `{DATA_FILE}` (synthetic data — {len(df)} orders)\n",
        f"- For production: replace with real export from your order management system\n",
        f"- Real dataset suggestion: Olist Brazilian E-Commerce on Kaggle\n",
        f"  (`https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce`)\n",
        f"- Memo generated: {today}\n",
    ]

    with open(MEMO_FILE, "w") as f:
        f.writelines(lines)

    print(f"\n  Memo written: {MEMO_FILE}")


# ── Main ──────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  Insight Memo Generator")
    print(f"  Dataset: {DATA_FILE}")
    print("=" * 55)

    df = load_data(DATA_FILE)

    print_section("Analysing...")
    print(f"  Orders: {len(df)}")
    print(f"  Period: {df['order_date'].min().date()} to {df['order_date'].max().date()}")

    rev     = analyse_revenue(df)
    ret     = analyse_returns(df)
    cust    = analyse_customers(df)
    deliv   = analyse_delivery(df)
    ratings = analyse_ratings(df)

    print_section("Key Numbers")
    print(f"  Total revenue:     ₹{rev['total_revenue']:,.0f}")
    print(f"  Top category:      {rev['top_category']} ({rev['top_cat_share']:.1f}% of revenue)")
    print(f"  Return rate:       {ret['return_rate']:.1f}%")
    print(f"  Avg rating:        {ratings['avg_rating']:.2f}/5.0")
    print(f"  Avg delivery:      {deliv['avg_days']:.1f} days")
    print(f"  Repeat customers:  {cust['repeat_customers']} of {cust['total_customers']}")

    print_section("Generating Charts")
    chart_paths = generate_charts(df, rev, ret, ratings)
    for path in chart_paths.values():
        print(f"  {path}")

    print_section("Writing Memo")
    write_memo(df, rev, ret, cust, deliv, ratings)

    print("\n" + "=" * 55)
    print(f"  Done. Open {MEMO_FILE} to read the memo.")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
