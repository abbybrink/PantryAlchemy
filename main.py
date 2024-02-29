from imports import *
from getJsonAndDocs import *
from esearch import *
load_dotenv()

# Searching Spoonacular for the given food
api_key = os.getenv("API_KEY") # Spoonacular API Key form .env
elasticsearch_key = os.getenv("ELASTICSEARCH_KEY") # Elasticsearch Key from .env 
base_url = 'https://api.spoonacular.com/recipes/complexSearch'
food_name = input("Give the name of food: ")
query_params = 'query='+ food_name
response = requests.get(f'{base_url}?apiKey={api_key}&{query_params}')

while (response.status_code != 200):
    food_name = input("Food not found, enter another food name: ")
    query_params = 'query='+ food_name
    response = requests.get(f'{base_url}?apiKey={api_key}&{query_params}')

# Creating the json and getting the docs
file_name = 'json/' + food_name + '.json'
docs = createJsonAndDocs(food_name, response, file_name)

# Creating the elasticsearch cluster
es = Elasticsearch('https://localhost:9200', ca_certs='http_ca.crt', basic_auth=("elastic", elasticsearch_key))

results = getResults(es, food_name, docs)
#Extract and return the recipe names from the results
total_results = results['hits']['total']['value']
#print(total_results)
results_hits = results['hits']['hits']
for num, doc in enumerate(results_hits):
    print(num+1, '--', doc['_source']['title'])

