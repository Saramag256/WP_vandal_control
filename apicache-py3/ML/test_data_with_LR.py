import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler

# прочитаем данные с атрибутами аккаунтов компаний на Facebook и активностью на них
fb = pd.read_csv('/datasets/dataset_facebook_cosmetics.csv', sep = ';')

# разделяем данные на признаки (матрица X) и целевую переменную (y)
X = fb.drop('Total Interactions', axis = 1)
y = fb['Total Interactions']

# разделяем модель на обучающую и валидационную выборку
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# стандартизируем данные методом StandartScaler
scaler = StandardScaler()
scaler.fit(X_train)
X_train_st = scaler.transform(X_train)
X_test_st = scaler.transform(X_test)

# зададим алгоритм для нашей модели
model = Lasso()

# обучим модель
model.fit(X_train_st, y_train)

# воспользуемся уже обученной моделью, чтобы сделать прогнозы
predictions = model.predict(X_test_st)

# создадим датафрейм с признаками и их весами
features = pd.DataFrame({'feature':X.columns, 'coeff':model.coef_})# воспользуйтесь методом coef_
features['coeff_abs'] = abs(features['coeff'])# напишите свой код здесь

# выведите упорядоченный по модулю коэффициентов фрейм с признаками
print(features.sort_values('coeff_abs', ascending=False))