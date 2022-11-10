import socket
import csv
from time import sleep

def read_csv(filename):
    data_x = " "
    data_y = " "
    ## We start by opening the file
    with open(filename) as file_name:
        ## Then we use the csv.reader() function to allow python to read the data
        file_read = csv.reader(file_name)
        # Next, we go through each row of the data and pull out the x point and the y point
        for row in file_read:
            # We add the x point to a list of the x points
            data_x += str(row[0])+ ","
            # We add the y point to a list of the y points
            data_y += str(row[1]) +","

    print(data_x)
    goals = data_x + data_y
    print(goals)
    return goals


def main():
    interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    allips = [ip[-1][0] for ip in interfaces]
    goals = read_csv('track_and_plan/testgoals.csv')
    # msg = b'hello hi world bald'
    i = 0
    while True:
        msg = bytes(goals,'utf-8-sig')
        for ip in allips:
            print(f'sending on {ip}', flush = True)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip,0))
            sock.sendto(msg, ("255.255.255.255", 5005))
            sock.close()

        i += 1

        sleep(2)

if __name__ == "__main__":
    main()