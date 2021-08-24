# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from imdb_helper_functions import set_base_url

import requests

from imdb_code import get_actors_by_movie_soup, get_movies_by_actor_soup, get_movie_distance, \
    get_movie_distance_between_highest_paid_actors
from bs4 import BeautifulSoup


def test_get_actors_by_movie_soup_with_optional_parameter() :
    url = 'https://www.imdb.com/title/tt6334354/fullcredits'
    set_base_url(url)
    response = requests.get(url)
    cast_page_soup = BeautifulSoup(response.text, "html.parser")
    actors_list = get_actors_by_movie_soup(cast_page_soup, 10)
    assert (len(actors_list) == 10)
    print("test_get_actors_by_movie_soup_with_optional_parameter() is executed")


def test_get_actors_by_movie_soup_without_optional_parameter() :
    url = 'https://www.imdb.com/title/tt6334354/fullcredits'
    set_base_url(url)
    response = requests.get(url)
    cast_page_soup = BeautifulSoup(response.text, "html.parser")
    actors_list = get_actors_by_movie_soup(cast_page_soup, None)
    assert (len(actors_list) == 104)
    print("test_get_actors_by_movie_soup_without_optional_parameter() is executed")


def test_get_movies_by_actor_soup_with_optional_parameter() :
    url = 'https://www.imdb.com/name/nm0740264'
    set_base_url(url)
    response = requests.get(url)
    actor_page_soup = BeautifulSoup(response.text, "html.parser")
    movies_list = get_movies_by_actor_soup(actor_page_soup, 10)
    assert (len(movies_list) == 10)
    print("test_get_movies_by_actor_soup_with_optional_parameter() is executed")


def test_get_movies_by_actor_soup_without_optional_parameter() :
    url = 'https://www.imdb.com/name/nm0740264'
    set_base_url(url)
    response = requests.get(url)
    actor_page_soup = BeautifulSoup(response.text, "html.parser")
    movies_list = get_movies_by_actor_soup(actor_page_soup, None)
    assert (len(movies_list) == 64)
    print("test_get_movies_by_actor_soup_without_optional_parameter() is executed")


def test_get_movies_by_actor_soup_without_optional_parameter_for_female_actor() :
    url = 'https://www.imdb.com/name/nm0205626'
    set_base_url(url)
    response = requests.get(url)
    actor_page_soup = BeautifulSoup(response.text, "html.parser")
    movies_list = get_movies_by_actor_soup(actor_page_soup, None)
    assert (len(movies_list) == 43)
    print("test_get_movies_by_actor_soup_without_optional_parameter_for_female_actor() is executed")


def test_get_movie_distance_1() :
    actor_start_url = "https://www.imdb.com/name/nm0205626"
    actor_end_url = "https://www.imdb.com/name/nm0740264/"
    set_base_url(actor_start_url)
    movie_distance = get_movie_distance(actor_start_url, actor_end_url, None, None)
    assert (movie_distance == 1)
    print("test_get_movie_distance_1() is executed")


def test_get_movie_distance_2() :
    actor_start_url = "https://www.imdb.com/name/nm0205626"
    actor_end_url = "https://www.imdb.com/name/nm0474774/"
    set_base_url(actor_start_url)
    movie_distance = get_movie_distance(actor_start_url, actor_end_url, None, None)
    assert (movie_distance == 4)
    print("test_get_movie_distance_2() is executed")


def test_get_movie_distance_between_highest_paid_actors() :
    actor_list = []
    actor_list.append("https://www.imdb.com/name/nm0425005")
    actor_list.append("https://www.imdb.com/name/nm1165110")
    actor_list.append("https://www.imdb.com/name/nm0000375")
    actor_list.append("https://www.imdb.com/name/nm0474774")
    actor_list.append("https://www.imdb.com/name/nm0000329")
    actor_list.append("https://www.imdb.com/name/nm0177896")
    actor_list.append("https://www.imdb.com/name/nm0001191")
    actor_list.append("https://www.imdb.com/name/nm0424060")
    actor_list.append("https://www.imdb.com/name/nm0005527")
    actor_list.append("https://www.imdb.com/name/nm0262635")
    get_movie_distance_between_highest_paid_actors(actor_list)
    print("test_get_movie_distance_between_highest_paid_actors is executed")


# Press the green button in the gutter to run the script.
if __name__ == '__main__' :
    test_get_actors_by_movie_soup_with_optional_parameter()
    test_get_actors_by_movie_soup_without_optional_parameter()
    test_get_movies_by_actor_soup_with_optional_parameter()
    test_get_movies_by_actor_soup_without_optional_parameter()
    test_get_movies_by_actor_soup_without_optional_parameter_for_female_actor()
    test_get_movie_distance_1()
    test_get_movie_distance_2()
