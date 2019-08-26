import pytest


def test_post(post, unwrap):
    response = post(json={})
    assert response.status_code == 400


@pytest.mark.skip
def test_patch_citizens(patch_citizens, unwrap):
    response = patch_citizens(import_id=0, citizen_id=0, json={})
    assert response.status_code == 200


@pytest.mark.skip
def test_get_citizens(get_citizens, unwrap):
    response = get_citizens(import_id=0)
    assert response.status_code == 200

    citizens = unwrap(response)
    assert isinstance(citizens, list)


@pytest.mark.skip
def test_get_citizens_birthdays(get_citizens_birthdays, unwrap):
    response = get_citizens_birthdays(import_id=0)
    assert response.status_code == 200

    birthdays = unwrap(response)
    assert isinstance(birthdays, dict)


@pytest.mark.skip
def test_get_towns_stat_percentile_age(get_towns_stat_percentile_age, unwrap):
    response = get_towns_stat_percentile_age(import_id=0)
    assert response.status_code == 200

    stats = unwrap(response)
    assert isinstance(stats, list)
