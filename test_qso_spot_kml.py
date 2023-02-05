from qso_spot_kml import transform_spot_kml

def test_add_qso_1(capsys):  # or use "capfd" for fd-level
    #call the method to add qsos
    test_spot = '-106.578838, 32.382328,-90.3550100117382,41.4721178800016,2023/01/30 09:15:00,0,14058.3,VE6JY'
    fields = test_spot.split(",")
    kml_fields = transform_spot_kml(fields)
    #check that the output line was formatted correctly
    assert kml_fields[4]=='<TimeStamp>2023-01-30T09:15:00</TimeStamp>'
 
