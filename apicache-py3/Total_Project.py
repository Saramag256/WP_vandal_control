# подгружаем все необходимые библиотеки и файл данных
import pandas as pd
#import datetime as dt
import numpy as np
from scipy import stats as st
#import scipy.stats as stats
#import seaborn as sns
#from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
#from plotly.subplots import make_subplots
import math as mth

# загрузим даннные
try:
    df = pd.read_csv('/datasets/logs_exp.csv', sep="\s+")
except:
    df = pd.read_csv('C://Users//Katumka//datasets//logs_exp.csv', sep="\s+")

# вставляем заранее заготовленную функцию для быстрого обзора данных, далее применяем ее к датасетам
def helicopter(data):
    """Функция обработки row-файла"""
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

def check(trials1, sucsess1, trials2, sucsess2):
    """"Опеределение критического уровеня статистической значимости"""
    # пропорция успехов в первой группе:
    p1 = sucsess1/trials1
    p2 = sucsess2/trials2
    # пропорция успехов в комбинированном датасете:
    p_combined = (sucsess1 + sucsess2) / (trials1 + trials2)
    # разница пропорций в датасетах
    difference = p1 - p2
    # считаем статистику в ст.отклонениях стандартного нормального распределения
    z_value = difference / mth.sqrt(p_combined * (1 - p_combined) * (1 / trials1 + 1 / trials2))
    # задаем стандартное нормальное распределение (среднее 0, ст.отклонение 1)
    distr = st.norm(0, 1)
    p_value = round((1 - distr.cdf(abs(z_value))) * 2, 3)
    print("Нулевая гипотеза: статистически значимых различий между группами нет.")
    print("Альтернативная гипотеза: статистически значимые различия между группами есть.")
    print('p-значение: ', p_value)
    if p_value < .05:
        print('Отвергаем нулевую гипотезу: между долями есть значимая разница')
    else:
        print('Не получилось отвергнуть нулевую гипотезу, нет оснований считать доли разными')


helicopter(df)

# переименуем столбцы
df.columns = ['event', 'id', 'fulldate', 'group']

# удалим полные дубликаты
df = df.drop_duplicates().reset_index(drop=True)

# преобразуем даты к типу дат pd.to_datetime
df['fulldate'] = pd.to_datetime(df['fulldate'], unit='s')

# выделим в отдельный столбец день
df['day'] = df['fulldate'].astype('datetime64[D]')
df.head()

# сохраняем очищенные данные в новый датасет
df_work = df.query('day >= "2019-08-01"')
df_work['id'].nunique()

# сгруппируем события по пользователям
users = df_work.groupby('id', as_index=False).agg({'event': pd.Series.count})

# построим 'ящик с усами'
fig = px.box(users, y="event", points="all")
fig.update_traces(marker_color='#2f5d62', boxmean=True)
fig.update_layout(height=600, width=300, title_text="количество событий на пользователя",
                    plot_bgcolor='#E0ECE4')
fig.show()

# переименуем для удобства
df_work = df_work.replace({'event' : { 'MainScreenAppear' : 'переход на главный экран', 'OffersScreenAppear' : 'переход на экран выбора товара',
                                'CartScreenAppear' : 'переход в корзину', 'PaymentScreenSuccessful' : 'переход на экран об успешной оплате',
                                'Tutorial' : 'руководство'}})

# посчитаем, сколько пользователей совершали каждое из этих событий
funnel = df_work.groupby('event')['id'].nunique().sort_values(ascending=False).to_frame().reset_index()
funnel.columns = ['event', 'unique_users']
funnel['unique_users_share']= round((funnel['unique_users']/funnel['unique_users'].sum() * 100), 2)
funnel

# удаляем лишнее событие
df_work = df_work.query('event != "руководство"')
funnel = funnel.query('event != "руководство"')

# группируем данные для построения воронки по группам
funnel_by_gr = df_work.groupby(['group','event'])['id'].nunique().reset_index(name='count')

# формируем мини-датасеты по группам
gr_246 = funnel_by_gr[funnel_by_gr['group'] == 246].sort_values(['count'], ascending=[False]).reset_index(drop=True)
gr_246['share']= round((gr_246['count']/gr_246['count'].sum() * 100), 2)
gr_247 = funnel_by_gr[funnel_by_gr['group'] == 247].sort_values(['count'], ascending=[False]).reset_index(drop=True)
gr_247['share']= round((gr_247['count']/gr_247['count'].sum() * 100), 2)
gr_248 = funnel_by_gr[funnel_by_gr['group'] == 248].sort_values(['count'], ascending=[False]).reset_index(drop=True)
gr_248['share']= round((gr_248['count']/gr_248['count'].sum() * 100), 2)

# вывод графика
fig = go.Figure()
fig.add_trace(go.Funnel(
    name = 'gr_246',
    y = gr_246['event'],
    x = gr_246['count'],
    marker = {"color": '#5E8B7E'},
    textinfo = "value+percent initial+percent previous"))
fig.add_trace(go.Funnel(
    name = 'gr_247',
    orientation = "h",
    y = gr_247['event'],
    x = gr_247['count'],
    marker = {"color": '#A7C4BC'},
    textposition = "inside",
    textinfo = "value+percent initial+percent previous"))
fig.add_trace(go.Funnel(
    name = 'gr_248',
    orientation = "h",
    y = gr_248['event'],
    x = gr_248['count'],
    marker = {"color": '#2f5d62'},
    textposition = "inside",
    textinfo = "value+percent initial+percent previous"))
fig.update_layout(height=500, width=1000, title_text="Воронка событий по тестовым группам", \
                 plot_bgcolor='#E0ECE4',
                 yaxis={"title":"событие"})
fig.show()

print('Событие: переход на экран об успешной оплате')
check(gr_248['count'].sum(), gr_248.loc[3, 'count'], gr_247['count'].sum() + gr_246['count'].sum(),\
      gr_247.loc[3, 'count'] + gr_246.loc[3, 'count'])