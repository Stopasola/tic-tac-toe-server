from tkinter import *
from datetime import *
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter import messagebox
import threading

global containerDir, container_CRUD, Input_line, Input_Column, matriz, play, matriz, wrong_play, bad_play, play, end_game, time_to_play
global texto_00, texto_01, texto_02, texto_10, texto_11, texto_12, texto_20, texto_21, texto_22, play_simbol, play_ok, janela
wrong_play = 0
texto_00 = ' '
texto_01 = ' '
texto_02 = ' '
texto_10 = ' '
texto_11 = ' '
texto_12 = ' '
texto_20 = ' '
texto_21 = ' '
texto_22 = ' '
play_simbol = True
bad_play = False
play_ok = False
play = True
end_game = False
time_to_play = False
matriz = [[0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]

def prep(event):
    event.widget.config(bg='light blue')
    event.widget.focus_set()  # give keyboard focus to the label
    event.widget.bind('<Key>', edit)

def edit(event):
    print('peido')


def logical_validation(line, column):
    global play, matriz, wrong_play

    if line < 0 or line > 3 or column < 0 or column > 3:
        wrong_play = wrong_play + 1
        if wrong_play >= 3:
            return 'BYE'
        return 'PLAY NOK'

    if play == True:
        if matriz[line][column] != 0:
            wrong_play = wrong_play + 1
            if wrong_play >= 3:
                return 'BYE'
            return 'PLAY NOK'
        matriz[line][column] = 'X'
        play = False
    else:
        if matriz[line][column] != 0:
            wrong_play = wrong_play + 1
            if wrong_play >= 3:
                return 'BYE'
            return 'PLAY NOK'
        matriz[line][column] = 'O'
        play = True

    print(matriz)

    for i in range(0, 3):
        if matriz[i][0] == 'X' and matriz[i][1] == 'X' and matriz[i][2] == 'X':
            return 'PLAYER WIN'
        if matriz[i][0] == 'O' and matriz[i][1] == 'O' and matriz[i][2] == 'O':
            return 'PLAYER WIN'

        if matriz[0][i] == 'X' and matriz[1][i] == 'X' and matriz[2][i] == 'X':
            return 'PLAYER WIN'
        if matriz[0][i] == 'X' and matriz[1][i] == 'X' and matriz[2][i] == 'X':
            return 'PLAYER WIN'

    if matriz[0][0] == 'X' and matriz[1][1] == 'X' and matriz[2][2] == 'X':
        return 'PLAYER WIN'
    if matriz[0][0] == 'O' and matriz[1][1] == 'O' and matriz[2][2] == 'O':
        return 'PLAYER WIN'

    if matriz[2][0] == 'X' and matriz[1][1] == 'X' and matriz[0][2] == 'X':
        return 'PLAYER WIN'
    if matriz[2][0] == 'O' and matriz[1][1] == 'O' and matriz[0][2] == 'O':
        return 'PLAYER WIN'

    return 'False'


def send_command():

    global Input_line, Input_Column, wrong_play, bad_play, play_ok, time_to_play, end_game, janela
    result = logical_validation(int(Input_line.get()), int(Input_Column.get()))
    if time_to_play == True:
        print('passou result')
        if result == 'PLAYER WIN':
            if play_simbol == True:
                messagebox.showinfo('Fim de Jogo', 'Jogador X venceu!!')
            else:
                messagebox.showinfo('Fim de Jogo', 'Jogador O venceu!!')
            play_ok = True
            janela.destroy()
        if result == 'BYE':
            messagebox.showinfo('Fim de Jogo', 'O usuário jogou 3 jogadas erradas consecutivas!!')
            end_game = True
            janela.destroy()
        if result == 'PLAY NOK':
            messagebox.showinfo('Erro na Jogada', 'Jogue novamente!!')
            bad_play = True

        if result == 'False':
            print(result)
            wrong_play = 0
            play_ok = True


def func_insert():

    global Input_line, Input_Column
    insere_info = Frame(containerDir)

    lbLine = ttk.Label(insere_info, text="Linha:", font=("Verdana", "15"))
    Input_line = ttk.Entry(insere_info)
    lbColuna = ttk.Label(insere_info, text="Coluna:", font=("Verdana", "15"))
    Input_Column = ttk.Entry(insere_info)
    btnSendcommand = ttk.Button(insere_info, text="Enviar", command=send_command)

    #Input_BuscaCPF.bind('<Return>', lambda event=None: btnSendcommand.invoke())

    lbLine.grid(row=0, column=0, padx=30, pady=1, sticky=W)
    Input_line.grid(row=0, column=1, padx=52, pady=1)
    lbColuna.grid(row=1, column=0, padx=30, pady=1, sticky=W)
    Input_Column.grid(row=1, column=1, padx=52, pady=1)
    btnSendcommand.grid(row=2, column=0, padx=8, pady=15)
    insere_info.grid(row=0, column=0, padx=1, pady=1, sticky=W) #Pos Container

def Widget_set_Entrys(janela):

    global container_CRUD, texto_00, texto_01, texto_02, texto_10, texto_11, texto_12, texto_20, texto_21, texto_22

    container_CRUD = ttk.Frame(janela)
    my_canvas = Canvas(container_CRUD, height=1600, width=1600)

    lbl_0_0 = Label(my_canvas, text=texto_00, font=FonteTitulo, height=1, width=2)
    lbl_0_0.bind('<Button-1>', prep)
    lbl_0_1 = Label(my_canvas, text=texto_01, font=FonteTitulo, height=1, width=2)
    lbl_0_1.bind('<Button-1>', prep)
    lbl_0_2 = Label(my_canvas, text=texto_02, font=FonteTitulo, height=1, width=2)
    lbl_0_2.bind('<Button-1>', prep)


    lbl_1_0 = Label(my_canvas, text=texto_10, font=FonteTitulo, height=1, width=2)
    lbl_1_0.bind('<Button-1>', prep)
    lbl_1_1 = Label(my_canvas, text=texto_11, font=FonteTitulo, height=1, width=2)
    lbl_1_1.bind('<Button-1>', prep)
    lbl_1_2 = Label(my_canvas, text=texto_12, font=FonteTitulo, height=1, width=2)
    lbl_1_2.bind('<Button-1>', prep)


    lbl_2_0 = Label(my_canvas, text=texto_20, font=FonteTitulo, height=1, width=2)
    lbl_2_0.bind('<Button-1>', prep)
    lbl_2_1 = Label(my_canvas, text=texto_21, font=FonteTitulo, height=1, width=2)
    lbl_2_1.bind('<Button-1>', prep)
    lbl_2_2 = Label(my_canvas, text=texto_22, font=FonteTitulo, height=1, width=2)
    lbl_2_2.bind('<Button-1>', prep)

    """"""
    my_canvas.create_line(0, 200, 550, 200, fill='black', width=10)
    my_canvas.create_line(0, 400, 550, 400, fill='black', width=10)
    my_canvas.create_line(200, 0, 200, 550, fill='black', width=10)
    my_canvas.create_line(400, 0, 400, 550, fill='black', width=10)

    """  Def Grid  """

    my_canvas.grid(row=0, column=0)
    container_CRUD.grid(row=0, column=0, padx=100, pady=20, sticky=N + W)  # container_CRUD

    lbl_0_0.grid(row=0, column=0, padx=35, pady=35, sticky=W)
    lbl_0_1.grid(row=0, column=1, padx=35, pady=35, sticky=W)
    lbl_0_2.grid(row=0, column=2, padx=25, pady=35, sticky=W)

    lbl_1_0.grid(row=1, column=0, padx=35, pady=35, sticky=W)
    lbl_1_1.grid(row=1, column=1, padx=35, pady=35, sticky=W)
    lbl_1_2.grid(row=1, column=2, padx=35, pady=35, sticky=W)

    lbl_2_0.grid(row=2, column=0, padx=35, pady=35, sticky=W)
    lbl_2_1.grid(row=2, column=1, padx=35, pady=35, sticky=W)
    lbl_2_2.grid(row=2, column=2, padx=35, pady=35, sticky=W)

def atualiza_interface(line, column):

    global texto_00, texto_01, texto_02, texto_10, texto_11, texto_12, texto_20, texto_21, texto_22, play_simbol

    if play_simbol == True:
        text = 'X'
        play_simbol = False
    else:
        text = 'O'
        play_simbol = True

    if line == 0 and column == 0:
        texto_00 = text
    elif line == 0 and column == 1:
        texto_01 = text
    elif line == 0 and column == 2:
        texto_02 = text
    elif line == 1 and column == 0:
        texto_10 = text
    elif line == 1 and column == 1:
        texto_11 = text
    elif line == 1 and column == 2:
        texto_12 = text
    elif line == 2 and column == 0:
        texto_20 = text
    elif line == 2 and column == 1:
        texto_21 = text
    elif line == 2 and column == 2:
        texto_22 = text


def run_game(connection, start_player, janela):
    print('start_player: ', start_player)
    global bad_play, Input_line, Input_line, play_ok, container_CRUD, play_simbol, time_to_play
    while True:
        if start_player == 1:
            time_to_play = True
            if bad_play == True:
                bad_play = False
                Input_line.delete(0, END)
                Input_line.delete(0, END)
                continue
            elif play_ok == True:
                print('play_ok')
                msg = 'PLAY ' + Input_line.get() + ' ' + Input_Column.get()
                connection.send(msg.encode())

                data = connection.recv(1024)
                command = data.decode().split(" ")
                print('command', command)
                if command[0] == 'PLAY' and command[1] == 'OK':
                    print('play okkk')
                    start_player = 2
                    container_CRUD.grid_forget()
                    atualiza_interface(int(Input_line.get()), int(Input_Column.get()))
                    Widget_set_Entrys(janela)
                    Input_line.delete(0, END)
                    Input_Column.delete(0, END)
                    play_ok = False
                    time_to_play = False
                    continue

            elif end_game == True:
                msg = 'BYE'
                connection.send(msg.encode())
        else:

            data = connection.recv(1024)
            command = data.decode().split(" ")
            print('command', command)
            if command[0] == 'PLAY' and command[1] == 'OK':
                print('play okkk')
                continue
            if command[0] == 'BYE':
                messagebox.showinfo('Fim de Jogo', 'O jogador adversário jogou 3x errado, Você Ganhou!!')
                janela.destroy()

            if command[0] == 'PLAY':
                msg = 'PLAY OK'
                connection.send(msg.encode())
                if play_simbol == True:
                    matriz[int(command[1])][int(command[2])] = 'X'
                else:
                    matriz[int(command[1])][int(command[2])] = 'O'

            start_player = 1
            container_CRUD.grid_forget()
            atualiza_interface(int(command[1]), int(command[2]))
            Widget_set_Entrys(janela)


FonteTitulo = ("Verdana", "72")

def start_game_scream(connection, start_player):

    global containerDir, container_CRUD, bad_play, play_ok, janela
    janela = Tk()
    janela.title("Jogo")

    janela.geometry("1240x720")  # tentar definir widescream
    print('ooooooooo2')
    """ Funções """
    containerDir = ttk.Frame(janela)

    print('ooooooooo3')
    containerDir.grid(row=0, column=1, padx=10, pady=10)


    Widget_set_Entrys(janela)
    func_insert()

    if start_player == 1:
        messagebox.showinfo('Inicio de Jogo', 'Você inicia a jogada')

    thread1 = threading.Thread(target=run_game, args=(connection, start_player, janela))
    thread1.start()


    janela.mainloop()

