def test_post(post, unwrap):
    response = post(json={})
    assert response.status_code == 201

    import_id = unwrap(response)["import_id"]
    assert isinstance(import_id, int)


def test_patch_citizens(patch_citizens, unwrap):
    response = patch_citizens(import_id=0, citizen_id=0, json={})
    assert response.status_code == 200

    citizen = unwrap(response)
    assert isinstance(citizen, dict)


def test_get_citizens_fail(get_citizens, unwrap):
    response = get_citizens(import_id=0)
    assert response.status_code == 400


def test_get_citizens_birthdays(get_citizens_birthdays, unwrap):
    response = get_citizens_birthdays(import_id=0)
    assert response.status_code == 200

    birthdays = unwrap(response)
    assert isinstance(birthdays, dict)


def test_get_towns_stat_percentile_age(get_towns_stat_percentile_age, unwrap):
    response = get_towns_stat_percentile_age(import_id=0)
    assert response.status_code == 200

    stats = unwrap(response)
    assert isinstance(stats, list)
