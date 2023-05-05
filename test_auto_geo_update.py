from auto_geo_update import get_qrz_session
from auto_geo_update import get_qrz_call_geo_address
from auto_geo_update import get_call_lat_lng
from auto_geo_update import dump_rm_rbn_history
from expe_kml_defs import expe_kml
from qso_spot_kml import qso_spot_kml
import datetime
#from auto_geo_vars import kml_title, tx_lng, tx_lat
import auto_geo_vars

def test_get_qrz_session():
    #call with env_variable password
    sess_id = get_qrz_session("KD0FNR")
    assert sess_id != None

def test_get_qrz_call_geo_address():
    addr_geo = get_qrz_call_geo_address("NU6XB")
    assert addr_geo == "506+Cory+Hall,Berkeley,CA,United+States"

def test_get_call_lat_lng():
    geo_loc = get_call_lat_lng("NU6XB")
    assert geo_loc == "-122.2573242,37.8750364"

def test_dump_rm_rbn_history(capsys):
    result = dump_rm_rbn_history('test_qso_update.csv')
    #Tests that the output results are sorted by date time as expected
    assert result[4][6] == "K6EL"
    #Test that s2s functions corectly see issue #42
    assert result[4][3] == "-122.2218,37.8834"

def test_expe_kml():
    #Tests that five QSOs go in and five QSOs come out
    result = dump_rm_rbn_history('test_qso_update.csv')
    result = expe_kml(result[0][1], result[0][2],result[0][4],result[len(result)-1][4],result)
    assert len(result) == 9
    result = qso_spot_kml("junk",77,result,"SOTA Cerros de Los Lunas Auto!")
    assert result == 9

def test_time():
    qso_dt = []
    qso_dt.append(datetime.datetime.strptime("2023/04/25 03:30:00", "%Y/%m/%d %H:%M:%S"))
    qso_dt.append(datetime.datetime.strptime("2023/04/25 04:30:00", "%Y/%m/%d %H:%M:%S"))
    qso_time_range = auto_geo_vars.time_hh(qso_dt)
    assert qso_time_range[0] == datetime.datetime.strptime("2023/04/25 03:00:00", "%Y/%m/%d %H:%M:%S")
    assert qso_time_range[1] == datetime.datetime.strptime("2023/04/25 05:00:00", "%Y/%m/%d %H:%M:%S")
