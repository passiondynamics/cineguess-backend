import requests
import json

# TMDB API endpoints.
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_POPULAR_URI = "/movie/popular"
TMDB_TOP_RATED_URI = "/movie/top_rated"
TMDB_MOVIE_ACTORS_URI_FMT = "/movie/{}/credits"
TMDB_ACTOR_IMAGES_URI_FMT = "/person/{}/images"
TMDB_ACTOR_CREDITS_URI_FMT = "/person/{}/movie_credits"

CONTENT_LANGUAGE = "en-US"
NUMBER_OF_ACTORS = 4
TMDB_REGION_CODE_USA = (
    840  # See https://en.wikipedia.org/wiki/ISO_3166-1 for other country codes.
)
TMDB_GENRE_ANIMATION = 16


def popular_movies(pages, headers):
    """
    Calls the TMDB API for the popular movies list

    :param pages: int - number of pages of top rated movies to get (there are 20 results on each page)
    :param headers: dict - api authorization header
    :return: dict - the api response of popular movies
    """

    # api endpoint
    url = "{}{}".format(TMDB_BASE_URL, TMDB_POPULAR_URI)
    params = {
        "language": CONTENT_LANGUAGE,
        "page": pages,
        "region": TMDB_REGION_CODE_USA,
    }

    # use the api url and headers to get the information on the popular movies
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def toprated_movies(pages, headers):
    """
    Calls the TMDB API for the top rated movies list

    :param pages: int - number of pages of top rated movies to get (20 per page)
    :param headers: dict - api authorization header
    :return: dict - the api response of top rated movies
    """

    # api endpoint
    url = "{}{}".format(TMDB_BASE_URL, TMDB_TOP_RATED_URI)
    params = {
        "language": CONTENT_LANGUAGE,
        "page": pages,
        "region": TMDB_REGION_CODE_USA,
    }

    # use the api url and headers to get the information on the popular movies
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def extract_movie_data(movies):
    """
    Take the movie id and title out of the API results

    :param movies: dict - movie data
    :return: dict - the extracted data for each movie
    """

    # extract ID and Title
    extracted_data = []
    for movie in movies.get("results", []):
        movie_id = movie.get("id")
        title = movie.get("title")
        genre_ids = movie.get("genre_ids", [])

        # We are choosing to ignore animation for now since it will be difficult to recognize actors.
        if TMDB_GENRE_ANIMATION not in genre_ids:
            extracted_data.append(
                {
                    "id": movie_id,
                    "title": title,
                }
            )

    return {"movies": extracted_data}


def actors(movies, headers):
    """
    Gets the actors from a given movie and then adds the most popular ones to the movie data.

    :param movies: dict - movie data
    :param headers: dict - api authorization header
    """

    # run an api call on each movie and get the cast, after that call popular_actors to get the most popular actors and add them to the json
    for movie in movies.get("movies", []):
        movie_id = movie.get("id")

        # api endpoint
        movie_actors_uri = TMDB_MOVIE_ACTORS_URI_FMT.format(movie_id)
        url = "{}{}".format(TMDB_BASE_URL, movie_actors_uri)
        params = {"language": CONTENT_LANGUAGE}

        # use the api url and headers to get the cast
        response = requests.get(url, params=params, headers=headers)
        most_popular_actors = popular_actors(response.json())

        # Update the existing movie data with actor ids
        movie["actors"] = most_popular_actors


def popular_actors(cast):
    """
    Gets the most popular actors from a given movie cast.

    :param cast: dict - data on the actors in a movie, each entry in the format:
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

    :return: dict - the ids of the most popular actors
    """

    # sort the cast list based on popularity in descending order
    sorted_cast = sorted(cast["cast"], key=lambda x: x["popularity"], reverse=True)

    # get the ids of the top 4 actors
    most_popular_actors = [actor["id"] for actor in sorted_cast[:NUMBER_OF_ACTORS]]
    return most_popular_actors


def actor_images(movies, headers):
    """
    Gets the actors images from the api

    :param movies: dict - movie data
    :param headers: dict - api authorization header
    """

    for movie in movies.get("movies", []):
        actor_urls = []
        actor_ids = movie.get("actors", [])
        for actor_id in actor_ids:

            # api endpoint for getting actor images
            actor_images_uri = TMDB_ACTOR_IMAGES_URI_FMT.format(actor_id)
            url = "{}{}".format(TMDB_BASE_URL, actor_images_uri)
            response = requests.get(url, headers=headers)
            images = response.json().get("profiles", [])

            # Get the 1920x1080 image if available, otherwise use the first available image
            if images:
                find_1080p_image = (
                    img["file_path"]
                    for img in images
                    if img["width"] == 1920 and img["height"] == 1080
                )
                image_url = next(find_1080p_image, images[0]["file_path"])
                actor_urls.append(image_url)

        movie["actor_images"] = (
            actor_urls  # note for testing make sure this adds to actor_images and does not overwrite actor images
        )
        # TODO: I don't understand what's going on here ^.


def related_movies(movies, headers):
    """
    Gets the related movies to the given movies (to consider other answers that will have the same 4 actors, e.g. in a
    sequel)

    :param movies: dict - movie data
    :param headers: dict - api authorization header
    """

    movie_set = None

    for movie in movies.get("movies", []):
        actor_ids = movie.get("actors", [])
        for actor_id in actor_ids:
            # api endpoint
            actor_credits_uri = TMDB_ACTOR_CREDITS_URI_FMT.format(actor_id)
            url = "{}{}".format(TMDB_BASE_URL, actor_credits_uri)
            params = {"language": CONTENT_LANGUAGE}
            response = requests.get(url, params=params, headers=headers)
            actor_movies = response.json().get("cast", [])

            # create a set of the movies and then find the intersection of those sets
            if movie_set is None:
                movie_set = set(m["title"] for m in actor_movies)
            else:
                temp_set = set(m["title"] for m in actor_movies)
                movie_set = set.intersection(movie_set, temp_set)

        # add the alternative answers to the movie json
        movie["alternative_answers"] = movie_set
