#!/usr/bin/python2

# Author: Deepak Pandita
# Date created: 17 Oct 2017

import pandas as pd
import numpy as np
import itertools

input_file = 'adult/adult.data'
min_sup = 60

data = pd.read_csv(input_file, delimiter=', ', header = None, engine='python', na_values='?')
data.columns = ['age','workclass','fnlwgt','education','education_num','marital_status','occupation','relationship','race','sex','capital_gain','capital_loss','hours_per_week','native-country','income'];

#Preprocess the data
def preprocess(data):
	#remove fnlwgt and education_num columns
	data = data.drop('fnlwgt',1)
	data = data.drop('education_num',1)
	data = data.dropna()	#drop all rows with any missing value
	#discretize the values of attributes age, capital_gain, capital_loss and hours_per_week
	data['age'] = pd.cut(data['age'],3,labels=['young','senior','old'],include_lowest=True)
	data['capital_gain'] = pd.cut(data['capital_gain'],3,labels=['low-gain','med-gain','high-gain'],include_lowest=True)
	data['capital_loss'] = pd.cut(data['capital_loss'],3,labels=['low-loss','med-loss','high-loss'],include_lowest=True)
	data['hours_per_week'] = pd.cut(data['hours_per_week'],[0,25,40,100],labels=['part-time','full-time','overtime'])
	return data

#reduce the transactions by removing the transactions which doesn't contain frequent k-itemsets
def transaction_reduction(D,Lk):
	#print 'Before:',len(D.index)
	rows_deleted = 0
	for row in D.iterrows():
		#print row
		row_values = []
		for i in range(0,len(row[1])):
			row_values.append(str(row[1][i]).strip())
		#print row_values
		trans = 0
		for l in Lk['items']:
			flag = True
			#print l
			for val in l:
				if val not in row_values:
					flag = False
			if flag:
				break
			trans += 1
		if trans==len(Lk):
			D.drop(row[0], inplace=True)
			rows_deleted += 1
	print 'Rows deleted:', rows_deleted
	#print 'After:',len(D.index)
	return D

#get all frequent 1-itemsets
def getL1(D, support_count):
	C1 = D.stack().value_counts()
	L1 = C1[C1>=support_count].reset_index().rename(columns={'index':'items', 0:'count'})
	L1 = L1.sort_values(['items'])
	column = L1['items']
	n = L1.columns[0]
	L1.drop(n,axis=1)
	values = []
	for val in column:
		ls = []
		ls.append(str(val).strip())
		values.append(ls)
	L1[n] = values
	L1 = L1.reset_index(drop=True)
	return L1

#check for infrequent subset
def has_infrequent_subset(c, Lk1):
	k1_subset = []
	#print "Inside infrequent subset"
	#print c
	ls = list(itertools.combinations(c, (len(c) - 1) ))
	#print ls
	for l in ls:
		s = list(l)
		s.sort()
		k1_subset.append(s)
	#print k1_subset
	
	for s in k1_subset:
		#print s, Lk1['items'].tolist()
		if s not in Lk1['items'].tolist():
			return True
	return False

#generate candidate k-itemsets
def apriori_gen(Lk1):
	Ck = []
	#print "Inside apriori gen"
	#print Lk1
	for i in range(0,len(Lk1)):
		for j in range(i+1,len(Lk1)):
			l1 = Lk1.iloc[i]['items']
			l2 = Lk1.iloc[j]['items']
			#print l1
			#print l2
			c=[]
			flag = True
			if len(l1) > 1:
				for m in range(0,len(l1)-1):
					if l1[m] != l2[m]:
						flag = False
						break
			if flag:
				if l1[len(l1)-1] < l2[len(l1)-1]:
					if len(l1) > 1:
						for m in range(0,len(l1)-1):
							c.append(l1[m])
					c.append(l1[len(l1)-1])
					c.append(l2[len(l1)-1])
			if len(c)>0:
				if not has_infrequent_subset(c,Lk1):	#check if c has infrequent subset
					Ck.append(c)
	#print "end"
	return Ck

#Apriori algorithm with transaction reduction for finding frequent itemsets
def apriori(D, min_sup):
	support_count = min_sup*len(D.index)/100
	print "Support count:", support_count
	
	L=[]
	#generate frequent 1-itemsets
	L1 = getL1(D,support_count)
	print "L1", L1
	L.append(L1)
	
	k=2
	while len(L[k-2])>0:
		Lk = pd.DataFrame()
		#generate candidate itemsets
		Ck = apriori_gen(L[k-2])
		#print "Ck",k-1,Ck
		if len(Ck) > 0:
			dict = {}
			#reduce the number of transactions
			D = transaction_reduction(D,L[k-2])
			print "Reading all transaction from D for k: ", k
			num_t = 0
			for row in D.iterrows():
				row_values = []
				for i in range(0,len(row[1])):
					row_values.append(str(row[1][i]).strip())
				#print row_values
				for c in Ck:
					flag = True
					#print c
					for val in c:
						if val not in row_values:
							flag = False
					if flag:
						dict[tuple(c)] = dict.get(tuple(c),0) + 1
				num_t+=1
				if (num_t%10000)==0:
					print "Read",num_t,"transactions"
			dict = {k:v for (k, v) in dict.items() if v >= support_count}
			dict = sorted(dict.items())
			itemsColumn = []
			countColumn = []
			for element in dict:
				itemsColumn.append(list(element[0]))
				countColumn.append(element[1])
			Lk['items'] = itemsColumn
			Lk['count'] = countColumn
			Lk.sort_values(['items'])
		k += 1
		
		L.append(Lk)
		print "L",k-1,Lk
	
	return L

data = preprocess(data)
L = apriori(data,min_sup)