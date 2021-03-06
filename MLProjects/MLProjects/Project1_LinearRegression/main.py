﻿import numpy as np
from normalizeDatas import normalizeDatas


# CONFIG ------------------------------------
IGNORED_DIMENSIONS = [] # Input dimensions which shall be ignored
DEGREE_OF_POLYNOMIAL_REGRESSION = 1 # The degree of the highest polynom of the polynomial regression
REGULATION_Y = 2 # 0 = Least Squares, 1 = Lasso, 2 = Ridge
REGULATION_LAMBDA = 1 # Influence factor of regulation
INCLUDE_BIAS = True # this option activates the bias/intercerpt. Should be of course always activated.
NORMALIZE = True # when this option is activated the input data is normalized


# DATA HELPERS ------------------------------
def importData (path, validation = False):
    """ Imports the data. 
    Used for trainings and validation datafiles of project1.

    Parameters:
        path - path to the file, that contains the data
        training - defines whether Y is created and returned
        
    Returns:
        vector of IDs
        matrix of Vector for each dim
        vector of Y
        The Vectors are of course as long as the imput file is long

    Raises:
        IOError - when file cannot be found or opened
    """
    ids, targets = [], []
    variables = [[] for x in xrange(14-len(IGNORED_DIMENSIONS))]
    with open(path, 'r') as file:
        for line in file:
            line = line.strip().split(",") 
            ids.append(int(line[0]))
            if validation:
                intervall = line[1:]
            else:
                targets.append(float(line[-1]))
                intervall = line[1:-1]

            i = 0
            for j in intervall:
                if j not in IGNORED_DIMENSIONS:
                    variables[i].append(float(j))
                    i+=1                   
    if validation:
        return np.array(ids), np.transpose(np.matrix(variables))
    else:
        return np.array(ids), np.transpose(np.matrix(variables)), np.transpose(np.matrix(targets))


def writeResult (ids, delays, filename):
    """ Write the result to file. 
    Writes the result to the specified file,
    in the kaddle-compatible way.
    
    Parameters:
        ids - array of the ids
        delays - array of the predicted delays
                 in same order as ids
        filename - the filename including the path
    """

    if not filename.endswith('.csv'):
        filename += ".csv"  
    file = open(filename, 'w+')
    file.write("Id,Delay\n")
    for cur in zip(ids, delays):
        file.write(str(cur[0]) + "," + str(cur[1].item(0)) + "\n")



# ESTIMATORS---------------------------------
def leastSquares (X, Y):
    W = np.transpose(X) * X
    W = np.linalg.inv(W)
    W = W * np.transpose(X)
    return W * Y

def ridgeRegression (X, Y):
    W = np.transpose(X) * X + REGULATION_LAMBDA * np.identity(X.shape[1])
    W = np.linalg.inv(W)
    W = W * np.transpose(X)
    return W * Y 



# MAIN PROGRAM ------------------------------
if __name__ == "__main__":
    # Import data
    ids, X, Y = importData("Project1_LinearRegression/data/train.csv");
    
    if NORMALIZE:
        X, Y, a,b,c,d = normalizeDatas(X,Y)

    X_basic = X
    for i in xrange(2,DEGREE_OF_POLYNOMIAL_REGRESSION+1):
        X = np.c_[X,np.power(X_basic,i)]

    if (INCLUDE_BIAS):
        X = np.c_[np.ones(X.shape[0]),X]


    # Determin the minimal Beta Vector by LeastSquaresEstimate
    if REGULATION_Y == 0 :
        B = leastSquares(X, Y)
    elif REGULATION_Y == 2 :
        B = ridgeRegression(X, Y)

    # Predict the result
    idsPredict, XPredict = importData("Project1_LinearRegression/data/validate_and_test.csv", validation = True)
    X_basic = XPredict
    for i in xrange(2,DEGREE_OF_POLYNOMIAL_REGRESSION+1):
        XPredict = np.c_[XPredict, np.power(X_basic,i)]
    if (INCLUDE_BIAS):
        XPredict = np.c_[np.ones(XPredict.shape[0]),XPredict]

        
    YPredict = XPredict * B

    
    if NORMALIZE:
        XPredict, YPredict, a,b,c,d = normalizeDatas(XPredict, YPredict)


    # Output the result
    writeResult(idsPredict, YPredict, "Project1_LinearRegression/results/results.csv");
