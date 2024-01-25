# Importing required libraries
import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup

from imagedetect import find_ingredients
from listrecipes import list_recipes

def printRecipes(recipes):
    for i, recipe in enumerate(recipes):
        st.subheader(f"**Recipe {i+1}: {recipe.title}**")
        st.write(f"{recipe.likes} like(s)")
        
        url = recipe.imageURL
        st.write(url)

        # image2 = Image.open("https://t4.ftcdn.net/jpg/02/32/98/31/360_F_232983161_9lmUyHKnWbLW0vQPvWCrp5R5DSpexhbx.jpg")
        # st.image(image2, caption="PEANUT", width=800, channels="RGBA")
        
        st.write("----")
        ing_used = ", ".join(ingredient for ingredient in recipe.ingredientsUsed)
        st.write(f"Ingredients Used: {ing_used}")
        ing_missing = ", ".join(ingredient for ingredient in recipe.ingredientsMissing)
        st.write(f"Ingredients Missing: {ing_missing}")
        st.write("----")
        soup = BeautifulSoup(recipe.summary)
        st.write(soup.get_text())
        # st.write(recipe.summary)

st.title("**LensCook** - Let's Cook Together.")
st.subheader("Seek | Cook | Savor")

# im = cv2.imread("candy.jpg",mode='BGR2RGB')
# st.image(im)


with st.sidebar:
    st.title("LensCook.")
    st.subheader("Your recipe curator.")
    st.write("LensCook is an application that allows users to upload a picture of their available ingredients and have recipes specific to those ingredients generated. LensCook harnesses the power of recognition and artificial intelligence to revolutionize the cooking experience for users © LensCook 2024")
st.divider()

num_of_recipes = st.number_input("Number of recipes: ",min_value=1)
num_of_servings = st.slider("Servings: ", min_value=1, max_value=20)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:    
    dish_types = st.radio("Select dish type: ", ["Breakfast", "Lunch", "Dinner"])
with col2:
    time_needed = st.radio("Cook times: ", ["Quick", "Normal", "Sophisticated"])
with col3:
    price_choice = st.radio("Preperation price: ", ["Cheap", "Expensive"])
with col4:
    recipe_preferences = st.radio("Dietary Restrictions: ", ["None", "Vegan", "Vegetarian", "Dairy Free", "Gluten Free"])
with col5:
    allergens_control = st.multiselect("Select Any Allergens / No-Gos: ", ["Peanuts", "Lactose", "Seafood", "Wheat", "Eggs"])

pic_choice = st.radio("Which one do you want to use?", ["Camera to take Image", "Upload Image"])

if pic_choice == "Camera to take Image":
    ingredients_pic = st.camera_input("Snap a pic of your ingredients!")
else:
    ingredients_pic = st.file_uploader("Upload Image")

if ingredients_pic is not None:
    im1 = Image.open(ingredients_pic)   
    saved_path = "ingredients.jpg"
    im1.save(saved_path)

    ingredients = find_ingredients(path=saved_path)
    ranking = 2 # reduce missing ingredients   
    limit_license = "true"
    ignore_pantry = "false"

    detected_ing = ingredients
    d_ings = ", ".join(ing for ing in detected_ing)
    st.write(f"Detected ingredients: {d_ings}")
    modify_choice = st.radio("Do you want to modify the detected ingredients?", ["no", "yes"])

    if modify_choice == "yes":
        new_ing = st.text_input("Type updated ingredients list (separated by commas)", d_ings)
        st.write(new_ing)

    confirm = st.button("Confirm Choices and start curating recipes")

    recipes = list(set(list_recipes(detected_ing, num_of_recipes, ranking, limit_license, ignore_pantry)))

    ingredients_found = False

    if recipes:
        ingredients_found = True
        recipes.sort(key=lambda x: x.likes, reverse=True)

        printRecipes(recipes)
    else:
        ingredients_found = False
        print("No recipes / ingredients found.")
else:
    st.write("")
