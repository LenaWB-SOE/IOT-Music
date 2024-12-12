import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os


class DataAnalysisClass:
    def __init__(self, data_csv = "ambient_data.csv"):
        self.sensor_data = pd.read_csv(data_csv)

        # print(self.sensor_data.head()) # Display the first few rows
        # print(self.sensor_data.info()) # Check the columns and data types
        # print(self.sensor_data.describe()) # Summary statistics for numerical columns
        # print(self.sensor_data.isnull().sum()) # Check for missing values

        # Convert a timestamp column to datetime
        self.sensor_data['Timestamp'] = pd.to_datetime(self.sensor_data['Timestamp'])
        self.sensor_data.set_index('Timestamp', inplace=True) # Set it as the index for easier time-based analysis

        # Group by Label and calculate mean
        grouped_stats = self.sensor_data.groupby('Label').mean()
        #print(grouped_stats)

    def boxplot(self, feature):
        # Boxplot for feature by Label
        # sns.boxplot(x='Label', y= feature, data=self.sensor_data)
        # plt.title(f'{feature} by Label')
        # plt.xticks(rotation=45)
        # plt.show()

        # Exclude the label "Wake up" and "Morning work"
        filtered_data1 = self.sensor_data[self.sensor_data["Label"] != "Morning work"]
        filtered_data2 = filtered_data1[filtered_data1["Label"] != "Wake up"]

        # Create the boxplot
        sns.boxplot(data=filtered_data2, x="Label", y= feature)
        plt.title("Boxplot Excluding 'Morning work' and 'Wake up'")
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
        # sns.pairplot(self.sensor_data, hue='Label', diag_kind='kde')
        # plt.title('Pairwise Comparison by Label')
        # plt.show()

        # Exclude the label "Wake up" and "Morning work"
        filtered_data1 = self.sensor_data[self.sensor_data["Label"] != "Morning work"]
        filtered_data2 = filtered_data1[filtered_data1["Label"] != "Wake up"]

        sns.pairplot(filtered_data2, hue='Label', diag_kind='kde')
        plt.title('Pairwise Comparison by Label (Excluding "Wake up" and "Morning work")')
        plt.show()

    def machine_learning(self, save_path="ml_models"):
        # Create a directory for saving model files if it doesn't exist
        os.makedirs(save_path, exist_ok=True)

        # Encode labels as integers
        encoder = LabelEncoder()
        self.sensor_data['Label_encoded'] = encoder.fit_transform(self.sensor_data['Label'])

        # Select features and target
        X = self.sensor_data[['Light RAW', 'Light VOLTAGE', 'Radar AVG', 'Radar STDEV']]
        y = self.sensor_data['Label_encoded']

        # Check the class-to-label mapping
        class_mapping = dict(zip(encoder.classes_, encoder.transform(encoder.classes_)))
        print("Class-to-label mapping:", class_mapping)

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Train Random Forest model
        clf = RandomForestClassifier(random_state=42)
        clf.fit(X_train, y_train)

        # Evaluate the model
        y_pred = clf.predict(X_test)
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        print("Confusion Matrix:")
        print(cm)

        # Plot the confusion matrix as a heatmap
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=encoder.classes_, yticklabels=encoder.classes_)
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.show()

        # Feature importance
        importances = clf.feature_importances_
        for feature, importance in zip(X.columns, importances):
            print(f"{feature}: {importance:.4f}")

        # Save the model, scaler, and encoder
        joblib.dump(clf, f"{save_path}/trained_model.pkl")
        joblib.dump(encoder, f"{save_path}/label_encoder.pkl")

        print(f"Model, scaler, and encoder saved in '{save_path}'.")



def main():
    data_analysis = DataAnalysisClass("ambient_data.csv")

    # data_analysis.boxplot('Light RAW')
    # data_analysis.boxplot('Light VOLTAGE')
    # data_analysis.boxplot('Radar AVG')
    # data_analysis.boxplot('Radar STDEV')

    # data_analysis.pairplot()

    data_analysis.machine_learning()

if __name__ == "__main__":
    main()



