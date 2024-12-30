import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import json

data = pd.read_csv("Customers.csv")

columns_to_keep = ['Gender', 'Age', 'Annual Income ($)', 'Spending Score (1-100)']
filtered_data = data[columns_to_keep].copy()
filtered_data['Gender'] = filtered_data['Gender'].map({'Male': 0, 'Female': 1})
filtered_data = filtered_data.dropna()

df = pd.DataFrame(filtered_data)

X = df[['Gender', 'Age', 'Annual Income ($)']]
y = df['Spending Score (1-100)']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

joblib.dump(model, "linear_regression_model.joblib")

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

metrics = {
    "mae": mae,
    "r2_score": r2
}

with open("model_metrics.json", "w") as metrics_json:
    json.dump(metrics, metrics_json)
