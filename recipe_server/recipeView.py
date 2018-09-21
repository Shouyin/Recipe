from django import http
from django.shortcuts import render
from django.shortcuts import render_to_response
from . import settings
from .scripts import logic
import os
import urllib

def recipe_html(request):
    print(os.path.join(settings.BASE_DIR, "recipe_server/static"))
    return render_to_response("recipe.html")


def recipe_api(request):
    fridge = urllib.parse.unquote(request.GET["fridge"])
    recipe = urllib.parse.unquote(request.GET["recipe"])
    print(fridge)
    return http.HttpResponse(logic.main(fridge, recipe))