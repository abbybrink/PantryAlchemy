from flask import Flask, render_template, request
import requests
from elasticsearch import Elasticsearch
import json
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)
es = Elasticsearch('https://localhost:9200', ca_certs='http_ca.crt', basic_auth=("elastic", "=Q0LSPrqauirlURpWZHO"))


@app.route("/") #default temp
def index():
    return render_template('index.html')

@app.route("/search", methods=['GET', 'POST']) #format, fetch then add to html
def search():
    ingredients = request.form['ingredients']
    ingredients = ingredients.split(',')
    apiKey = '96ef38777c94480b8b5e59393bac8bca'
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {'ingredients': ingredients,
              'number': 100,
              'apiKey': apiKey
              }
    recipes = requests.get(url=url, params=params)
    recipes = recipes.json()
    if recipes:
        with open("new.json", "w") as file:
            json.dump(recipes, file, indent = 4)
            #add index bullshit

        if request.form['checkbox'].checked == True:
            search_query = {
                "query": {
                    "match": {
                        "missedIngredientCount": 0
                    }
                }
            }
        else:
            search_query = {
                "query": {
                    "match": {
                        "usedIngredientCount": ingredients.count
                    }
                }
            }

        results = es.search(index="", body=search_query)
        return render_template('index.html', recipes=results)
    else:
        return render_template('index.html')

@app.route('/recipe/<int:recipe_id>') # dynamic URL to handle individual recipes
def recipe(recipe_id):
    apiKey = '96ef38777c94480b8b5e59393bac8bca'
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {'apiKey': apiKey}
    recipe_details = requests.get(url=url, params=params)
    recipe_details = recipe_details.json()
    return render_template('recipe.html', recipe=recipe_details)

@app.route("/pantry")  # Route for the Pantry page
def pantry():
    return render_template('pantry.html')


@app.route("/account")  # Route for the Pantry page
def account():
    return render_template('account.html')
