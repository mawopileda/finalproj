import requests

def generate_meal_plans(timeFrame="day",diet="",calories="",exclude=""):
    main_url = "https://api.spoonacular.com/mealplanner/generate?"
    time= "timeFrame="+timeFrame
    main_url += time
    if calories != "":
        main_url += "&targetCalories"+calories
    main_url += "&diet"+diet
    if exclude != "":
        main_url += "&exclude"+exclude
    
    main_url += "&apiKey=58251539aec54ef3b3edd17cc4d8281c"
    headers = {"X-Api-Key ": "rAxol81OhBlSp73DgOwzGg==kAfZazwXkDq7rIpD"}
    return requests.get(main_url,headers).json()