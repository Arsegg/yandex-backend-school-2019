from flask import url_for


def test_app(client):
    response = client.get(url_for("hello_world"))
    assert response.status_code == 200
    assert response.get_data() == b"Hello World!"
