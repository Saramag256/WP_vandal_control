import pandas as pd

df = pd.read_csv('C:/Users/Katumka/PycharmProjects/WP_vandal_control/apicache-py3/music_project.csv')

#количество повторений
def find_genre(genre_name):
    count = 0
    for row in genres_list:
        if row == genre_name:
            count += 1

    return count

#количество записей
def find_hip_hop(df, wrong):
    df['genre_name'] = df['genre_name'].replace(wrong, 'hiphop')
    for row in genres_list:
        wrong_count = df[df['genre_name'] == wrong]['genre_name'].count()

    return wrong_count

#сумма треков
def number_tracks(df, day, city):
    track_list = (df[(df['weekday'] == day) & (df['city'] == city)])
    track_list_count = track_list['genre_name'].count()

    return track_list_count

#распеределение по дням
def genre_weekday(df, day, time1, time2):
    genre_list = (df[(df['weekday'] == day) & (df['time'] > time1) & (df['time'] < time2)])
    genre_list_sorted = genre_list.groupby('genre_name')['genre_name'].count()
    genre_list_sorted = genre_list_sorted.sort_values(ascending = False)

    return genre_list_sorted.head(10)

df.info()

df.set_axis(['user_id', 'track_name', 'artist_name', 'genre_name', 'city', 'time', 'weekday'], axis='columns', inplace=True)
df['track_name'] = df['track_name'].fillna('unknown')
df['artist_name'] = df['artist_name'].fillna('unknown')
#поиск 0 значений
df.isnull().sum()
df.dropna(subset=['genre_name'], inplace=True)
#поиск дубликатов
df.duplicated().sum()
df = df.drop_duplicates().reset_index(drop=True)

genres_list = df['genre_name'].unique()
df.groupby('city')['genre_name'].count()

columns = ['city', 'monday', 'wednesday', 'friday']
table = pd.DataFrame(data=data, columns=columns)

#определение данных по МСК
moscow_general = table.get_group('Moscow')
genre_weekday(moscow_general, 'Friday', '17:00:00', '23:00:00')
moscow_genres = moscow_general.sort_values(ascending=False)
moscow_genres.head(10)