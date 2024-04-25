# Results

## Goal

Predict the average unit price for avocado in a given location for a certain date.

## Slicing the data

We are slicing the data for every run to evaluate relevant data subsets that we could safely 
predict.

We established the following runs

|Run| Date | Year | Type | Geography | Total volume | Volume Components (PLUs, Bag S/M/L) |
|---|------|------|------|-----------|--------------|-------------------------------------|
| 1 | No   |  No  | Yes  |    Yes    |     Yes      |        No                           |
| 2 | No   |  No  | Con  |    Yes    |     Yes      |        No                           |
| 3 | Yes  |  ?   | All  |    Region |     Yes      |        No                           |
| 4 | Year, Month | All  |    Region |     Yes      |        No                           |
| 5 | Year, Qarter| All  |           |              |                                     |
|   |      |      |      |           |              |                                     |
|   |      |      |      |           |              |                                     |
|   |      |      |      |           |              |                                     |
|   |      |      |      |           |              |                                     |
|   |      |      |      |           |              |                                     |

### 1. Only considering total volume

In this scenario we only kept the following columns: average_price,total_volume,type,geography.

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

* Both Algorithms perform poorly
* Decision tree is overfitting the training data
* Linear model without polynomial features doesn't fit this data
    + TODO Build tabele with different degrees (sinus curve with 7 potenz)
    + TODO Splines Transformierung in report
* Using different scalers didn't affect the score
* It's very inneficient to experiment without using sklearn pipelines
* It's much easier to iterate on a jupyter notebook but less reliable

### 2. Removing total_volume and keeping all volume components

In this scenario we 
* Moved to use sklearn pipelines. Replicated the results to make sure.
* Kept all components of volume. 

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


### 3a. Removing total_volume and keeping all volume components, only keeping conventional or organic avocados

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

LASSO and Ridge regression only after overfitting in the Mean squared error regression (simple)

### 3b. Keeping onlyy total_volume and keeping either conventional or organic avocados

For Conventional, the results were much worse

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
* Total volume alone is not a good estimator for average avocado price.

### 4. Keeping the volume components, but now adding year and week

Baseline
|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 64.70%       |
| Linear regression | 53.57%           | 54.60%       |

First we added year to the best data processing, but treated it as a categorical variable.

It improves a bit the decision tree.

TODO PCA applied - Replicated the results

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 69.44%       |
| Linear regression | 57.24%           | 58.13%       |


Then added week and encoding it (treating it again as a categorical variable)

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 68.41%       |
| Linear regression | 61.87%           | 62.18%       |


Then considered it as a numerical varialble and scaled it.

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 77.92%       |
| Linear regression | 54.98%           | 55.61%       |


Then if we treat the dates as numerical for the Decision Tree, 
and as categorical for the Linear Regression,

|                   | Training score   | Test score   |
|-------------------|------------------|--------------|
| Decision Tree     | 100.00%          | 78.13%       |
| Linear regression | 61.87%           | 62.18%       |


Adding PCA see if reducing dimensionality of the many volume components
increases the model's performance, especially for the regression.



### 5. Moving to use the cross validation with RMSE

So far our scores were calculated without cross-validation.
The score for the Decision Tree was the default as RMSE.
The score for the Linear Regression was the default as ?.

Now we can 