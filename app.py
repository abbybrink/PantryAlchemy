from flask import Flask, render_template, request
import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)
es = Elasticsearch('https://localhost:9200', ca_certs='http_ca.crt', basic_auth=("elastic", "123456"))



@app.route("/") #default temp
def index():
    return render_template('index.html')

@app.route("/search", methods=['GET', 'POST']) #format, fetch then add to html
def search():
    ingredients = request.form['ingredients']
    #ingredients = ingredients.split(',')
    apiKey = '96ef38777c94480b8b5e59393bac8bca'
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {'ingredients': ingredients,
              'number': 5,
              'apiKey': apiKey
              }
    recipes = requests.get(url=url, params=params)
    recipes = recipes.json()
    if recipes:
        index_recipes(recipes)
        # for recipe in recipes:
        #     recipe['_index'] = "num"
        # with open("new.json", "w") as file:
        #     json.dump(recipes, file, indent = 4)

        # if request.form['checkbox'].checked == True:
        #     search_query = {
        #         "query": {
        #             "match": {
        #                 "missedIngredientCount": 0
        #             }
        #         }
        #     }
        # else:
        # search_query = {
        #     "query": {
        #         "term": {
        #             "usedIngredientCount": {
        #                 "value": len(ingredients)
        #             }
        #         }
        #     },
        #     "_source": ["id", "title", "image", "index"]
        # }
        search_query = generate_query(ingredients)
        # bulk(es, recipes)
        results = es.search(index="recipes-index", body=search_query)
        # print(results)
        new_list = []
        for hit in results['hits']['hits']:
            recipe_info = {
            'id': hit['_source']['id'],
            'title': hit['_source']['title'],
            'image': hit['_source']['image']
            }
            new_list.append(recipe_info)
        # print(new_list)
        results = {}
        return render_template('index.html', recipes=new_list)
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

def index_recipes(recipes):
    for recipe in recipes:
        # Here, we're assuming each recipe has a unique ID you can use as the Elasticsearch document ID
        es.index(index="recipes-index", id=recipe['id'], body=recipe)

def generate_query(target_ingredients):
    """
    Generates an Elasticsearch query to find recipes where any ingredient name
    contains the given target string, e.g., 'rice'.
    """
    # Prepare the list of wildcard queries for each target ingredient
    wild_clauses = []
    for ingredient in target_ingredients:
        wild_clauses.append({"wildcard": {"usedIngredients.name": f"*{ingredient}*"}})
    
    # Construct the query using the wild_clauses list directly in the should clause
    query = {
        "query": {
            "bool": {
                "should": wild_clauses,  # Directly use the list here
                "minimum_should_match": all
            }
        }
    }

    return query

