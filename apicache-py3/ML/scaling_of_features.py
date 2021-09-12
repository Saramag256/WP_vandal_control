import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# прочитайте данные с атрибутами аккаунтов компаний на Facebook и активностью на них
fb = pd.read_csv('/datasets/dataset_facebook_cosmetics.csv', sep = ';')

# разделяем данные на признаки (матрица X) и целевую переменную (y)
X = fb.drop('Total Interactions', axis = 1)
y = fb['Total Interactions']

# выведите название признаков в датасете
print(X.columns) # ваш код здесь

# разделяем модель на обучающую и валидационную выборку
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# выведите среднее и стандартное отклонение признака 'Page total likes'
print('Mean for train', np.mean(X_train['Page total likes']))
print('Std for train', np.std(X_train['Page total likes']))

# стандартизируем данные
scaler = StandardScaler()
scaler.fit(X_train)# обучите scaler на обучающей выборке методом fit
X_train_st = scaler.transform(X_train) # стандартизируйте обучающую выборку методом transform scaler
X_test_st = scaler.transform(X_test) # стандартизируйте тестовую выборку методом transform scaler

print('Mean for standartized train', np.mean(X_train_st[:,0]))
print('Std for standartized train', np.mean(X_test_st[:,0]))
print('Mean for standartized test', np.std(X_train_st[:,0]))
print('Std for standartized test', np.std(X_test_st[:,0]))