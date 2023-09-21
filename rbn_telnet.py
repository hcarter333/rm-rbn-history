import telnetlib

#host = "your_host_address"
#port = 23  # The telnet port

tn = telnetlib.Telnet("telnet.reversebeacon.net", 7000)
data = tn.read_until(b"Please enter your call:")
command = "kd0fnr\r\n"
tn.write(command.encode("utf-8"))
#frequencies we can use
#14058.0 14058.1 14058.2 14057.5 14057.4 14057.6 14057.9 
useful_freqs = {"14058.0": -1,
                "14058.1": -1,
                "14058.2": -1, 
                "14057.5": -1,
                "14057.4": -1,
                "14057.3": -1,
                "14057.6": -1,
                "14057.9": -1}
try:
    while True:
        data = tn.read_until(b"\n")  # Read data until a newline character
        # Search incoming data for the list of frequencies the Rockmite can 
        #use to transmit and receive
        print_freq = -1;
        for frequ in useful_freqs:
            print_freq = data.find(bytes(frequ, encoding='utf8'))
            if(print_freq != -1):
                break
        
        if print_freq != -1:
            print(data)

except KeyboardInterrupt:
    print("Exiting...")
    tn.close()

