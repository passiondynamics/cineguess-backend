from src.movies import *
from src.config import load_env_vars

env_vars = load_env_vars()

def main():
    # number of pages of movies to get from the API. 1 page is 20 movies.
    pages = 1

    # api authorization
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + env_vars["TMDB_API_TOKEN"]
    }

    data = toprated_movies(pages, headers) # gets movie data from the TMDB API
    data = extract_movie_data(data) # removes any animated movies from the list and any unnecessary data
    data = actors(data, headers) # adds the top actors to the json
    data = actor_images(data, headers) # adds the top actors images to the json
    data = related_movies(data, headers) # find any related movies that could be alternative answers



if __name__ == "__main__":
    main()
