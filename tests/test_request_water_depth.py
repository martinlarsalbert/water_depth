import src.data.request_water_depth as request_water_depth

def test_request():
    response = request_water_depth.request()
    assert response.status_code==200

def test_get():
    data_depth = request_water_depth.get()

def test_run(tmpdir):

    save_dir_path = str(tmpdir)
    request_water_depth.run(save_dir_path=save_dir_path)
    