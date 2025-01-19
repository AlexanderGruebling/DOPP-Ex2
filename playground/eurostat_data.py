import eurostat
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Fetch and Clean Data
dataset_code = 'NRG_IND_REN'  # Eurostat dataset for renewable energy adoption
print("Fetching Eurostat data...")
data = eurostat.get_data_df(dataset_code)

# Rename columns for clarity
data.rename(columns={"geo\\TIME_PERIOD": "geo"}, inplace=True)

# Reshape data to long format
data_long = data.melt(id_vars=["geo", "freq", "nrg_bal", "unit"], var_name="year", value_name="value")

# Convert 'year' to numeric and clean data
data_long["year"] = pd.to_numeric(data_long["year"], errors="coerce")
data_long = data_long.dropna(subset=["value", "year"])
data_long["value"] = pd.to_numeric(data_long["value"], errors="coerce")

print("Data cleaned. Here's a preview:")
print(data_long.head())

# Step 2: Overall Trends in Renewable Energy Adoption Across Europe
data_trends = data_long.groupby("year")["value"].mean().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=data_trends, x="year", y="value", marker="o")
plt.title("Overall Renewable Energy Adoption in Europe", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Average Renewable Energy Adoption (%)", fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 3: Adoption Trends by Energy Type
energy_types = data_long.groupby(["year", "nrg_bal"])["value"].mean().reset_index()

plt.figure(figsize=(14, 8))
sns.lineplot(data=energy_types, x="year", y="value", hue="nrg_bal", marker="o")
plt.title("Adoption Trends by Renewable Energy Type in Europe", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Average Adoption (%)", fontsize=12)
plt.legend(title="Energy Type", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 4: Country-Specific Renewable Energy Adoption (All European Countries)
plt.figure(figsize=(18, 10))

sns.lineplot(data=data_long, x="year", y="value", hue="geo", marker="o", legend="full", ci=None)
plt.title("Country-Specific Renewable Energy Adoption Trends (All European Countries)", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Renewable Energy Adoption (%)", fontsize=12)
plt.legend(title="Country", bbox_to_anchor=(1.05, 1), loc="upper left", ncol=2)
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 5: Comparison of Average Renewable Energy Adoption by Country
country_averages = data_long.groupby("geo")["value"].mean().reset_index()
country_averages = country_averages.sort_values(by="value", ascending=False)

plt.figure(figsize=(16, 6))
sns.barplot(data=country_averages, x="geo", y="value", palette="viridis")
plt.title("Average Renewable Energy Adoption by Country", fontsize=16)
plt.xlabel("Country", fontsize=12)
plt.ylabel("Average Adoption (%)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()