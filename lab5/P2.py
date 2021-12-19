import numpy as np
import matplotlib.pyplot as plt
def sigmoid(x):
    return 1/(1+np.exp(-x))
def judge(x,threshold):
    ans=[]
    for i in x:
        if i>threshold:ans.append(1)
        else:ans.append(0)
    return np.array(ans)
def CELoss_binary(X, y, theta):
    '''
    paras: X is a mini-batch of samples, y is the true label of the samples
        in the mini-batch, theta is the parameter we need to learn in logistic regression
    return: the binary cross entropy
    '''
    sigmoid_theta_x=sigmoid(np.dot(theta,X.T))
    return (-np.dot(y,np.log(sigmoid_theta_x))-np.dot((1-y),np.log(1-sigmoid_theta_x))).mean()

    """Your code here"""

def precision(y_true, y_predict):
    '''
    paras: y_true is the true label, y_predict is the predicted label of your model
    return: the precision
    '''
    return np.sum(y_true == y_predict) / y_true.shape[0]

def gradient(X, y, theta):
    '''
    paras: X is a mini-batch of samples, y is the true label of the samples
        in the mini-batch, theta is the parameter we need to learn in logistic regression
    return: the mini-batch gradient of the binary cross entropy loss function with respect to 
        the parameter theta for a given mini-batch of samples
    '''
    """Your code here"""
    
    return np.dot(sigmoid(np.dot(theta,X.T))-y,X)/len(X)
def get_gradient(X,y,theta,method):
    if method=='stochastic':
        import random
        item=random.randint(0,len(X)-1)
        return gradient(X[item:item+1],y[item:item+1],theta)
    elif method=='mini-batch':
        batch_size=10
        sets=set()
        import random
        while(len(sets)<batch_size):
            item=random.randint(0,len(X)-1)
            if item not in sets:sets.add(item)
        list_x,list_y=[],[]
        for i in sets:
            list_x.append(X[i])
            list_y.append(y[i])
        return gradient(np.array(list_x),np.array(list_y),theta)
    elif method=='batch':
        return gradient(X,y,theta)
    else:
        print("no method")
        exit()
def train(learning_rates,thresholds,X_all,y_all):
    iteration_size=10000
    methods=["stochastic",'mini-batch','batch']
    for method in methods:
        for threshold in thresholds:
            line=[]
            name=[]
            for learning_rate in learning_rates:
                theta=np.array([0,0])
                Time=[]
                Loss=[]
                Precise=[]
                for i in range(iteration_size):
                    gradients=get_gradient(X_all,y_all,theta,method)
                    theta=theta-learning_rate*gradients
                    y_predict=judge(sigmoid(np.dot(theta,X_all.T)),threshold)
                    if i%100==0:
                        Precise.append(precision(y_all,y_predict))
                        Time.append(i+1)
                        Loss.append(CELoss_binary(X_all,y_all,theta))
                # l1,=plt.plot(Time,Precise,linewidth = '1')
                # line.append(l1)
                # name.append('Precise:learning rate=%.2f'%learning_rate)
                l2,=plt.plot(Time,Loss,linewidth = '1')
                line.append(l2)
                name.append('Loss:learning rate=%.2f'%learning_rate)
            plt.legend(handles=line,labels=name)
            plt.title("Descent Method="+method+" threshold=%.2f"%threshold)
            plt.savefig("fig/Loss "+method+" threshold=%.2f"%threshold+".png")
            plt.clf()
    return
if __name__ == "__main__":
    X_all, y_all = np.load('Data2_X.npy'), np.load('Data2_Y.npy')
    learning_rate=[0.5,0.1,0.02]
    threshold=[0.2,0.5,0.8]
    train(learning_rate,threshold,X_all,y_all)
    """Your code here"""

    