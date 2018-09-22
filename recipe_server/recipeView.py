from django import http
from django.shortcuts import render
from django.shortcuts import render_to_response
from . import settings
from .scripts import logic
import os
import urllib
import json

def recipe_html(request):
    print(os.path.join(settings.BASE_DIR, "recipe_server/static"))
    return render_to_response("recipe.html")


def recipe_api(request):
    fridge = request.GET["fridge"]
    reconstructed_string = ""
    for i in json.loads(fridge):
        reconstructed_string += i + "\n"
    recipe = request.GET["recipe"]
    print(reconstructed_string)
    return http.HttpResponse(logic.main(reconstructed_string, recipe))