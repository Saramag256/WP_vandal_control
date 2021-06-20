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
hypothesis = pd.read_csv('C://Users//Katumka//datasets//hypothesis.csv')
orders = pd.read_csv('orders.csv')
visitors = pd.read_csv('visitors.csv')

# зададим количество символов для отображения
pd.options.display.max_colwidth = 150

# рассчитаем показатели и отсортируем их по убыванию
hypothesis['ICE'] = (hypothesis['Impact'] * hypothesis['Confidence'] / hypothesis['Efforts']).round(1)
hypothesis.sort_values(by='ICE', ascending=False)

# вставляем заранее заготовленную функцию для быстрого обзора данных, далее применяем ее к датасетам
line = '______________________________________'

def helicopter(data):
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

helicopter(visitors)
helicopter(orders)

# преобразуем даты к типу дат pd.to_datetime
orders['date'] = orders['date'].map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
visitors['date'] = visitors['date'].map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))

# применим группировку по группам с подсчетом уникальных пользователей
orders.groupby('group')['visitorId'].nunique()

# сформируем листы по группам, содержащие уникальных пользователей
group_A = orders.query('group == "A"').visitorId.unique()
group_B = orders.query('group == "B"').visitorId.unique()

# сформируем лист, в котором будут повторяющиеся пользователи в группах
visitor_everywhere = list(set(group_A) & set(group_B))
print("Количество пользователей, входящих в группу А и в группу В", len(visitor_everywhere))

# создаем массив уникальных пар значений дат и групп теста
datesGroups = orders[['date','group']].drop_duplicates()

# получаем агрегированные кумулятивные по дням данные о заказах
ordersAggregated = (datesGroups
          .apply(lambda x: orders[np.logical_and(orders['date'] <= x['date'], orders['group'] == x['group'])]
          .agg({'date' : 'max', 'group' : 'max', 'transactionId' : pd.Series.nunique, \
                'visitorId' : pd.Series.nunique, 'revenue' : 'sum'}), axis=1)
          .sort_values(by=['date','group']))

# получаем агрегированные кумулятивные по дням данные о посетителях интернет-магазина
visitorsAggregated = (datesGroups
          .apply(lambda x: visitors[np.logical_and(visitors['date'] <= x['date'], visitors['group'] == x['group'])]
          .agg({'date' : 'max', 'group' : 'max', 'visitors' : 'sum'}), axis=1)
          .sort_values(by=['date','group']))

# объединяем кумулятивные данные в одной таблице и присваиваем ее столбцам понятные названия
cumulativeData = ordersAggregated.merge(visitorsAggregated, left_on=['date', 'group'], right_on=['date', 'group'])
cumulativeData.columns = ['date', 'group', 'orders', 'buyers', 'revenue', 'visitors']

cumulativeData.head()

# построим графики кумулятивной выручки по дням и группам A/B-тестирования
# датафрейм с кумулятивным количеством заказов и кумулятивной выручкой по дням в группе А
cumulativeRevenueA = cumulativeData[cumulativeData['group']=='A'][['date','revenue', 'orders']]

# датафрейм с кумулятивным количеством заказов и кумулятивной выручкой по дням в группе B
cumulativeRevenueB = cumulativeData[cumulativeData['group']=='B'][['date','revenue', 'orders']]

# строим графики выручки групп А и В
fig = go.Figure()
fig.add_trace(go.Scatter(x=cumulativeRevenueA['date'], y=cumulativeRevenueA['revenue'],name='группа A', line=dict(color='#2f5d62')))
fig.add_trace(go.Scatter(x=cumulativeRevenueB['date'], y=cumulativeRevenueB['revenue'],name='группа B', line=dict(color='#ffc93c')))
fig.update_traces(hoverinfo='x+y', mode='lines+markers')
fig.update_layout(height=500, width=700, title_text="Кумулятивная выручка по группам", plot_bgcolor='#E0ECE4')
fig.update_xaxes(title_text='дата')
fig.update_yaxes(title_text='выручка, млн')
fig.show()