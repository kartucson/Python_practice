import os
import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.tree import DecisionTreeClassifier

def data_input():
    df = pd.read_csv('https://raw.githubusercontent.com/kartucson/Python_practice/master/Classification_dataset.csv')
    cate_var = df.select_dtypes(['object'])  ## Filter out the categorical variables
    num_var = df.select_dtypes(['float64'])  ## Filter out the numerical inputs

    cate_in = cate_var.drop('Outcome',axis=1)  ## Remove the outcome variable
    output_var = cate_var.ix[:,-1]             ## Outcome as a dataframe  

    print df.count(axis=0, level=None, numeric_only=False)  ## Print the variables with non-zero count of values for each attribute

    df = df.drop(['White_noise','Room_type','Window_distance'],axis=1)  ## Remove the variables which have too many missing values ( > 50%)
    num_var = num_var.fillna(num_var.mean())   ## Impute the numerical input matrix with grand means for each attribute 

    categorical_ind = pd.DataFrame([])  ## Creating an empty dataframe 
    var_names = list(cate_in.columns.values)  ## Names of columns of categorical variables to use in the forthcoming loop

    for i in range(0,(cate_in.shape[1])):
        var_ind = pd.get_dummies(cate_in.ix[:,var_names[i]],prefix = var_names[i])   ## Creates {1,0} indicator variables 
        categorical_ind = pd.concat([categorical_ind,var_ind],axis=1)                  

    input_var = pd.concat([categorical_ind,num_var],axis=1) ## Concatenate the input dataset again
    return input_var, output_var

def model_fitting (input_var,output_var):
    model_set = []
    model_set = [LinearSVC, LogisticRegression, Perceptron, DecisionTreeClassifier,RandomForestClassifier]
    model_fit = []
    for m in range(0,len(model_set)-1):
        model_out = model_set[m]().fit(input_var,output_var)
        model_fit.append(model_out)  
    return model_fit 
    
def prediction_accuracy (model, input_var, output_var):         ## Function to compute insample prediction accuracy    
    model_pred = model.predict(input_var)
    model_pred = pd.DataFrame(model_pred)
    output_var = pd.DataFrame(output_var)

    Accuracy_mat = pd.concat([model_pred,output_var], axis=1)
    Accuracy_mat.columns = ['Predicted', 'Actual']
    
    Accuracy_count = 0
    for c in range(0,Accuracy_mat.shape[0]):                    ## compute prediction accuracy
        predicted = Accuracy_mat.ix[c,0]
        actual = Accuracy_mat.ix[c,1]
        if(predicted == actual):
            Accuracy_count = Accuracy_count + 1

    print "Accuracy of model is", np.round(float(Accuracy_count)/float(Accuracy_mat.shape[0])*100,2), "%" 
    
def main():
    input_matrix, output_matrix = data_input()
    model_list = ["SVM", "Logistic Regression", "Neural Networks", "Decision Trees","Random-Forest"]
    models = []
    models = model_fitting(input_matrix, output_matrix)
    for i in range(0,len(model_list)-1):
        print "Model performance for ", model_list[i], " classifier: \n", prediction_accuracy (models[i],input_matrix, output_matrix)
    #print "Model performance for Decision Tree classifier: \n", prediction_accuracy (Decision_tree,input_matrix, output_matrix)

if __name__=="__main__":
    main()
