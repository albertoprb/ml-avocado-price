
# EDA TODO:
* (Postpone) Plot different total volume of avocados (PLC and Bagged)
* Time series clean
    * Investigate Dec 2018
    * Investigate duplicate dates
    * Dec 2020 missing
* Plot seasonality
    * Plot the price vs volume
    * Plot the price vs avocado season
* Correlation table (price and regions, and volumes)
* Investigate duplicate days (Hypothesis)
* Create a data dictionary

# ML TODO:

### Planned
* Encode avocado type
* Remove unnecessary columns
    * Total volume, Total bags
* Scale of numeric data (all columns)
* sklearn imputer for number headers (e.g. 4046)
---
* Prepare the date column (test it out without the time as well?)
    * Year, Week (1-52, or rolling 1-360)
    * Year, Quarter
    * Year, Season
* 3 weeks of data missing in Dec 2018 --> Would it affect the ML algorithm
* Time series split 

### Things to consider
* Organic vs conventional split --> Not lose much (maybe postpone it)
* Slice by Region level? Total US vs. Regions 

### Tomorrow

* Decide on split then each person tries a new algo
    * Total US, non-time series
    * Regions, non-time series
    * Regions, with time series
* Repeat for further slices

Challenges
* Bags split would help or not? 
* National data granularity helpful or not?


### Maybes

* PCA for dimension reduction 



