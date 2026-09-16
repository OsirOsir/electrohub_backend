# ElectroHub Backend

ElectroHub is an e-commerce application for browsing and purchasing electronic products. This repository contains the **Python/Flask backend**, including application logic, database management, authentication, product management, cart functionality, and checkout workflows.

The application supports electronics such as smartphones, laptops, desktops, TVs, headphones, speakers, smartwatches, tablets, and related accessories.

## Features

- User registration, login, and logout
- Product catalog and product details
- Product search and filtering
- Shopping cart management
- Checkout workflow
- Product reviews
- Order management
- Administrative product management
- PostgreSQL database integration
- REST-based communication with the frontend application

## Tech Stack

### Backend
- Python
- Flask

### Database
- PostgreSQL
- SQLAlchemy

### Database Migrations
- Flask-Migrate / Alembic

### Frontend
- React
- JavaScript
- Bootstrap / CSS

The frontend is maintained separately:

[ElectroHub Frontend](https://github.com/OsirOsir/electrohub-frontend)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/OsirOsir/electrohub_backend.git
cd electrohub_backend
```

### 2. Create and activate the virtual environment

If the project uses Pipenv:

```bash
pipenv install
pipenv shell
```

Alternatively, if using `requirements.txt`:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
FLASK_APP=app.py
FLASK_RUN_PORT=5555
DATABASE_URL=postgresql://username:password@localhost/electrohub_db
```

Do not commit actual passwords, API keys, database credentials, or other secrets to GitHub.

### 4. Set up the PostgreSQL database

Create the required PostgreSQL database and configure the `DATABASE_URL` environment variable.

If migrations are already included in the repository, run:

```bash
flask db upgrade
```

When creating new migrations during development:

```bash
flask db migrate -m "migration description"
flask db upgrade
```

### 5. Run the application

```bash
flask run
```

or:

```bash
python app.py
```

The backend will normally be available at:

```text
http://localhost:5555
```

## Application Functionality

### Product Catalog

Users can browse available electronic products, search the catalog, filter products, and view detailed product information.

### Authentication

Users can create accounts, log in, log out, and access functionality available to authenticated users.

### Shopping Cart

Products can be added to and managed within a shopping cart before checkout.

### Checkout

The application provides a checkout workflow for processing customer orders.

### Administration

Administrative functionality supports management of products and orders.

## Project Goals

ElectroHub was developed to demonstrate the design and implementation of a full-stack e-commerce application using a Flask backend, PostgreSQL database, and React frontend.

The project demonstrates experience with:

- Backend application development
- Relational database design
- ORM-based data management
- API integration
- User authentication
- E-commerce workflows
- Frontend/backend integration
- Version control with Git and GitHub

## Frontend Repository

The client-side application is available here:

[ElectroHub Frontend](https://github.com/OsirOsir/electrohub-frontend)

## Contributing

Contributions and improvements are welcome.

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/your-feature
```

3. Commit your changes:

```bash
git commit -m "Add new feature"
```

4. Push the branch:

```bash
git push origin feature/your-feature
```

5. Open a pull request.

## License

This project is intended for educational and portfolio purposes.
