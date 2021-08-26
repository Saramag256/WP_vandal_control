import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# прочитайте данные с атрибутами аккаунтов компаний на facebook и активностью на них
fb = pd.read_csv("/datasets/dataset_facebook_cosmetics.csv", sep =';')

# разделите данные на признаки (матрица X) и целевую переменную (y)
X = fb.drop('Total Interactions', axis = 1)
y = fb['Total Interactions']

# разделяем модель на обучающую и валидационную выборку
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# зададим алгоритм для нашей модели
model = RandomForestRegressor(random_state=0) # задайте модель как элемент класса RandomForestRegressor (random_state=0)

# обучим модель
model.fit(X_train, y_train)# обучите вашу модель на обучающей выборке

# воспользуемся уже обученной моделью, чтобы сделать прогнозы
predictions = model.predict(X_test) # сделайте прогноз для валидационной выборки с помощью вашей модели

# оценим метрику R-квадрат на валидационной выборке и напечатаем
r2 = r2_score(y_test, predictions) # напишите свой код здесь
print('Значение метрики R-квадрат: ', r2)

#I: результат в 0,733 низок для продакшена