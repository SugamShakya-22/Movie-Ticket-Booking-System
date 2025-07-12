# Movie-Ticket-Booking-System
A Movie Ticket Booking System built with Python and Streamlit, allowing users to browse movies, book or cancel tickets, and manage shows through an admin panel. This project demonstrates effective use of Python, object-oriented design, and a simple GUI for both users and administrators.

It is a simple movie ticket booking system built using Python and [Streamlit](https://streamlit.io/), with support for user authentication, movie management, dynamic pricing, and more. Designed with clean architecture using service, model, and data layers.

---

# Features

- User & Admin authentication
- Browse movies and view posters/trailers
- Book/cancel movie tickets
- Dynamic pricing based on seats booked
- Admin panel to manage movies, showtimes, prices, posters, and trailers
- View booking history

---

# Technologies Used

- **Python** `>= 3.13.3`
- **Streamlit** for frontend
- **PostgreSQL** for database
- **psycopg2** for PostgreSQL connection
- **passlib** for password hashing
- Clean OOP structure: `models`, `services`, `data`, `pages`

---

# Required Libraries

Install the dependencies using pip:

```bash
pip install streamlit psycopg2 passlib
```

 Setup and Installation
1. Clone the Repository
```bash
git clone https://github.com/yourusername/movie-ticket-booking-system.git
cd movie-ticket-booking-system
```

2. Create and Configure PostgreSQL Database
Create a database (e.g., movie_booking)

Run the SQL schema to create tables:

```sql

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
);

-- Movies table
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    poster_url TEXT, 
    trailer_url TEXT, 
    price_per_seat NUMERIC(10, 2) DEFAULT 0.00,
);

-- Showtimes table
CREATE TABLE showtimes (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER NOT NULL REFERENCES movies(id) ON DELETE CASCADE,
    time TEXT NOT NULL,
);

-- Bookings table
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    showtime_id INTEGER NOT NULL REFERENCES showtimes(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_cancelled BOOLEAN DEFAULT FALSE,
    cancelled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price INTEGER DEFAULT 0,
);

-- Booking seats table
CREATE TABLE booking_seats (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
    seat_label TEXT NOT NULL
);

```
3. Set Your PostgreSQL Connection
Update your data/db.py:

```python

def get_connection():
    return psycopg2.connect(
        dbname="movie_ticket_db",
        user="your_db_user",
        password="your_db_password",  
        host="localhost",
        port="5432"
    )
```
# How to Run the Application
Run the app using Streamlit:

```bash
streamlit run main.py
```

# Admin Login Info (Default)
Use this email to log in as admin:

Email: admin@hotmail.com

Password: (Set this at registration time)

# System Interfaces
1. Register
   ![register](https://github.com/user-attachments/assets/efc4a0b2-5cff-40a2-8ec0-ab2550af7b28)

2. Login
![login](https://github.com/user-attachments/assets/5dedf53f-8c66-4353-83c3-5a74b97d3aca)

3. Browse Movies
   ![Browse Movie](https://github.com/user-attachments/assets/d5c899e9-a326-44e9-a9b5-4785f2e5d6bb)
   
4. Book Tickets
   ![Book Tickets](https://github.com/user-attachments/assets/f73c4228-5c11-4fdc-98db-d37fbf7dd87c)

5. Cancel Bookings
<img width="1912" height="897" alt="image" src="https://github.com/user-attachments/assets/a6ae6582-9ad9-4c99-bd37-4b0f65ca4254" />

6. Admin Panel
   <img width="1920" height="935" alt="image" src="https://github.com/user-attachments/assets/194ab890-acb4-4619-bf68-db64553cef22" />

# License
This project is for educational purposes and is not licensed for commercial use.

# Developed By
Sugam Shakya – Python Backend Intern at Verisk Nepal
