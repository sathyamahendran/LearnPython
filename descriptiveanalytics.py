import numpy as np # type: ignore
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore


# Numpy : Creating a 1D array
array = np.array([1, 2, 3, 4, 5])
print(f"Numpy 1D Array: {array}")

# Numpy : Creating a 2D array
array_2d = np.array([[1, 2, 3], [4, 5, 6]])
print(f"Numpy 2D Array:\n{array_2d}")

# Pandas: Creating a DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35]}
df = pd.DataFrame(data)
print(f"Pandas DataFrame:\n{df}")

# Working with Data 
url = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv'
tips = pd.read_csv(url)
print(tips.head())

# Exploring the Data

#Checking the dimensions of the dataset
print(f"Dataset Dimensions: {tips.shape}")
#Displaying the data types of each column 
print(f"Data Types:\n{tips.dtypes}")
#Summary statistics of the numeric columns
print(f"Summary Statistics:\n{tips.describe()}")

# Cleaning the Data
#Checking for missing values
print(f"Missing Values:\n{tips.isnull().sum()}")
#Dropping rows with missing values (if any)
tips_cleaned = tips.dropna()
#Removing duplicates
tips_cleaned = tips_cleaned.drop_duplicates()
#Displaying the cleaned dataset
print(f"Cleaned Dataset:\n{tips_cleaned.head()}")
print(f"Summary Statistics:\n{tips_cleaned.describe()}")

# Descriptive Statistics
#Calculating mean, median, and standard deviation for the 'total_bill' column
mean_total_bill = tips_cleaned['total_bill'].mean()
print(f"Mean Total Bill: {mean_total_bill}")
median_total_bill = tips_cleaned['total_bill'].median()
print(f"Median Total Bill: {median_total_bill}")
std_total_bill = tips_cleaned['total_bill'].std()
print(f"Standard Deviation of Total Bill: {std_total_bill}")

#Basic Visualizations
#Histogram of total bill
sns.histplot(tips_cleaned['total_bill'], kde=True)
plt.title('Distribution of Total Bill')
plt.xlabel('Total Bill')
plt.ylabel('Frequency')
plt.show()

#Bar Chart of Total Bill by Day
sns.barplot(x='day', y='total_bill', data=tips_cleaned)
plt.title('Average Total Bill by Day')
plt.xlabel('Day of the Week')
plt.ylabel('Average Total Bill')
plt.show()

#Scatter Plot of Total Bill vs Tip
sns.scatterplot(x='total_bill', y='tip', data=tips_cleaned)
plt.title('Total Bill vs Tip')
plt.xlabel('Total Bill')
plt.ylabel('Tip')
plt.show()


# Correlation Heatmap
plt.figure(figsize=(10, 6))
correlation_matrix = tips_cleaned.corr(numeric_only=True)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm',
            linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()
# Pairplot
sns.pairplot(tips_cleaned, hue='sex')
plt.suptitle('Pairplot of Features by Sex', y=1.02)
plt.show()
# Boxplot of Total Bill by Day and Time
sns.boxplot(x='day', y='total_bill', hue='time', data=tips_cleaned)
plt.title('Boxplot of Total Bill by Day and Time')
plt.show()
# Violin Plot of Tip by Day
sns.violinplot(x='day', y='tip', data=tips_cleaned)
plt.title('Violin Plot of Tip by Day')
plt.show()
# Swarm Plot of Total Bill by Day and Time
sns.swarmplot(x='day', y='total_bill', hue='time', data=tips_cleaned)
plt.title('Swarm Plot of Total Bill by Day and Time')
plt.show()