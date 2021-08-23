import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import seaborn as sns

#train data
fb = pd.read_csv('/datasets/dataset_facebook_cosmetics.csv', sep = ';')

#data crop
X = fb.drop('Total Interactions', axis = 1)
y = fb['Total Interactions']

model = RandomForestRegressor()

#ML
model.fit(X, y)

#prediction
predictions = model.predict(X)

#show plot
sns.scatterplot(y, predictions, s = 15, alpha = 0.6)
plt.title('График Прогноз-Факт')
plt.ylabel('Прогноз')
plt.xlabel('Факт')
plt.show()

##I: очевидно, что есть переобучение + тест по тем же данным