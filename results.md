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

# 1. Only considering total volume

In this scenario we only kept the following columns: average_price,total_volume,type,geography.

With Ordinal Encoder
+-------------------+------------------+--------------+
|                   | Training score   | Test score   |
|-------------------+------------------+--------------|
| Decision tree     | 100.00%          | 41.37%       |
| Linear Regression | 38.50%           | 39.14%       |
+-------------------+------------------+--------------+

With OneHot Encoder and No Scaler
+-------------------+------------------+--------------+
|                   | Training score   | Test score   |
|-------------------+------------------+--------------|
| Decision tree     | 100.00%          | 41.94%       |
| Linear Regression | 53.63%           | 54.19%       |
+-------------------+------------------+--------------+

Using the OneHot Encoder and StandardScaler for total_volume
The scaler is only used for the Linear Regression.

+-------------------+------------------+--------------+
|                   | Training score   | Test score   |
|-------------------+------------------+--------------|
| Decision tree     | 100.00%          | 41.94%       |
| Linear Regression | 53.63%           | 54.19%       |
+-------------------+------------------+--------------+

Conclusions

* Both perform poorly
* Decision tree is overfitting the training data
* Linear model without polynomial features doesn't fit this data
* Using different scalers didn't affect the score
* It's very inneficient to experiment without using sklearn pipelines
* It's much easier to iterate on a jupyter notebook but less reliable

# 2. Removing total_volume and keeping all volume components

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

+-------------------+------------------+--------------+
|                   | Training score   | Test score   |
|-------------------+------------------+--------------|
| Decision Tree     | 100.00%          | 64.70%       |
| Linear regression | 53.57%           | 54.60%       |
+-------------------+------------------+--------------+

Then we apply the polynomial features to capture the non-linear data behavior


# 3. Only total volume and only conventional avocados
