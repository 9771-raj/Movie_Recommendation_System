import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    api_key="..........."  # use your api key 
    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key={}".format(movie_id,api_key))
    data=response.json()
    print(data['poster_path'])
    return "http://image.tmdb.org/t/p/w500"+data['poster_path']

# for list of movies for select
movies_dict=pickle.load(open('movie_dict.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
movies_name=pd.DataFrame(movies_dict)

def recommendation(movie):
    index=movies_name[movies_name['title']==movie].index[0]
    distance=similarity[index]
    sorted_list=sorted(enumerate(distance),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movie=[]
    recommended_poster=[]
    for i in sorted_list:
         movie_id=movies_name.iloc[i[0]].movie_id
         # for fetching movie poster we use movie_id in TMDB API
         recommended_poster.append(fetch_poster(movie_id))
         recommended_movie.append(movies_name.iloc[i[0]].title)
     
    return recommended_movie,recommended_poster


st.title("Movie Recommender System")
option = st.selectbox(
     'Select or Type Movie Name!',
     (movies_name['title'].values))

if st.button('Recommend'):
    a,posters=recommendation(option)
    col1, col2, col3,col4,col5= st.columns(5)
    with col1:
        st.text(a[0])
        st.image(posters[0])
    with col2:
        st.text(a[1])
        st.image(posters[1])
    with col3:
        st.text(a[2])
        st.image(posters[2])
    with col4:
        st.text(a[3])
        st.image(posters[3])
    with col5:
        st.text(a[4])
        st.image(posters[4])


