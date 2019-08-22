from sklearn import preprocessing
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import svm

import scipy.stats as stats
from sklearn.cross_validation import train_test_split
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from neo4j import GraphDatabase

def SVMTrain():
	file_read_flow = open('analysis.csv')

	x_test = []
	y_test = []
	index1 = 0
	index2 = 0
	threshhold = 20
	for line in file_read_flow:
		a = str(line).split(',')
		for i in range(7):
			a[i] = float(a[i])
		x_test.append(a[0:6])

		if a[6] < threshhold:
			index1 += 1
			a[6] = 0.0
		if a[6] >= threshhold:
			index2 += 1
			a[6] = 1.0
			'''
            for j in range(3):
                x_test.append(a[1:5])
                y_test.append(a[5])'''

		'''if a[5]>=27:

            a[5]=2.0'''
		y_test.append(a[6])

	print(index1, index2)

	INDEX = np.arange(index1 + index2)
	np.random.shuffle(INDEX)
	x_test = np.array(x_test)
	y_test = np.array(y_test)
	x_test = x_test[INDEX, :]
	y_test = y_test[INDEX]

	refined_list = []
	count = 0
	for i in range(index1 + index2):
		if y_test[i] == 1:
			refined_list.append(i)
		else:
			count += 1
			if count <= 355:
				refined_list.append(i)

	x_test = x_test[refined_list, :]
	y_test = y_test[refined_list]

	X = np.array(x_test)
	X = X[:, [1, 2, 3, 4, 5]]
	print(X[0])
	Y = np.array(y_test)

	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=3)
	clf = svm.SVC(kernel='rbf', C=50, decision_function_shape="ovo")
	clf.fit(X_train, Y_train)
	return clf

def getFlightInfo(FlightNO):
    driver = GraphDatabase.driver("bolt://192.168.15.150:7687", auth=('neo4j', '123'))
    match_FlightNO = "MATCH (n:FlightObject) WHERE n.name=~\""+FlightNO+".*\" RETURN n LIMIT 1"
    result_list=[]
    with driver.session() as session:
        results = session.run(match_FlightNO).values()
        for result in results:
            result_list.append(result[0]._properties)
    return result_list[0]

def delayPredict(clf,FlightInfo):
	print(clf.predict([[9, 101, 38, 31, 100]]))


example = getFlightInfo("CSN6446")

print(example)
# print(example["AveFlyTime"])

def save_model():
	clf = SVMTrain()
	joblib.dump(clf,"svm_model.m")

def svm_test():
	clf_load = joblib.load("svm_model.m")
	c = clf_load.predict([[9, 101, 38, 31, 590]])
	print(c)

if __name__ =='__main__':
	svm_test()