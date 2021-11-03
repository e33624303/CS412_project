import numpy as np
from sklearn.linear_model import LinearRegression
from data import data_init
import matplotlib.pyplot as plt

data = data_init()
X = np.array([data['Population'], data['Density'], data['Land Area'], data['Years']]).T
Y = np.array(data['Deaths']).T

regr = LinearRegression().fit(X[:3000, :], Y[:3000])

Y_pr = regr.predict(X[3000:])
print(np.mean(np.square(Y[3000:]-Y_pr)))

X_axis = np.array([data['Country']]).T+np.array(['-'])+np.array([data['Years']], dtype=str).T
ticks = []

for i in range(X_axis[3000:].shape[0]):
    ticks.append(i)
ticks = np.array(ticks)
plt.plot(ticks, Y_pr)
plt.scatter(ticks, Y[3000:],c='r', s=1)
plt.show()

