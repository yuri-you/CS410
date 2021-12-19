import numpy as np

if __name__ == "__main__":
    X = np.load('Data1_X.npy')
    Y = np.load('Data1_Y.npy')
    X1=np.mat(X)
    Y1=np.mat(Y)
    theta=(X1.T*X1).I*X1.T*Y1
    Y2=X1*theta
    """Your code here"""



