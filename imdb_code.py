# define helper functions if needed
# and put them in `imdb_helper_functions` module.
# you can import them and use here like that:

from imdb_helper_functions import get_base_url

import urllib
import re
import requests
import csv
from bs4 import BeautifulSoup

current_distance = 1


def get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit) :
    casts = cast_page_soup.find('table', {'class' : 'cast_list'}).find_all('tr', class_=['odd', 'even'])
    cast_dict = {}
    if num_of_actors_limit is not None :
        for cast in casts[:num_of_actors_limit] :
            data = cast.find_all('td')[1].find('a')
            cast_dict[data.text] = urllib.parse.urljoin(get_base_url(), data['href'])
    else :
        for cast in casts :
            data = cast.find_all('td')[1].find('a')
            cast_dict[data.text] = urllib.parse.urljoin(get_base_url(), data['href'])

    return list(cast_dict.items())


def get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit) :
    acting_work_soup = actor_page_soup.findAll('div', id=re.compile("actor-|actress-"))
    movie_work_dict = {}
    filtered_movie_work_list = []
    for work in acting_work_soup :
        movie_list = []
        year = work.find('a', {'class' : 'in_production'})
        if year is None :
            text = work.text
            if text.find('TV Movie') == -1 and text.find('Short') == -1 and text.find('Video Game') == -1 and text.find(
                    'Video short') == -1 and text.find('Video') == -1 and text.find('TV Series') == -1 and text.find(
                'TV Mini Series') == -1 and text.find('TV Series short') == -1 and text.find('TV Special') == -1 :
                movie_link = urllib.parse.urljoin(get_base_url(), work.find('b').find('a')['href'])
                movie_name = work.find('b').find('a').text
                movie_list.append(movie_name)
                movie_list.append(movie_link)
                filtered_movie_work_list.append(movie_list)
    if num_of_movies_limit is not None :
        filtered_movie_work_list = filtered_movie_work_list[:num_of_movies_limit]
    return filtered_movie_work_list


def get_movie_distance(actor_start_url, actor_end_url,
                       num_of_actors_limit, num_of_movies_limit) :
    global current_distance
    actor_start_response = requests.get(actor_start_url)
    actor_start_soup = BeautifulSoup(actor_start_response.text, "html.parser")
    actor_start_movies_list = get_movies_by_actor_soup(actor_start_soup, None)
    if num_of_movies_limit is not None :
        actor_start_movies_list = actor_start_movies_list[num_of_movies_limit :]
    distance_level_1_list = []
    for movie, movie_url in actor_start_movies_list :
        movie_url = movie_url + 'fullcredits'
        response = requests.get(movie_url)
        cast_page_soup = BeautifulSoup(response.text, "html.parser")
        actors_list = get_actors_by_movie_soup(cast_page_soup, None)
        if num_of_actors_limit is not None :
            actors_list = actors_list[num_of_actors_limit :]
        for actor, actor_url in actors_list :
            actor_lst = []
            actor_lst.append(actor)
            actor_lst.append(actor_url)
            distance_level_1_list.append(actor_lst)
    for actor, actor_url in distance_level_1_list :
        if actor_end_url == actor_url :
            return int(current_distance)

    if current_distance <= 3 :
        current_distance += 1
        get_movie_distance(actor_url, actor_end_url, None, None)
    else :
        print("There is no connection between two actors")
    return int(current_distance)


def get_movie_distance_between_highest_paid_actors(actors_list) :
    movie_distance_list = []
    actor_pair_list = list(zip(actors_list, actors_list[1 :] + actors_list[:1]))
    for actor_start_url, actor_end_url in actor_pair_list :
        movie_distance = get_movie_distance(actor_start_url, actor_end_url, 5, 5)
        movie_distance_list.append(actor_start_url)
        movie_distance_list.append(actor_end_url)
        movie_distance_list.append(movie_distance)

    file = open('pair-wise.csv', 'w', newline='')
    with file :
        header = ['Actor Start URL', 'Actor End URL', 'Movie Distance']
        writer = csv.DictWriter(file, fieldnames=header)

        # writing data row-wise into the csv file
        writer.writeheader()
        for movie_distance in movie_distance_list :
            for start_url, end_url, movie_distance in movie_distance :
                writer.writerow({'Actor Start URL' : start_url,
                                 'Actor End URL' : end_url,
                                 'Movie Distance' : movie_distance})


def get_movie_descriptions_by_actor_soup(actor_page_soup) :
    # your code here
    return  # your code here
