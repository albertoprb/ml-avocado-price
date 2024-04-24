# %%
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
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
# Data visualization
from tabulate import tabulate
import time

np.set_printoptions(precision=2, suppress=True)
np.random.seed(42)

# %%

input_path = os.path.join(os.path.dirname(__file__), "../data/output/")

print("Reading CSV input")
df = pd.read_csv(
    os.path.normpath(input_path + "avocados_2.csv")
)

print("Sample from CSV read")
print(tabulate(df.sample(5), headers='keys', tablefmt='psql'))

# Shuffle the dataframe because it was originally ordered by date
# In this model, we removed the date from the features, so we need to reshuffle
# df = df.sample(frac=1)

# Splitting features and target
X, y = df.drop('average_price', axis=1), df['average_price']

print("\nX sample is \n", tabulate(X.sample(5), headers='keys', tablefmt='psql'))

# %%
numeric_features = ["4046","4225","4770","small_bags","large_bags","xlarge_bags"]
numeric_transformer_no_scaling = Pipeline(
    steps=[
        ("scaler", StandardScaler(with_mean=False, with_std=False)) # Not scaling
    ]
)
numeric_transformer = Pipeline(
    steps=[
        ("polynomial", PolynomialFeatures(3)),
        ("scaler", StandardScaler()) 
    ]
)

categorical_features = ["type", "geography"]
categorical_transformer = Pipeline(
    steps=[
        ("encoder", OneHotEncoder())
    ]
)

# %%
decision_tree_preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer_no_scaling, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

decision_tree_pipeline = Pipeline(
    steps=[
        ("preprocessor", decision_tree_preprocessor), 
        ("decision_tree", tree.DecisionTreeRegressor())
    ]
)

decision_tree_pipeline

# %%
linear_regression_processor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

linear_regression_pipeline = Pipeline(
    steps=[
        ("preprocessor", linear_regression_processor), 
        ("linear regression", LinearRegression())
    ]
)

# Scale data, Polinomial
# model = make_pipeline(PolynomialFeatures(2), LinearRegression())
# model.fit(X_train, y_train)
# linear_regression_model = 
# linear_regression_model.fit(X_train, y_train)
# result_scores.loc["Linear Regression"] = [
#         linear_regression_model.score(X_train, y_train),
#         linear_regression_model.score(X_test, y_test),
#         "Linear regression without scaling and poly"
#     ]

linear_regression_pipeline

# %%
print("Features shape: ", X.shape)
print("Target shape: ", y.shape)

print("\nFeatures sample: \n", X.sample(2), "\n")


print("Splitting training and test data")

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.33
)

print("Training features shape: ", X_train.shape)
print("Test features shape: ", X_test.shape)

print("\nTraining X sample: \n", X_train.sample(2), "\n")
print("\nTraining y sample: \n", y_train.sample(2), "\n")

# %%
columns_scores = [
    "Training score",
    "Test score"
]
result_scores = pd.DataFrame(columns=columns_scores)

# %%
pipelines = {
    "Decision Tree": decision_tree_pipeline, 
    "Linear regression": linear_regression_pipeline
}

for pipeline_name, pipeline in pipelines.items():
    pipeline.fit(X_train, y_train)
    result_scores.loc[pipeline_name] = [
            f"{pipeline.score(X_train, y_train) * 100:.2f}%",
            f"{pipeline.score(X_test, y_test) * 100:.2f}%"
        ]

# TODO Cross-validation
# TODO Optimize Decision Tree
# TODO Optimize Linear Regression
# TODO Move to expanded dataset

# TODO PCA on components of volume

# Cross validation
# scores = cross_val_score(
#     decision_tree_model,
#     X,
#     y,
#     cv=5,
#     scoring='mean_squared_error'
# )

# %%
print(tabulate(result_scores, headers='keys', tablefmt='psql'))
result_scores.to_csv(
    os.path.normpath(
        input_path +
        "model_1_results_" +
        time.strftime("%Y%m%d-%H%M%S") +
        ".csv"
    )
)


