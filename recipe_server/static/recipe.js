var textareaFridge = document.getElementById("fridge-textarea");
var textareaRecipe = document.getElementById("recipe-textarea");
var resultp = document.getElementById("result-p");

var REQUEST_URL = "recipeapi"

var recipeInPage = () => {
    var newRequest = new XMLHttpRequest();
    newRequest.onreadystatechange = () => {
        resultp.innerHTML = newRequest.responseText;
    }
    
    var gotFridge = textareaFridge.value;
    gotFridge = gotFridge.split("\n");
    
    var gotRecipe = textareaRecipe.value;
    gotRecipe = gotRecipe.replace("\n", "");
    
    var requestUrl = REQUEST_URL + "?fridge=" + JSON.stringify(gotFridge) + "&recipe=" + gotRecipe;
    
    newRequest.open("GET", requestUrl, true);
    newRequest.send();
    
};