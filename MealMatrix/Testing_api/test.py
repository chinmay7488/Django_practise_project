import requests

MeadDb_url = 'https://www.themealdb.com/api/json/v1/1/categories.php'
recipe_url_filter = 'https://www.themealdb.com/api/json/v1/1/filter.php?c='

json = requests.get(MeadDb_url).json()
recipe=[]
for j in json['categories']:
    # print( j['idCategory'] ,j['strCategory'])
    print(f'{recipe_url_filter}{j['strCategory']}')
    print(requests.get(f'{recipe_url_filter}{j['strCategory']}').json())
    