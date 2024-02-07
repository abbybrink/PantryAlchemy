from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
import requests
import json
import os

load_dotenv()

api_key = os.getenv("API_KEY") # Spoonacular API Key (Unique) 
base_url = 'https://api.spoonacular.com/recipes/complexSearch'
query_params = 'query=chicken'

# Make the API request
response = requests.get(f'{base_url}?apiKey={api_key}&{query_params}')

#Check the response status
if response.status_code == 200:
    data = response.json()
    with open('file.json', 'w') as f:
        json.dump(data, f)
else:
    print(f'Error: {response.status_code} - {response.text}')

#Create the elasticsearch cluster
es = Elasticsearch('https://localhost:9200', ca_certs='http_ca.crt', basic_auth=("elastic", "=Q0LSPrqauirlURpWZHO"))

#Read the json file and add a "_index" attribute to each document
docs = list()
with open("file.json") as file:
    docs = json.loads(file.read())["results"]
    for document in docs:
        document['_index'] = "recipe"

with open("file.json", "w") as file:
    json.dump(docs, file)
file.close()

#Delete an index
#If you inserted documents into the cluster in a previous run, you will need to run this command.
#es.options(ignore_status=[400,404]).indices.delete(index='recipe')


#To get a list of all indices in your elasticsearch cluster
#Indices are permanantly inside your cluster after you insert them once.
# for index in es.indices.get_alias(index='*'):
#     print(index)
#       OR
# all_indices = es.indices.get_alias().keys()
# print(all_indices)

#Using elasticsearch helpers to insert documents into the cluster
helpers.bulk(es, docs)
    
# Define the search query
search_query = {
    "query": {
        "match": {
            "title": "chicken"
        }
    }
}

# Perform the search
results = es.search(index="recipe", body=search_query)
print(results)

#Extract and return the recipe names from the results
total_results = results['hits']['total']['value']
#print(total_results)
results_hits = results['hits']['hits']
for num, doc in enumerate(results_hits):
    print(num+1, '--', doc['_source']['title'])


 
