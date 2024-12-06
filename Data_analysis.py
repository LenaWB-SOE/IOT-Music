import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalysisClass:
    def __init__(self, data_csv = "ambient_data.csv"):
        self.sensor_data = pd.read_csv(data_csv)

        print(self.sensor_data.head()) # Display the first few rows
        print(self.sensor_data.info()) # Check the columns and data types
        print(self.sensor_data.describe()) # Summary statistics for numerical columns
        print(self.sensor_data.isnull().sum()) # Check for missing values

        # Convert a timestamp column to datetime
        self.sensor_data['Timestamp'] = pd.to_datetime(self.sensor_data['Timestamp'])
        self.sensor_data.set_index('Timestamp', inplace=True) # Set it as the index for easier time-based analysis

        # Resample data by day and calculate the mean
        daily_mean = self.sensor_data.resample('D').mean()
        print(daily_mean)

        # Group by Label and calculate mean
        grouped_stats = self.sensor_data.groupby('Label').mean()
        print(grouped_stats)

    def boxplot(self, feature):
        # Boxplot for feature by Label
        sns.boxplot(x='Label', y= feature, data=self.sensor_data)
        plt.title(f'{feature} by Label')
        plt.xticks(rotation=45)
        plt.show()

    def histogram(self, feature):
        # Histogram for feature
        sns.histplot(self.sensor_data[feature], kde=True)
        plt.title(f'Distribution of {feature}')
        plt.show()
        #would be good if this was also by label

    def line_plot(self, feature):
        # Line plot for a column over time
        plt.figure(figsize=(10, 5))
        plt.plot(self.sensor_data.index, self.sensor_data['Light RAW'])
        plt.title("Sensor Values Over Time")
        plt.xlabel("Time")
        plt.ylabel("Light RAW")
        plt.show()
        #would maybe be good if this plotted three things on same plot?
        #would be good if this was over the course of a day rather than all time
        #scatter plot

    def correlation_matrix(self):
        # Not very useful
        # Compute correlation matrix
        correlation_matrix = self.sensor_data.corr()

        # Plot heatmap
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix')
        plt.show()

    def pairplot(self):
        # Pairplot for multi-dimensional comparisons
        sns.pairplot(self.sensor_data, hue='Label', diag_kind='kde')
        plt.title('Pairwise Comparison by Label')
        plt.show()





