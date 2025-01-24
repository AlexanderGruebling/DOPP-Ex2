import wbgapi as wb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Define countries and indicators
countries = [
    "AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA",
    "DEU", "GRC", "HUN", "ISL", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT",
    "NLD", "NOR", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE", "CHE", "GBR"
]  # ISO codes for European countries

indicators = {
    "NY.GDP.MKTP.CD": "GDP",  # GDP in current USD
    "SP.POP.TOTL": "Population",  # Total population
    "SP.URB.TOTL.IN.ZS": "Urbanization Rate"  # Urbanization percentage
}

# Step 2: Fetch data for all indicators
print("Fetching data from World Bank...")
data_frames = {}
try:
    for indicator, name in indicators.items():
        print(f"Fetching {name} data...")
        df = wb.data.DataFrame(indicator, countries, time=range(2000, 2025), labels=True)
        df = df.reset_index().melt(id_vars=["Country"], var_name="year", value_name=name)
        
        # Use raw string for regex and handle missing years
        df["year"] = df["year"].str.extract(r"(\d+)$")  # Extract year as string
        df = df.dropna(subset=["year", name])  # Drop rows with missing years or values
        df["year"] = df["year"].astype(int)  # Convert year to integer
        df[name] = pd.to_numeric(df[name], errors="coerce")  # Convert values to numeric
        
        # Store cleaned data
        data_frames[name] = df
    print("Data fetched successfully!")
except Exception as e:
    print(f"Error fetching data: {e}")
    data_frames = {}

# Step 3: Visualize data
def plot_data(data, y, title, ylabel):
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=data, x="year", y=y, hue="Country", alpha=0.7)
    plt.title(title, fontsize=16)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.legend(title="Country", bbox_to_anchor=(1.05, 1), loc="upper left")  # Add legend
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Plot GDP
if "GDP" in data_frames:
    plot_data(data_frames["GDP"], "GDP", "GDP Trends Across European Countries", "GDP (Current USD)")

# Plot Population
if "Population" in data_frames:
    plot_data(data_frames["Population"], "Population", "Population Trends Across European Countries", "Population")

# Plot Urbanization Rate
if "Urbanization Rate" in data_frames:
    plot_data(data_frames["Urbanization Rate"], "Urbanization Rate", "Urbanization Rate Trends Across European Countries", "Urbanization Rate (%)")