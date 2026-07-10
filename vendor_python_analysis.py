# ============================================================
# VENDOR SALES PERFORMANCE - Python EDA & Visualizations
# Tools: pandas, numpy, matplotlib, seaborn
# ============================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Styling ────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
COLORS = ["#2196F3","#FF5722","#4CAF50","#9C27B0","#FF9800",
          "#00BCD4","#E91E63","#8BC34A","#795548","#607D8B"]
plt.rcParams.update({"figure.dpi":150,"font.family":"DejaVu Sans"})

# ============================================================
# STEP 1 – LOAD DATA
# ============================================================
df = pd.read_csv("/home/claude/vendor_sales_data.csv", parse_dates=["Order_Date"])
print("Shape:", df.shape)
print(df.dtypes)
print("\nMissing values:\n", df.isnull().sum())

# ============================================================
# STEP 2 – DATA CLEANING
# ============================================================
# Fill missing Discount with median (robust to outliers)
df["Discount"].fillna(df["Discount"].median(), inplace=True)

# Fill missing Profit: derive from Sales * avg profit margin
avg_margin = (df["Profit"] / df["Sales_Amount"]).dropna().median()
df["Profit"].fillna(df["Sales_Amount"] * avg_margin, inplace=True)

# Feature engineering
df["Month"]        = df["Order_Date"].dt.to_period("M").astype(str)
df["Year"]         = df["Order_Date"].dt.year
df["Month_Name"]   = df["Order_Date"].dt.strftime("%b %Y")
df["Profit_Margin"]= (df["Profit"] / df["Sales_Amount"] * 100).round(2)

print("\nAfter cleaning – missing:\n", df.isnull().sum())
print("\nBasic Stats:\n", df[["Sales_Amount","Profit","Discount","Quantity"]].describe().round(2))

# ============================================================
# STEP 3 – KPI SUMMARY
# ============================================================
total_sales  = df["Sales_Amount"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order_ID"].nunique()
avg_discount = df["Discount"].mean() * 100
top_vendor   = df.groupby("Vendor_Name")["Sales_Amount"].sum().idxmax()

print(f"\n{'='*50}")
print(f"Total Sales  : ₹{total_sales:,.0f}")
print(f"Total Profit : ₹{total_profit:,.0f}")
print(f"Total Orders : {total_orders}")
print(f"Avg Discount : {avg_discount:.1f}%")
print(f"Top Vendor   : {top_vendor}")
print(f"{'='*50}")

# ============================================================
# STEP 4 – AGGREGATIONS
# ============================================================
vendor_sales = (df.groupby("Vendor_Name")
                  .agg(Total_Sales=("Sales_Amount","sum"),
                       Total_Profit=("Profit","sum"),
                       Orders=("Order_ID","count"))
                  .sort_values("Total_Sales", ascending=False)
                  .reset_index())

region_sales = (df.groupby("Region")
                  .agg(Total_Sales=("Sales_Amount","sum"),
                       Total_Profit=("Profit","sum"))
                  .reset_index())

monthly_sales = (df.groupby("Month")["Sales_Amount"].sum()
                   .reset_index().sort_values("Month"))

category_sales = (df.groupby("Product_Category")
                    .agg(Total_Sales=("Sales_Amount","sum"),
                         Total_Profit=("Profit","sum"))
                    .sort_values("Total_Sales", ascending=False)
                    .reset_index())

# ============================================================
# STEP 5 – VISUALIZATIONS (3 figures, each saved separately)
# ============================================================

# --- Figure 1: Overview Dashboard (2x2) ----------------------
fig1, axes = plt.subplots(2, 2, figsize=(16, 11))
fig1.suptitle("Vendor Sales Performance – Overview", fontsize=16, fontweight="bold", y=1.01)

# 5a. Top 10 Vendors by Sales (horizontal bar)
ax = axes[0,0]
v10 = vendor_sales.head(10)
bars = ax.barh(v10["Vendor_Name"][::-1], v10["Total_Sales"][::-1]/1e6, color=COLORS[:10])
ax.set_xlabel("Total Sales (₹ Millions)")
ax.set_title("Top 10 Vendors by Sales", fontweight="bold")
for bar, val in zip(bars, v10["Total_Sales"][::-1]/1e6):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
            f"₹{val:.1f}M", va="center", fontsize=8)

# 5b. Region-wise Sales (pie)
ax = axes[0,1]
ax.pie(region_sales["Total_Sales"], labels=region_sales["Region"],
       autopct="%1.1f%%", colors=COLORS[:5], startangle=140,
       wedgeprops=dict(edgecolor="white",linewidth=1.5))
ax.set_title("Region-wise Sales Distribution", fontweight="bold")

# 5c. Monthly Sales Trend (line)
ax = axes[1,0]
ax.plot(range(len(monthly_sales)), monthly_sales["Sales_Amount"]/1e6,
        marker="o", linewidth=2, color="#2196F3", markersize=4)
ax.fill_between(range(len(monthly_sales)), monthly_sales["Sales_Amount"]/1e6,
                alpha=0.15, color="#2196F3")
tick_step = max(1, len(monthly_sales)//8)
ax.set_xticks(range(0, len(monthly_sales), tick_step))
ax.set_xticklabels(monthly_sales["Month"].iloc[::tick_step], rotation=45, ha="right", fontsize=8)
ax.set_ylabel("Sales (₹ Millions)")
ax.set_title("Monthly Sales Trend (2023–2024)", fontweight="bold")

# 5d. Category Sales (bar)
ax = axes[1,1]
cat_sorted = category_sales.sort_values("Total_Sales")
ax.barh(cat_sorted["Product_Category"], cat_sorted["Total_Sales"]/1e6,
        color=COLORS[:len(cat_sorted)])
ax.set_xlabel("Total Sales (₹ Millions)")
ax.set_title("Sales by Product Category", fontweight="bold")

plt.tight_layout()
fig1.savefig("/home/claude/fig1_overview.png", bbox_inches="tight", dpi=150)
plt.close()

# --- Figure 2: Profit & Discount Analysis (2x2) --------------
fig2, axes = plt.subplots(2, 2, figsize=(16, 11))
fig2.suptitle("Profit & Discount Analysis", fontsize=16, fontweight="bold")

# 5e. Sales vs Profit (scatter)
ax = axes[0,0]
scatter = ax.scatter(df["Sales_Amount"]/1e3, df["Profit"]/1e3,
                     c=df["Discount"], cmap="RdYlGn_r", alpha=0.6, s=20)
plt.colorbar(scatter, ax=ax, label="Discount Rate")
ax.set_xlabel("Sales Amount (₹ '000)")
ax.set_ylabel("Profit (₹ '000)")
ax.set_title("Sales vs Profit (colored by Discount)", fontweight="bold")

# 5f. Discount distribution (histogram)
ax = axes[0,1]
ax.hist(df["Discount"]*100, bins=20, color="#FF5722", edgecolor="white", alpha=0.8)
ax.axvline(df["Discount"].mean()*100, color="navy", linestyle="--",
           label=f"Mean: {df['Discount'].mean()*100:.1f}%")
ax.set_xlabel("Discount (%)")
ax.set_ylabel("Frequency")
ax.set_title("Discount Distribution", fontweight="bold")
ax.legend()

# 5g. Vendor Profit Margin (bar)
ax = axes[1,0]
vm = vendor_sales.copy()
vm["Margin%"] = (vm["Total_Profit"]/vm["Total_Sales"]*100).round(1)
vm_sorted = vm.sort_values("Margin%", ascending=True)
colors_margin = ["#4CAF50" if x >= 20 else "#FF9800" if x >= 15 else "#F44336"
                 for x in vm_sorted["Margin%"]]
ax.barh(vm_sorted["Vendor_Name"], vm_sorted["Margin%"], color=colors_margin)
ax.axvline(vm["Margin%"].mean(), color="navy", linestyle="--",
           label=f"Avg: {vm['Margin%'].mean():.1f}%")
ax.set_xlabel("Profit Margin (%)")
ax.set_title("Profit Margin by Vendor", fontweight="bold")
ax.legend(fontsize=8)

# 5h. Category Profit vs Sales (grouped bar)
ax = axes[1,1]
x = np.arange(len(category_sales))
w = 0.35
ax.bar(x - w/2, category_sales["Total_Sales"]/1e6, w, label="Sales", color="#2196F3", alpha=0.85)
ax.bar(x + w/2, category_sales["Total_Profit"]/1e6, w, label="Profit", color="#4CAF50", alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(category_sales["Product_Category"], rotation=40, ha="right", fontsize=7)
ax.set_ylabel("₹ Millions")
ax.set_title("Sales vs Profit by Category", fontweight="bold")
ax.legend()

plt.tight_layout()
fig2.savefig("/home/claude/fig2_profit.png", bbox_inches="tight", dpi=150)
plt.close()

# --- Figure 3: Advanced Insights (2x2) -----------------------
fig3, axes = plt.subplots(2, 2, figsize=(16, 11))
fig3.suptitle("Advanced Analytics & Insights", fontsize=16, fontweight="bold")

# 5i. Year-over-Year monthly comparison
ax = axes[0,0]
for yr, col in zip([2023,2024],["#2196F3","#FF5722"]):
    yd = df[df["Year"]==yr].groupby(df["Order_Date"].dt.month)["Sales_Amount"].sum()/1e6
    ax.plot(yd.index, yd.values, marker="o", label=str(yr), color=col, linewidth=2)
ax.set_xticks(range(1,13))
ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
ax.set_ylabel("Sales (₹ Millions)")
ax.set_title("Year-over-Year Monthly Comparison", fontweight="bold")
ax.legend()

# 5j. Region × Category heatmap
ax = axes[0,1]
heat = df.pivot_table(values="Sales_Amount", index="Region",
                      columns="Product_Category", aggfunc="sum", fill_value=0)
heat_norm = heat.div(1e6)
sns.heatmap(heat_norm, ax=ax, cmap="Blues", annot=True, fmt=".1f",
            linewidths=0.5, cbar_kws={"label":"Sales (₹M)"})
ax.set_title("Region × Category Sales Heatmap (₹M)", fontweight="bold")
ax.tick_params(axis='x', rotation=40)

# 5k. Top 5 vendors quarterly (stacked bar)
ax = axes[1,0]
df["Quarter"] = df["Order_Date"].dt.to_period("Q").astype(str)
top5 = vendor_sales.head(5)["Vendor_Name"].tolist()
qv = (df[df["Vendor_Name"].isin(top5)]
        .groupby(["Quarter","Vendor_Name"])["Sales_Amount"].sum()/1e6
        .unstack(fill_value=0).reset_index(drop=True) if False else (df[df["Vendor_Name"].isin(top5)].groupby(["Quarter","Vendor_Name"])["Sales_Amount"].sum()/1e6).unstack(fill_value=0))
qv.plot(kind="bar", ax=ax, color=COLORS[:5], alpha=0.9, width=0.8)
ax.set_xlabel("")
ax.set_ylabel("Sales (₹ Millions)")
ax.set_title("Top 5 Vendors – Quarterly Sales", fontweight="bold")
ax.legend(fontsize=7, loc="upper right")
ax.tick_params(axis='x', rotation=30)

# 5l. Orders per region (donut)
ax = axes[1,1]
reg_orders = df.groupby("Region")["Order_ID"].count()
wedges, texts, autotexts = ax.pie(reg_orders, labels=reg_orders.index,
                                   autopct="%1.1f%%", colors=COLORS[:5],
                                   startangle=90, pctdistance=0.8,
                                   wedgeprops=dict(width=0.6, edgecolor="white"))
ax.set_title("Order Count by Region", fontweight="bold")

plt.tight_layout()
fig3.savefig("/home/claude/fig3_advanced.png", bbox_inches="tight", dpi=150)
plt.close()

print("\nAll 3 figures saved successfully.")
print(f"\nVendor Sales Summary:\n{vendor_sales.to_string(index=False)}")
