import telnetlib

#host = "your_host_address"
#port = 23  # The telnet port

tn = telnetlib.Telnet("telnet.reversebeacon.net", 7000)
data = tn.read_until(b"Please enter your call:")
command = "kd0fnr\r\n"
tn.write(command.encode("utf-8"))
try:
    while True:
        data = tn.read_until(b"\n")  # Read data until a newline character
        #print(data)
        # Assuming the callsign is enclosed in square brackets, e.g., [CALLSIGN]
        frequency_find = data.find(b"14058.")
        
        if frequency_find != -1:
            print(data)

except KeyboardInterrupt:
    print("Exiting...")
    tn.close()

