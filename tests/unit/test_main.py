from unittest.mock import patch

from src.main import main

@patch("src.main.related_movies")
@patch("src.main.actor_images")
@patch("src.main.actors")
@patch("src.main.extract_movie_data")
@patch("src.main.toprated_movies")
def test_main(
    mock_toprated_movies,
    mock_extract_movie_data,
    mock_actors,
    mock_actor_images,
    mock_related_movies,
):
    mock_toprated_movies.return_value = {"data": "mock-data-1"}
    mock_extract_movie_data.return_value = {"data": "mock-data-2"}

    mock_api_token = "mock-api-token"
    expected_headers = {
        "Accept": "application/json",
        "Authorization": "Bearer mock-api-token",
    }

    with patch.dict("src.main.env_vars", {"TMDB_API_TOKEN": mock_api_token}, clear=True):
        main()

    mock_toprated_movies.assert_called_once_with(1, expected_headers)
    mock_extract_movie_data.assert_called_once_with({"data": "mock-data-1"})
    mock_actors.assert_called_once_with({"data": "mock-data-2"}, expected_headers)
    mock_actor_images.assert_called_once()
    mock_related_movies.assert_called_once()
