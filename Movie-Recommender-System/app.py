import streamlit as st
import joblib
import requests

st.title('Movie Recommender System')
final_movies = joblib.load('df_final_movies.pkl')
movie_list_name = final_movies['title'].values

similarity = joblib.load('similarity.pkl')


def fetch_poster(poster_movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=52cd9f945291e5c803bb0ab8927cd54a&language=en-US".format(poster_movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    image_full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return image_full_path


def recommend(movie):
    movie_index = final_movies[final_movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie = []
    recommend_posters = []

    for j in movie_list:
        recommended_movie.append(final_movies.iloc[j[0]]['title'])
        recommend_posters.append(fetch_poster(final_movies.iloc[j[0]]['movie_id']))

    return recommended_movie, recommend_posters


selected_movie_name = st.selectbox(
    'Type or select a movie from the dropdown',
    movie_list_name)

if st.button('Recommend'):
    recommendations, recommend_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommendations[0])
        st.image(recommend_posters[0])

    with col2:
        st.text(recommendations[1])
        st.image(recommend_posters[1])

    with col3:
        st.text(recommendations[2])
        st.image(recommend_posters[2])

    with col4:
        st.text(recommendations[3])
        st.image(recommend_posters[3])

    with col5:
        st.text(recommendations[4])
        st.image(recommend_posters[4])
