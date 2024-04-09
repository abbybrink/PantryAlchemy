## Recipe Search API with Flask and Elasticsearch

## Overview

This project implements a Recipe Search API using Flask and Elasticsearch. The API enables users to search for recipes based on provided ingredients. Flask is utilized as the web framework to handle HTTP requests, while Elasticsearch efficiently retrieves relevant recipes.

## Features

- **Ingredient-based Search**: Users can input a list of ingredients, and the API will return recipes containing those ingredients.

## Prerequisites

Ensure you have the following installed on your system:

- Python (version 3.x)
- Flask
- Elasticsearch

# Installation

## Clone the repository
git clone https://github.com/abbybrink/PantryAlchemy.git

## Install dependencies
pip install -r requirements.txt

# Configure Elasticsearch
## Update the Elasticsearch configuration in config.py with the appropriate information

## Run Elasticsearch
bin/elasticsearch

## Run the application
flask run
