# pages/browse_movies_page.py

import streamlit as st
from data.data import get_movies, get_showtime_for_movie

class BrowseMoviesPage:
    def render(self):
        st.subheader("🎬 Now Showing")

        movies = get_movies()

        if not movies:
            st.info("No movies available.")
        else:
            for movie in movies:
                st.markdown(f"### {movie['title']}")
                st.caption(movie['description'])

                showtimes = get_showtime_for_movie(movie["id"])
                if showtimes:
                    st.markdown("**Showtimes:** " + ", ".join(showtimes))
                else:
                    st.markdown("*No showtimes available.*")

                st.markdown("---")
