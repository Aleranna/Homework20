import pytest
from unittest.mock import MagicMock

from dao.model.director import Director
from dao.model.genre import Genre
from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def movie_dao_fixture():
    movie_dao = MovieDAO(None)

    d1 = Director(id=1, name='test')
    g1 = Genre(id=1, name='test')

    m1 = Movie(id=1, title='funny movie', genre_id=1, director_id=1, director=d1, genre=g1, year=2020)
    m2 = Movie(id=2, title='sad movie', genre_id=1, director_id=1, director=d1, genre=g1, year=2030)

    movie_dao.get_one = MagicMock(return_value=m1)
    movie_dao.get_all = MagicMock(return_value=[m1, m2])
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao_fixture):
        self.movie_service = MovieService(dao=movie_dao_fixture)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None, 'movie is None'
        assert movie.id == 1, 'wrong movie id'

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert movies is not None, 'movies is None'
        assert len(movies) == 2, 'wrong amount'

    def test_create(self):
        movie_new = {
            'title': 'boring film'
        }

        movie = self.movie_service.create(movie_new)

        assert movie.id is not None, 'movie id is None'

    def test_update(self):
        movie_updated = {
            'id': 1,
            'title': 'my movie'
        }
        self.movie_service.update(movie_updated)

    def test_partially_update(self):
        movie_data = {
            'id': 1,
            'year': 2000
        }

        self.movie_service.partially_update(movie_data)

        assert self.movie_service.get_one(1).year == movie_data.get('year')

    def test_delete(self):
        self.movie_service.delete(1)
