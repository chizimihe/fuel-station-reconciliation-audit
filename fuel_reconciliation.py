
import pandas as pd
import numpy as np

# 1. SIMULATE STATION DATA
np.random.seed(42)

days = pd.date_range(start="2026-10-01", periods=10, freq="D")

# POS sales in litres
pos_sales = {
    "Fuel_P1": [1000, 950, 1100, 980, 1050, 1020, 990, 1080, 970, 1000],
    "Fuel_P2": [800, 850, 820, 900, 880, 870, 910, 860, 890, 920]
}

df_pos = pd.DataFrame(pos_sales, index=days)

# 2. PHYSICAL METER READINGS
p1_physical = [1000.2, 949.9, 1100.3, 980.0, 1049.8,
               1020.1, 990.2, 1079.9, 970.2, 1005.0]

p2_physical = [800.0, 850.2, 819.9, 900.1, 880.0,
               895.0, 910.2, 859.8, 890.1, 920.0]

# Generate cumulative meter readings
p1_opening = [10000]
p2_opening = [20000]

for i in range(1, len(days)):
    p1_opening.append(p1_opening[-1] + p1_physical[i-1])
    p2_opening.append(p2_opening[-1] + p2_physical[i-1])

meter_data = {
    "P1_Opening": p1_opening,
    "P1_Closing": np.array(p1_opening) + p1_physical,
    "P2_Opening": p2_opening,
    "P2_Closing": np.array(p2_opening) + p2_physical
}

df_meters = pd.DataFrame(meter_data, index=days)

# 3. COMBINE DATASETS
df_recon = pd.concat([df_pos, df_meters], axis=1)

# 4. CALCULATE PHYSICAL VOLUME DISPENSED
df_recon["P1_Meter_Dispensed"] = df_recon["P1_Closing"] - df_recon["P1_Opening"]
df_recon["P2_Meter_Dispensed"] = df_recon["P2_Closing"] - df_recon["P2_Opening"]

# 5. CALCULATE VARIANCES
df_recon["P1_Variance_Liters"] = df_recon["P1_Meter_Dispensed"] - df_recon["Fuel_P1"]
df_recon["P2_Variance_Liters"] = df_recon["P2_Meter_Dispensed"] - df_recon["Fuel_P2"]

# 6. CALCULATE VARIANCE PERCENTAGES
df_recon["P1_Variance_Pct"] = (
    df_recon["P1_Variance_Liters"] / df_recon["Fuel_P1"].replace(0, np.nan)
) * 100

df_recon["P2_Variance_Pct"] = (
    df_recon["P2_Variance_Liters"] / df_recon["Fuel_P2"].replace(0, np.nan)
) * 100

# 7. FLAG ANOMALIES
THRESHOLD_PCT = 0.5

df_recon["P1_Status"] = np.where(
    df_recon["P1_Variance_Pct"].abs() > THRESHOLD_PCT,
    "FLAGGED", "OK"
)

df_recon["P2_Status"] = np.where(
    df_recon["P2_Variance_Pct"].abs() > THRESHOLD_PCT,
    "FLAGGED", "OK"
)

# 8. DISPLAY AUDIT REPORT
columns_to_show = [
    "Fuel_P1", "P1_Meter_Dispensed",
    "P1_Variance_Liters", "P1_Status",
    "Fuel_P2", "P2_Meter_Dispensed",
    "P2_Variance_Liters", "P2_Status"
]

print("\n--- FUEL STATION RECONCILIATION AUDIT REPORT ---")
print(df_recon[columns_to_show].round(2).to_string())

# 9. AUDIT EXCEPTIONS LOG
print("\n--- AUDIT EXCEPTIONS LOG ---")

for pump, status_col, variance_col, pct_col in [
    ("Pump 1", "P1_Status", "P1_Variance_Liters", "P1_Variance_Pct"),
    ("Pump 2", "P2_Status", "P2_Variance_Liters", "P2_Variance_Pct")
]:
    flagged = df_recon[df_recon[status_col] == "FLAGGED"]

    for date, row in flagged.iterrows():
        print(
            f"[ALERT] {date.strftime('%Y-%m-%d')} | {pump} | "
            f"Variance: {row[variance_col]:.1f} L "
            f"({row[pct_col]:.2f}%)"
        )

# 10. AUDIT SUMMARY
print("\n--- AUDIT SUMMARY ---")
print("Total Days Audited:", len(df_recon))
print("Pump 1 Exceptions:", (df_recon["P1_Status"] == "FLAGGED").sum())
print("Pump 2 Exceptions:", (df_recon["P2_Status"] == "FLAGGED").sum())

print(
    "Total Exceptions:",
    (df_recon["P1_Status"] == "FLAGGED").sum()
    + (df_recon["P2_Status"] == "FLAGGED").sum()
)
