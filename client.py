from socket import *
import pickle
import threading
import time
from tkinter import messagebox
from game_interface import start_game_scream
import select

global play, matriz, wrong_play, end_thread1
end_thread1 = False
wrong_play = 0
play = True



# USER PAULO 300

def time_count(login_command, UDP_IP_ADDRESS, UDP_PORT_NO):
    now = int(time.time())
    future = int(now + 10)

    while int(time.time()) <= future:
        if int(time.time()) == future:
            clientSock = socket(AF_INET, SOCK_DGRAM)
            clientSock.sendto(login_command.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))
            future = int(time.time()) + 10
        if end_thread1:
            return


def login_server(UDP_IP_ADDRESS, UDP_PORT_NO, username):

    data = ''
    login_command = 'USER ' + username + ' ' + str(UDP_PORT_NO)
    print(login_command)
    clientSock = socket(AF_INET, SOCK_DGRAM)
    clientSock.sendto(login_command.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

    clientSock.settimeout(1.0)

    try:

        data = clientSock.recv(1024)  # recive com temporizador senão usa thread

    except Exception:
        pass

    if data == b'USER OK':

        thread1 = threading.Thread(target=time_count, args=(login_command, UDP_IP_ADDRESS, UDP_PORT_NO))
        thread1.start()
        return True
    else:
        return False


def comunication_server(UDP_IP_ADDRESS, UDP_PORT_NO, command):
    global end_thread1
    # função responsavel por lidar com todos os comandos com o servidor
    clientSock = socket(AF_INET, SOCK_DGRAM)
    clientSock.sendto(command.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

    command = command.split(" ")
    data, addr = clientSock.recvfrom(4096)

    if command[0] == 'LIST':
        return pickle.loads(data)
    if command[0] == 'EXIT':
        end_thread1 = True


def connection_client_TCP(name_user, ip_adversary, port_adversary):

    data = ''
    tcp = socket(AF_INET, SOCK_STREAM)
    dest = (ip_adversary, port_adversary)
    tcp.connect(dest)

    msg = 'START ' + str(name_user)
    tcp.send(msg.encode())

    try:
        data = tcp.recv(1024)
    except Exception:
        pass

    print('data', data)
    if data == b'BYE':
        tcp.close()
        return False
    else:
        start_game_scream(tcp, 1)



def listen_client_TCP_connection():
    host = ''
    port = 5000

    tcp = socket(AF_INET, SOCK_STREAM)
    orig = (host, port)
    tcp.bind(orig)
    tcp.listen(1)

    while True:
        con, cliente = tcp.accept()
        while True:
            msg = con.recv(1024)
            command = msg.decode().split(" ")
            print('command[0]', command[0])
            if command[0] == 'START': # recebe soliciatação
                user_option = messagebox.askyesno('Solicitação de Jogo', 'Deseja iniciar a conexão com o usuário: ' + str(command[1]))
                if user_option:
                    msg = 'START OK'
                    con.send(msg.encode())
                    start_game_scream(con, 2)
                else:
                    msg = 'BYE'
                    con.send(msg.encode())
                    break
    con.close()



