import os
import requests
from dotenv import load_dotenv

def check_meal_type(mealtype):
  if mealtype == "breakfast" or "lunch" or "dinner":
    return True
  else:
    return False

class Recipe:
  def __init__(self, id, title, imageURL, likes, ingredientsUsed, ingredientsUnused, ingredientsMissing):
    self.id = id
    self.title = title
    self.imageURL = imageURL
    self.likes = likes

    self.api_key = load_dotenv()
    
    self.ingredientsUsed = ingredientsUsed
    self.ingredientsUnused = ingredientsUnused
    self.ingredientsMissing = ingredientsMissing

    self.ingredientsInRecipe = ingredientsUsed + ingredientsMissing

    # url = f"https://api.spoonacular.com/recipes/{self.id}/information?apiKey={self.api_key}"
    # response = requests.get(url).json()
    # self.servings = response["servings"]
    # self.timeNeeded = response["readyInMinutes"]
    # self.cheap = response["cheap"]
    # self.dairyFree = response["dairyFree"]
    # self.glutenFree = response["glutenFree"]
    # self.vegan = response["vegan"]
    # self.vegetarian = response["vegetarian"]
    # self.dishTypes = filter(check_meal_type, response["dishTypes"])

  @property
  def numIngredientsUsed(self):
    return len(self.ingredientsUsed)

  @property
  def numIngredientsUnused(self):
    return len(self.ingredientsUnused)

  @property
  def numIngredientsMissing(self):
    return len(self.ingredientsMissing)

  @property
  def summary(self):
    url = f"https://api.spoonacular.com/recipes/{self.id}/summary?apiKey={self.api_key}"
    response = requests.get(url).json()

    return(response["summary"])

  @property
  def ingredientsImageURL(self):
    url = f"https://api.spoonacular.com/recipes/{self.id}/ingredientWidget.png?apiKey={self.api_key}"
    response = requests.get(url)

    print(response)
