# подгружаем все необходимые библиотеки и файл данных
import pandas as pd
import datetime as dt
import numpy as np
from scipy import stats as st
import scipy.stats as stats
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# загрузим даннные и прочитаем их
try:
    df = pd.read_csv('logs_exp.csv')  #для Практикума
except:
    df = pd.read_csv('C://Users//Katumka//datasets//logs_exp.csv', sep='\s+')

# вставляем заранее заготовленную функцию для быстрого обзора данных, далее применяем ее к датасетам
line = '______________________________________'


def helicopter(data):
    print('\033[1m' + "Размер данных: {}".format(data.shape) + '\033[0m')
    print(line)

    print('\033[1m' + 'Первые и последние 5 строк данных' + '\033[0m')
    display(pd.concat([data.head(), data.tail()]))
    print(line)

    print('\033[1m' + "Количество пропусков в данных" + '\033[0m')
    nulls = data.isnull().sum()
    display(nulls)
    print(line)

    print('\033[1m' + "Количество дубликатов в данных" + '\033[0m')
    print(data.duplicated().sum())
    print(line)

    print('\033[1m' + "Типы данных" + '\033[0m')
    tmp = pd.DataFrame(
        data=[(col, data[col].dtypes) for col in
              data.columns],
        columns=['Название столбца', 'Тип данных']).set_index('Название столбца')
    display(tmp)
    print(line)

    print('\033[1m' + "Описание числовых данных" + '\033[0m')
    display(data.describe())
    print(line)

helicopter(df)

# построим гистограмму событий по времени
fig = go.Figure(data=[go.Histogram(x=df['fulldate'])])
fig.update_layout(height=500, width=1000, title_text="Распределение событий по времени", \
                 plot_bgcolor='#E0ECE4',
                 xaxis={"title":"дата и время события"},
                 yaxis={"title":"количество событий, шт"})
fig.update_traces(marker_color='#2f5d62')
fig.show()

# уникальных пользователи
df_id = df.id.unique()
df_aug_id = df.query('day < "2019-08-01"').id.unique()
id_repeat = list(set(df_id) & set(df_aug_id))
print(len(id_repeat))
print('Сколько уникальных пользователей потеряли после удаления данных июля', df_aug['id'].nunique() - len(id_repeat))

# построим воронку событий
df.sort_values(by='quantity', ascending=False)
user_unique = df.groupby('event')['id'].nunique().sort_values(ascending=False).to_frame()
user_unique.columns = ['unique_users']
user_unique['unique_users_share']= round((user_unique['unique_users']/user_unique['unique_users'].sum() * 100), 2)
user_unique
print(round((4613 / 7439 * 100), 2), '% переходят на шаг "появление экрана предложения"')
print(round((3749 / 4613 * 100), 2), '% переходят на шаг "появление экрана корзины"')
print(round((3547 / 3749 * 100), 2), '% переходят на шаг "появление оповещения об успешной оплате"')

# сформируем листы по группам, содержащие уникальных пользователей
group_246 = df_work.query('group == 246').id.unique()
group_247 = df_work.query('group == 247').id.unique()
group_248 = df_work.query('group == 248').id.unique()

# сформируем лист, в котором будут повторяющиеся пользователи в группах
id_246_247 = list(set(group_246) & set(group_247))
id_247_248 = list(set(group_247) & set(group_248))
id_246_248 = list(set(group_246) & set(group_248))
print("Количество пользователей, входящих в группы")
print("246 и 247", len(id_246_247))
print("246 и 248", len(id_246_248))
print("247 и 248", len(id_247_248))

# создаем массив уникальных пар значений дат и групп теста
datesGroups = df[['date','group']].drop_duplicates()
orders = df[['date','group']]

# получаем агрегированные кумулятивные по дням данные о заказах
ordersAggregated = (datesGroups
          .apply(lambda x: orders[np.logical_and(orders['date'] <= x['date'], orders['group'] == x['group'])]
          .agg({'date' : 'max', 'group' : 'max', 'transactionId' : pd.Series.nunique,
                'visitorId' : pd.Series.nunique, 'revenue' : 'sum'}), axis=1)
          .sort_values(by=['date','group']))

# объединяем кумулятивные данные в одной таблице и присваиваем ее столбцам понятные названия
cumulativeData = ordersAggregated.merge(visitorsAggregated, left_on=['date', 'group'], right_on=['date', 'group'])
cumulativeData.columns = ['date', 'group', 'orders', 'buyers', 'revenue', 'visitors']
cumulativeData.head()

df_id = df.id.unique()
df_aug_id = df.query('day < "2019-08-01"').id.unique()
id_repeat = list(set(df_id) & set(df_aug_id))
print(len(id_repeat))
print('Сколько уникальных пользователей потеряли после удаления данных июля', df['id'].nunique() - len(id_repeat))