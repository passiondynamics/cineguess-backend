import pytest
import json
import src.movies
import requests_mock

def test_popular_movies():
    # api authorization since we are using mock this doesn't need to have real values in it
    headers = {
        "accept": "accept",
        "Authorization": "authorization"
    }

    # this function makes it so a call to the api using this endpoint will return this information
    # essentially we are testing the fact that the function calls the right endpoint
    with requests_mock.Mocker() as mock_requests:
        mock_requests.get("https://api.themoviedb.org/3/movie/popular?language=en-US&page=1&region=840", json={
            "page": 1,
            "results": [
                {
                    "id": 609681
                }
            ]
        }
        )
        expected = { # I think make expected the same as the mock request
            "page": 1,
            "results": [
                {
                    "id": 609681
                }
            ]
        }
        actual = src.movies.popular_movies(1, headers) # call the request with popular_movies
        assert actual == expected # if popular_movies calls the correct endpoint then our assertion will be true
    

def test_toprated_movies():
    # api authorization
    headers = {
        "accept": "accept",
        "Authorization": "authorization"
    }

    # copied the same testing style as popular movies refer to that for more detailed comments
    with requests_mock.Mocker() as mock_requests:
        mock_requests.get("https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1&region=840", json={
            "page": 1,
            "results": [
                {
                    "id": 278
                }
            ]
        }
        )
        expected = {
            "page": 1,
            "results": [
                {
                    "id": 278
                }
            ]
        }
        actual = src.movies.toprated_movies(1, headers)
        assert actual == expected


def test_extract_movie_data():
    data = {
        "page": 1,
        "results": [
            {
                "backdrop_path": "/kXfqcdQKsToO0OUXHcrrNCHDBzO.jpg",
                "genre_ids": [
                18,
                80
                ],
                "id": 278,
                "original_language": "en",
                "original_title": "The Shawshank Redemption",
                "overview": "Framed in the 1940s for the double murder of his wife and her lover, upstanding banker Andy Dufresne begins a new life at the Shawshank prison, where he puts his accounting skills to work for an amoral warden. During his long stretch in prison, Dufresne comes to be admired by the other inmates -- including an older prisoner named Red -- for his integrity and unquenchable sense of hope.",
                "popularity": 139.421,
                "poster_path": "/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
                "release_date": "1994-09-23",
                "title": "The Shawshank Redemption",
                "vote_average": 8.711,
                "vote_count": 25398
            },
            {
                "backdrop_path": "/rSPw7tgCH9c6NqICZef4kZjFOQ5.jpg",
                "genre_ids": [
                18,
                80
                ],
                "id": 238,
                "original_language": "en",
                "original_title": "The Godfather",
                "overview": "Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch, Vito Corleone barely survives an attempt on his life, his youngest son, Michael steps in to take care of the would-be killers, launching a campaign of bloody revenge.",
                "popularity": 129.69,
                "poster_path": "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
                "release_date": "1972-03-24",
                "title": "The Godfather",
                "vote_average": 8.7,
                "vote_count": 19340
            },
            {
                "backdrop_path": "/kGzFbGhp99zva6oZODW5atUtnqi.jpg",
                "genre_ids": [
                18,
                80
                ],
                "id": 240,
                "original_language": "en",
                "original_title": "The Godfather Part II",
                "overview": "In the continuing saga of the Corleone crime family, a young Vito Corleone grows up in Sicily and in 1910s New York. In the 1950s, Michael Corleone attempts to expand the family business into Las Vegas, Hollywood and Cuba.",
                "popularity": 71.736,
                "poster_path": "/hek3koDUyRQk7FIhPXsa6mT2Zc3.jpg",
                "release_date": "1974-12-20",
                "title": "The Godfather Part II",
                "vote_average": 8.6,
                "vote_count": 11667
            }
        ]
    }
        
    expected = {
        "movies": [
                {
                "id": 278,
                "title": "The Shawshank Redemption"
                },
                {
                "id": 238,
                "title": "The Godfather"
                },
                {
                "id": 240,
                "title": "The Godfather Part II"
                }
        ]
    }
    actual = src.movies.extract_movie_data(data)
    assert actual == expected

    data = {
        "page": 1,
        "results": [
            {
                "backdrop_path": "/kXfqcdQKsToO0OUXHcrrNCHDBzO.jpg",
                "genre_ids": [
                18,
                80,
                16
                ],
                "id": 278,
                "original_language": "en",
                "original_title": "The Shawshank Redemption",
                "overview": "Framed in the 1940s for the double murder of his wife and her lover, upstanding banker Andy Dufresne begins a new life at the Shawshank prison, where he puts his accounting skills to work for an amoral warden. During his long stretch in prison, Dufresne comes to be admired by the other inmates -- including an older prisoner named Red -- for his integrity and unquenchable sense of hope.",
                "popularity": 139.421,
                "poster_path": "/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
                "release_date": "1994-09-23",
                "title": "The Shawshank Redemption",
                "vote_average": 8.711,
                "vote_count": 25398
            },
            {
                "backdrop_path": "/rSPw7tgCH9c6NqICZef4kZjFOQ5.jpg",
                "genre_ids": [
                18,
                80
                ],
                "id": 238,
                "original_language": "en",
                "original_title": "The Godfather",
                "overview": "Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch, Vito Corleone barely survives an attempt on his life, his youngest son, Michael steps in to take care of the would-be killers, launching a campaign of bloody revenge.",
                "popularity": 129.69,
                "poster_path": "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
                "release_date": "1972-03-24",
                "title": "The Godfather",
                "vote_average": 8.7,
                "vote_count": 19340
            },
            {
                "backdrop_path": "/kGzFbGhp99zva6oZODW5atUtnqi.jpg",
                "genre_ids": [
                18,
                80
                ],
                "id": 240,
                "original_language": "en",
                "original_title": "The Godfather Part II",
                "overview": "In the continuing saga of the Corleone crime family, a young Vito Corleone grows up in Sicily and in 1910s New York. In the 1950s, Michael Corleone attempts to expand the family business into Las Vegas, Hollywood and Cuba.",
                "popularity": 71.736,
                "poster_path": "/hek3koDUyRQk7FIhPXsa6mT2Zc3.jpg",
                "release_date": "1974-12-20",
                "title": "The Godfather Part II",
                "vote_average": 8.6,
                "vote_count": 11667
            }
        ]
    }
        
    expected = {
        "movies": [
                {
                "id": 238,
                "title": "The Godfather"
                },
                {
                "id": 240,
                "title": "The Godfather Part II"
                }
        ]
    }

    actual = src.movies.extract_movie_data(data)
    assert actual == expected


def test_actors():
    # api authorization
    headers = {
        "accept": "accept",
        "Authorization": "authorization"
    }

    # copied the same testing style as popular movies refer to that for more detailed comments.
    with requests_mock.Mocker() as mock_requests:      
        mock_requests.get("https://api.themoviedb.org/3/movie/278/credits?language=en-US", json={
            "id": 278,
            "cast": [
                    {
                    "gender": 2,
                    "id": 504,
                    "known_for_department": "Acting",
                    "name": "Tim Robbins",
                    "original_name": "Tim Robbins",
                    "popularity": 32.322,
                    "profile_path": "/A4fHNLX73EQs78f2G6ObfKZnvp4.jpg",
                    "cast_id": 3,
                    "character": "Andy Dufresne",
                    "credit_id": "52fe4231c3a36847f800b131",
                    "order": 0
                    },
                    {
                    "gender": 2,
                    "id": 192,
                    "known_for_department": "Acting",
                    "name": "Morgan Freeman",
                    "original_name": "Morgan Freeman",
                    "popularity": 119.503,
                    "profile_path": "/jPsLqiYGSofU4s6BjrxnefMfabb.jpg",
                    "cast_id": 4,
                    "character": "Ellis Boyd 'Red' Redding",
                    "credit_id": "52fe4231c3a36847f800b135",
                    "order": 1
                    },
                    {
                    "gender": 2,
                    "id": 4029,
                    "known_for_department": "Acting",
                    "name": "Bob Gunton",
                    "original_name": "Bob Gunton",
                    "popularity": 29.707,
                    "profile_path": "/ulbVvuBToBN3aCGcV028hwO0MOP.jpg",
                    "cast_id": 5,
                    "character": "Warden Norton",
                    "credit_id": "52fe4231c3a36847f800b139",
                    "order": 2
                    },
                    {
                    "gender": 2,
                    "id": 6573,
                    "known_for_department": "Acting",
                    "name": "William Sadler",
                    "original_name": "William Sadler",
                    "popularity": 40.262,
                    "profile_path": "/rWeb2kjYCA7V9MC9kRwRpm57YoY.jpg",
                    "cast_id": 7,
                    "character": "Heywood",
                    "credit_id": "52fe4231c3a36847f800b13d",
                    "order": 3
                    },
                    {
                    "gender": 2,
                    "id": 6574,
                    "known_for_department": "Acting",
                    "name": "Clancy Brown",
                    "original_name": "Clancy Brown",
                    "popularity": 60.126,
                    "profile_path": "/9RgzFqbmWBLVfq9wvyDo5UW8VT1.jpg",
                    "cast_id": 8,
                    "character": "Captain Byron T. Hadley",
                    "credit_id": "52fe4231c3a36847f800b141",
                    "order": 4
                    },
                    {
                    "gender": 2,
                    "id": 6575,
                    "known_for_department": "Acting",
                    "name": "Gil Bellows",
                    "original_name": "Gil Bellows",
                    "popularity": 27.165,
                    "profile_path": "/eCOIv2nSGnWTHdn88NoMyNOKWyR.jpg",
                    "cast_id": 9,
                    "character": "Tommy",
                    "credit_id": "52fe4231c3a36847f800b145",
                    "order": 5
                    },
                    {
                    "gender": 2,
                    "id": 6577,
                    "known_for_department": "Acting",
                    "name": "James Whitmore",
                    "original_name": "James Whitmore",
                    "popularity": 20.057,
                    "profile_path": "/d1nOu22OvPzdwS8euWE0FNHwx8K.jpg",
                    "cast_id": 11,
                    "character": "Brooks Hatlen",
                    "credit_id": "52fe4231c3a36847f800b14d",
                    "order": 6
                    },
                    {
                    "gender": 2,
                    "id": 6576,
                    "known_for_department": "Acting",
                    "name": "Mark Rolston",
                    "original_name": "Mark Rolston",
                    "popularity": 15.239,
                    "profile_path": "/hcrNRIptYMRXgkJ9k76BlQu6DQp.jpg",
                    "cast_id": 10,
                    "character": "Bogs Diamond",
                    "credit_id": "52fe4231c3a36847f800b149",
                    "order": 7
                    }
                ]
        }
        )
        expected = {'movies': [{'id': 278, 'title': "The Shawshank Redemption", 'actors': [192, 6574, 6573, 504]}]}

        data = {
        "movies": [
                {
                "id": 278,
                "title": "The Shawshank Redemption"
                }
        ]
        }

        actual = src.movies.actors(data, headers)
        assert actual == expected


def test_popular_actors():
    # create a fake cast output from the api
    cast={
            "id": 278,
            "cast": [
                    {
                    "gender": 2,
                    "id": 504,
                    "known_for_department": "Acting",
                    "name": "Tim Robbins",
                    "original_name": "Tim Robbins",
                    "popularity": 32.322,
                    "profile_path": "/A4fHNLX73EQs78f2G6ObfKZnvp4.jpg",
                    "cast_id": 3,
                    "character": "Andy Dufresne",
                    "credit_id": "52fe4231c3a36847f800b131",
                    "order": 0
                    },
                    {
                    "gender": 2,
                    "id": 192,
                    "known_for_department": "Acting",
                    "name": "Morgan Freeman",
                    "original_name": "Morgan Freeman",
                    "popularity": 119.503,
                    "profile_path": "/jPsLqiYGSofU4s6BjrxnefMfabb.jpg",
                    "cast_id": 4,
                    "character": "Ellis Boyd 'Red' Redding",
                    "credit_id": "52fe4231c3a36847f800b135",
                    "order": 1
                    },
                    {
                    "gender": 2,
                    "id": 4029,
                    "known_for_department": "Acting",
                    "name": "Bob Gunton",
                    "original_name": "Bob Gunton",
                    "popularity": 29.707,
                    "profile_path": "/ulbVvuBToBN3aCGcV028hwO0MOP.jpg",
                    "cast_id": 5,
                    "character": "Warden Norton",
                    "credit_id": "52fe4231c3a36847f800b139",
                    "order": 2
                    },
                    {
                    "gender": 2,
                    "id": 6573,
                    "known_for_department": "Acting",
                    "name": "William Sadler",
                    "original_name": "William Sadler",
                    "popularity": 40.262,
                    "profile_path": "/rWeb2kjYCA7V9MC9kRwRpm57YoY.jpg",
                    "cast_id": 7,
                    "character": "Heywood",
                    "credit_id": "52fe4231c3a36847f800b13d",
                    "order": 3
                    },
                    {
                    "gender": 2,
                    "id": 6574,
                    "known_for_department": "Acting",
                    "name": "Clancy Brown",
                    "original_name": "Clancy Brown",
                    "popularity": 60.126,
                    "profile_path": "/9RgzFqbmWBLVfq9wvyDo5UW8VT1.jpg",
                    "cast_id": 8,
                    "character": "Captain Byron T. Hadley",
                    "credit_id": "52fe4231c3a36847f800b141",
                    "order": 4
                    },
                    {
                    "gender": 2,
                    "id": 6575,
                    "known_for_department": "Acting",
                    "name": "Gil Bellows",
                    "original_name": "Gil Bellows",
                    "popularity": 27.165,
                    "profile_path": "/eCOIv2nSGnWTHdn88NoMyNOKWyR.jpg",
                    "cast_id": 9,
                    "character": "Tommy",
                    "credit_id": "52fe4231c3a36847f800b145",
                    "order": 5
                    },
                    {
                    "gender": 2,
                    "id": 6577,
                    "known_for_department": "Acting",
                    "name": "James Whitmore",
                    "original_name": "James Whitmore",
                    "popularity": 20.057,
                    "profile_path": "/d1nOu22OvPzdwS8euWE0FNHwx8K.jpg",
                    "cast_id": 11,
                    "character": "Brooks Hatlen",
                    "credit_id": "52fe4231c3a36847f800b14d",
                    "order": 6
                    },
                    {
                    "gender": 2,
                    "id": 6576,
                    "known_for_department": "Acting",
                    "name": "Mark Rolston",
                    "original_name": "Mark Rolston",
                    "popularity": 15.239,
                    "profile_path": "/hcrNRIptYMRXgkJ9k76BlQu6DQp.jpg",
                    "cast_id": 10,
                    "character": "Bogs Diamond",
                    "credit_id": "52fe4231c3a36847f800b149",
                    "order": 7
                    }
                ]
        }
    
    # ensure the parsing is working correctly
    expected = [192, 6574, 6573, 504]
    actual = src.movies.popular_actors(cast)
    assert actual == expected


def test_actor_images():
    
    # api authorization
    headers = {
        "accept": "accept",
        "Authorization": "authorization"
    }

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get("https://api.themoviedb.org/3/person/192/images", json={
            "id": 192,
            "profiles": [
                {
                "aspect_ratio": 0.667,
                "height": 2700,
                "file_path": "/jPsLqiYGSofU4s6BjrxnefMfabb.jpg",
                "vote_average": 5.326,
                "vote_count": 7,
                "width": 1800
                },
                {
                "aspect_ratio": 0.667,
                "height": 3000,
                "file_path": "/905k0RFzH0Kd6gx8oSxRdnr6FL.jpg",
                "vote_average": 5.264,
                "vote_count": 8,
                "width": 2000
                },
                {
                "aspect_ratio": 0.667,
                "height": 1920,
                "file_path": "/nhFqNPXDyWTRzHqIUqwayfvDmCn.jpg",
                "vote_average": 5.258,
                "vote_count": 6,
                "width": 1280
                },
                {
                "aspect_ratio": 0.667,
                "height": 999,
                "file_path": "/iRl1tJADZhnkTcirVm21zs8kJhH.jpg",
                "vote_average": 5.198,
                "vote_count": 7,
                "width": 666
                },
                {
                "aspect_ratio": 0.667,
                "height": 3000,
                "file_path": "/1ahENoyEgKSbRUd0IsydIff7rt1.jpg",
                "vote_average": 5.19,
                "vote_count": 5,
                "width": 2000
                },
                {
                "aspect_ratio": 0.667,
                "height": 1920,
                "file_path": "/iuX6R4Sfm6FK5nbfSQ8OgvWcOjy.jpg",
                "vote_average": 5.18,
                "vote_count": 3,
                "width": 1280
                }
            ]
        }
        )
        mock_requests.get("https://api.themoviedb.org/3/person/6574/images", json={
            "id": 6574,
            "profiles": [
                {
                "aspect_ratio": 0.667,
                "height": 1500,
                "file_path": "/9RgzFqbmWBLVfq9wvyDo5UW8VT1.jpg",
                "vote_average": 5.27,
                "vote_count": 10,
                "width": 1000
                },
                {
                "aspect_ratio": 0.667,
                "height": 750,
                "file_path": "/xjg0ZIxP0tFcEQCTeRgKxNtLdpe.jpg",
                "vote_average": 5.264,
                "vote_count": 8,
                "width": 500
                },
                {
                "aspect_ratio": 0.667,
                "height": 1500,
                "file_path": "/uzkU71DkwwRyO7qxwD0A254PjAS.jpg",
                "vote_average": 5.19,
                "vote_count": 5,
                "width": 1000
                },
                {
                "aspect_ratio": 0.667,
                "height": 900,
                "file_path": "/ekaX4du53NcOeEmce7nsk564cBZ.jpg",
                "vote_average": 5.18,
                "vote_count": 3,
                "width": 600
                },
                {
                "aspect_ratio": 0.667,
                "height": 2048,
                "file_path": "/9UwM8st1EdHIJIlJXD2N9PWA8uG.jpg",
                "vote_average": 5.146,
                "vote_count": 10,
                "width": 1365
                }
            ]
            }
        )

        expected = {'movies': [{'id': 278, 'title': "The Shawshank Redemption", 'actors': [192, 6574], 'actor_images': ["/jPsLqiYGSofU4s6BjrxnefMfabb.jpg", "/9RgzFqbmWBLVfq9wvyDo5UW8VT1.jpg"]}]}
        input = {'movies': [{'id': 278, 'title': "The Shawshank Redemption", 'actors': [192, 6574]}]}
        actual = src.movies.actor_images(input, headers)
        assert actual == expected


def test_related_movies():

    # api authorization
    headers = {
        "accept": "accept",
        "Authorization": "authorization"
    }
    
    with requests_mock.Mocker() as mock_requests:
        mock_requests.get("https://api.themoviedb.org/3/person/109/movie_credits?language=en-US", json={
  "cast": [
    {
      "adult": False,
      "backdrop_path": "/jz9Kep0xWjiA6QDHSsd43ASxNfj.jpg",
      "genre_ids": [
        878,
        18,
        10749
      ],
      "id": 38,
      "original_language": "en",
      "original_title": "Eternal Sunshine of the Spotless Mind",
      "overview": "Joel Barish, heartbroken that his girlfriend underwent a procedure to erase him from her memory, decides to do the same. However, as he watches his memories of her fade away, he realises that he still loves her, and may be too late to correct his mistake.",
      "popularity": 81.875,
      "poster_path": "/5MwkWH9tYHv3mV9OdYTMR5qreIz.jpg",
      "release_date": "2004-03-19",
      "title": "Eternal Sunshine of the Spotless Mind",
      "video": False,
      "vote_average": 8.097,
      "vote_count": 14398,
      "character": "Patrick",
      "credit_id": "52fe4211c3a36847f8001677",
      "order": 4
    },
    {
      "adult": False,
      "backdrop_path": "/6G73mNyooWAEQTpckPSnFxFoNmc.jpg",
      "genre_ids": [
        12,
        14,
        28
      ],
      "id": 121,
      "original_language": "en",
      "original_title": "The Lord of the Rings: The Two Towers",
      "overview": "Frodo and Sam are trekking to Mordor to destroy the One Ring of Power while Gimli, Legolas and Aragorn search for the orc-captured Merry and Pippin. All along, nefarious wizard Saruman awaits the Fellowship members at the Orthanc Tower in Isengard.",
      "popularity": 115.753,
      "poster_path": "/5VTN0pR8gcqV3EPUHHfMGnJYN9L.jpg",
      "release_date": "2002-12-18",
      "title": "The Lord of the Rings: The Two Towers",
      "video": False,
      "vote_average": 8.4,
      "vote_count": 21140,
      "character": "Frodo Baggins",
      "credit_id": "52fe421ac3a36847f8004589",
      "order": 0
    },
    {
      "adult": False,
      "backdrop_path": "/2u7zbn8EudG6kLlBzUYqP8RyFU4.jpg",
      "genre_ids": [
        12,
        14,
        28
      ],
      "id": 122,
      "original_language": "en",
      "original_title": "The Lord of the Rings: The Return of the King",
      "overview": "Aragorn is revealed as the heir to the ancient kings as he, Gandalf and the other members of the broken fellowship struggle to save Gondor from Sauron's forces. Meanwhile, Frodo and Sam take the ring closer to the heart of Mordor, the dark lord's realm.",
      "popularity": 132.611,
      "poster_path": "/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg",
      "release_date": "2003-12-01",
      "title": "The Lord of the Rings: The Return of the King",
      "video": False,
      "vote_average": 8.5,
      "vote_count": 23384,
      "character": "Frodo Baggins",
      "credit_id": "52fe421bc3a36847f80046f7",
      "order": 0
    },
    {
      "adult": False,
      "backdrop_path": "/x2RS3uTcsJJ9IfjNPcgDmukoEcQ.jpg",
      "genre_ids": [
        12,
        14,
        28
      ],
      "id": 120,
      "original_language": "en",
      "original_title": "The Lord of the Rings: The Fellowship of the Ring",
      "overview": "Young hobbit Frodo Baggins, after inheriting a mysterious ring from his uncle Bilbo, must leave his home in order to keep it from falling into the hands of its evil creator. Along the way, a fellowship is formed to protect the ringbearer and make sure that the ring arrives at its final destination: Mt. Doom, the only place where it can be destroyed.",
      "popularity": 164.708,
      "poster_path": "/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",
      "release_date": "2001-12-18",
      "title": "The Lord of the Rings: The Fellowship of the Ring",
      "video": False,
      "vote_average": 8.4,
      "vote_count": 24324,
      "character": "Frodo Baggins",
      "credit_id": "52fe421ac3a36847f800448f",
      "order": 0
    }
            ]
        }
        )
        mock_requests.get("https://api.themoviedb.org/3/person/1327/movie_credits?language=en-US", json={
            "cast": [
                {
                "adult": False,
                "backdrop_path": "/5EEdDTV0IBxJ2J4jDUDvl076v7f.jpg",
                "genre_ids": [
                    18,
                    53,
                    80
                ],
                "id": 59,
                "original_language": "en",
                "original_title": "A History of Violence",
                "overview": "An average family is thrust into the spotlight after the father commits a seemingly self-defense murder at his diner.",
                "popularity": 31.45,
                "poster_path": "/3qnO72NHmUgs9JZXAmu4aId9QDl.jpg",
                "release_date": "2005-09-23",
                "title": "A History of Violence",
                "video": False,
                "vote_average": 7.168,
                "vote_count": 3072,
                "character": "Tom Stall / Joey Cusack",
                "credit_id": "52fe4212c3a36847f8001927",
                "order": 0
                },
                {
                "adult": False,
                "backdrop_path": "/6G73mNyooWAEQTpckPSnFxFoNmc.jpg",
                "genre_ids": [
                    12,
                    14,
                    28
                ],
                "id": 121,
                "original_language": "en",
                "original_title": "The Lord of the Rings: The Two Towers",
                "overview": "Frodo and Sam are trekking to Mordor to destroy the One Ring of Power while Gimli, Legolas and Aragorn search for the orc-captured Merry and Pippin. All along, nefarious wizard Saruman awaits the Fellowship members at the Orthanc Tower in Isengard.",
                "popularity": 115.753,
                "poster_path": "/5VTN0pR8gcqV3EPUHHfMGnJYN9L.jpg",
                "release_date": "2002-12-18",
                "title": "The Lord of the Rings: The Two Towers",
                "video": False,
                "vote_average": 8.4,
                "vote_count": 21140,
                "character": "Aragorn",
                "credit_id": "52fe421ac3a36847f8004591",
                "order": 4
                },
                {
                "adult": False,
                "backdrop_path": "/2u7zbn8EudG6kLlBzUYqP8RyFU4.jpg",
                "genre_ids": [
                    12,
                    14,
                    28
                ],
                "id": 122,
                "original_language": "en",
                "original_title": "The Lord of the Rings: The Return of the King",
                "overview": "Aragorn is revealed as the heir to the ancient kings as he, Gandalf and the other members of the broken fellowship struggle to save Gondor from Sauron's forces. Meanwhile, Frodo and Sam take the ring closer to the heart of Mordor, the dark lord's realm.",
                "popularity": 132.611,
                "poster_path": "/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg",
                "release_date": "2003-12-01",
                "title": "The Lord of the Rings: The Return of the King",
                "video": False,
                "vote_average": 8.5,
                "vote_count": 23384,
                "character": "Aragorn",
                "credit_id": "52fe421bc3a36847f80046ff",
                "order": 3
                },
                {
                "adult": False,
                "backdrop_path": "/x2RS3uTcsJJ9IfjNPcgDmukoEcQ.jpg",
                "genre_ids": [
                    12,
                    14,
                    28
                ],
                "id": 120,
                "original_language": "en",
                "original_title": "The Lord of the Rings: The Fellowship of the Ring",
                "overview": "Young hobbit Frodo Baggins, after inheriting a mysterious ring from his uncle Bilbo, must leave his home in order to keep it from falling into the hands of its evil creator. Along the way, a fellowship is formed to protect the ringbearer and make sure that the ring arrives at its final destination: Mt. Doom, the only place where it can be destroyed.",
                "popularity": 164.708,
                "poster_path": "/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",
                "release_date": "2001-12-18",
                "title": "The Lord of the Rings: The Fellowship of the Ring",
                "video": False,
                "vote_average": 8.4,
                "vote_count": 24324,
                "character": "Aragorn",
                "credit_id": "52fe421ac3a36847f8004497",
                "order": 2
                },
                {
                "adult": False,
                "backdrop_path": "/q3ND5eHCkwzbx7xL0inrSJko0PL.jpg",
                "genre_ids": [
                    80,
                    53,
                    18
                ],
                "id": 1965,
                "original_language": "en",
                "original_title": "A Perfect Murder",
                "overview": "Millionaire industrialist Steven Taylor is a man who has everything but what he craves most: the love and fidelity of his wife. A hugely successful player in the New York financial world, he considers her to be his most treasured acquisition. But she needs more than simply the role of dazzling accessory.",
                "popularity": 32.477,
                "poster_path": "/wC0ax12N9GQ8vMXPEs4nES5AAiB.jpg",
                "release_date": "1998-06-05",
                "title": "A Perfect Murder",
                "video": False,
                "vote_average": 6.519,
                "vote_count": 1311,
                "character": "David Shaw",
                "credit_id": "52fe4326c3a36847f803e3a5",
                "order": 2
                }
            ]
        }
        )
        mock_requests.get("https://api.themoviedb.org/3/person/1328/movie_credits?language=en-US", json={
            "cast": [
                {
                "adult": False,
                "backdrop_path": "/5EEdDTV0IBxJ2J4jDUDvl076v7f.jpg",
                "genre_ids": [
                    18,
                    53,
                    80
                ],
                "id": 59,
                "original_language": "en",
                "original_title": "A History of Violence",
                "overview": "An average family is thrust into the spotlight after the father commits a seemingly self-defense murder at his diner.",
                "popularity": 31.45,
                "poster_path": "/3qnO72NHmUgs9JZXAmu4aId9QDl.jpg",
                "release_date": "2005-09-23",
                "title": "A History of Violence",
                "video": False,
                "vote_average": 7.168,
                "vote_count": 3072,
                "character": "Tom Stall / Joey Cusack",
                "credit_id": "52fe4212c3a36847f8001927",
                "order": 0
                },
                {
                "adult": False,
                "backdrop_path": "/6G73mNyooWAEQTpckPSnFxFoNmc.jpg",
                "genre_ids": [
                    12,
                    14,
                    28
                ],
                "id": 121,
                "original_language": "en",
                "original_title": "The Lord of the Rings: The Two Towers",
                "overview": "Frodo and Sam are trekking to Mordor to destroy the One Ring of Power while Gimli, Legolas and Aragorn search for the orc-captured Merry and Pippin. All along, nefarious wizard Saruman awaits the Fellowship members at the Orthanc Tower in Isengard.",
                "popularity": 115.753,
                "poster_path": "/5VTN0pR8gcqV3EPUHHfMGnJYN9L.jpg",
                "release_date": "2002-12-18",
                "title": "The Lord of the Rings: The Two Towers",
                "video": False,
                "vote_average": 8.4,
                "vote_count": 21140,
                "character": "Aragorn",
                "credit_id": "52fe421ac3a36847f8004591",
                "order": 4
                },
                {
                "adult": False,
                "backdrop_path": "/2u7zbn8EudG6kLlBzUYqP8RyFU4.jpg",
                "genre_ids": [
                    12,
                    14,
                    28
                ],
                "id": 122,
                "original_language": "en",
                "original_title": "The Lord of the Rings: The Return of the King",
                "overview": "Aragorn is revealed as the heir to the ancient kings as he, Gandalf and the other members of the broken fellowship struggle to save Gondor from Sauron's forces. Meanwhile, Frodo and Sam take the ring closer to the heart of Mordor, the dark lord's realm.",
                "popularity": 132.611,
                "poster_path": "/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg",
                "release_date": "2003-12-01",
                "title": "The Lord of the Rings: The Return of the King",
                "video": False,
                "vote_average": 8.5,
                "vote_count": 23384,
                "character": "Aragorn",
                "credit_id": "52fe421bc3a36847f80046ff",
                "order": 3
                },
                {
                "adult": False,
                "backdrop_path": "/x2RS3uTcsJJ9IfjNPcgDmukoEcQ.jpg",
                "genre_ids": [
                    12,
                    14,
                    28
                ],
                "id": 120,
                "original_language": "en",
                "original_title": "The Lord of the Rings: The Fellowship of the Ring",
                "overview": "Young hobbit Frodo Baggins, after inheriting a mysterious ring from his uncle Bilbo, must leave his home in order to keep it from falling into the hands of its evil creator. Along the way, a fellowship is formed to protect the ringbearer and make sure that the ring arrives at its final destination: Mt. Doom, the only place where it can be destroyed.",
                "popularity": 164.708,
                "poster_path": "/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",
                "release_date": "2001-12-18",
                "title": "The Lord of the Rings: The Fellowship of the Ring",
                "video": False,
                "vote_average": 8.4,
                "vote_count": 24324,
                "character": "Aragorn",
                "credit_id": "52fe421ac3a36847f8004497",
                "order": 2
                },
                {
                "adult": False,
                "backdrop_path": "/q3ND5eHCkwzbx7xL0inrSJko0PL.jpg",
                "genre_ids": [
                    80,
                    53,
                    18
                ],
                "id": 1965,
                "original_language": "en",
                "original_title": "A Perfect Murder",
                "overview": "Millionaire industrialist Steven Taylor is a man who has everything but what he craves most: the love and fidelity of his wife. A hugely successful player in the New York financial world, he considers her to be his most treasured acquisition. But she needs more than simply the role of dazzling accessory.",
                "popularity": 32.477,
                "poster_path": "/wC0ax12N9GQ8vMXPEs4nES5AAiB.jpg",
                "release_date": "1998-06-05",
                "title": "A Perfect Murder",
                "video": False,
                "vote_average": 6.519,
                "vote_count": 1311,
                "character": "David Shaw",
                "credit_id": "52fe4326c3a36847f803e3a5",
                "order": 2
                }
            ]
        }
        )
        mock_requests.get("https://api.themoviedb.org/3/person/110/movie_credits?language=en-US", json={
            "cast": [
                {
                "adult": False,
                "backdrop_path": "/5EEdDTV0IBxJ2J4jDUDvl076v7f.jpg",
                "genre_ids": [
                    18,
                    53,
                    80
                ],
                "id": 59,
                "original_language": "en",
                "original_title": "A History of Violence",
                "overview": "An average family is thrust into the spotlight after the father commits a seemingly self-defense murder at his diner.",
                "popularity": 31.45,
                "poster_path": "/3qnO72NHmUgs9JZXAmu4aId9QDl.jpg",
                "release_date": "2005-09-23",
                "title": "A History of Violence",
                "video": False,
                "vote_average": 7.168,
                "vote_count": 3072,
                "character": "Tom Stall / Joey Cusack",
                "credit_id": "52fe4212c3a36847f8001927",
                "order": 0
                },
                {
                "adult": False,
                "backdrop_path": "/6G73mNyooWAEQTpckPSnFxFoNmc.jpg",
                "genre_ids": [
                    12,
                    14,
                    28
                ],
                "id": 121,
                "original_language": "en",
                "original_title": "The Lord of the Rings: The Two Towers",
                "overview": "Frodo and Sam are trekking to Mordor to destroy the One Ring of Power while Gimli, Legolas and Aragorn search for the orc-captured Merry and Pippin. All along, nefarious wizard Saruman awaits the Fellowship members at the Orthanc Tower in Isengard.",
                "popularity": 115.753,
                "poster_path": "/5VTN0pR8gcqV3EPUHHfMGnJYN9L.jpg",
                "release_date": "2002-12-18",
                "title": "The Lord of the Rings: The Two Towers",
                "video": False,
                "vote_average": 8.4,
                "vote_count": 21140,
                "character": "Aragorn",
                "credit_id": "52fe421ac3a36847f8004591",
                "order": 4
                },
                {
                "adult": False,
                "backdrop_path": "/2u7zbn8EudG6kLlBzUYqP8RyFU4.jpg",
                "genre_ids": [
                    12,
                    14,
                    28
                ],
                "id": 122,
                "original_language": "en",
                "original_title": "The Lord of the Rings: The Return of the King",
                "overview": "Aragorn is revealed as the heir to the ancient kings as he, Gandalf and the other members of the broken fellowship struggle to save Gondor from Sauron's forces. Meanwhile, Frodo and Sam take the ring closer to the heart of Mordor, the dark lord's realm.",
                "popularity": 132.611,
                "poster_path": "/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg",
                "release_date": "2003-12-01",
                "title": "The Lord of the Rings: The Return of the King",
                "video": False,
                "vote_average": 8.5,
                "vote_count": 23384,
                "character": "Aragorn",
                "credit_id": "52fe421bc3a36847f80046ff",
                "order": 3
                },
                {
                "adult": False,
                "backdrop_path": "/x2RS3uTcsJJ9IfjNPcgDmukoEcQ.jpg",
                "genre_ids": [
                    12,
                    14,
                    28
                ],
                "id": 120,
                "original_language": "en",
                "original_title": "The Lord of the Rings: The Fellowship of the Ring",
                "overview": "Young hobbit Frodo Baggins, after inheriting a mysterious ring from his uncle Bilbo, must leave his home in order to keep it from falling into the hands of its evil creator. Along the way, a fellowship is formed to protect the ringbearer and make sure that the ring arrives at its final destination: Mt. Doom, the only place where it can be destroyed.",
                "popularity": 164.708,
                "poster_path": "/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",
                "release_date": "2001-12-18",
                "title": "The Lord of the Rings: The Fellowship of the Ring",
                "video": False,
                "vote_average": 8.4,
                "vote_count": 24324,
                "character": "Aragorn",
                "credit_id": "52fe421ac3a36847f8004497",
                "order": 2
                },
                {
                "adult": False,
                "backdrop_path": "/q3ND5eHCkwzbx7xL0inrSJko0PL.jpg",
                "genre_ids": [
                    80,
                    53,
                    18
                ],
                "id": 1965,
                "original_language": "en",
                "original_title": "A Perfect Murder",
                "overview": "Millionaire industrialist Steven Taylor is a man who has everything but what he craves most: the love and fidelity of his wife. A hugely successful player in the New York financial world, he considers her to be his most treasured acquisition. But she needs more than simply the role of dazzling accessory.",
                "popularity": 32.477,
                "poster_path": "/wC0ax12N9GQ8vMXPEs4nES5AAiB.jpg",
                "release_date": "1998-06-05",
                "title": "A Perfect Murder",
                "video": False,
                "vote_average": 6.519,
                "vote_count": 1311,
                "character": "David Shaw",
                "credit_id": "52fe4326c3a36847f803e3a5",
                "order": 2
                }
            ]
        }
        )
    
            
        input = {'movies': [{'id': 238, 'title': 'The Lord of the Rings: The Return of the King', 'actors': [110, 109, 1328, 1327], 'actor_images': ['/jPsLqiYGSofU4s6BjrxnefMfabb.jpg', '/9RgzFqbmWBLVfq9wvyDo5UW8VT1.jpg']}]}
        expected = {'movies': [{'id': 238, 'title': 'The Lord of the Rings: The Return of the King', 'actors': [110, 109, 1328, 1327], 'actor_images': ['/jPsLqiYGSofU4s6BjrxnefMfabb.jpg', '/9RgzFqbmWBLVfq9wvyDo5UW8VT1.jpg'], 'alternative_answers': {'The Lord of the Rings: The Two Towers', 'The Lord of the Rings: The Return of the King', 'The Lord of the Rings: The Fellowship of the Ring'}}]}

        actual = src.movies.related_movies(input, headers)
        assert actual == expected