import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
sensor_data = pd.read_csv("ambient_data.csv")




print(sensor_data.head()) # Display the first few rows
print(sensor_data.info()) # Check the columns and data types
print(sensor_data.describe()) # Summary statistics for numerical columns
print(sensor_data.isnull().sum()) # Check for missing values


# Convert a timestamp column to datetime
sensor_data['Timestamp'] = pd.to_datetime(sensor_data['Timestamp'])
sensor_data.set_index('Timestamp', inplace=True) # Set it as the index for easier time-based analysis

# Histogram for Light RAW
sns.histplot(sensor_data['Light RAW'], kde=True)
plt.title('Distribution of Light RAW')
plt.show()

# Boxplot for Radar AVG by Label
sns.boxplot(x='Label', y='Radar AVG', data=sensor_data)
plt.title('Radar AVG by Label')
plt.xticks(rotation=45)
plt.show()

# Resample data by day and calculate the mean
daily_mean = sensor_data.resample('D').mean()
print(daily_mean)


# Line plot for a column over time
plt.figure(figsize=(10, 5))
plt.plot(sensor_data.index, sensor_data['Light RAW'])
plt.title("Sensor Values Over Time")
plt.xlabel("Time")
plt.ylabel("Light RAW")
plt.show()

# Histogram to see distribution
plt.figure(figsize=(8, 5))
sns.histplot(sensor_data['Light RAW'], bins=30, kde=True)
plt.title("Distribution of Sensor Values")
plt.show()

# Compute correlation matrix
correlation_matrix = sensor_data.corr()

# Plot heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()

# Group by Label and calculate mean
grouped_stats = sensor_data.groupby('Label').mean()
print(grouped_stats)

# Pairplot for multi-dimensional comparisons
sns.pairplot(sensor_data, hue='Label', diag_kind='kde')
plt.title('Pairwise Comparison by Label')
plt.show()

