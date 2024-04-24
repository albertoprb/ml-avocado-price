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
# Data visualization
from tabulate import tabulate
import time

np.set_printoptions(precision=2, suppress=True)
np.random.seed(42)

input_path = os.path.join(os.path.dirname(__file__), "../data/output/")

print("Reading CSV input")
df = pd.read_csv(
    os.path.normpath(input_path + "avocados_1.csv")
)

print("Sample from CSV read")
print(tabulate(df.sample(5), headers='keys', tablefmt='psql'))

# Shuffle the dataframe because it was originally ordered by date
# In this model, we removed the date from the features, so we need to reshuffle
# df = df.sample(frac=1)

# Splitting features and target
print("Splitting features and target")
X, y = df.drop('average_price', axis=1).values, df['average_price'].values

print("Features shape: ", X.shape)
print("Target shape: ", y.shape)
print("\nFeatures sample: \n", X[:10, :], "\n")


print("Splitting training and test data")

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.33
)
print("Training features shape: ", X_train.shape)
print("Test features shape: ", X_test.shape)

print("\nTraining X sample: \n", X_train[:5, :], "\n")
print("\nTraining y sample: \n", y_train[:5], "\n")

# Encoding categorical variables
encoder = OrdinalEncoder()
encoder.fit(X_train)
X_train = encoder.transform(X_train)
X_test = encoder.transform(X_test)

columns_scores = [
    "Training score",
    "Test score",
    "Description"
]
result_scores = pd.DataFrame(columns=columns_scores)

decision_tree_model = tree.DecisionTreeRegressor()
decision_tree_model.fit(X_train, y_train)
result_scores.loc["Decision tree"] = [
        f"{decision_tree_model.score(X_train, y_train) * 100:.2f}%",
        f"{decision_tree_model.score(X_test, y_test) * 100:.2f}%",
        "Decision tree with Ordinal Encoder"
    ]

# Cross validation
# scores = cross_val_score(
#     decision_tree_model,
#     X,
#     y,
#     cv=5,
#     scoring='mean_squared_error'
# )




# Scale data, Polinomial
# model = make_pipeline(PolynomialFeatures(2), LinearRegression())
# model.fit(X_train, y_train)
# linear_regression_model = LinearRegression()
# linear_regression_model.fit(X_train, y_train)
# result_scores.loc["Linear Regression"] = [
#         linear_regression_model.score(X_train, y_train),
#         linear_regression_model.score(X_test, y_test),
#         "Linear regression without scaling and poly"
#     ]

print(tabulate(result_scores, headers='keys', tablefmt='psql'))
result_scores.to_csv(
    os.path.normpath(
        input_path +
        "model_1_results_" +
        time.strftime("%Y%m%d-%H%M%S") +
        ".csv"
    )
)
