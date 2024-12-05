import pandas as pd

# Load data
data = pd.read_csv("ambient_data.csv")

# Display the first few rows
print(data.head())

# Check the columns and data types
print(data.info())

# Summary statistics for numerical columns
print(data.describe())

# Check for missing values
print(data.isnull().sum())

