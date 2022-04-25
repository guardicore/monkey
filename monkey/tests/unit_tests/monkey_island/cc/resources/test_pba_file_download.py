def test_file_download_endpoint(tmp_path, flask_client):
    file_contents = "HelloWorld!"
    file_name = "test_file"
    (tmp_path / "custom_pbas" / file_name).write_text(file_contents)

    resp = flask_client.get(f"/api/pba/download/{file_name}")

    assert resp.status_code == 200
    assert next(resp.response).decode() == file_contents


def test_file_download_endpoint_404(tmp_path, flask_client):
    file_name = "nonexistant_file"

    resp = flask_client.get(f"/api/pba/download/{file_name}")

    assert resp.status_code == 404
