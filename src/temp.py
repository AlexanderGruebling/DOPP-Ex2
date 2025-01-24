import eurostat
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Fetch and Clean Data for Renewable Energy Sources
dataset_code = 'NRG_BAL_PETC'  # Eurostat dataset for energy balances by product (includes renewable sources)
print("Fetching Eurostat data on renewable energy sources...")
data = eurostat.get_data_df(dataset_code)

# Filter for renewable energy sources only
renewable_sources = [
    'RA100',  # Hydro power
    'RA200',  # Wind power
    'RA300',  # Solar power
    'RA400',  # Geothermal energy
    'RA500',  # Biomass and waste
    'RA600'   # Other renewables
]
data = data[data['nrg_bal'].isin(renewable_sources)]

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

# Step 2: Overall Trends in Renewable Energy Sources Across Europe
data_trends = data_long.groupby("year")["value"].mean().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=data_trends, x="year", y="value", marker="o")
plt.title("Overall Renewable Energy Source Adoption in Europe", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Average Renewable Energy Generation (TWh)", fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 3: Adoption Trends by Specific Renewable Energy Source
energy_types = data_long.groupby(["year", "nrg_bal"])["value"].mean().reset_index()

plt.figure(figsize=(14, 8))
sns.lineplot(data=energy_types, x="year", y="value", hue="nrg_bal", marker="o")
plt.title("Adoption Trends by Renewable Energy Source in Europe", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Average Generation (TWh)", fontsize=12)
plt.legend(title="Energy Source", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 4: Country-Specific Renewable Energy Source Adoption
plt.figure(figsize=(18, 10))
sns.lineplot(data=data_long, x="year", y="value", hue="geo", marker="o", legend="full", ci=None)
plt.title("Country-Specific Renewable Energy Source Adoption Trends", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Renewable Energy Generation (TWh)", fontsize=12)
plt.legend(title="Country", bbox_to_anchor=(1.05, 1), loc="upper left", ncol=2)
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 5: Comparison of Average Renewable Energy Generation by Country
country_averages = data_long.groupby("geo")["value"].mean().reset_index()
country_averages = country_averages.sort_values(by="value", ascending=False)

plt.figure(figsize=(16, 6))
sns.barplot(data=country_averages, x="geo", y="value", palette="viridis")
plt.title("Average Renewable Energy Generation by Country", fontsize=16)
plt.xlabel("Country", fontsize=12)
plt.ylabel("Average Generation (TWh)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
