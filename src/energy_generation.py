import pandas as pd
import matplotlib.pyplot as plt

# File path to the CSV
file_path = "ELECSTAT_20250111-190005.csv"

# Load the CSV file into a Pandas DataFrame
try:
    print("Loading the dataset...")
    df = pd.read_csv(file_path, index_col=[0, 1, 2, 3, 4])  # Use multi-index columns
    print("Dataset loaded successfully!")

    # Reset index to flatten the multi-index structure
    print("Resetting index...")
    df = df.reset_index()

    # Rename columns for clarity
    df.columns = ['Country', 'Technology', 'Data Type', 'Grid Connection', 'Year', 'Value']

    # Convert 'Year' to integers and 'Value' to floats
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

    # Drop rows with missing data in essential columns
    df = df.dropna(subset=['Year', 'Value', 'Country'])

    # Display basic information about the dataset
    print("Processed dataset info:")
    print(df.info())

    # Preview of the dataset
    print("Preview of the processed dataset:")
    print(df.head())

    # Example: Visualizing Renewable Energy Production Trends
    renewable_df = df[df['Technology'].str.contains("Renewable", case=False, na=False)]

    plt.figure(figsize=(12, 6))
    for country in renewable_df['Country'].unique():
        country_data = renewable_df[renewable_df['Country'] == country]
        plt.plot(country_data['Year'], country_data['Value'], label=country)

    plt.title("Renewable Energy Production Trends by Country")
    plt.xlabel("Year")
    plt.ylabel("Electricity Generation (GWh)")
    plt.legend(loc="best", fontsize="small")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Error processing the dataset: {e}")