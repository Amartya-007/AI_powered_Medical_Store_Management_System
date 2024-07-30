import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load data
monthly_sales = pd.read_csv(r'D:\virutal env\trail\Assets\monthly_sales.csv')
supervised_data = pd.read_csv(r'D:\virutal env\trail\Assets\supervised_data.csv')

# Split data into train and test
train_data = supervised_data[:-12]
test_data = supervised_data[-12:]

# Data preprocessing
scaler = MinMaxScaler(feature_range=(-1, 1))
scaler.fit(train_data)
train_data = scaler.transform(train_data)
test_data = scaler.transform(test_data)

X_train, y_train = train_data[:, 1:], train_data[:, 0]
X_test, y_test = test_data[:, 1:], test_data[:, 0]

# Train Linear Regression model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_pre = lr_model.predict(X_test)

# Inverse transform predictions and calculate final sales
lr_pre = lr_pre.reshape(-1, 1)
lr_pre_test_set = np.concatenate([lr_pre, X_test], axis=1)
lr_pre_test_set = scaler.inverse_transform(lr_pre_test_set)

result_list = []
for index in range(len(lr_pre_test_set)):
    result_list.append(lr_pre_test_set[index][0] + monthly_sales['sales'].iloc[-13 + index])

# Calculate metrics
lr_mse = np.sqrt(mean_squared_error(result_list, monthly_sales['sales'][-12:]))
lr_mae = mean_absolute_error(result_list, monthly_sales['sales'][-12:])
lr_r2 = r2_score(result_list, monthly_sales['sales'][-12:])
print("Linear Regression MSE: ", lr_mse)
print("Linear Regression MAE: ", lr_mae)
print("Linear Regression R2: ", lr_r2)

# Plot results
plt.figure(figsize=(15, 5))
plt.plot(monthly_sales['date'], monthly_sales['sales'])
plt.plot(monthly_sales['date'][-12:], result_list)
plt.title('Customer Sales Forecast using LR Model')
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend(['Actual Sales', 'Predicted Sales'])
plt.show()


