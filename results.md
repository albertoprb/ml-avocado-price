# Results

## Goal

Predict the average unit price for avocado in a given location for a certain date. This should influence buyers decisions (when to buy), and seller decision (when to purchase). 

## Slicing the data

We are slicing the data to evalute relevant data subsets s baselines for the models later.

We established the following runs initially

|Run| Date | Year | Type | Geography | Total volume | Volume Components (PLUs, Bag S/M/L) |
|---|------|------|------|-----------|--------------|-------------------------------------|
| 1 | No   |  No  | Yes  |    Yes    |     Yes      |        No                           |
| 2 | No   |  No  | Con  |    Yes    |     Yes      |        No                           |
| 3 | Yes  |  ?   | All  |    Region |     Yes      |        No                           |
| 4 | Year, Month | All  |    Region |     Yes      |        No                           |
| 5 | Year, Qarter| All  |           |              |                                     |

### 1. Only considering total volume

In the first scenario we only kept the following columns: average_price,total_volume,type,geography.
We are using the model score function which defaults to R2.

With Ordinal Encoder

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision tree     | 100.00%          | 41.37%       |
| Linear Regression | 38.50%           | 39.14%       |


With OneHot Encoder and No Scaler

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision tree     | 100.00%          | 41.94%       |
| Linear Regression | 53.63%           | 54.19%       |


Using the OneHot Encoder and StandardScaler for total_volume
The scaler is only used for the Linear Regression.

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision tree     | 100.00%          | 41.94%       |
| Linear Regression | 53.63%           | 54.19%       |


Conclusions

* Both Algorithms perform poorly with the smallest data subset.
* Decision tree is overfitting the training data because max_depth is uncapped. 
* Linear model without polynomial features doesn't fit this data. We'll try in the next step.
* Using different scalers (MinMax, Standard) didn't affect the score
* It's very inneficient to experiment without using sklearn pipelines
* It's much easier/faster to iterate on a jupyter notebook but less reliable

if we have more time
* We would try the splines transformation

### 2. Removing total_volume and keeping all volume components

In this scenario we 
* Moved to use sklearn pipelines. Replicated the results to make sure.
* Kept all components of volume to have more features for the algorithm to learn.

The hypothesis is that for the same total volume, if certain components have higher representation, they will affect average price. 
That is, if there's more wholesale than retail then for the same volume you will have lower average price. See this example

| Date       | AveragePrice | TotalVolume | SmallHass | LargeHass  | XLargeHass | TotalBags  | SmallBags  | LargeBags  | XLargeBags | Type    | Year | Region   |
|------------|--------------|-------------|-----------|------------|------------|------------|------------|------------|------------|---------|------|----------|
| 2017-01-01 | 2.06         | 39260.55    | 6071.7    | 20105.65   | 1025.49    | 12057.71   | 11934.77   | 122.94     | 0          | organic | 2017 | New York |
| 2019-01-20 | 1.4          | 39243.75    | 50.98     | 2616.8     | 0          | 36575.97   | 24531.82   | 12044.15   | 0          | organic | 2019 | Boston   |

This change improves dramatically the test score for the Decision Tree, and only very little for the Linear regression.

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 64.70%       |
| Linear regression | 53.57%           | 54.60%       |

Then we apply the polynomial features to capture the non-linear data behavior. No significant difference for degrees 2, and 3.

Conclusions

* Using a sklearn pipeline makes changes much easier 
* The Test score improved drammatically using the components of volume but the linear regression could be better. 
* Polynomial features in this scenario did not help.

If we had more time, we

* Would build a table with the polynomial features degree to evaluate it better, and try a different function (e.g. sinus)


### 3a. Removing total_volume and keeping all volume components, only keeping conventional or organic avocados

Then we wanted to experiment with keeping only 1 avodado type. So we went back to step 1, to see if that would help.

For Conventional, the results were much worse

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 48.74%       |
| Linear regression | 38.39%           | 38.11%       |


Similar for Organic

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 37.82%       |
| Linear regression | 30.38%           | 29.77%       |


Conclusions

* Slicing the data on avocado type did not yield better results.
* We tried Lasso and Ridge but learned it doesn't make sense as there's no overfitting of training data.

### 3b. Keeping onlyy total_volume and keeping either conventional or organic avocados

The we retried step 2 (all components of volume), but only for Conventional, the results were much worse

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 14.43%       |
| Linear regression | 37.08%           | 36.70%       |


And drammatically worse for Organic

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 1.00%        |
| Linear regression | 29.44%           | 28.70%       |


Conclusions
* Total volume alone is not a good estimator for average avocado price, in any circunstance. As a reminder in 99,4% of the cases the difference between total_volume and the sum of PLUs, and Bag sizes is 0%. 

### 4. Keeping the volume components, but now adding year and week

In this step we keep working with the individual volume components and introduced dates. Dates were processed to contain only year/week.

Remember this was the baseline

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 64.70%       |
| Linear regression | 53.57%           | 54.60%       |


First we treated year as a categorical variable. It improved both scores.

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 69.44%       |
| Linear regression | 57.24%           | 58.13%       |


Then added week and encoding it (treating it again as a categorical variable). It improved the linear regression.

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 68.41%       |
| Linear regression | 61.87%           | 62.18%       |


Then considered it as a numerical varialble instead and scaled it. Here the decision tree performed much better.

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 77.92%       |
| Linear regression | 54.98%           | 55.61%       |


Then if we treat the dates as numerical for the Decision Tree, and as categorical for the Linear Regression, so having 2 data processing pipelines, we get the best result so far. We also added PCA to the processing pipeline.

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 78.13%       |
| Linear regression | 61.87%           | 62.18%       |

### 5. Moving to use the cross validation with RMSE

So far our scores were calculated without cross-validation, and using the default R2 score.

We decided to use the RMSE score instead of the R2 because 

* The R2 score uses the squared error predicted in relation to the mean. Given our data is periodic, the the mean for all years might not be a good optimization hook, unless we would calculate our own local R2 (e.g. using quarters). Unfortunately, we do not have time for that.
* The RMSE score is relatively easy to understand for the stakeholders, and the score is in the same unit as the price.

Based on that we re-run the model on the training data with cross validation using 6 folds. 
We also show regression error metrics as a baseline on the train/test split, for each algorithm.

**Models CV scores (On train data, RMSE)**

Avocado average_price on train data: $ 1.379 

|                         | Fold 1   | Fold 2   | Fold 3   | Fold 4   | Fold 5   | Fold 6   |
|-------------------------|----------|----------|----------|----------|----------|----------|
| DecisionTreeRegressor() | $ 0.19   | $ 0.19   | $ 0.19   | $ 0.19   | $ 0.19   | $ 0.19   |
| LinearRegression()      | $ 0.23   | $ 0.23   | $ 0.23   | $ 0.23   | $ 0.25   | $ 0.24   | 

**Models errors (On test split 0.33)**

Avocado average_price on test data: $ 1.382 

|                         | MAE   | MAE %   |   MSE | RMSE   |   R2 |
|-------------------------|-------|---------|-------|--------|------|
| DecisionTreeRegressor() | $0.12 | 8.72%   |  0.03 | $0.18  | 0.78 |
| LinearRegression()      | $0.18 | 13.38%  |  0.05 | $0.23  | 0.62 | 

So at this point we have a RMSE of $0.19 as a baseline to optimize.

### 6. Re-consider avocado types

Then we decided to re-consider the avocado types column.

First, the dataset contains as many samples for conventional and organic avocados. However, the average price and total volumes are drastically different. For all years, see the table below:

| geography     | price (conventional) | price (organic) | volume millions (conventional) | volume millions (organic) |
|---------------|-----------------------|-----------------|-------------------------------|---------------------------|
| California    | 1.15                  | 1.74            | 6.31                          | 0.20                      |
| Great Lakes   | 1.15                  | 1.47            | 3.81                          | 0.17                      |
| Midsouth      | 1.17                  | 1.57            | 3.43                          | 0.15                      |
| Northeast     | 1.31                  | 1.77            | 4.83                          | 0.21                      |
| Plains        | 1.13                  | 1.57            | 2.02                          | 0.06                      |
| South Central | 0.86                  | 1.35            | 6.65                          | 0.13                      |
| Southeast     | 1.12                  | 1.54            | 4.42                          | 0.09                      |
| West          | 1.02                  | 1.62            | 6.76                          | 0.26                      |

The total distribution look likes the following 

|                            |    count |   mean |   std |   min |   50% |   75% |   95% |   99% |   max |
|----------------------------|----------|--------|-------|-------|-------|-------|-------|-------|-------|
| average_price_conventional | 16524.00 |   1.14 |  0.25 |  0.46 |  1.12 |  1.30 |  1.59 |  1.80 |  2.22 |
| total_volume (millions)    | 16524.00 |   1.87 |  5.41 |  0.03 |  0.48 |  1.14 |  6.48 | 36.78 | 63.72 |
| average_price_organic      | 16521.00 |   1.62 |  0.34 |  0.44 |  1.58 |  1.82 |  2.21 |  2.59 |  3.25 |
| total_volume (millions)    | 16521.00 |   0.06 |  0.19 |  0.00 |  0.02 |  0.04 |  0.23 |  1.21 |  2.39 | 

So we think that splitting them again should yield better results. And given volume of conventional avocados, it's better if we optimize for it first, given that's where the business interests lie. Let's see the results

**For organic the RMSE is worse than the combined dataset**

CV scores (Train data, RMSE)

Avocado average_price on train data: $ 1.616 

|                         | Fold 1   | Fold 2   | Fold 3   | Fold 4   | Fold 5   | Fold 6   |
|-------------------------|----------|----------|----------|----------|----------|----------|
| DecisionTreeRegressor() | $ 0.22   | $ 0.22   | $ 0.22   | $ 0.22   | $ 0.22   | $ 0.23   |
| LinearRegression()      | $ 0.26   | $ 0.26   | $ 0.26   | $ 0.26   | $ 0.27   | $ 0.27   | 

Errors (Test split 0.33)

Avocado average_price on test data: $ 1.613 

|                         | MAE   | MAE %   |   MSE | RMSE   |   R2 |
|-------------------------|-------|---------|-------|--------|------|
| DecisionTreeRegressor() | $0.14 | 8.73%   |  0.04 | $0.20  | 0.65 |
| LinearRegression()      | $0.20 | 13.29%  |  0.07 | $0.26  | 0.40 | 


**For conventional, the RMSE results are better than the combined dataset**

CV scores (Train data, RMSE)

Avocado average_price on train data: $ 1.146 

|                         | Fold 1   | Fold 2   | Fold 3   | Fold 4   | Fold 5   | Fold 6   |
|-------------------------|----------|----------|----------|----------|----------|----------|
| DecisionTreeRegressor() | $ 0.14   | $ 0.15   | $ 0.15   | $ 0.14   | $ 0.15   | $ 0.15   |
| LinearRegression()      | $ 0.16   | $ 0.17   | $ 0.16   | $ 0.16   | $ 0.16   | $ 0.16   | 

Errors (Test split 0.33)

Avocado average_price on test data: $ 1.142 

|                         | MAE   | MAE %   |   MSE | RMSE   |   R2 |
|-------------------------|-------|---------|-------|--------|------|
| DecisionTreeRegressor() | $0.10 | 8.70%   |  0.02 | $0.14  | 0.67 |
| LinearRegression()      | $0.13 | 11.25%  |  0.03 | $0.16  | 0.58 | 


Lessons learned
* Here the lesson learned is how important the error metric is. The R2 score once again shows a worse result in both splits because the mean is also changing, however there was a clear improvement for the conventional avocado using the RMSE as a reference.
* In this scenario the linear regression got much better results. It's expected as the decision tree might be able to early in the tree to split the data.
* Later maybe the 2 models can be deployed separately. For now, we'll focus to have better predictions where there's more market volume, that is, the conventional avocados.

### 7. Include more models

Now that we have a baseline with simple models, and a proven data processing pipeline, we experimented with more regression models.
We believe the RandomForestRegresson will improve the DecisionTreeRegressor score, and the SVM is also promissing.

**CV scores (Train data, RMSE)**

Avocado average_price on train data: $ 1.146 

|                                                        | Fold 1   | Fold 2   | Fold 3   | Fold 4   | Fold 5   | Fold 6   |
|--------------------------------------------------------|----------|----------|----------|----------|----------|----------|
| DecisionTreeRegressor()                                | $ 0.14   | $ 0.15   | $ 0.15   | $ 0.15   | $ 0.15   | $ 0.15   |
| LinearRegression()                                     | $ 0.16   | $ 0.17   | $ 0.16   | $ 0.16   | $ 0.16   | $ 0.16   |
| KNeighborsRegressor(n_neighbors=4, weights='distance') | $ 0.13   | $ 0.13   | $ 0.13   | $ 0.13   | $ 0.12   | $ 0.13   |
| SVR(epsilon=0.01)                                      | $ 0.10   | $ 0.10   | $ 0.10   | $ 0.09   | $ 0.09   | $ 0.10   |
| RandomForestRegressor()                                | $ 0.10   | $ 0.10   | $ 0.10   | $ 0.10   | $ 0.09   | $ 0.10   | 

**Errors (Test split 0.33)**

Avocado average_price on test data: $ 1.142 

|                                                        | MAE   | MAE %   |   MSE | RMSE   |   R2 |
|--------------------------------------------------------|-------|---------|-------|--------|------|
| DecisionTreeRegressor()                                | $0.10 | 8.66%   |  0.02 | $0.14  | 0.67 |
| LinearRegression()                                     | $0.13 | 11.25%  |  0.03 | $0.16  | 0.58 |
| KNeighborsRegressor(n_neighbors=4, weights='distance') | $0.09 | 8.09%   |  0.02 | $0.12  | 0.76 |
| SVR(epsilon=0.01)                                      | $0.07 | 6.15%   |  0.01 | $0.10  | 0.86 |
| RandomForestRegressor()                                | $0.07 | 6.24%   |  0.01 | $0.09  | 0.86 | 

We clearly see that the RandomForest and the SVM with default params are winning and taking us to an RMSE around $ 0.10

**Lessons learned**

* The most hardware intensive models take very long to run (Around 15m to cross-validate all models) but the results are great.
* Tried to run the same models in a google TPU4. We learned that SKLearn doesn't support GPU workloads.
* Open question: Why does the RandomForestRegressor need a cross-validation? Intuitively we though it did not need it.

### 8. Fine tuning best model params

Then we run the SVM and RandomForest with a gridsearch with CV=3

GridsearchCV results

**SVM best params**

{'C': 5, 'degree': 3, 'epsilon': 0.01, 'kernel': 'rbf'}

Degree and kernel are the default.


**Random Forest best params**

{'bootstrap': False, 'max_depth': None, 'max_features': 1, 'n_estimators': 100}

All except bootstrap are the dafault.


#### Final model 

This is the final table with all algorithms run but the SVM and RandomForest tuned based on gridsearch.

**CV scores (Train data, RMSE)**

Avocado average_price on train data: $ 1.146 

|                                                        | Fold 1   | Fold 2   | Fold 3   | Fold 4   | Fold 5   | Fold 6   |
|--------------------------------------------------------|----------|----------|----------|----------|----------|----------|
| DecisionTreeRegressor()                                | $ 0.14   | $ 0.15   | $ 0.15   | $ 0.14   | $ 0.15   | $ 0.15   |
| LinearRegression()                                     | $ 0.16   | $ 0.17   | $ 0.16   | $ 0.16   | $ 0.16   | $ 0.16   |
| KNeighborsRegressor(n_neighbors=4, weights='distance') | $ 0.13   | $ 0.13   | $ 0.13   | $ 0.13   | $ 0.12   | $ 0.13   |
| SVR(C=5.0, epsilon=0.01)                               | $ 0.09   | $ 0.10   | $ 0.09   | $ 0.09   | $ 0.10   | $ 0.10   |
| RandomForestRegressor(bootstrap=False)                 | $ 0.14   | $ 0.15   | $ 0.15   | $ 0.14   | $ 0.14   | $ 0.14   | 

Errors (Test split 0.33)

**Avocado average_price on test data: $ 1.142**

|                                                        | MAE   | MAE %   |   MSE | RMSE   |   R2 |
|--------------------------------------------------------|-------|---------|-------|--------|------|
| DecisionTreeRegressor()                                | $0.10 | 8.78%   |  0.02 | $0.14  | 0.67 |
| LinearRegression()                                     | $0.13 | 11.25%  |  0.03 | $0.16  | 0.58 |
| KNeighborsRegressor(n_neighbors=4, weights='distance') | $0.09 | 8.09%   |  0.02 | $0.12  | 0.76 |
| SVR(C=5.0, epsilon=0.01)                               | $0.07 | 6.11%   |  0.01 | $0.09  | 0.86 |
| RandomForestRegressor(bootstrap=False)                 | $0.09 | 8.33%   |  0.02 | $0.14  | 0.70 | 

Here it seems the RandomForest became slightly worse so we would need to review the grid search params but we don't have time for that.
The winner is the SVR with RMSE of $0.09. Given the average price of $1.142, this is an acceptable result to use in the business.

If we had more time

* We would re-run the grid search for RandomForest
* We would run the same models with organic and see performance.
* We would experiment with Ensemble methods.
* We would bullet proof regional data. Maybe the predictions are good for a given region but not usable in another, so this would need to be clear before business decisions are taken with it.

### AutoML Experiment

As a side experiment we tried to run the data using a AutoML framework to see wich result we would get. 
In only 3 lines of code we got $0.08. But running it needs serious processing power, so we run it on a TPU4.

Using Auto Gluon with a TPU4 GPU
https://colab.research.google.com/drive/1WNQjVZflQWbGPpXjerY0AXfZtfv0odoH?hl=en#scrollTo=O90xYI_HdlNL


Fitting model: WeightedEnsemble_L2
Ensemble Weights: {'LightGBMXT': 0.458, 'LightGBM': 0.292, 'LightGBMLarge': 0.208, 'CatBoost': 0.042}
-0.0782	 = Validation score   (-root_mean_squared_error)