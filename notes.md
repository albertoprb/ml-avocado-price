
# EDA TODO:

* Correlation table (price and regions, and volumes)

# ML TODO:

### Planned
* Encode avocado type
* Remove unnecessary columns
    * Total volume, Total bags
* Scale of numeric data (all columns)
* sklearn imputer for number headers (e.g. 4046)
---
* Time series clean
    * Investigate Dec 2018
    * Investigate duplicate dates
* Investigate duplicate days (Hypothesis)
* Prepare the date column (test it out without the time as well?)
    * Year, Week (1-52, or rolling 1-360)
    * Year, Quarter
    * Year, Season
* 3 weeks of data missing in Dec 2018 --> Would it affect the ML algorithm
* Time series split

### Things to consider
* Organic vs conventional split --> Not lose much (maybe postpone it)
* Slice by Region level? Total US vs. Regions 

### Steps

* Decide on split then each person tries a new algo
    * Total US, non-time series
    * Regions, non-time series
    * Regions, with time series
* Repeat for further slices

Challenges
* Bags split would help or not? 
* National data granularity helpful or not?


### Future plans

* Create a data dictionary