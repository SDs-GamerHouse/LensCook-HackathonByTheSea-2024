from flask import Flask, jsonify
import os
from google.cloud import vision
from PIL import Image
from dotenv import load_dotenv
import requests
from typing import List


from Recipe import Recipe


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "backend/key.json"

api_key = load_dotenv()

def find_ingredients(path):
    """Localize objects in the local image and draw bounding polygons with labels.

    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    ingredients = client.object_localization(image=image, max_results=100).localized_object_annotations
    new_ing_names = []
    for i, ingredient in enumerate(ingredients):
        img = Image.open(path)
        width, height = img.size
        vx = []
        vy = []
        for vertex in ingredient.bounding_poly.normalized_vertices:
            vx.append([vertex.x * width])
            vy.append([vertex.y * height])
        left = min(vx)
        right = max(vx)
        top = min(vy)
        bottom = max(vy)
        dims = (left[0],top[0], right[0], bottom[0])
        im = img.crop(dims)
        name = "backend/segments/segment" + str(i) + ".jpg"
        im = im.save(name)
        with open(name, "rb") as image_file:
            content = image_file.read()
        im = vision.Image(content=content)
        newings = client.object_localization(image=im, max_results=100).localized_object_annotations
        for ing in newings:
            if ing.name not in ["Vegetable", "Baked Goods", "Packaged Goods", "Food"]:
                new_ing_names.append(ing.name)
    return new_ing_names

app = Flask(__name__)

@app.route("/get-user/<path>")
def recipe(imgpath):
    ingredients = find_ingredients(imgpath)
    
    return "Home"

if __name__ == "__main__":
    app.run(debug=True)