import pytest
from unittest.mock import MagicMock

from dao.model.director import Director
from dao.director import DirectorDAO
from service.director import DirectorService


@pytest.fixture()
def director_dao_fixture():
    director_dao = DirectorDAO(None)

    sasha = Director(id=1, name='sasha')
    masha = Director(id=2, name='masha')

    director_dao.get_one = MagicMock(return_value=sasha)
    director_dao.get_all = MagicMock(return_value=[sasha, masha])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao_fixture):
        self.director_service = DirectorService(dao=director_dao_fixture)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director is not None, 'director is None'
        assert director.id == 1, 'wrong director id'

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert directors is not None, 'director is None'
        assert len(directors) == 2, 'wrong amount'

    def test_create(self):
        director_new = {
            'name': 'Alexa'
        }

        director = self.director_service.create(director_new)

        assert director.id is not None, 'director id is None'

    def test_update(self):
        director_updated = {
            'id': 1,
            'name': 'Max'
        }
        self.director_service.update(director_updated)

    def test_partially_update(self):
        data = {
            'id': 1,
            'name': 'Petya'
        }

        self.director_service.partially_update(data)

        assert self.director_service.get_one(1).name == data.get('name')

    def test_delete(self):
        self.director_service.delete(1)


