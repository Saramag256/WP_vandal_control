import pandas as pd
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt

# прочитайте данные с атрибутами аккаунтов компаний на facebook и активностью на них
fb = pd.read_csv('/datasets/dataset_facebook_cosmetics.csv', sep = ';')

# разделите данные на признаки (матрица X) и целевую переменную (y)
X = fb.drop('Total Interactions', axis = 1)
y = fb['Total Interactions']

# разделяем модель на обучающую и валидационную выборку
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# гистограмма целевой переменной на train
sns.distplot(y_train)# напишите ваш код здесь

# гистограмма целевой переменной на test
sns.distplot(y_test)# напишите ваш код здесь
# корреляционная матрица
corr_m = fb.corr() # напишите ваш код здесь

# нарисуем heatmap
sns.heatmap(corr_m, square = True, annot = True)
plt.figure(figsize = (15,15))

#I нужно подробнее исследовать данные - гистограмма и прямая сверка имеющихся признаков недостаточна.
