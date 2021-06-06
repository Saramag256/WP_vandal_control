# подгружаем все необходимые библиотеки и файлы данных
import pandas as pd
import numpy as np
from scipy import stats as st
from matplotlib import pyplot as plt

visits = pd.read_csv('visits_log.csv')
orders = pd.read_csv('orders_log.csv')
costs = pd.read_csv('costs.csv')

# вставляем заранее заготовленную функцию для быстрого обзора данных, далее применяем ее к датасетам
line = '______________________________________'


def helicopter(data):
    print("Размер данных: {}".format(data.shape))
    print(line)

    print("Первые и последние 5 строк данных")
    print(line)

    print("Количество пропусков в данных")
    nulls = data.isnull().sum()
    print(line)

    print("Количество дубликатов в данных")
    print(data.duplicated().sum())
    print(line)

    print("Типы данных")
    tmp = pd.DataFrame(data=[(col, data[col].dtypes) for col in data.columns], columns=['Название столбца', 'Тип данных']).set_index('Название столбца')

    print(line)

    print("Описание данных")
    print(line)

helicopter(visits)
helicopter(orders)
helicopter(costs)

#предобработка данных
visits.columns = ['device', 'end_ts', 'source_id', 'start_ts', 'uid']
orders.columns = ['buy_ts', 'revenue', 'uid']

visits['start_ts'] = pd.to_datetime(visits['start_ts'])
visits['end_ts'] = pd.to_datetime(visits['end_ts'])
orders['buy_ts'] = pd.to_datetime(orders['buy_ts'])
costs['dt'] = pd.to_datetime(costs['dt'])

orders = orders.query('buy_ts < "2018-06-01"').reset_index()

#нахождение аномальных значений
visits['duration'] = (visits['end_ts'] - visits['start_ts'])
print('количество сессий с продолжительностью 0 секунд и меньше:', len(visits.query('duration <= "00:00:00"')))
print('процент сессий с продолжительностью 0 секунд и меньше:', len(visits.query('duration <= "00:00:00"')) / len(visits) * 100)
print('количество сессий с отрицательной продолжительностью:', len(visits.query('duration < "00:00:00"')))

visits = visits.query('duration >= "00:00:00"').reset_index()
len(visits)

#преобразуем столбец с продолжительностью в секунды для дальнейшего удобства анализа
visits['duration'] = visits['duration'].dt.seconds

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

#рассчитаем средние значения метрик DAU, WAU и MAU за весь период, то есть сколько уникальных пользователей пользуются исследуемым сервисом

def mean_DAU_WAU_MAU(abbreviation):
    visits[abbreviation] = visits['start_ts'].dt.date
    dau_list = visits.groupby(abbreviation).agg({'uid': 'nunique'})
    number = int(dau_list.mean())
    return number

dau = mean_DAU_WAU_MAU('day')
wau = mean_DAU_WAU_MAU('week')
mau = mean_DAU_WAU_MAU('month')

# сгруппируем таблицу по дням, количеству визитов и уникальных пользователей
visits_per_user = visits.groupby(['day']).agg({'uid': ['count','nunique']})
visits_per_user.columns = ['n_sessions', 'n_users']

# разделим число сессий на количество пользователей за период
visits_per_user['visits_per_user'] = visits_per_user['n_sessions'] / visits_per_user['n_users']
print('В день один пользователь в среднем заходит на сайт',visits_per_user['visits_per_user'].mean().round(2),'раз.')
print('Средняя продолжительность сессии или ASL', (visits['duration']/60).mean().round(2), 'минут')
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

# находим изначальное количество пользователей в каждой из когорт и переименовываем
initial_users_count = cohorts[cohorts['cohort_lifetime'] == 0][['first_activity_month','uid']]
initial_users_count = initial_users_count.rename(columns={'uid':'cohort_users'}).reset_index()
print(initial_users_count)

#определение дат активностей пользователей
first_order_date_by_customers = orders.groupby('uid')['buy_ts'].min()
first_order_date_by_customers.name = 'first_order_date'
first_orders = orders.join(first_order_date_by_customers,on='uid')
first_orders['first_order_day'] = first_orders['first_order_date'].astype('datetime64[D]')

first_orders_pivot = first_orders.pivot_table(values=['days_to_order'], index=['uid'])
first_orders_pivot.hist(bins= 50, figsize=(15, 5))
plt.title('Количество дней от первого посещения сайта до первой покупки')
plt.ylabel('количество пользователей ')
plt.xlabel('Количество дней от первого посещения сайта до первой покупки')
plt.show()

#средний чек
orders['revenue'].mean().round()

#сгруппируем таблицу заказов по месяцу первой покупки и месяцу каждого заказа и сложим выручку
#сбросим индекс методом reset_index()
cohorts_orders_ltv = orders.groupby(['first_order_month', 'buy_month']).agg({'revenue': 'sum'}).reset_index()
cohorts_orders_ltv.columns = ['first_order_month', 'buy_month', 'revenue']
cohorts_orders_ltv

#добавим в таблицу cohorts данные о том, сколько людей первый раз совершили покупку в каждый месяц
ltv = pd.merge(cohorts_orders_ltv, cohorts_orders_ltv, on='first_order_month')
ltv['gp'] = ltv['revenue']
ltv['age'] = (ltv['buy_month'] - ltv['first_order_month']) / np.timedelta64(1, 'M')
ltv['age'] = ltv['age'].round().astype('int')
ltv['ltv'] = ltv['gp'] / ltv['n_buyers']

# соберем сводную по когортам, их возрасту и количеству заказов
ltv_pivot = ltv.pivot_table(index='first_order_month',columns='age',values='ltv',aggfunc='mean').round(2)
print('Среднее значение LTV за шестой месяц жизни когорты', ltv_pivot.iloc[:,5].mean(), 'у.е.')

#рассчитем средний CAC на одного покупателя для всего проекта и для каждого источника трафика
costs['dt'] = pd.to_datetime(costs['dt']).dt.date
first_orders = orders.groupby('uid').agg({'buy_ts': 'min'}).reset_index()
first_orders['first_order_dt'] = pd.to_datetime(first_orders['buy_ts']).dt.date
first_source = visits.sort_values(by='start_ts').groupby('uid').first().reset_index()
first_source = first_source.merge(first_orders, on='uid')
first_source = first_source.groupby(['source_id', 'first_order_dt']).agg({'uid': 'count'}).reset_index()
source_cac = first_source.merge(costs, left_on=['source_id', 'first_order_dt'], right_on=['source_id', 'dt'])
source_cac['cac'] = source_cac['costs'] / source_cac['uid']
print('Cредний CAC на одного покупателя для всего проекта', source_cac['cac'].mean().round(), 'у.е')
print('CAC для каждого источника трафика:')
source_cac_final = source_cac.groupby('source_id')['cac'].mean()
print(source_cac_final)

### ROMI ###

# найдем, когда покупатель совершил первую покупку
first_orders_romi = orders.groupby('uid').agg({'buy_month': 'min'}).reset_index()
first_orders_romi.columns = ['uid', 'first_order_month']

# определим количество покупателей в каждом месяце (когорте)
cohort_sizes_romi = (
    first_orders_romi.groupby('first_order_month').agg({'uid': 'nunique'}).reset_index())
cohort_sizes_romi.columns = ['first_order_month', 'n_buyers']

# вычислим первые визиты покупателей
first_source_romi = visits.sort_values(by='start_ts').groupby('uid').first().reset_index()

# добавим к таблице заказов построенную таблицу с месяцем первой покупки каждого покупателя
# далее к полученной таблице присоединим данные о первом визите
orders_romi = pd.merge(orders, first_orders_romi, on='uid')
orders_romi = pd.merge(orders_romi, first_source_romi, on='uid')

# схлопнем данные по месяцу первой покупки и месяцу каждого заказа и сложим выручку.
cohorts_romi = (orders_romi.groupby(['first_order_month', 'buy_month', 'source_id']).agg({'uid': 'nunique', 'revenue': 'sum'}).reset_index())

# объединим количесвто покупателей в когорте с полученной таблицей
report_romi = pd.merge(cohort_sizes_romi, cohorts_romi, on='first_order_month')
report_romi

# рассчитаем валовую прибыль
report_romi['gp'] = report_romi['revenue'] * 1

# определим возраст когорт
report_romi['age'] = (report_romi['buy_month'] - report_romi['first_order_month']) / np.timedelta64(1, 'M')
report_romi['age'] = report_romi['age'].round().astype('int')

# схлопнем таблицу по источнику, месяцу и возрасту, суммируя валовую прибыль для когорт проживших 6 месяцев
ltv_for_romi = report_romi.query('age <= 6' and 'first_order_month <= "2017-12-01"').groupby(['first_order_month', 'source_id']).agg({'uid': 'sum', 'gp': 'sum'}).reset_index()
# рассчитаем LTV
ltv_for_romi['ltv'] = ltv_for_romi['gp'] / ltv_for_romi['uid']

# у ранее полученной таблицы САС, возьмем только показатели до декабря 2017 года включительно, т.е. за тот период, по которому берем когорты
source_cac['first_order_dt'] = pd.to_datetime(source_cac['first_order_dt'])
cac_for_romi = source_cac.query('first_order_dt <= "2017-12-01"').groupby(['first_order_dt', 'source_id'])['cac'].mean().reset_index()
cac_for_romi.columns = ['first_order_month', 'source_id', 'cac']

# посчитаем ROMI
romi = pd.merge(cac_for_romi, ltv_for_romi, on=['source_id', 'first_order_month'])
romi['romi'] = romi['ltv'] / romi['cac']
romi_pivot = romi.pivot_table(index='source_id',values='romi',columns='first_order_month',)
print(romi_pivot)

