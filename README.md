# Avocado Price Predictor
## 1. Business Understanding
https://www.kaggle.com/datasets/timmate/avocado-prices-2020/data

### The Scope and Goal of the Project:
##### - Scope
1. Analyse each column 
<br>  * Check duplicate entries and remove if necessary (e.x. Days)
<br>
<br>
2. Understand the relationship between columns 
 * check linear correlation between the total bags and s, l, xl types of bags
 * check the correlation between the total_volume and each of the avocado varities 
 * insights price variations in the regions ??? (could we move to hypothesis )
    seosonality -> could check it per region
<br>
<br>

3. Hypothesis on the data
   * Where is the highest consumption of avocado
4. Scaling & Dimension reduction
5. Jahreszeit, Region und Avocado-Sorte (try if when slicing the data we get better or worse score)

##### - Goal 
1. Predict how the prices of regular & bio Avocado will be in the coming year




## 2. Data Understanding
##### Data Source
https://www.kaggle.com/datasets/timmate/avocado-prices-2020/data

##### Data dictionary 

Columns descriptions

* Date - The date of the observation 
* AveragePrice - the average price of a single avocado
* type - conventional or organic
* year - the year
* geography - the city or region of the observation
* Total Volume - Total number of avocados sold

* From [Hass avocados varieties,size,type](https://loveonetoday.com/how-to/identify-hass-avocados/)
    * Small/Medium Hass Avocado (~3-5oz avocado) | #4046 Avocado
    * Large Hass Avocado (~8-10oz avocado) | #4225 Avocado
    * Extra Large Hass Avocado (~10-15oz avocado) | #4770 Avocado


Todo
- check Date and Numbers format 
- Create the complete Data Dictionary
- check the info on https://hassavocadoboard.com/wp-content/uploads/2019/04/Hass-Avocado-Board-Price-Elasticities-of-Demand-or-Fresh-Hass-Avocados-2019.pdf