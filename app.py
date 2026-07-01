import streamlit as st
import pickle
import pandas as pd
import requests
import os
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.markdown(
    """
    <h1 style="text-align:center;">
        🎬 <span style="color:#ff77b7;">Movie</span>
        <span style="color:#a855f7;"> Recommender</span>
    </h1>
    <h4 style="text-align:center;color:gray;">
        Find movies similar to your favorite one
    </h4>
    """,
    unsafe_allow_html=True,
)


def get_api_key():
    # Prefer Streamlit secrets (for Streamlit Cloud), fall back to env var (for local/other hosts)
    try:
        return st.secrets["OMDB_API_KEY"]
    except (KeyError, FileNotFoundError):
        key = os.environ.get("OMDB_API_KEY")
        if not key:
            st.error("OMDB_API_KEY is not set. Add it to .streamlit/secrets.toml or as an environment variable.")
            st.stop()
        return key


@st.cache_data
def fetch_poster(movie_name):
    api_key = get_api_key()

    url = f"https://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        return data["Poster"]
    else:
        return "https://via.placeholder.com/300x450?text=No+Poster"


similarity = pickle.load(open('similarity.pkl', 'rb'))


from concurrent.futures import ThreadPoolExecutor

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]

    # Get movie names
    recommended_movies = [
        movies.iloc[i[0]].title
        for i in movies_list
    ]

    # Fetch posters in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        recommended_posters = list(
            executor.map(fetch_poster, recommended_movies)
        )

    return recommended_movies, recommended_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
st.title("Select a Movie to Get Similar Recommendations")
selected_movie_name = st.selectbox('', movies['title'].values, label_visibility="collapsed")


if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    left, right = st.columns([5, 1])
    with left:
        st.subheader(f"🍿 Because You Liked **{selected_movie_name}**")

    with right:
        st.image(fetch_poster(selected_movie_name), width=200)
        st.markdown(f"<h3 style='text-align:center'>{selected_movie_name}</h3>",
                    unsafe_allow_html=True)
    
    st.subheader("Recommended Movies")
    
    st.divider()

    cols1 = st.columns(5)

    for i in range(5):
        with cols1[i]:
            st.image(posters[i], use_container_width=True)
            st.write(names[i])

    st.write("")

    cols2 = st.columns(5)

    for i in range(5,10):
        with cols2[i-5]:
            st.image(posters[i], use_container_width=True)
            st.write(names[i])
