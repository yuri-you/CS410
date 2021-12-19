# <center>Lab 5 </center>

<font face="楷体" size=4>

<p align="right"> 姓名：游灏溢<br/>班级：F1903302<br/>时间：3/11/2021 </p>

[toc]


## Exercise1 Linear Regression

Transform the array into the matrix and use the formula to finish the linear regression(Using matrix can provide the inverse matrix X.T to help calculate).

$$\theta=(X\cdot X^T)^{-1}\cdot X^T\cdot y\\\hat{y}=\theta\cdot X$$

```python
    X1=np.mat(X)
    Y1=np.mat(Y)
    theta=(X1.T*X1).I*X1.T*Y1
    Y2=X1*theta
```

The linear regression can map the $X$(in 500-dimension space) into 100-dimension space.


## Exercise2 Logistic Regression
We choose 

```python
learning_rate=[0.5,0.1,0.02]
threshold=[0.2,0.5,0.8]
```

Since it is hard to place all the line in one graph, here I draw 9 graphs, you can refer them in the appendice.

Based on the result, we can have

1. When the learning rate increasing, the decreasing speed of loss and increasing speed of precise will be fast, but when it is to high, both of two will be not stable and fluctuate.
2. Learning speed are all similar, but the stochastic is too instable, especially when the learning rate is high
3. The difference between different threshold is no very distinct.
According to the result, for decision boundary of predictions, when the threshold is large, the predict will have more on 0 than 1. 

## Exercise 3 L1/L2 Regularization

1. I record the time w.r.t 2 methods and compare its distance, Here is

   ![image-20211218234102864](C:\Users\yurii\AppData\Roaming\Typora\typora-user-images\image-20211218234102864.png)

   So Ridge cost a little bit more time than Lasso
   
2. Based on the data, the Lasso create a sparser output.

3.  It's a trade-off. More regularization will force to choose larger $\lambda$, thus makes more errors between the predict and actual data. When dealing with the complex model, we should take both the regularization and generalizability into consideration, in order to guarantee both precision and avoid overfitting .

   ![Ridge](C:\交大\大三上\ai\ai_homework\lab5\fig\Ridge.png)

   ![Lasso](C:\交大\大三上\ai\ai_homework\lab5\fig\Lasso.png)

## Exercise 4: Two-layer Perceptron Network

Here is the result

neurons=2

![Figure_4](C:\交大\大三上\ai\ai_homework\lab5\fig\Figure_4.png)

neurons=20

![Figure_20](C:\交大\大三上\ai\ai_homework\lab5\fig\Figure_20.png)

neurons=100

![Figure_100](C:\交大\大三上\ai\ai_homework\lab5\fig\Figure_100.png)

We can find more neurons will make more precise result.

But it also cause more calculations

## Appendice

![stochastic threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Precise stochastic threshold=0.20.png)

![stochastic threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Precise stochastic threshold=0.50.png)

![stochastic threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Precise stochastic threshold=0.80.png)

![mini-batch threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Precise mini-batch threshold=0.20.png)

![mini-batch threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Precise mini-batch threshold=0.50.png)

![mini-batch threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Precise mini-batch threshold=0.80.png)

![batch threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Precise batch threshold=0.20.png)

![batch threshold=0.50](C:\交大\大三上\ai\ai_homework\lab5\fig\Precise batch threshold=0.20.png)

![batch threshold=0.80](C:\交大\大三上\ai\ai_homework\lab5\fig\Precise batch threshold=0.20.png)

![stochastic threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Loss stochastic threshold=0.20.png)

![stochastic threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Loss stochastic threshold=0.50.png)

![stochastic threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Loss stochastic threshold=0.80.png)

![mini-batch threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Loss mini-batch threshold=0.20.png)

![mini-batch threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Loss mini-batch threshold=0.50.png)

![mini-batch threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Loss mini-batch threshold=0.80.png)

![batch threshold=0.20](C:\交大\大三上\ai\ai_homework\lab5\fig\Loss batch threshold=0.20.png)

![batch threshold=0.50](C:\交大\大三上\ai\ai_homework\lab5\fig\Loss batch threshold=0.20.png)

![batch threshold=0.80](C:\交大\大三上\ai\ai_homework\lab5\fig\Loss batch threshold=0.20.png)