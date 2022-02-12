import asyncio
from asyncio.tasks import sleep
import requests
import pandas as pd

api_key = "de1632918bac5ab984eaca945ade7adm"
'''
https://api.themoviedb.org/3/list/1?api_key=de1642918bac5ab994eaca945ade7ad8&language=en-US
'''

# To get requests response
async def get_data(api_base_url):
    response = requests.get(api_base_url) 
    return response.json() if response.ok else None

# To movies list
async def movies(page):
    try:
        api_base_url = f"https://api.themoviedb.org/3/list/{page}?api_key={api_key}&language=en-US"
        print(api_base_url)
        movies_data = await get_data(api_base_url)
        # movies_list = movies_data.get('items')
        return movies_data
    except:
        return {}

# To fetch and store movies provider
async def providers():
    page = 1
    extra_count = 0
    main_provider = []
    while True:
        movies_list = []
        movies_data = await movies(page)
        if movies_data:
            movies_list = movies_data.get('items') if movies_data.get('items') else []
        page += 1
        if movies_data and movies_data.get('item_count') <=0:
            extra_count += 1
        else:
            extra_count = 0
        if extra_count ==10:
            break
        if movies_list:
            for movie in movies_list:
                movie_id = movie.get('id')
                movie_name = movie.get('original_title')
                provider_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}"
                r = requests.get(provider_url)
                data =r.json()         
                movie_au_data = data.get('results').get('AU', '') if data.get('results') else {}
                if movie_au_data:
                    buy_provider = data.get('results').get('AU').get('buy') if data.get('results').get('AU').get('buy') else []
                    if buy_provider:
                        for provider in buy_provider:
                            buyprovider ={}
                            buyprovider["movie_name"] = movie_name
                            buyprovider["provider_name"] = provider.get('provider_name')
                            buyprovider["type"] = "buy"
                            
                            main_provider.append(buyprovider)

                    flatrate_provider = data.get('results').get('AU').get('flatrate') if data.get('results').get('AU').get('flatrate') else []
                    if flatrate_provider:
                        for provider in flatrate_provider:
                            flatrateprovider ={}
                            flatrateprovider["movie_name"] = movie_name
                            flatrateprovider["provider_name"] = provider.get('provider_name')
                            flatrateprovider["type"] = "flatrate"

                            main_provider.append(flatrateprovider)

                    rent_provider = data.get('results').get('AU').get('rent') if data.get('results').get('AU').get('rent') else []
                    if rent_provider:
                        for provider in rent_provider:
                            rentprovider ={}
                            rentprovider["movie_name"] = movie_name
                            rentprovider["provider_name"] = provider.get('provider_name')
                            rentprovider["type"] = "rent"
                            
                            main_provider.append(rentprovider)

    df = pd.DataFrame([s for s in main_provider])
    # df.to_csv('data2.csv', encoding='utf-8',index=False)
    # print(df)
    df.to_excel('output3.xlsx', header=False, index=False)
    print(df)

asyncio.run(providers())