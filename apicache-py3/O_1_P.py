# подгружаем все необходимые библиотеки и файлы данных
import pandas as pd
import numpy as np
from scipy import stats as st
import seaborn as sns
from matplotlib import pyplot as plt

visits = pd.read_csv('visits_log.csv')
orders = pd.read_csv('orders_log.csv')
costs = pd.read_csv('costs.csv')

# стандартная обработка
visits.columns = ['device', 'end_ts', 'source_id', 'start_ts', 'uid']
orders.columns = ['buy_ts', 'revenue', 'uid']
visits['start_ts'] = pd.to_datetime(visits['start_ts'])
visits['end_ts'] = pd.to_datetime(visits['end_ts'])
orders['buy_ts'] = pd.to_datetime(orders['buy_ts'])
costs['dt'] = pd.to_datetime(costs['dt'])

# задание 1
visits['duration'] = (visits['end_ts'] - visits['start_ts'])
print('количество сессий с продолжительностью 0 секунд и меньше:', len(visits.query('duration <= "00:00:00"')))
print('процент сессий с продолжительностью 0 секунд и меньше:', len(visits.query('duration <= "00:00:00"')) / len(visits) * 100)
print('количество сессий с отрицательной продолжительностью:', len(visits.query('duration < "00:00:00"')))

# сделаем сводную таблицу и построим на её основе распределение по датам
pivot_no_zero = (
    visits.query('duration == 0')
    .pivot_table(index=['end_ts'], values='duration', aggfunc='count')
)
pivot_no_zero.plot(grid=True, figsize=(20,5), legend=False)
plt.xlabel('дата')
plt.ylabel('количество нулевых сессий')
plt.title('распределение нулевых сессий по датам')
plt.show()

# сгруппируем таблицу по дням, количеству визитов и уникальных пользователей
visits_per_user = visits.groupby(['day']).agg({'uid': ['count','nunique']})
visits_per_user.columns = ['n_sessions', 'n_users']

# разделим число сессий на количество пользователей за период
visits_per_user['visits_per_user'] = visits_per_user['n_sessions'] / visits_per_user['n_users']
print('В день один пользователь в среднем заходит на сайт',visits_per_user['visits_per_user'].mean().round(2),'раз.')
print("Медианное значение продолжительности сесии", visits['duration'].median() / 60, "минут")

# найдем дату первой активности пользователей
first_activity_date = visits.groupby(['uid'])['start_ts'].min()

# изменим имя столбца
first_activity_date.name = 'first_activity_date'

# объединим его с исходным датафреймом
visits = visits.join(first_activity_date,on='uid')

# выделим месяцы
visits['activity_month'] = visits['start_ts'].astype('datetime64[M]')
visits['first_activity_month'] = visits['first_activity_date'].astype('datetime64[M]')

# получаем целое число месяцев, обозначающее порядковый месяц совершения покупки относительно месяца первой покупки
visits['cohort_lifetime'] = visits['activity_month'] - visits['first_activity_month']
visits['cohort_lifetime'] = (visits['cohort_lifetime'] / np.timedelta64(1, 'M')).round()
visits['cohort_lifetime'] = visits['cohort_lifetime'].astype('int')

# формируем когорты
cohorts = visits.groupby(['first_activity_month','cohort_lifetime']).agg({'uid':'nunique'}).reset_index()

# выделим колонку с месяцем
orders['buy_month'] = orders['buy_ts'].astype('datetime64[M]')

# получим месяц первой покупки каждого покупателя
first_orders = orders.groupby('uid').agg({'buy_month': 'min'}).reset_index()
first_orders.columns = ['uid', 'first_order_month']

# посчитаем количество новых покупателей (n_buyers) за каждый месяц
cohort_sizes = first_orders.groupby('first_order_month').agg({'uid': 'nunique'}).reset_index()
cohort_sizes.columns = ['first_order_month', 'n_buyers']

# создадим когорты. Добавим месяц первой покупки каждого покупателя в таблицу с заказами
orders_new = pd.merge(orders,first_orders, on='uid')

# сгруппируем таблицу заказов по месяцу первой покупки и месяцу каждого заказа и посчитаем кол-во заказов сбросим индекс методом reset_index()
cohorts_orders = orders_new.groupby(['first_order_month','buy_month']).agg({'revenue': 'count'}).reset_index()
cohorts_orders.columns = ['first_order_month', 'buy_month', 'n_orders']

# добавим в таблицу cohorts данные о том, сколько людей первый раз совершили покупку в каждый месяц
orders_cohorts = pd.merge(cohort_sizes, cohorts_orders, on='first_order_month')

# сгруппируем таблицу заказов по месяцу первой покупки и месяцу каждого заказа и сложим выручку сбросим индекс методом reset_index()
cohorts_orders_ltv = orders_new.groupby(['first_order_month', 'buy_month']).agg({'revenue': 'sum'}).reset_index()
cohorts_orders_ltv.columns = ['first_order_month', 'buy_month', 'revenue']
cohorts_orders_ltv

# добавим в таблицу cohorts данные о том, сколько людей первый раз совершили покупку в каждый месяц
ltv = pd.merge(cohort_sizes, cohorts_orders_ltv, on='first_order_month')

# добавим столбец с возрастом когорт
ltv['gp'] = ltv['revenue']
ltv['age'] = (ltv['buy_month'] - ltv['first_order_month']) / np.timedelta64(1, 'M')
ltv['age'] = ltv['age'].round().astype('int')
ltv['ltv'] = ltv['gp'] / ltv['n_buyers']

# соберем сводную по когортам, их возрасту и количеству заказов
ltv_pivot = ltv.pivot_table(
    index='first_order_month',
    columns='age',
    values='ltv',
    aggfunc='mean').round(2)

# так как LTV накопительная метрика, примерним к значениям функцию cumsum
ltv_pivot = ltv_pivot.cumsum(axis=1).round(2)
ltv_pivot.reset_index().fillna('')
print('Среднее значение LTV за шестой месяц жизни когорты', ltv_pivot.iloc[:,5].mean(), 'у.е.')
