import socket, pickle
import threading
import time

def update_time():

    global Online_Users_List

    now = int(time.time())
    future = int(now + 1)

    while int(time.time()) <= future:

        if int(time.time()) == future:

            if len(Online_Users_List) > 0:
                for x in range(0, len(Online_Users_List)):


                    Online_Users_List[x][2] = int(Online_Users_List[x][2]) + 1
                    print('Online_Users_List[x][2]', Online_Users_List[x][2])


                    if Online_Users_List[x][2] > 60:

                        del Online_Users_List[x]
                        break

            print('update_time', Online_Users_List)
            future = int(time.time()) + 1


def Add_New_User(name, port, IP):

    flag = False
    time = 0
    for x in name:
        if x.isalpha() == False and x != '_' and x.isnumeric() == False:
            return "USER NOK"

    for x in port:
        if x.isnumeric() == False:
            return "USER NOK"

    count = 0
    for x in Online_Users_List:
        if str(x[1]) == str(IP[0]):
            if str(x[0]) != str(name):
                x[0] = name
            else:
                x[2] = 0 # tempo 0
        count = count + 1

    for x in Online_Users_List:
        if str(x[0]) == str(name):
            flag = True

    if not flag:
        Online_Users_List.append([name, IP[0], time, port])

    return "USER OK"


def list_users():

    Return_Client_List = list()
    Return_Client_List.insert(0, len(Online_Users_List))
    for x in Online_Users_List:
        Return_Client_List.append((x[0] + ':' + x[1] + ':' + x[3] ))

    return Return_Client_List


def remove_user(IP):
    for x in range(0, len(Online_Users_List)):
        if str(Online_Users_List[x][1]) == str(IP[0]):
            del Online_Users_List[x]
            break


def Connection_server_UDP():

    UDP_IP_ADDRESS = "192.168.0.20"  # Endereco IP do Servidor
    UDP_PORT_NO = 5000  # Porta que o Servidor esta

    #Cria Socket
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

    thread1 = threading.Thread(target=update_time)
    thread1.start()

    print("Servidor Iniciado")

    while True:
        data, addr = serverSock.recvfrom(4096)
        data = data.decode().split(" ")

        if data[0] == 'USER' and len(data) == 3:
            print(data)
            answer = Add_New_User(data[1], data[2], addr)
            serverSock.sendto(answer.encode(), addr)

        elif data[0] == 'LIST' and len(data) == 1:
            Return_Client_List = list_users()
            data = pickle.dumps(Return_Client_List)
            serverSock.sendto(data, addr)
        elif data[0] == 'EXIT':
            remove_user(addr)
            answer = 'EXIT'
            serverSock.sendto(answer.encode(), addr)


global Online_Users_List
Online_Users_List = list()



Connection_server_UDP()