async function fetchRecipes(ingredients) {
    const apiKey = '96ef38777c94480b8b5e59393bac8bca'; // API Key
    const apiUrl = 'https://api.spoonacular.com/recipes/findByIngredients'; // Link to get recipes by ingredient
    const params = new URLSearchParams({
        ingredients: ingredients, // user input
        number: 5, // display 5 recipes
        apiKey: apiKey // apiKey
    });

    try {
        const response = await fetch(`${apiUrl}?${params}`); // fetch command, using apiKey and url
        if (!response.ok) { // error checking for fetch
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json(); // json response
    } catch (error) { // error for if it doesn't work
        console.error('Error fetching recipes:', error);
        return null;
    }
}

function displayRecipes(recipes) { //display function
    const recipesDiv = document.getElementById('recipes'); // get recipes
    recipesDiv.innerHTML = ''; // clears the recipes
    recipes.forEach(recipe => { // for each recipe
        const recipeElement = document.createElement('div'); // div for each recipe
        recipeElement.innerHTML = `<h3>${recipe.title}</h3><img src="${recipe.image}" alt="${recipe.title}" style="width:100px;"><br>`; // grab image and more html
        recipesDiv.appendChild(recipeElement); // add recipe div to recipesDiv
    });
}

document.getElementById('findRecipesButton').addEventListener('click', async () => { // html when click button
    const ingredientInput = document.getElementById('ingredientInput').value; // grab ingredient values
    const ingredients = ingredientInput.split(',').map(ingredient => ingredient.trim());
    const recipes = await fetchRecipes(ingredients); // run fetch
    if (recipes) { // display recipes
        displayRecipes(recipes);
    } else { // no recipes
        document.getElementById('recipes').innerHTML = '<p>No recipes found.</p>';
    }
});

<img src="{{ recipe.image() }}" alt="{{ recipe.title }}" style="width:100px;"></img>
