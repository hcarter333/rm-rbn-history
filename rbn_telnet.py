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
        print(data)
        # Assuming the callsign is enclosed in square brackets, e.g., [CALLSIGN]
        callsign_start = data.find(b"[") + 1
        callsign_end = data.find(b"]")

        if callsign_start != -1 and callsign_end != -1:
            callsign = data[callsign_start:callsign_end].decode("utf-8")
            print("Received callsign:", callsign)

except KeyboardInterrupt:
    print("Exiting...")
    tn.close()

