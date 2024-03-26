import pyrebase
import os
from flask import Flask, render_template, request, redirect, session
import requests
from elasticsearch import Elasticsearch

from dotenv import load_dotenv

app = Flask(__name__)
# es = Elasticsearch('http://localhost:9201/')
elasticsearch_key = os.getenv("ELASTICSEARCH_KEY")
es = Elasticsearch('https://localhost:9200', ca_certs='http_ca.crt', basic_auth=("elastic", elasticsearch_key))


load_dotenv()
# Initialize Firebase app
firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
}
firebase=pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
#PLEASE ADD "SECRET_KEY" to the .env file to make this line work, you can make it any string
app.secret_key = os.getenv("SECRET_KEY")
db=firebase.database()


@app.route("/") #default temp
def index():
    return render_template('index.html')

@app.route("/search", methods=['GET', 'POST']) #format, fetch then add to html
def search():
    if request.form['ingredients']:
        ingredients_list = request.form.getlist('ingredients')
        ingredients = ",".join(ingredients_list)
    apiKey = os.getenv("API_KEY")
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {'ingredients': ingredients,
              'number': 12,
              'apiKey': apiKey
              }
    recipes = requests.get(url=url, params=params)
    recipes = recipes.json()
    if recipes:
        index_recipes(recipes)
        search_query = generate_query(ingredients.split(','))
        results = es.search(index="recipes-index", body=search_query)
        new_list = []
        for hit in results['hits']['hits']:
            recipe_info = {
            'id': hit['_source']['id'],
            'title': hit['_source']['title'],
            'image': hit['_source']['image']
            }
            new_list.append(recipe_info)
        return render_template('index.html', recipes=recipes)
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
     # Fetch pantry items for the user from Firebase database
    pantry_items = []
    user = session.get('user')  # Get the user's ID from the session
    user_id=user['localId']
    pantry_items=get_ingredients(user_id)
    return render_template('pantry.html', pantry_items=pantry_items)

def get_ingredients(user_id):
    pantry_data = db.child('pantry').child(user_id).get()
    pantry_items = {}  # Initialize an empty dictionary for pantry items

    if pantry_data.each():
        # Iterate through each item in pantry_data (assuming it's a Firebase data snapshot)
        for item in pantry_data.each():
            # Extract the local ID of the item (assuming it's stored as 'id' in the item data)
            item_id = item.key()
            # Extract key-value pairs from the item and create a dictionary for each item
            item_dict = {k: v for k, v in item.val().items()}
            # Store the item dictionary in the pantry_items dictionary with the item ID as the key
            pantry_items[item_id] = item_dict
    return pantry_items


@app.route("/add_to_pantry", methods=['POST'])
def add_to_pantry():
    ingredient = request.form['ingredient']
    expiration_date = request.form['expiration_date']
    user = session.get('user')  # Get the user's ID from the session
    user_id=user['localId']
    db.child('pantry').child(user_id).push({'ingredient': ingredient, 'expiration_date': expiration_date})
    pantry_items=get_ingredients(user_id)
    return render_template('pantry.html',pantry_items=pantry_items)  # Redirect or render as needed

from flask import request, session, redirect

# Your existing code and imports...

@app.route("/delete_from_pantry", methods=['POST'])
def delete_from_pantry():
    item_id_to_delete = request.form.get('ingredient_id')  # Get the item ID to delete from form data
    if item_id_to_delete:
        user = session.get('user')  # Get the user's ID from the session
        user_id = user['localId']
        db.child('pantry').child(user_id).child(item_id_to_delete).remove()  # Remove the ingredient based on item ID
        # Redirect back to the pantry page after deletion
        pantry_items = get_ingredients(user_id)
        return render_template('pantry.html', pantry_items=pantry_items)
    else:
        # Handle case where item ID to delete is not provided
        return "Item ID to delete not specified", 400  # Return a 400 Bad Request status

@app.route("/edit_pantry_item", methods=['POST'])
def edit_pantry_item():
    item_id = request.form.get('ingredient_id')
    new_ingredient = request.form.get('new_ingredient')
    new_expiration_date = request.form.get('new_expiration_date')
    user = session.get('user')
    user_id = user['localId']
    if item_id:
        pantry_ref = db.child('pantry').child(user_id).child(item_id)
        if new_ingredient or new_expiration_date:  # Check if either new_ingredient or new_expiration_date is provided
            updated_data = {}  # Create a dictionary to store updated data
            if new_ingredient:
                updated_data['ingredient'] = new_ingredient
            if new_expiration_date:
                updated_data['expiration_date'] = new_expiration_date

            pantry_ref.update(updated_data)  # Update the pantry item with the provided data

            # Redirect to the pantry page after updating
            return redirect('/pantry')  # Replace '/pantry' with the actual URL of your pantry page
        else:
            return "Nothing changed", 400  # Return a 400 Bad Request status if nothing is updated
    else:
        return "Item ID not specified", 400  # Return a 400 Bad Request status if item ID is not provided




@app.route("/account")  # Route for the account page
def account():
    if ("user" in session):
        return render_template('account.html', user=session.get("user"))
    else:
        return render_template('account.html')

@app.route("/about")  # Route for the About page
def about():
    return render_template('about.html')

@app.route("/signupForm")  # Route for the About page
def signupForm():
    return render_template('signup.html')

@app.route("/signup", methods=["POST"])
def signup():
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        error_message = "Password and confirm password do not match."
        return render_template("signup.html", error=error_message)
    else:
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session["user"] = user

            return render_template("account.html", user=user)
        except requests.exceptions.HTTPError as e:
            error_message = str(e)  # Get the error message from the HTTPError
            return render_template("signup.html", error=error_message)
        except Exception as e:
            error_message = "An error occurred during signup."
            return render_template("signup.html", error=error_message)

@app.route("/user", methods=["POST"])
def user():
    if request.method == "POST":
        # Get email and password from the form
        email = request.form["email"]
        password = request.form["password"]
        # to reset password auth.send_password_reset_email(email)
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session["user"] = user  # Optionally, store the user's email as well

            # Authentication successful, you may redirect to another page if needed
            print("Authentication successful")
            return render_template("account.html", user=user)
        except:
            # Authentication failed
            error_message = "Authentication failed. Please try again."
            return render_template("account.html", error=error_message)


@app.route("/logout", methods=["POST"])
def logout():
    # # Clear the user session
    session.pop("user",)
    # Redirect the user to the login page
    return redirect("/")

@app.route("/darkmode")
def darkmode():
    return render_template('darkmode.html')

def index_recipes(recipes):
    for recipe in recipes:
        # Here, we're assuming each recipe has a unique ID you can use as the Elasticsearch document ID
        es.index(index="recipes-index", id=recipe['id'], body=recipe)

def generate_query(target_ingredients):
    # Prepare the list of queries for each target ingredient
    ingredient_clauses = []
    for ingredient in target_ingredients:
        ingredient_clauses.append({"match": {"usedIngredients.name": f"{ingredient}"}})

    # Construct the query using the list directly in the should clause
    query = {
        "query": {
            "bool":{
                "should": ingredient_clauses
            }
        }
    }

    return query
