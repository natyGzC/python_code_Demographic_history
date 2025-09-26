
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

# Cargar archivos
df_temp = pd.read_excel("Global_paleo-temperature_Ne_150k_years.xlsx", sheet_name="Hoja1")
df_temp = df_temp.rename(columns={"Age_2": "Time"})
df_temp = df_temp[["Time", "Temp_C"]]

df_ne = pd.read_excel("median_data_total_mexico.xlsx", sheet_name="Sheet 1")
df_ne = df_ne.rename(columns={"x": "Time", "y": "Ne"})

# Interpolación ponderada
def weighted_interpolation(time_val, time_col, ne_col):
    distances = abs(time_col - time_val)
    if 0 in distances.values:
        return ne_col[distances.idxmin()]
    weights = 1 / distances
    return (weights * ne_col).sum() / weights.sum()

df_temp["Ne"] = df_temp["Time"].apply(lambda t: weighted_interpolation(t, df_ne["Time"], df_ne["Ne"]))

# Crear grupos de tiempo
bins = [0, 30000, 60000, 90000, 120000, 150000]
labels = ["0 - 30k years", "30k - 60k years", "60k - 90k years", "90k - 120k years", "120k - 150k years"]
df_temp["Time_group"] = pd.cut(df_temp["Time"], bins=bins, labels=labels, include_lowest=True)

# Calcular correlaciones
correlations = {}
p_values = {}
for group in df_temp["Time_group"].unique():
    subset = df_temp[df_temp["Time_group"] == group]
    if len(subset) > 2:
        r, p = stats.spearmanr(subset["Temp_C"], subset["Ne"])
        correlations[group] = r
        p_values[group] = p

# Guardar scatterplot
plt.figure(figsize=(8, 6))
sns.scatterplot(x=df_temp["Temp_C"], y=df_temp["Ne"], color="darkgreen", alpha=0.5, label="Data Points")
sns.regplot(x=df_temp["Temp_C"], y=df_temp["Ne"], scatter=False, color="red", lowess=True, label="LOESS Model")
plt.xlabel("Temperature (ºC)")
plt.ylabel("Effective Population Size (Ne)")
plt.title("Scatterplot: Temperature (ºC) vs. Effective Population Size (Interpolación Ponderada)", pad=20)
plt.legend()
plt.yticks(range(2500, int(df_temp["Ne"].max()) + 2500, 2500))
plt.savefig("scatterplot_temp_vs_ne_ponderada_300ppi.png", dpi=300, bbox_inches='tight')
plt.close()

# Guardar dual-axis plot
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.set_xlabel("Time (years)")
ax1.set_ylabel("Temperature (ºC)", color="blue")
ax1.plot(df_temp["Time"], df_temp["Temp_C"], color="blue", lw=1, label="Temperature (ºC)")
ax1.tick_params(axis="y", labelcolor="blue")
ax2 = ax1.twinx()
ax2.set_ylabel("Effective Population Size (Ne)", color="green")
ax2.plot(df_temp["Time"], df_temp["Ne"], color="green", lw=1, label="Effective Population Size (Ne)")
ax2.tick_params(axis="y", labelcolor="green")
ax2.set_yticks(range(2500, int(df_temp["Ne"].max()) + 2500, 2500))
ax1.set_xticks(range(0, 150001, 25000))
plt.title("Dual-axis Plot: Temperature (ºC) vs. Effective Population Size (Interpolación Ponderada)", pad=20)
fig.legend(loc="upper left", bbox_to_anchor=(0.15, 0.85))
fig.savefig("dual_axis_temp_vs_ne_ponderada_300ppi.png", dpi=300, bbox_inches='tight')
plt.close()
