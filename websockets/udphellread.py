import socket

def read_goals(split_data):
    goalx_list = []
    goaly_list = []
    flag = 0
    start_flag = 0
    for entry in split_data:
        # print(entry)
        if entry == " r1x" or start_flag == 0:
            # print("here 1")
            flag = 0
            start_flag = 1
        elif entry == " r1y" or entry == "endx":
            flag = 1
            # print("here 2")
        elif entry == "endy":
            break
        else:
            # print("here 3")
            if (flag == 0):
                # print("here 4")
                goalx_list.append(float(entry))
            else:
                # print("here 5")
                goaly_list.append(float(entry))


    return goalx_list,goaly_list

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(("0.0.0.0", 5005))

while True:
    # sock.sendto(bytes("hello", "utf-8"), ip_co)
    data, addr = sock.recvfrom(1024)
    split_data = data.split(",")
    # print(split_data[0])

    print(split_data[1])
    if split_data[1] == "goals":
        goalsx,goalsy = read_goals(split_data)
        print(goalsx,goalsy)



    # print(data)#, flush=True)
