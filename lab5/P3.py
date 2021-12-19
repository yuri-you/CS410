import time

import matplotlib.pyplot as plt
import numpy as np

from utils import plot, prepare_data_sine


def ridge_regression(x, y, lamda):
    # Normalize data.
    x = (x - x.mean(axis=-1, keepdims=True)) / x.std(axis=-1, keepdims=True)

    """Your code here"""
    from sklearn import linear_model
    ridge=linear_model.Ridge(alpha=lamda)
    ridge.fit(x,y)
    y_pred =ridge.predict(x) # predicted labels of size (n_samples, )
    intercept = ridge.intercept_ # b of size ()
    coef = ridge.coef_  # theta of size (n_dims, )

    return y_pred, intercept, coef

def lasso_regression(x, y, lamda):
    # Normalize data.
    x = (x - x.mean(axis=-1, keepdims=True)) / x.std(axis=-1, keepdims=True)
    from sklearn import linear_model
    lasso=linear_model.Lasso(alpha=lamda)
    lasso.fit(x,y)
    y_pred =lasso.predict(x) # predicted labels of size (n_samples, )
    intercept = lasso.intercept_ # b of size ()
    coef = lasso.coef_  # theta of size (n_dims, )

    return y_pred, intercept, coef

def main():
    # Prepare data.
    x, y = prepare_data_sine()
    plot(x[:, 0], y, 111)
    plt.show()

    # Set the different values of lambda to be tested.
    lamda_ridge = [1e-15, 1e-10, 1e-4, 1e-3, 1e-2, 5]
    plot_pos = [231, 232, 233, 234, 235, 236]
    T1,T2=[],[]
    for lamda, pos in zip(lamda_ridge, plot_pos):
        start = time.time()
        y_pred, intercept, coef = ridge_regression(x, y, lamda)
        time_cost = time.time() - start
        T1.append(time_cost)
        rss = sum((y_pred - y) ** 2)
        sparsity = np.mean(np.abs(coef) < 1e-7) * 100
        print(time_cost, rss, sparsity)
        print("spacity%f"%sparsity)
        plot(x[:, 0], y, pos, y_pred=y_pred, title=f"Ridge ($\lambda$={lamda:.3g})")

    # plt.show()

    # Set the different values of lambda to be tested.
    lamda_lasso = [1e-10, 1e-5, 1e-4, 1e-3, 1e-2, 1]
    plot_pos = [231, 232, 233, 234, 235, 236]

    for lamda, pos in zip(lamda_lasso, plot_pos):
        start = time.time()
        y_pred, intercept, coef = lasso_regression(x, y, lamda)
        time_cost = time.time() - start
        T2.append(time_cost)

        rss = sum((y_pred - y) ** 2)
        sparsity = np.mean(np.abs(coef) < 1e-7) * 100
        print(time_cost, rss, sparsity)
        print("spacity%f"%sparsity)

        plot(x[:, 0], y, pos, y_pred=y_pred, title=f"Lasso ($\lambda$={lamda:.3g})")

    # plt.show()
    print("Time distance=%f"%(np.array(T1).mean()-np.array(T2).mean()))
if __name__ == "__main__":
    main()
