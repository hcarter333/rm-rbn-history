from qso_spot_kml import transform_spot_kml
from qso_spot_kml import transfom_qso_to_kml
from pathlib import Path

def test_add_qso_1(capsys):  # or use "capfd" for fd-level
    test_spot = '-106.578838, 32.382328,-90.3550100117382,41.4721178800016,2023/01/30 09:15:00,0,14058.3,VE6JY'
    fields = test_spot.split(",")
    #call the method to create fields for kml output
    kml_fields = transform_spot_kml(fields)
    #check that the output line was formatted correctly
    assert kml_fields[4]=='<TimeStamp>2023-01-30T09:15:00</TimeStamp>'
    #flush out this test case
 
def test_add_qso_with_errors(capsys):  # or use "capfd" for fd-level
    #create qso input file
    test_spot = '-106.578838,32.382328,-90.3550100117382,bad_field,41.4721178800016,2023/01/30 09:15:00,0,14058.3,VE6JY'
    return_value = transfom_qso_to_kml(test_spot)
    captured = capsys.readouterr()
    assert captured.out.find("Input line does not have 8 fields:") != -1
    test_spot = '-106.578838,32.382328,-90.3550100117382, 41.4721178800016,2023/01/30 09:15:00,0,14058.3,VE6JY'
    return_value = transfom_qso_to_kml(test_spot)
    captured = capsys.readouterr()
    assert captured.out.find("Input line has a space after comma:") != -1
    #test that a good line still passes
    test_spot = '-106.578838,32.382328,-90.3550100117382,41.4721178800016,2023/01/30 09:15:00,0,14058.3,VE6JY'
    return_value = transfom_qso_to_kml(test_spot)
    captured = capsys.readouterr()
    assert captured.out.find("Input line has a space after comma:") == -1
    assert captured.out.find("Input line does not have 8 fields:") == -1
    assert return_value == 0
