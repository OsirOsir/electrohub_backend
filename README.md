# electrohub_backend

# Electrohub e-commerce website

- A fully functional e-commerce website built using Python and Flask. This platform allows users to browse and purchase electronics, user authentication and secure checkout functionality.

- The featured electronics include: Smartphones, Laptops, Desktops, TVs, Earbuds, Headphones, Sound systems, Speakers, Smartwatches, Tablets

# Installation
To run this project locally, follow these steps:
1. To clone the repository:
    `git clone git@github.com:OsirOsir/electrohub_backend.git`
    `cd electrohub_backend`

2. To set up virtual environment:
    run `pipenv install` on your terminal.
    `pipenv shell` to enter into the virtual environment.

3. To install dependencies:
    `pip install -r requirements.txt`

4. To set up the database:
    `flask db init`
    `flask db migrate -m "<migration_message>"`
    `flask db upgrade head`

5. Set environment variables:
    `export FLASK_APP=app.py`
    `export FLASK_RUN_PORT=5555`
    DATABASE_URL='postgresql://groupthree:group3@localhost/electrohub_db'

6. To run the application and database:
    `flask run` or `python app.py`

# Usage

- Homepage: Displays featured electronics, electronics on offer and customer support.

- Item details: Allows users to view product details, including price, features, add to cart option and reviews.

- Checkout: Users can proceed with payment through a secure checkout page.

- Authentication: Users can sign up, log in, and manage their accounts.

# Features

- Product catalog with featured electronics filtering and a search option.

- User authentication (sign-up, login, logout).

- Add to cart and checkout functionality.

- Admin panel for managing products and orders.

# Tech Stack

- Backend: Python, Flask

- Database: PostgreSQL

- ORM: SQLAlchemy

- Frontend: React, CSS (Bootstrap for styling)

- Authentication: Flask-Login

# Contributing

- We welcome contributions to the project! To contribute:

        - Fork the repository

        - Create a new branch (`git checkout -b feature/your-feature`)

        - Commit your changes (`git commit -m 'Add new feature'`)

        - Push to the branch (`git push origin feature/your-feature`)

        - Create a new pull request