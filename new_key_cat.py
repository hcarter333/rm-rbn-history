import sys
#open the existing presentation file

#Make a list of all the keys
#data_file will normally be 
#rm_rnb_history_pres.cs
def make_key_list(data_file):
    list2 = []
    with open(data_file) as f:
        for row in f:
            #there are non-separator commas, but since the key is in the 
            #first field, we'll be fine
            list2.append(row.split(",")[0])
    return list2

#Now, as each line comes in from stdin only output it 
#if its key isn't in the list
def new_key_cat(test_file):
    print("entered new_key_cat", file=sys.stderr)
    existing_key_list = make_key_list("rm_rnb_history_pres.csv")
    if(test_file==""):
        f = sys.stdin
    else:
        f = open(test_file)
    for line in f:
        if(line.split(",")[0] not in existing_key_list):
            print(line)
            print(line, file=sys.stderr)
