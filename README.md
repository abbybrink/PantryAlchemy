Recipe Search API with Flask and Elasticsearch

Overview

This project is a Recipe Search API built using Flask and Elasticsearch. The purpose of this API is to allow users to search for recipes based on ingredients they provide. The application uses Flask as the web framework to handle HTTP requests and Elasticsearch as the search engine to efficiently retrieve relevant recipes.

Features

Ingredient-based Search: Users can input a list of ingredients, and the API will return a list of recipes that include those ingredients.

Prerequisites
Make sure you have the following installed on your system:

Python (version 3.x)
Flask
Elasticsearch

Installation
Clone the repository:
git clone https://github.com/abbybrink/PantryAlchemy.git 
cd PantryAlchemy
Install dependencies:
pip install -r requirements.txt

Configure Elasticsearch:
Update the Elasticsearch configuration in config.py with the appropriate host and port information.

Run the application:
run flask
