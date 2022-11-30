from bs4 import BeautifulSoup
import requests
import pandas as pd


main_url = "https://www.themoviedb.org"

movie_data = []
for i in range(1,51):
    base_url = f"https://www.themoviedb.org/movie?page={i}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    page = requests.get(base_url,headers=headers)
    soup = BeautifulSoup(page.content,'lxml')
    lists = soup.find_all('div',class_= 'card style_1')
    
    for list in lists:
        url1 = main_url + list.find('a')['href']
        movie_data.append(url1)

lst = []
for url in movie_data:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    req = requests.get(url,headers=headers)
    soup = BeautifulSoup(req.content,'lxml')
    infos = soup.find_all('div',class_='header large border first')

    
    for info in infos:
        title = info.find('h2').text.strip()
        rating = info.find('div',class_='user_score_chart')['data-percent'].strip()
        genre = info.find('span',class_='genres').text.strip()
        release = info.find('span',class_='release').text.strip()
        try:
            casts = info.select('ol',class_='people no_image')
            for cast in casts:
                director = cast.find('a').text
        except:
            director = 'N/A'
        url = url.strip()
        try:
            runtime = info.find('span',class_='runtime').text.strip()
        except:
            runtime = 'N/A'

        all_movie = {
            'Title' : title,
            'Rating' : rating,
            'Genre' : genre,
            'Release' : release,
            'Runtime' : runtime,
            'Director' : director,
            'URL' : url
        }
        lst.append(all_movie)


df = pd.DataFrame(lst)
a = df.to_excel('movie_data4.xlsx')



    