
# EDA TODO:

* 

# ML TODO:

### Planned
* Encode avocado type
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



Target: price

Features for every run
| Date | Year | Type | Geography | Total volume | Volume Components (PLUs, Bag S/M/L) |
|------|------|------|-----------|--------------|-------------------------------------|
| No   |  No  | Yes  |    Yes    |     Yes      |        No                           |
| No   |  No  | Con  |    Yes    |     Yes      |        No                           |
| Yes  |  ?   | All  |    Region |     Yes      |        No                           |
| Year, Month | All  |    Region |     Yes      |        No                           |
| Year, Qarter|      |           |              |                                     |
|      |      |      |           |              |                                     |
|      |      |      |           |              |                                     |
|      |      |      |           |              |                                     |
|      |      |      |           |              |                                     |
|      |      |      |           |              |                                     |



Challenges
* Bags split would help or not? 
* National data granularity helpful or not?

## TODOs

Play with the scoring
* Training score as a reference in the beginning . Test score later to optimize the algo
* Cross-validation
* Choose scoring metric (R2 model.score) split in all of them
* Time series split

Optimize params
* Algos: SVM, Random Forest; KNN Regressor
* Optimize DecisionTree and LinearRegression or others / Gridsearch

Play with data input
* Try with the CSV of the missing data 3 weeks of Dec 2018
* Remove outliers?
* Try PCA with all data (without splitting data first)

Play
* AutoML

--- 81

--- 10
TODO Datenbeschreibung ausführlich trainscore cvscore verschiedene 
? Parameter im Algorithmus mit Score testscore   
--- 5,5
Score-Festlegung
Auswahl der Algorithmen und Parameter
Auswertung der Leistungen
Ideen für individuelle Verfeinerungen
Gesamtbeurteilung
--- 3,5
Gridsearch 
PCA 
DONE Pipeline 
Klassen, die im Unterricht nicht behandelt wurden mit Erklärung wie sie arbeiten 
eigene Klassen
