# Insight Memo — E-Commerce Performance
**Prepared:** 15 June 2026  
**Data Period:** 05 Jan – 24 Mar 2024  
**Dataset:** `data/ecommerce_sample.csv` (70 orders)

---
## Executive Summary
The business processed **70 orders** worth **₹340,940** in the period 05 Jan – 24 Mar 2024. **Electronics** is the top revenue driver at 79.4% of total revenue. Overall return rate is **8.6%**, and average customer rating is **4.09/5.0**.

---
## 1. Revenue
| Metric | Value |
|--------|-------|
| Total Revenue | ₹340,940 |
| Total Orders | 70 |
| Average Order Value | ₹4,871 |
| Total Units Sold | 181 |
| Best Month | 2024-02 (↓ 26.9% vs previous month) |

**Revenue by Category:**

| Category | Revenue | Share |
|----------|---------|-------|
| Electronics | ₹270,700 | 79.4% |
| Clothing | ₹44,050 | 12.9% |
| Books | ₹14,050 | 4.1% |
| Food | ₹12,140 | 3.6% |

**Finding:** Electronics contributes 79.4% of revenue despite being a single category. Books and Food have higher order counts but lower order values.

---
## 2. Returns
| Metric | Value |
|--------|-------|
| Total Returns | 6 orders (8.6%) |
| Avg Rating (Returned) | 2.67/5.0 |
| Avg Rating (Not Returned) | 4.22/5.0 |
| High-Value Returns (>₹10,000) | 3 orders |

**Return Rate by Category:**

| Category | Return Rate |
|----------|-------------|
| Electronics | 30.0% ⚠ |
| Books | 0.0% |
| Clothing | 0.0% |
| Food | 0.0% |

**Finding:** Returned orders have a 1.6-point lower average rating (2.67 vs 4.22). This confirms returns are driven by dissatisfaction, not just remorse purchases. High-value Electronics returns have the most financial impact.

---
## 3. Customers & Geography
| Metric | Value |
|--------|-------|
| Unique Customers | 56 |
| Repeat Customers (2+ orders) | 5 (8.9%) |
| Top Customer | C012 (6 orders, ₹33,200) |

**Top 5 States by Revenue:**

| State | Revenue |
|-------|--------|
| Maharashtra | ₹57,820 |
| Tamil Nadu | ₹36,860 |
| West Bengal | ₹35,400 |
| Karnataka | ₹31,370 |
| Rajasthan | ₹24,940 |

**Top 5 Cities by Revenue:**

| City | Revenue |
|------|--------|
| Kolkata | ₹35,400 |
| Mumbai | ₹33,200 |
| Srinagar | ₹21,500 |
| Chennai | ₹20,120 |
| Nashik | ₹19,800 |

**Finding:** 8.9% of customers placed more than one order. Repeat customers are a high-value segment — a loyalty programme could increase this rate.

---
## 4. Delivery Performance
| Metric | Value |
|--------|-------|
| Avg Delivery Time | 3.2 days |
| Median Delivery Time | 3.0 days |
| Orders Taking > 5 Days | 11 (15.7%) |
| Rating–Delivery Days Correlation | -0.380 |

**Avg Delivery Days by Category:**

| Category | Avg Days |
|----------|----------|
| Electronics | 5.5 |
| Books | 3.1 |
| Clothing | 3.0 |
| Food | 1.0 |

**Finding:** The correlation between delivery time and rating is -0.380 (negative). Longer delivery times are associated with lower ratings. 15.7% of orders took more than 5 days — these are highest-risk for low ratings.

---
## 5. Customer Satisfaction
| Metric | Value |
|--------|-------|
| Overall Avg Rating | 4.09/5.0 |
| Orders Rated < 3.5 | 6 |
| Orders Rated ≥ 4.5 | 17 |

**Avg Rating by Category:**

| Category | Avg Rating |
|----------|-----------|
| Food | 4.41/5.0 |
| Clothing | 4.00/5.0 |
| Books | 3.97/5.0 ⚠ |
| Electronics | 3.96/5.0 ⚠ |

**Finding:** Electronics has the lowest average rating. Low ratings in high-return categories amplify each other — fixing delivery speed in these categories would likely improve both returns and ratings.

---
## 6. Recommendations

| Priority | Recommendation | Evidence |
|----------|---------------|----------|
| **HIGH** | Investigate Electronics return causes | 30.0% return rate — highest of all categories |
| **HIGH** | Reduce orders with delivery > 5 days | 15.7% of orders exceed 5 days; correlates with low ratings |
| **MEDIUM** | Launch loyalty programme for repeat customers | 5 repeat customers generate disproportionate revenue |
| **MEDIUM** | Expand presence in Maharashtra | ₹57,820 — largest revenue state by far |
| **LOW** | Review discount strategy | Discounted orders should be tracked for margin impact |

---
## 7. Data Notes
- Dataset: `data/ecommerce_sample.csv` (synthetic data — 70 orders)
- For production: replace with real export from your order management system
- Real dataset suggestion: Olist Brazilian E-Commerce on Kaggle
  (`https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce`)
- Memo generated: 15 June 2026
