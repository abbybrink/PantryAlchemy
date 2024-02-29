from imports import *
load_dotenv()

# Creating a json file
def createJsonAndDocs(food_name, response, file_name): 
    if response.status_code == 200:
        data = response.json()
        if os.path.isfile(file_name):
            print(food_name + ".json already exists in json folder")
        else: 
            with open(file_name, 'w') as f:
                json.dump(data, f)
                f.close()
    else:
        print(f'Error: {response.status_code} - {response.text}')

    return getDocs(file_name, food_name)

def getDocs(file_name, food_name):
    docs = list()
    already_edited = False 
    id = 1

    with open(file_name) as file:
        docs = json.loads(file.read())
        if "results" in docs:           # Remove the results wrapper
            docs = docs["results"]
        
        if '_index' in docs[1].keys():
            print("_index has been added previously.")
            already_edited = True
        else:
            for document in docs:
                document['_index'] = food_name
    if not already_edited:
        with open(file_name, "w") as file:
            json.dump(docs, file)
    file.close()
    return docs