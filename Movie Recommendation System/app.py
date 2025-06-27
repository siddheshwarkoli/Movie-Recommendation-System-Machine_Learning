import pickle
import streamlit as st
import requests
import os

# =================== Add Background and Title Style =====================

from PIL import Image
import streamlit as st
import base64

def set_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: auto;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Example: use your own image
set_bg_from_local("siddhu.jpg")  # Make sure this image is in the same folder as app.py


# =================== Functions =====================

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + poster_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# =================== App =====================

st.markdown("<h4 style='text-align: center;color: #87CEEB;text-shadow: 2px 2px 4px #000000; '>DEVELOPED BY : SIDDHESHWAR KOLI</h4>", unsafe_allow_html=True)
st.markdown("""
    <h1 style='text-align: center; color: #FFFACD;text-shadow: 2px 2px 4px #000000; font-family: Poppins, sans-serif;'>
        MOVIE RECOMMENDATION
    </h1>
""", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white;'>Get instant recommendations based on your favorite movies</h4>", unsafe_allow_html=True)




base_dir = os.path.dirname(os.path.abspath(__file__))
#model_dir = os.path.join(base_dir, "Models")

movies_path = os.path.join(base_dir, "movie_list.pkl")
similarity_path = os.path.join(base_dir, "similarity.pkl")

movies = pickle.load(open(movies_path, 'rb'))
similarity = pickle.load(open(similarity_path, 'rb'))



movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.markdown(f"**{names[i]}**")
