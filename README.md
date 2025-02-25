# Lami-Revy

Lamy-Revi is a demonstration e-commerce website where users can search for items, filter results, register, log in, manage orders, and access additional features like chat assistance and user predictions. This project was built as a final project to showcase various web development and backend techniques.

## Features

### User Management

* Registration: Create a new user account.

* Login: Secure login with hashed passwords.

* Authentication: Users must be authenticated to perform actions like adding items to their favorites, using chat assistance, and placing orders.

### Item Management

* Search and Filter: Browse the items list with search functionality and filters for price and amount.

* Order Management:

  * Add items to your cart.

  * Confirm orders.

  * View your order history.

### Chat Assistance

* Integrated with the ChatGPT API to provide conversational assistance for user queries.

### User Predictions

* Includes a model to create predictions about user behavior, built using scikit-learn (sklearn) for linear regression.

## How to Run the Project

1. Install Dependencies: Enure you have Python installed, then run:

    >pip install -r requirements.txt

2. Run with Docker:

    >docker-compose up --build

3. Run the Application:

    >uvicorn main:app --reload

4. Run the Client:
Navigate to the ui directory and run:

    >cd ui

    >streamlit run main.py

## Technologies Used

* Backend: FastAPI (Python)

* Frontend: Streamlit (Python)

* Database: MySQL

* Containerization: Docker

* Caching: Redis

* Chat assistant: ChatGPT 

* Machine Learning: scikit-learn (for user behavior predictions)
