var textareaFridge = document.getElementById("fridge-textarea");
var textareaRecipe = document.getElementById("recipe-textarea");
var resultp = document.getElementById("result-p");

var REQUEST_URL = "recipeapi"

console.log(textareaFridge);

var recipeInPage = () => {
    var newRequest = new XMLHttpRequest();
    newRequest.onreadystatechange = () => {
        resultp.innerHTML = newRequest.responseText;
    }
    
    var requestUrl = REQUEST_URL + "?fridge=" + textareaFridge.innerHTML + "&recipe=" + textareaRecipe.innerHTML;
    
    newRequest.open("GET", requestUrl, true);
    newRequest.send();
    
};