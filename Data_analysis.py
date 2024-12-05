import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Convert a timestamp column to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Set it as the index for easier time-based analysis
data.set_index('timestamp', inplace=True)

# Line plot for a column over time
plt.figure(figsize=(10, 5))
plt.plot(data.index, data['sensor_value'])
plt.title("Sensor Values Over Time")
plt.xlabel("Time")
plt.ylabel("Sensor Value")
plt.show()

# Histogram to see distribution
plt.figure(figsize=(8, 5))
sns.histplot(data['sensor_value'], bins=30, kde=True)
plt.title("Distribution of Sensor Values")
plt.show()

