from sklearn.linear_model import LinearRegression
import numpy as np

# Preparing the data
temp = np.array([20, 24, 28, 32, 35, 30, 22]).reshape(-1, 1)
sales = np.array([50, 65, 82, 95, 110, 90, 58])

# Training the model
model = LinearRegression()
model.fit(temp, sales)

# Predicting for a 38-degree day
prediction = model.predict([[38]])
print(f"Predicted Sales: {prediction[0]:.0f} drinks")