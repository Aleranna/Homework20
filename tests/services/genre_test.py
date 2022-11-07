import pytest
from unittest.mock import MagicMock

from dao.model.genre import Genre
from dao.genre import GenreDAO
from service.genre import GenreService


@pytest.fixture()
def genre_dao_fixture():
    genre_dao = GenreDAO(None)

    g1 = Genre(id=1, name='funny movie')
    g2 = Genre(id=2, name='sad movie')

    genre_dao.get_one = MagicMock(return_value=g1)
    genre_dao.get_all = MagicMock(return_value=[g1, g2])
    genre_dao.create = MagicMock(return_value=Genre(id=3))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao_fixture):
        self.genre_service = GenreService(dao=genre_dao_fixture)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre is not None, 'genre is None'
        assert genre.id == 1, 'wrong genre id'

    def test_get_all(self):
        genres = self.genre_service.get_all()

        assert genres is not None, 'genres is None'
        assert len(genres) == 2, 'wrong amount'

    def test_create(self):
        genre_new = {
            'name': 'boring film'
        }

        genre = self.genre_service.create(genre_new)

        assert genre.id is not None, 'genre id is None'

    def test_update(self):
        genre_updated = {
            'id': 1,
            'name': 'smth'
        }
        self.genre_service.update(genre_updated)

    def test_partially_update(self):
        data = {
            'id': 1,
            'name': 'testname'
        }

        self.genre_service.partially_update(data)

        assert self.genre_service.get_one(1).name == data.get('name')

    def test_delete(self):
        self.genre_service.delete(1)
