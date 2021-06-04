# Библиотеки и файлы данных
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

df1 = pd.read_csv('D:\Better version of yesterdays you\query_1.csv')
df2 = pd.read_csv('D:\Better version of yesterdays you\query_3.csv')

# Предобработка данных
line = '###'
def dataminer(data):
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

dataminer(df1)
dataminer(df2)

# Конвертация для уменьшение нагрузки на ресурсы
df2['average_flights'] = df2['average_flights'].astype('float16')

# Построение графиков
df1.plot(x='model', y='flights_amount', kind='barh', figsize=(10, 4), grid=True, legend=False)
matplotlib.style.use('seaborn-darkgrid')
plt.title('Количество рейсов по каждой модели самолета')
plt.xlabel('количество рейсов')
plt.ylabel('модель самолета')
plt.show()

top10.sort_values('average_flights').plot(x='city', y='average_flights', kind='barh', grid=True, legend=False, figsize=(10,4))
matplotlib.style.use('seaborn-darkgrid')
plt.title('Среднее количество рейсов по топ-10 городам')
plt.xlabel('среднее количество рейсов')
plt.ylabel('город')
plt.show()




