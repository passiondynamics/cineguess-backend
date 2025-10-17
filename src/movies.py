import requests
import json

# standard URL for the TMDB API
TMDB_BASE_URL = "https://api.themoviedb.org/3/"
# number of actors that will be used in the game (this will remain at 4)
NUMBER_OF_ACTORS = 4

def popular_movies(pages, headers):
    """
        This function calls the TMDB API for the popular movies list
    
        :param pages: int - number of pages of top rated movies to get there are 20 results on each page
        :param headers: dict - api authorization header
        :return: dict return the api response of popular movies
    """
    
    # api endpoint
    url = "{}movie/popular?language=en-US&page={}&region=840".format(TMDB_BASE_URL, pages) # region 840 is USA see https://en.wikipedia.org/wiki/ISO_3166-1 for other country codes

    # use the api url and headers to get the information on the popular movies
    response = requests.get(url, headers=headers)
    return response.json()


def toprated_movies(pages, headers):

    """
        This function calls the TMDB API for the top rated movies list
    
        :param pages: int - number of pages of top rated movies to get there are 20 results on each page
        :param headers: dict - api authorization header
        :return: dict return the api response of top rated movies
    """
    
    # api endpoint
    url = "{}movie/top_rated?language=en-US&page={}&region=840".format(TMDB_BASE_URL, pages)

    # use the api url and headers to get the information on the popular movies
    response = requests.get(url, headers=headers)
    return response.json()


def extract_movie_data(movies):
    """
        Take the movie id and title out of the API results

        :param movies: dict - a dict of movie data
        :return: dict return only the extracted data from the movies should be just the ids and the title
    """

    # extract ID and Title
    extracted_data = [
        {"id": movie.get("id"), "title": movie.get("title")}
        for movie in movies.get("results", [])
        if 16 not in movie.get("genre_ids", []) # genre 16 is animation we are choosing to ignore it for now since it will be difficult to recognize actors
    ]
    return {"movies": extracted_data}


def actors(movies, headers):
    """
        This function gets the actors from a given movie and then calls the popular_actors function to get the most popular ones

        :param movies: dict - a dict of movie data
        :param headers: dict - api authorization header
        :return: dict return the movies dict after adding the most popular actors to each movie
    """
    
    # run an api call on each movie and get the cast, after that call popular_actors to get the most popular actors and add them to the json
    for movie in movies.get("movies", []):
        movie_id = movie.get("id")
        # api endpoint
        url = "{}movie/{}/credits?language=en-US".format(TMDB_BASE_URL, movie_id)
        # use the api url and headers to get the cast
        response = requests.get(url, headers=headers)
        most_popular_actors = popular_actors(response.json())

        # Update the existing movie data with actor ids
        movie["actors"] = most_popular_actors

    return movies


def popular_actors(cast):
    """
        This is a helper function that gets the most popular actors from a given movie cast.

        :param cast: dict - the cast of a certain movie as well as data on the actors one entry looks like this 
        "cast": [
            {
            "adult": false,
            "gender": 2,
            "id": 504,
            "known_for_department": "Acting",
            "name": "Tim Robbins",
            "original_name": "Tim Robbins",
            "popularity": 32.809,
            "profile_path": "/A4fHNLX73EQs78f2G6ObfKZnvp4.jpg",
            "cast_id": 3,
            "character": "Andy Dufresne",
            "credit_id": "52fe4231c3a36847f800b131",
            "order": 0
            }
        ]
        
        :return: dict - return the ids of the most popular actors
    """
    # sort the cast list based on popularity in descending order
    sorted_cast = sorted(cast["cast"], key=lambda x: x["popularity"], reverse=True)

    # get the ids of the top 4 actors
    most_popular_actors = [actor["id"] for actor in sorted_cast[:NUMBER_OF_ACTORS]]
    return most_popular_actors


def actor_images(movies, headers):
    """
        This function gets the actors images from the api

        :param movies: dict - a dict of movie data
        :param headers: dict - api authorization header
        :return: dict the updated movies dict with pictures of the actors 
    """
    actor_url = []

    for movie in movies.get("movies", []):
        actor_ids = movie.get("actors", [])
        for actor_id in actor_ids:

            # api endpoint for getting actor images
            url = "{}person/{}/images".format(TMDB_BASE_URL, actor_id)
            response = requests.get(url, headers=headers)
            images = response.json().get("profiles", [])

            # Get the 1920x1080 image if available, otherwise use the first available image
            if images:
                image_url = next((img["file_path"] for img in images if img["width"] == 1920 and img["height"] == 1080), images[0]["file_path"])
                actor_url.append(image_url)

            movie["actor_images"] = actor_url # note for testing make sure this adds to actor_images and does not overwrite actor images
    
    return movies


def related_movies(movies, headers):
    """
        This function gets the related movies to the movies in our json this is to consider answers that will have the same 4 actors in a sequel

        :param movies: dict - a dict of movie data
        :param headers: dict - api authorization header
        :return: dict the movies dict with the related movies added
    """

    movie_set = None

    for movie in movies.get("movies", []):
        actor_ids = movie.get("actors", [])
        for actor_id in actor_ids:
            # api endpoint
            actor_url = "{}person/{}/movie_credits?language=en-US".format(TMDB_BASE_URL, actor_id)
            actor_response = requests.get(actor_url, headers=headers)
            actor_movies = actor_response.json().get("cast", [])
            
            # create a set of the movies and then find the intersection of those sets
            if movie_set is None:
                movie_set = set(m["title"] for m in actor_movies)
            else:
                temp_set = set(m["title"] for m in actor_movies)
                movie_set = set.intersection(movie_set, temp_set)

        # add the alternative answers to the movie json
        movie["alternative_answers"] = movie_set

    return movies
