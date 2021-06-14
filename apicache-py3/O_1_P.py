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
