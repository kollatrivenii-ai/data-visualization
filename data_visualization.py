"""
Data Visualization - Simple Base Project
----------------------------------------
Creates sample sales data and shows 6 common chart types:
line, bar, pie, histogram, scatter and heatmap.

Install:  pip install pandas numpy matplotlib seaborn
Run:      python data_visualization.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
np.random.seed(42)

# ---------------------------------------------------------------
# 1. CREATE / LOAD DATA
# ---------------------------------------------------------------
# To use your own file instead, replace this block with:
#   df = pd.read_csv("your_file.csv")
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
categories = ["Electronics", "Clothing", "Grocery", "Furniture", "Toys"]

rows = []
for m in months:
    for c in categories:
        sales = np.random.randint(2000, 10000)
        rows.append({
            "Month": m,
            "Category": c,
            "Sales": sales,
            "Profit": int(sales * np.random.uniform(0.05, 0.30)),
            "Customers": np.random.randint(50, 500),
        })

df = pd.DataFrame(rows)
df["Month"] = pd.Categorical(df["Month"], categories=months, ordered=True)

print("First 5 rows:\n", df.head(), "\n")
print("Summary statistics:\n", df.describe(), "\n")

# ---------------------------------------------------------------
# 2. PREPARE AGGREGATED DATA
# ---------------------------------------------------------------
monthly_sales = df.groupby("Month", observed=True)["Sales"].sum()
category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
pivot = df.pivot_table(index="Category", columns="Month",
                       values="Sales", aggfunc="sum", observed=True)

# ---------------------------------------------------------------
# 3. DASHBOARD WITH 6 CHARTS
# ---------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Sales Data Visualization Dashboard", fontsize=20, fontweight="bold")

# (a) Line chart - trend over time
axes[0, 0].plot(monthly_sales.index, monthly_sales.values,
                marker="o", color="tab:blue", linewidth=2)
axes[0, 0].set_title("Monthly Sales Trend (Line)")
axes[0, 0].set_xlabel("Month")
axes[0, 0].set_ylabel("Total Sales")
axes[0, 0].tick_params(axis="x", rotation=45)

# (b) Bar chart - compare categories
axes[0, 1].bar(category_sales.index, category_sales.values,
               color=sns.color_palette("viridis", len(category_sales)))
axes[0, 1].set_title("Sales by Category (Bar)")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Total Sales")
axes[0, 1].tick_params(axis="x", rotation=45)

# (c) Pie chart - share of total
axes[0, 2].pie(category_sales.values, labels=category_sales.index,
               autopct="%1.1f%%", startangle=90,
               colors=sns.color_palette("pastel"))
axes[0, 2].set_title("Category Share (Pie)")

# (d) Histogram - distribution
axes[1, 0].hist(df["Sales"], bins=15, color="tab:orange", edgecolor="black")
axes[1, 0].set_title("Sales Distribution (Histogram)")
axes[1, 0].set_xlabel("Sales")
axes[1, 0].set_ylabel("Frequency")

# (e) Scatter plot - relationship between two variables
sns.scatterplot(data=df, x="Customers", y="Sales", hue="Category",
                ax=axes[1, 1], s=60)
axes[1, 1].set_title("Customers vs Sales (Scatter)")

# (f) Heatmap - category x month
sns.heatmap(pivot, cmap="YlGnBu", ax=axes[1, 2], cbar_kws={"label": "Sales"})
axes[1, 2].set_title("Sales Heatmap (Category x Month)")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("dashboard.png", dpi=150)
print("Dashboard saved as dashboard.png")
plt.show()
