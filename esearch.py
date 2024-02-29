from imports import *
load_dotenv()

def getResults(es, food_name, docs):

    all_indices = es.indices.get_alias(index="*")
    #print(all_indices)

    if food_name not in all_indices:
        helpers.bulk(es, docs)

    # Define the search query
    search_query = {
        "query": {
            "match": {
                "title": ""
            }
        }
    }
    search_query["query"]["match"]["title"] = food_name

    es.indices.refresh(index=food_name)
    # Perform the search
    results = es.search(index=food_name, body=search_query)
    return results