import streamlit as st
from services.movie_service import MovieService
from services.showtime_service import ShowtimeService

class BrowseMoviesPage:
    def render(self):
        st.subheader("🎬 Now Showing")

        movies = MovieService.get_all_movies()

        if not movies:
            st.info("No movies available.")
        else:
            for movie in movies:
                st.markdown(f"### {movie.title}")                   # ✅ Movie Title
                st.caption(movie.description)                      # ✅ Movie Description

                # ✅ Display Poster if Available
                if movie.poster_url:
                    st.image(movie.poster_url, width=250, caption=movie.title)

                showtimes = ShowtimeService.get_showtimes_by_movie(movie.movie_id)
                if showtimes:
                    st.markdown("**Showtimes:** " + ", ".join(s.time for s in showtimes))
                else:
                    st.markdown("*No showtimes available.*")

                st.markdown("---")
