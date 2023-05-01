import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn import datasets

X, y = datasets.make_regression(n_samples=200,
                                n_features=1,
                                n_targets=1,
                                noise=10)

model = LinearRegression()
model.fit(X, y)
pred = model.predict(X)
print("Model slope:    ", model.coef_[0])

plt.plot(X, pred, c="red")
plt.scatter(X, y)
plt.show()
