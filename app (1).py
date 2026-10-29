import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="TMDB Movie Analytics", layout="wide")

st.title("🎬 Reel Insights: TMDB Movie Analytics")
st.write("Explore movie ratings, revenue, and genres.")

movies = pd.read_csv("/content/cleaned_movies.csv")
genres = pd.read_csv("/content/cleaned_genres.csv")
movie_genres = pd.read_csv("/content/cleaned_movie_genres.csv")

st.subheader("📊 Movie Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Movies", len(movies))

if "vote_average" in movies.columns:
    col2.metric("Average Rating", round(movies["vote_average"].mean(), 2))
else:
    col2.metric("Average Rating", "N/A")

if "revenue" in movies.columns:
    col3.metric("Total Revenue", f"${movies['revenue'].sum():,.0f}")
else:
    col3.metric("Total Revenue", "N/A")

st.subheader("🔍 Search Movie")
search = st.text_input("Enter movie name")

if "title" in movies.columns:
    filtered = movies.copy()

    if search:
        filtered = filtered[
            filtered["title"].astype(str).str.contains(
                search, case=False, na=False
            )
        ]

    st.write("Movies found:", len(filtered))
    st.dataframe(filtered, use_container_width=True)

if "vote_average" in movies.columns:
    st.subheader("⭐ Top Rated Movies")
    top_movies = movies.nlargest(10, "vote_average")

    if "title" in top_movies.columns:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(top_movies["title"], top_movies["vote_average"])
        ax.invert_yaxis()
        ax.set_xlabel("Rating")
        st.pyplot(fig)
        plt.close(fig)

if "revenue" in movies.columns and "title" in movies.columns:
    st.subheader("💰 Top 10 Movies by Revenue")
    top_revenue = movies.nlargest(10, "revenue")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(top_revenue["title"], top_revenue["revenue"])
    ax.invert_yaxis()
    ax.set_xlabel("Revenue")
    st.pyplot(fig)
    plt.close(fig)
