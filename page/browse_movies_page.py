# page/browse_movies_page.py

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
                st.markdown(f"### {movie.title}")
                st.caption(movie.description)

                # 🖼️ Show poster if available
                if movie.poster_url:
                    st.image(movie.poster_url, width=250)

                # 🎞️ Show trailer button if trailer URL exists
                if movie.trailer_url:
                    st.markdown(
                        f"""
                        <a href="{movie.trailer_url}" target="_blank">
                            <button style="background-color:#4CAF50;
                                           color:white;
                                           padding:8px 16px;
                                           border:none;
                                           border-radius:5px;
                                           cursor:pointer;
                                           font-size:14px;">
                                ▶️ Watch Trailer
                            </button>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

                # ⏰ Showtimes
                showtimes = ShowtimeService.get_showtimes_by_movie(movie.movie_id)
                if showtimes:
                    st.markdown("**Showtimes:** " + ", ".join(s.time for s in showtimes))
                else:
                    st.markdown("*No showtimes available.*")

                st.markdown("---")
