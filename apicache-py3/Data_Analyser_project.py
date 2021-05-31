import pandas as pd
import numpy as np
from scipy import stats as st
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/Katumka/PycharmProjects/WP_vandal_control/apicache-py3/music_project.csv')

line = '==='

# Отображение датасетов
def showdata(data):
    print("Размер данных: {}".format(data.shape))
    print(line)

    print("Первые и последние 5 строк данных")
    display(pd.concat([data.head(), data.tail()]))
    print(line)

    print("Количество пропусков в данных")
    nulls = data.isnull().sum()
    display(nulls)
    print(line)

    print("Количество дубликатов в данных")
    print(data.duplicated().sum())
    print(line)

    print("Типы данных")
    tmp = pd.DataFrame(
        data=[(col, data[col].dtypes) for col in
              data.columns],
        columns=['Название столбца', 'Тип данных']).set_index('Название столбца')
    display(tmp)
    print(line)

    print("Описание данных")
    display(data.describe())
    print(line)

# Функция вывода самого популярного региона
def pivot_user_reg(region, param):
    pivot_reg = df_actual.pivot_table(index=param, values=region, aggfunc=('count', 'sum')).sort_values(by='sum', ascending=False)
    pivot_reg['share'] = (pivot_reg['sum'] / pivot_reg['sum'].sum() * 100).round()
    if region == 'na_sales':
        reg = 'Северной Америке'
    elif region == 'eu_sales':
        reg = 'Европе'
    else:
        reg = 'Японии'
    return print('сводная таблица по продажам в {} по {}'.format(reg, param),  pivot_reg.head(5), sep='\n')

# Обработка исходных данных
df.columns = map(str.lower, df.columns)
df['name'].isna().sum()
df.dropna(subset = ['name'], inplace=True)
df = df.reset_index(drop=True)

# Заполнение значениями по умолчанию
df['year_of_release'] = df['year_of_release'].fillna(2020)

df['critic_score'].fillna(df.groupby('genre')['critic_score'].transform('median'), inplace=True)
df['user_score'] = df['user_score'].replace('tbd', 77777)
df['user_score'] = df['user_score'].astype(float)

# Построение графика
pivot_platform_year = (
    df.query('year_of_release != 2020')
    .pivot_table(index=['year_of_release'],columns='platform', values='sales_total', aggfunc='sum')
)
pivot_platform_year.plot(kind='line', grid=True, figsize=(15,9))
plt.title('График продаж')
plt.show()

# Коэффициента корреляции Пирсона 0-0
print(df_actual.query('platform =="PS4"')['sales_total'].corr(df_actual.query('platform =="PS4"')['critic_score']))


























