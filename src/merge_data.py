import eurostat
import pandas as pd
import wbgapi as wb

electstat_file_path = "data/ELECSTAT_20250111-190005.csv"

# ELECTSTAT: Statistics regarding energy generation
electstat = pd.read_csv(electstat_file_path, index_col=[0, 1, 2, 3, 4])
print(electstat.head())

# EUROSTAT: Statistics regarding renewable energy adoption
dataset_code = 'NRG_IND_REN' 
data = eurostat.get_data_df(dataset_code)
data.rename(columns={"geo\\TIME_PERIOD": "geo"}, inplace=True)
data_long = data.melt(id_vars=["geo", "freq", "nrg_bal", "unit"], var_name="year", value_name="value")
data_long["year"] = pd.to_numeric(data_long["year"], errors="coerce")
data_long = data_long.dropna(subset=["value", "year"])
data_long["value"] = pd.to_numeric(data_long["value"], errors="coerce")
print(data_long.head())

# EUROSTAT: Statistics regarding renewable energy sources
# dataset_code = 'NRG_BAL_C'
# data = eurostat.get_data_df(dataset_code)

# renewable_sources = [
#     'RA100',  # Hydro power
#     'RA200',  # Wind power
#     'RA300',  # Solar power
#     'RA400',  # Geothermal energy
#     'RA500',  # Biomass and waste
#     'RA600'   # Other renewables
# ]
# data = data[data['nrg_bal'].isin(renewable_sources)]
# data.rename(columns={"geo\\TIME_PERIOD": "geo"}, inplace=True)
# data_long = data.melt(id_vars=["geo", "freq", "nrg_bal", "unit"], var_name="year", value_name="value")
# data_long["year"] = pd.to_numeric(data_long["year"], errors="coerce")
# data_long = data_long.dropna(subset=["value", "year"])
# data_long["value"] = pd.to_numeric(data_long["value"], errors="coerce")

# print(data_long.head())


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

print(df.head())

