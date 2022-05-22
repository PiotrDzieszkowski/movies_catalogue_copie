import tmdb_client
from unittest.mock import Mock
from main import app
import pytest

def test_get_single_movie(monkeypatch):
    mock_single_movie = ["Movie 1", "Movie 2"]
    request_mock = Mock()
    response = request_mock.return_value
    response.json.return_value = mock_single_movie
    monkeypatch.setattr("tmdb_client.requests.get", request_mock)

    single_movie = tmdb_client.get_single_movie(movie_id=1)
    assert single_movie ==mock_single_movie


def test_get_single_movie_cast(monkeypatch):
    mock_single_movie_cast = ["Movie 1"]
    request_mock = Mock()
    response = request_mock.return_value
    response.json.return_value = mock_single_movie_cast
    monkeypatch.setattr("tmdb_client.requests.get", request_mock)

    single_movie_cast = tmdb_client.get_single_movie_cast(movie_id=1)
    assert single_movie_cast ==mock_single_movie_cast




def test_get_movie_images(monkeypatch):
    mock_movie_images = ["Movie 1"]
    request_mock = Mock()
    response = request_mock.return_value
    response.json.return_value = mock_movie_images
    monkeypatch.setattr("tmdb_client.requests.get", request_mock)

    movie_images = tmdb_client.get_movie_images(movie_id=1)
    assert movie_images ==mock_movie_images

def test_get_poster_url_uses_default_size():
   # Przygotowanie danych
   poster_api_path = "some-poster-path"
   expected_default_size = 'w342'
   # Wywołanie kodu, który testujemy
   poster_url = tmdb_client.get_poster_url(poster_api_path=poster_api_path)
   # Porównanie wyników
   assert expected_default_size in poster_url

def test_get_movies_list_type_popular():
   movies_list = tmdb_client.get_movies_list(list_type="popular")
   assert movies_list is not None

def test_get_movies_list(monkeypatch):
   # Lista, którą będzie zwracać przysłonięte "zapytanie do API"
   mock_movies_list = ['Movie 1', 'Movie 2']

   requests_mock = Mock()
   # Wynik wywołania zapytania do API
   response = requests_mock.return_value
   # Przysłaniamy wynik wywołania metody .json()
   response.json.return_value = mock_movies_list
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)


   movies_list = tmdb_client.get_movies_list(list_type="popular")
   assert movies_list == mock_movies_list
   
def get_movies_list(list_type):
   return call_tmdb_api(f"movie/{list_type}")



@pytest.mark.parametrize("list_type", 
                           (
                              "popular", 
                              "top_rated", 
                              "upcoming", 
                              "now_playing"
                           )
                        )
def test_movies_list(monkeypatch, list_type):
   api_mock = Mock(return_value={'results': []})
   monkeypatch.setattr("tmdb_client.requests.get", api_mock)

   with app.test_client() as client:
       response = client.get(f'/?list_type={list_type}')
       assert response.status_code == 200
       api_mock.assert_called_once_with(f'movie/{list_type}')



if __name__ == '__main__':
    pytest.main()

