import numpy as np
import pandas as pd
# Data preparation and Evaluation
import os
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
# Models
from sklearn import tree
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer
# Model evaluation
from sklearn.model_selection import cross_val_score
# Encoders
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
# Scalers
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
# Data visualization
from tabulate import tabulate
import time

np.set_printoptions(precision=2, suppress=True)
np.random.seed(42)

input_path = os.path.join(os.path.dirname(__file__), "../data/slices/")

print("Reading CSV input")
df = pd.read_csv(
    os.path.normpath(input_path + "total_volume_only.csv")
)

print("Sample from CSV read")
print(tabulate(df.sample(5), headers='keys', tablefmt='psql'))

# Shuffle the dataframe because it was originally ordered by date
# In this model, we removed the date from the features, so we need to reshuffle
# df = df.sample(frac=1)

# Splitting features and target
print("Splitting features and target")
X, y = df.drop('average_price', axis=1), df['average_price']

print("Features shape: ", X.shape)
print("Target shape: ", y.shape)
print(
    "\nFeatures: \n",
    tabulate(X.head(5), headers='keys', tablefmt='psql'), "\n"
)


print("Splitting training and test data")

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.33
)
print("Training features shape: ", X_train.shape)
print("Test features shape: ", X_test.shape)

print(
    "\nX_train sample: \n",
    tabulate(X_train.head(5), headers='keys', tablefmt='psql'), "\n"
)


print(
    "\ny_Train (Average Price): \n",
    y_train.head(5)
)

# Encoding categorical variables
encoder = OneHotEncoder(sparse_output=False).set_output(transform='pandas')
# encoder = OrdinalEncoder().set_output(transform='pandas')
X_train_cat_encoded = encoder.fit_transform(X_train[["type", "geography"]])
X_test_cat_encoded = encoder.fit_transform(X_test[["type", "geography"]])

# scaler = StandardScaler().set_output(transform='pandas')
scaler = MinMaxScaler().set_output(transform='pandas')
X_train_num_scaled = scaler.fit_transform(X_train[["total_volume"]])
X_test_num_scaled = scaler.fit_transform(X_test[["total_volume"]])

X_train_encoded = pd.concat(
    [X_train['total_volume'], X_train_cat_encoded],
    axis=1
)

X_test_encoded = pd.concat(
    [X_test['total_volume'], X_test_cat_encoded],
    axis=1
)

X_train_encoded_scaled = pd.concat(
    [X_train_num_scaled, X_train_cat_encoded],
    axis=1
)

X_test_encoded_scaled = pd.concat(
    [X_test_num_scaled, X_test_cat_encoded],
    axis=1
)

columns_scores = [
    "Training score",
    "Test score"
]
result_scores = pd.DataFrame(columns=columns_scores)

decision_tree_model = tree.DecisionTreeRegressor()
decision_tree_model.fit(X_train_encoded, y_train)
result_scores.loc["Decision tree"] = [
        f"{decision_tree_model.score(X_train_encoded, y_train) * 100:.2f}%",
        f"{decision_tree_model.score(X_test_encoded, y_test) * 100:.2f}%"
    ]

linear_regression_model = LinearRegression()
linear_regression_model.fit(X_train_encoded_scaled, y_train)
result_scores.loc["Linear Regression"] = [
        f"{linear_regression_model.score(X_train_encoded_scaled, y_train) * 100:.2f}%",
        f"{linear_regression_model.score(X_test_encoded_scaled, y_test) * 100:.2f}%"
    ]

print(tabulate(result_scores, headers='keys', tablefmt='psql'))
