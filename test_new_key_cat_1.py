from new_key_cat import make_key_list
from new_key_cat import new_key_cat

def test_answer():
    #list of keys
    key_list = []
    key_list = make_key_list("new_key_cat_test1.csv")
    assert("1516347974" in key_list)
    assert("1516342315" in key_list)
    assert("1516364560" in key_list)

def test_new_key_cat_2(capsys):  # or use "capfd" for fd-level
    #call the method with a file that has both new keys and 
    #existing keys
    new_key_cat("new_key_cat_test2.csv")
    captured = capsys.readouterr()
    #check that none of the existing keys were ouput
    for entry in make_key_list("new_key_cat_test1.csv"):
        assert captured.out.find(entry) == -1
    #Also check that the new key lines were output
    assert captured.out.find("2,") != -1
    assert captured.out.find("3,") != -1
