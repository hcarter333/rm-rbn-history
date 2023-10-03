import telnetlib
import argparse

#host = "your_host_address"
#port = 23  # The telnet port

#Accept frequency range per #64
parser = argparse.ArgumentParser(
                    prog='rbn_telnet.py',
                    description='Outputs CQs detected by the RBN over a give freqency range',
                    epilog='Text at the bottom of help')
parser.add_argument('-b', type=float, dest="start_freq", default=14057.3,\
                    help="start of frquency range to watch")
parser.add_argument('-e', type=float, dest="end_freq", default=14058.2,\
                     help="start of frquency range to watch")

args = parser.parse_args()

tn = telnetlib.Telnet("telnet.reversebeacon.net", 7000)
data = tn.read_until(b"Please enter your call:")
command = "kd0fnr\r\n"
tn.write(command.encode("utf-8"))

try:
    while True:
        data = tn.read_until(b"\n")  # Read data until a newline character
        # Search incoming data for the list of frequencies the Rockmite can 
        #use to transmit and receive
        #dump the fields split on space
        #print(data)
        fields = data.split()
        #print(str(len(fields)))
        #print(fields)
        if(len(fields) > 7):
            #print(fields[3])
            #print(str(float(fields[3]) + 1))
            try:
                curr_freq = float(fields[3])
                #print("freq " + str(fields[3]))
                if(curr_freq >= args.start_freq and curr_freq <= args.end_freq):
                    print(data)
            except Exception as error:
                print(fields[3][2:])
                print("found and exception " + str(error))
                continue

except KeyboardInterrupt:
    print("Exiting...")
    tn.close()

