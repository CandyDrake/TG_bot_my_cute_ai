from api import api


def test_get_city_id_from_hh():
    assert api.get_city_id('Москва') == '1'


def test_search_vacancies():
    assert type(api.search_vacancies('1', 'инженер', 'remote', 10000)) == dict
