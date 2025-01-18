import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2d16bf0b5057cf8ae2e8a17f313a08f4&language=en-US"
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        poster_path = data.get('poster_path') 
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return None 
    except requests.exceptions.RequestException:
        return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        recommended_movie_posters.append(poster)
    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System Using Machine Learning Developed by Anshit')

movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            if poster:
                st.image(poster)
            else:
                st.write("No poster available")
