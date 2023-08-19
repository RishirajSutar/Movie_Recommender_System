import pickle
import pandas as pd
import requests
import streamlit as st

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    recommanded_movies = []
    recommanded_movies_img = []
    for i in distances[1:5]:
        movie_id = movies.iloc[i[0]].movie_id
        recommanded_movies.append(movies.iloc[i[0]].title)
        recommanded_movies_img.append(poster(movie_id))
    return recommanded_movies , recommanded_movies_img


movies_dict = pickle.load(open('movie_dict.pkl' , 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl' , 'rb'))

st.title("Movie Recommendation")
st.caption(":red[_Tell us the movie you've watched recently. We will come up with four more movies of the same genre_ ]")

def poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c757632e7266dcca8d293dd585e36af1&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

selected_movie_name = st.selectbox(
    "Which Movie have you seen ..?" ,
    movies['title'].values)

if st.button(':red[Recommendations]'):
    recommandations , images  = recommend(selected_movie_name)
    col1 , col2 , col3 , col4  = st.columns(4 , gap = 'large')
    with col1:
        st.image(images[0] , caption=recommandations[0] , width=180)
    with col2:
        st.image(images[1] , caption=recommandations[1] , width=180)
    with col3:
        st.image(images[2] , caption=recommandations[2] , width=180)
    with col4:
        st.image(images[3] , caption=recommandations[3] , width=180)