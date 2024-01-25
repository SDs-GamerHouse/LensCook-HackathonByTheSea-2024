# Importing requires libraries
from listrecipes import list_recipes
import imagedetect

# PARAMETERS - Perhaps convert to dictionary for organization
ingredients = imagedetect.find_ingredients("uploads/pnut.jpg")
num_of_recipes = 5
ranking = 2 # reduce missing ingredients   
limit_license = "true"
ignore_pantry = "false"
allergens = []

recipes = list_recipes(ingredients, num_of_recipes, ranking, limit_license, ignore_pantry, allergens=["peanuts"])

# tysm stack overflow
# https://stackoverflow.com/questions/403421/how-do-i-sort-a-list-of-objects-based-on-an-attribute-of-the-objects

def printRecipes(recipes):
  for i, recipe in enumerate(recipes):
    print(f"Recipe {i+1}: {recipe.title}")
    print(f"{recipe.likes} like(s)")
    print(f"Image URL: {recipe.imageURL}")
    print("----")
    print(f"Ingredients Used: {recipe.ingredientsUsed}")
    print(f"Ingredients Missing: {recipe.ingredientsMissing}")
    print("----")
    # usage for new features: recipe.feature (i.e. servings, glutenFree, etc. [see Recipe class for all])
    print(recipe.summary)
    print("\n")

ingredients_found = False

if recipes:
  ingredients_found = True
  recipes.sort(key=lambda x: x.likes, reverse=True)

  printRecipes(recipes)
else:
  ingredients_found = False
  print("No recipes / ingredients found.")
