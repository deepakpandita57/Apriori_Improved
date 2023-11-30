# Implement an improvement on the Apriori algorithm for Frequent Itemset Mining.

Task
=============================================================================================================
To implement an improvement on the apriori algorithm for frequent itemset mining on the adult dataset from UCI ML repository.


Preprocessing
=============================================================================================================
The dataset used in this project is adult census dataset from UCI ML repository. It contains the following attributes ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native-country', 'income']. The following preprocessing steps are performed:
1.	Remove “fnlwgt” and “education_num” columns because they can be inferred from other attributes like education and hence are not useful.
2.	Drop all rows with any missing value.
3.	Discretize the values of the continuous valued columns “age”, “capital_gain”, “capital_loss” and ”hours_per_week”.
4.	“age”, “capital_gain” and “capital_loss” attributes are discretized into 3 equal-width bins ['young', 'senior', 'old'], ['low-gain', 'med-gain', 'high-gain'] and ['low-loss', 'med-loss', 'high-loss'] respectively.
5.	“hours_per_week” is also discretized into 3 bins with bin boundaries [0, 25, 40, 100] and labels ['part-time', 'full-time', 'overtime'].
It is implemented in “preprocess(data)” function.


Improvement on Apriori Algorithm
=============================================================================================================
Improvement on apriori algorithm is implemented in the script “apriori_improved.py”.
The improvement implemented is transaction reduction where the transactions to be considered in the subsequent iterations are reduced because if a transaction doesn’t contain any frequent k-itemsets, it cannot contain any frequent k+1-itemsets.
This script takes two input values “input_file” and “min_sup” for input file path and minimum support respectively. Output is L, the frequent itemsets in D transactions like the apriori algorithm.
The procedure and the functions are same except in “apriori(D, min_sup)” function we reduce the transactions after generating each frequent k-itemset using the function “transaction_reduction(D, Lk)”.


Sample Output
=============================================================================================================
For min_sup: 60
Support count: 18097
L1              items  count
0          [<=50K]  22654
1           [Male]  20380
2        [Private]  22286
3  [United-States]  27504
4          [White]  25933
5       [low-gain]  30009
6       [low-loss]  28815
7          [young]  18529
.
.
.
L 4                                           items  count
0    [<=50K, United-States, low-gain, low-loss]  19938
1            [<=50K, White, low-gain, low-loss]  18554
2  [Private, United-States, low-gain, low-loss]  19212
3          [Private, White, low-gain, low-loss]  18249
4    [United-States, White, low-gain, low-loss]  22920


References
=============================================================================================================
Adult dataset: https://archive.ics.uci.edu/ml/datasets/adult <br />
Have questions? Shoot me an [email](https://sites.google.com/view/deepakpandita/contact).
