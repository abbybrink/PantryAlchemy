from flask import Flask, render_template, request
import requests

# enter in command line 'flask run'
# look up this url: http://127.0.0.1:5000/

app = Flask(__name__)

@app.route("/") #default temp
def index():
    return render_template('index.html')

@app.route("/search", methods=['GET', 'POST']) #format, fetch then add to html
def search():
    ingredients = request.form['ingredients']
    ingredients = ingredients.split(',')
    apiKey = '96ef38777c94480b8b5e59393bac8bca'
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {'ingredients' : ingredients, 
              'number' : 5,
              'apiKey' : apiKey
              }
    recipes = requests.get(url = url, params = params)
    recipes = recipes.json()
    if recipes:
        return render_template('index.html', recipes=recipes)
    else:
        return render_template('index.html')


