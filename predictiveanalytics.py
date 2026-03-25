import numpy as np # type: ignore
import pandas as pd # type: ignore
from sklearn.datasets import fetch_california_housing # type: ignore



# Load the California housing dataset
california = fetch_california_housing()
print(f"California Housing Dataset Keys: {california.keys()}")
print(f"Dataset Description:\n{california['DESCR']}")
print(f"Feature Names: {california.feature_names}")
print(f"Target Names: {california.target_names}")
df = pd.DataFrame(california.data, columns=california.feature_names)
print(f"California Housing Dataset:\n{df.head()}")

# Add the target variable to the DataFrame
df['MedHouseVal'] = california.target
print(f"Dataset with Target Variable:\n{df.head()}")

# Shape of the dataset
print(f"Dataset Shape: {df.shape}")
# Data types of each column
print(f"Data Types:\n{df.dtypes}")
# Descriptive Statistics
print(f"Summary Statistics:\n{df.describe()}")

#Preparaion of Data - Feature Selection, Splitting the data (Training and Test Data), Scaling the data
