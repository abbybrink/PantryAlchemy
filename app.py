import pyrebase
import os
from flask import Flask, render_template, request, redirect, session
import requests
from elasticsearch import Elasticsearch

from dotenv import load_dotenv

app = Flask(__name__)

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
# db=firebase.database()
# storage=firebase.storage()




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
              'number': 5,
              'apiKey': apiKey
              }
    recipes = requests.get(url=url, params=params)
    recipes = recipes.json()
    if recipes:
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
    return render_template('pantry.html')


@app.route("/account")  # Route for the account page
def account():
    if ("user" in session):
        return render_template('account.html', user=user)
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
            # auth.send_email_verification(user['idToken'])
            return render_template("account.html", user=user)
        except:
            error_message = "Email already exists, or an error occurred during signup."
            return render_template("signup.html", error=error_message)

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        # Get email and password from the form
        email = request.form["email"]
        password = request.form["password"]
        #to reset password auth.send_password_reset_email(email)
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session["user"]=email
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

