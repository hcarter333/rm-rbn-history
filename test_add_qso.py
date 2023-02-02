from add_qso import add_qso

def test_add_qso_1(capsys):  # or use "capfd" for fd-level
    #call the method to add qsos
    add_qso("test_add_qso.txt", 7)
    captured = capsys.readouterr()
    #check that the output line was formatted correctly
    captured_fields = captured.out.split(",")
    assert captured.out=='7,"{""type"":""LineString"",""coordinates"":[[-106.579229, 32.380401],[-94.6250,38.6458]]}","2023/01/31 11:47:00",7,14057.6,KTEST\n'
 
def test_add_qso_2(capsys):  # or use "capfd" for fd-level
    #call the method to add qsos
    add_qso("test_add_qso2.txt", 7)
    captured = capsys.readouterr()
    #check that the output line was formatted correctly
    #Uses output directly from generating google sheet
    captured_fields = captured.out.split(",")
    assert captured.out=='7,"{""type"":""LineString"",""coordinates"":[[-106.578838,32.382328],[-97.0957613946923,30.0488933199194]]}","2023/01/29 17:32",0,14058.3,KF9RX\n'

#pass an empty file
def test_add_qso_3(capsys):  # or use "capfd" for fd-level
    #call the method to add qsos
    add_qso("qso_empty.txt", 7)
    captured = capsys.readouterr()
    #check that the output line was formatted correctly
    #Uses output directly from generating google sheet
    #There should be no captured output
    captured_fields = captured.out.split(",")
    assert captured.out==''
