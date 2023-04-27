from auto_geo_update import get_qrz_session
from auto_geo_update import get_qrz_call_geo_address

def test_get_qrz_session():
    #call with env_variable password
    sess_id = get_qrz_session("KD0FNR")
    assert sess_id != None

def test_get_qrz_call_geo_address():
    addr_geo = get_qrz_call_geo_address("NU6XB")
    assert addr_geo == "506+Cory+Hall,Berkeley,CA"
