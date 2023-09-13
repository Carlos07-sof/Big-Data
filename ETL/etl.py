import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/sundeepblue/movie_rating_prediction/master/movie_metadata.csv')


promedio = df['gross'].mean()

df['gross'].fillna(promedio, inplace=True) 


df['facenumber_in_poster'].apply(lambda x: 0 if pd.isnull(x) or x < 0 else x)


result = df['movie_imdb_link'].str.split('/').str.get(4)
df['TittleCode'] = result


df['title_year'].fillna(0, inplace=True)


df = df[df['country'] == 'USA']

df.to_csv('FilmTV_USAMovies.csv', index=False)
